import io
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, session, url_for
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = Path(__file__).resolve().parent / "uploads"
ALLOWED_EXTENSIONS = frozenset({"png", "jpg", "jpeg"})
ALLOWED_ROTATION_CW = frozenset({0, 90, 180, 270})
MAX_FILES = 5
MAX_IMAGE_WATERMARK_BYTES = 6 * 1024 * 1024

WM_POSITIONS = frozenset(
    {"center", "top-left", "top-right", "bottom-left", "bottom-right", "custom"}
)


app = Flask(__name__)
app.config["SECRET_KEY"] = "jakeimgresizer-dev"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def clamp_quality(q: int) -> int:
    return max(1, min(100, q))


def apply_rotation_clockwise(im: Image.Image, degrees_cw: int) -> Image.Image:
    if degrees_cw == 0:
        return im
    fill: tuple[int, ...] = (0, 0, 0, 0) if im.mode == "RGBA" else (0, 0, 0)
    return im.rotate(
        -degrees_cw,
        expand=True,
        resample=Image.Resampling.BICUBIC,
        fillcolor=fill,
    )


@dataclass(frozen=True)
class TextWatermarkConfig:
    text: str
    size: int
    rgb: tuple[int, int, int]
    opacity_pct: int
    position: str
    x_pct: float
    y_pct: float
    text_rotation_cw: float
    margin: int
    padding: int


@dataclass
class ImageWatermarkParams:
    """RGBA overlay; scaled per output image during apply."""

    image_rgba: Image.Image
    scale_pct: int
    opacity_pct: int
    position: str
    x_pct: float
    y_pct: float
    margin: int
    padding: int
    rotation_cw: float


def parse_hex_color(raw: str) -> tuple[int, int, int]:
    s = (raw or "").strip().lstrip("#")
    if len(s) == 6 and re.fullmatch(r"[0-9a-fA-F]{6}", s):
        return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    raise ValueError("invalid color")


def sanitize_watermark_text(raw: str) -> str:
    t = (raw or "").replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", t)
    if len(t) > 500:
        t = t[:500]
    return t.strip()


def parse_text_watermark(form) -> TextWatermarkConfig | None:
    if form.get("watermark_enabled") != "1":
        return None
    text = sanitize_watermark_text(form.get("watermark_text", ""))
    if not text:
        raise ValueError("Watermark text is empty.")
    try:
        size = int(form.get("watermark_size", 24))
    except ValueError as exc:
        raise ValueError("Invalid text size.") from exc
    if size < 8 or size > 120:
        raise ValueError("Text size must be between 8 and 120 (Pillow default font).")
    try:
        rgb = parse_hex_color(form.get("watermark_color", "#ffffff"))
    except ValueError as exc:
        raise ValueError("Invalid colour (use #RRGGBB).") from exc
    try:
        opacity_pct = int(form.get("watermark_opacity", 80))
    except ValueError as exc:
        raise ValueError("Invalid text opacity.") from exc
    opacity_pct = max(0, min(100, opacity_pct))
    position = (form.get("watermark_position") or "center").lower()
    if position not in WM_POSITIONS:
        raise ValueError("Invalid text position.")
    try:
        x_pct = float(form.get("watermark_x_pct", 50))
        y_pct = float(form.get("watermark_y_pct", 50))
    except ValueError as exc:
        raise ValueError("Invalid text coordinates.") from exc
    x_pct = max(0.0, min(100.0, x_pct))
    y_pct = max(0.0, min(100.0, y_pct))
    try:
        text_rotation_cw = float(form.get("watermark_text_rotation", 0))
    except ValueError as exc:
        raise ValueError("Invalid text rotation.") from exc
    if text_rotation_cw < -180 or text_rotation_cw > 180:
        raise ValueError("Text rotation must be between -180 and 180 degrees.")
    try:
        margin = int(form.get("watermark_margin", 16))
        padding = int(form.get("watermark_padding", 8))
    except ValueError as exc:
        raise ValueError("Invalid margin or padding.") from exc
    if margin < 0 or margin > 400 or padding < 0 or padding > 200:
        raise ValueError("Margin must be 0–400 px; padding 0–200 px.")
    return TextWatermarkConfig(
        text=text,
        size=size,
        rgb=rgb,
        opacity_pct=opacity_pct,
        position=position,
        x_pct=x_pct,
        y_pct=y_pct,
        text_rotation_cw=text_rotation_cw,
        margin=margin,
        padding=padding,
    )


def parse_image_watermark(files, form) -> ImageWatermarkParams | None:
    if form.get("watermark_image_enabled") != "1":
        return None
    wf = files.get("watermark_image")
    if not wf or not wf.filename:
        raise ValueError("Image watermark enabled but no image file was uploaded.")
    if not allowed_file(wf.filename):
        raise ValueError("Image watermark must be PNG or JPEG (.png, .jpg, .jpeg).")
    raw = wf.read()
    if len(raw) > MAX_IMAGE_WATERMARK_BYTES:
        raise ValueError("Image watermark file is too large (max 6 MB).")
    try:
        im = Image.open(io.BytesIO(raw)).convert("RGBA")
    except OSError as exc:
        raise ValueError("Could not read image watermark file.") from exc
    im.load()
    rgba = im.copy()
    try:
        scale_pct = int(form.get("watermark_img_scale", 25))
    except ValueError as exc:
        raise ValueError("Invalid image scale.") from exc
    if scale_pct < 5 or scale_pct > 100:
        raise ValueError("Image scale must be between 5 and 100 (% of output width).")
    try:
        opacity_pct = int(form.get("watermark_img_opacity", 80))
    except ValueError as exc:
        raise ValueError("Invalid image opacity.") from exc
    opacity_pct = max(0, min(100, opacity_pct))
    position = (form.get("watermark_img_position") or "bottom-right").lower()
    if position not in WM_POSITIONS:
        raise ValueError("Invalid image position.")
    try:
        x_pct = float(form.get("watermark_img_x_pct", 90))
        y_pct = float(form.get("watermark_img_y_pct", 90))
    except ValueError as exc:
        raise ValueError("Invalid image coordinates.") from exc
    x_pct = max(0.0, min(100.0, x_pct))
    y_pct = max(0.0, min(100.0, y_pct))
    try:
        margin = int(form.get("watermark_img_margin", 16))
        padding = int(form.get("watermark_img_padding", 8))
    except ValueError as exc:
        raise ValueError("Invalid image margin or padding.") from exc
    if margin < 0 or margin > 400 or padding < 0 or padding > 200:
        raise ValueError("Image margin must be 0–400 px; padding 0–200 px.")
    try:
        rotation_cw = float(form.get("watermark_img_rotation", 0))
    except ValueError as exc:
        raise ValueError("Invalid image rotation.") from exc
    if rotation_cw < -180 or rotation_cw > 180:
        raise ValueError("Image rotation must be between -180 and 180 degrees.")
    return ImageWatermarkParams(
        image_rgba=rgba,
        scale_pct=scale_pct,
        opacity_pct=opacity_pct,
        position=position,
        x_pct=x_pct,
        y_pct=y_pct,
        margin=margin,
        padding=padding,
        rotation_cw=rotation_cw,
    )


def overlay_anchor(
    bw: int,
    bh: int,
    rw: int,
    rh: int,
    position: str,
    x_pct: float,
    y_pct: float,
    margin: int,
    padding: int,
) -> tuple[float, float]:
    inset = margin + padding
    if position == "custom":
        return bw * (x_pct / 100.0), bh * (y_pct / 100.0)
    if position == "center":
        return bw / 2.0, bh / 2.0
    if position == "top-left":
        return inset + rw / 2.0, inset + rh / 2.0
    if position == "top-right":
        return bw - inset - rw / 2.0, inset + rh / 2.0
    if position == "bottom-left":
        return inset + rw / 2.0, bh - inset - rh / 2.0
    if position == "bottom-right":
        return bw - inset - rw / 2.0, bh - inset - rh / 2.0
    return bw / 2.0, bh / 2.0


def _text_bbox(
    draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont
) -> tuple[int, int, int, int]:
    if "\n" in text and hasattr(draw, "multiline_textbbox"):
        return draw.multiline_textbbox(xy, text, font=font, spacing=4)
    flat = text.replace("\n", " ")
    return draw.textbbox(xy, flat, font=font)


def build_text_sprite(
    text: str, font: ImageFont.ImageFont, fill_rgba: tuple[int, int, int, int], rotation_cw: float
) -> Image.Image:
    probe = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    bbox = _text_bbox(draw, (0, 0), text, font)
    tw = max(1, bbox[2] - bbox[0])
    th = max(1, bbox[3] - bbox[1])
    pad = 12
    layer = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    dr = ImageDraw.Draw(layer)
    ox = pad - bbox[0]
    oy = pad - bbox[1]
    if "\n" in text and hasattr(dr, "multiline_text"):
        dr.multiline_text((ox, oy), text, font=font, fill=fill_rgba, spacing=4)
    else:
        dr.text((ox, oy), text.replace("\n", " "), font=font, fill=fill_rgba)
    if rotation_cw % 360 == 0:
        return layer
    pil_angle = -rotation_cw
    return layer.rotate(
        pil_angle,
        expand=True,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0),
    )


def apply_text_watermark(base: Image.Image, wm: TextWatermarkConfig) -> Image.Image:
    if base.mode != "RGBA":
        base = base.convert("RGBA")
    try:
        font = ImageFont.load_default(wm.size)
    except TypeError:
        font = ImageFont.load_default()
    alpha = int(round(255 * (wm.opacity_pct / 100.0)))
    fill = (*wm.rgb, alpha)
    sprite = build_text_sprite(wm.text, font, fill, wm.text_rotation_cw)
    rw, rh = sprite.size
    ax, ay = overlay_anchor(
        base.width,
        base.height,
        rw,
        rh,
        wm.position,
        wm.x_pct,
        wm.y_pct,
        wm.margin,
        wm.padding,
    )
    x = int(round(ax - rw / 2))
    y = int(round(ay - rh / 2))
    x = max(0, min(x, base.width - rw))
    y = max(0, min(y, base.height - rh))
    base.alpha_composite(sprite, (x, y))
    return base


def _scale_rgba_opacity(im: Image.Image, opacity_pct: int) -> Image.Image:
    if opacity_pct >= 100:
        return im
    r, g, b, a = im.split()
    factor = opacity_pct / 100.0
    a = a.point(lambda p: int(round(p * factor)))
    return Image.merge("RGBA", (r, g, b, a))


def apply_image_watermark(base: Image.Image, wm: ImageWatermarkParams) -> Image.Image:
    if base.mode != "RGBA":
        base = base.convert("RGBA")
    tw = max(1, int(base.width * wm.scale_pct / 100.0))
    src = wm.image_rgba
    aspect = src.height / max(1, src.width)
    th = max(1, int(round(tw * aspect)))
    scaled = src.resize((tw, th), Image.Resampling.LANCZOS)
    scaled = _scale_rgba_opacity(scaled, wm.opacity_pct)
    if wm.rotation_cw % 360 != 0:
        scaled = scaled.rotate(
            -wm.rotation_cw,
            expand=True,
            resample=Image.Resampling.BICUBIC,
            fillcolor=(0, 0, 0, 0),
        )
    rw, rh = scaled.size
    ax, ay = overlay_anchor(
        base.width,
        base.height,
        rw,
        rh,
        wm.position,
        wm.x_pct,
        wm.y_pct,
        wm.margin,
        wm.padding,
    )
    x = int(round(ax - rw / 2))
    y = int(round(ay - rh / 2))
    x = max(0, min(x, base.width - rw))
    y = max(0, min(y, base.height - rh))
    base.alpha_composite(scaled, (x, y))
    return base


def flatten_rgba_for_jpeg(im: Image.Image) -> Image.Image:
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3])
    return bg


def resize_and_save(
    src_path: Path,
    dest_path: Path,
    ext: str,
    width: int,
    height: int,
    quality: int,
    rotate_cw: int = 0,
    text_watermark: TextWatermarkConfig | None = None,
    image_watermark: ImageWatermarkParams | None = None,
) -> None:
    quality = clamp_quality(quality)
    with Image.open(src_path) as im:
        if ext in ("jpg", "jpeg"):
            work = im.convert("RGB")
        elif im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            work = im.convert("RGBA")
        else:
            work = im.convert("RGB")
        if rotate_cw:
            work = apply_rotation_clockwise(work, rotate_cw)
        resized = work.resize((width, height), Image.Resampling.LANCZOS)
        if image_watermark:
            resized = apply_image_watermark(resized, image_watermark)
        if text_watermark:
            resized = apply_text_watermark(resized, text_watermark)
        if ext in ("jpg", "jpeg"):
            if resized.mode == "RGBA":
                resized = flatten_rgba_for_jpeg(resized)
            else:
                resized = resized.convert("RGB")
            resized.save(dest_path, "JPEG", quality=quality, optimize=True)
        else:
            level = max(0, min(9, 9 - quality // 12))
            if resized.mode != "RGBA":
                resized = resized.convert("RGBA")
            resized.save(dest_path, "PNG", compress_level=level, optimize=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("images")
        files = [f for f in files if f and f.filename]
        if not files:
            flash("Select at least one image.", "error")
            return redirect(url_for("index"))
        if len(files) > MAX_FILES:
            flash(f"At most {MAX_FILES} images allowed.", "error")
            return redirect(url_for("index"))

        try:
            width = int(request.form.get("width", 0))
            height = int(request.form.get("height", 0))
            quality = int(request.form.get("quality", 85))
            rotate_cw = int(request.form.get("rotate", 0))
        except ValueError:
            flash("Width, height, quality, and rotation must be valid numbers.", "error")
            return redirect(url_for("index"))

        if width < 1 or height < 1:
            flash("Width and height must be positive.", "error")
            return redirect(url_for("index"))

        if rotate_cw not in ALLOWED_ROTATION_CW:
            flash("Rotation must be 0°, 90°, 180°, or 270° (clockwise).", "error")
            return redirect(url_for("index"))

        try:
            text_wm = parse_text_watermark(request.form)
            image_wm = parse_image_watermark(request.files, request.form)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("index"))

        batch = []
        for f in files:
            if not allowed_file(f.filename):
                flash(f"Skipped (extension not allowed): {f.filename}", "error")
                continue
            ext = f.filename.rsplit(".", 1)[1].lower()
            safe = secure_filename(f.filename)
            if not safe:
                flash("Invalid filename.", "error")
                continue
            token = uuid.uuid4().hex[:12]
            stored_name = f"{token}_{safe}"
            tmp_path = UPLOAD_FOLDER / f".tmp_{token}_{safe}"
            out_path = UPLOAD_FOLDER / stored_name
            f.save(tmp_path)
            try:
                resize_and_save(
                    tmp_path,
                    out_path,
                    ext,
                    width,
                    height,
                    quality,
                    rotate_cw=rotate_cw,
                    text_watermark=text_wm,
                    image_watermark=image_wm,
                )
            except Exception as exc:  # noqa: BLE001
                flash(f"Could not process {f.filename}: {exc}", "error")
                if out_path.exists():
                    out_path.unlink()
            finally:
                if tmp_path.exists():
                    tmp_path.unlink()
            batch.append({"file": stored_name, "label": safe})

        if not batch:
            flash("No images were processed.", "error")
            return redirect(url_for("index"))

        session["last_batch"] = batch
        flash("Resize complete.", "ok")
        return redirect(url_for("preview"))

    return render_template(
        "index.html",
        max_files=MAX_FILES,
        active_page="upload",
    )


@app.route("/preview")
def preview():
    batch = session.get("last_batch") or []
    if not batch:
        flash("No preview yet. Upload images first.", "error")
        return redirect(url_for("index"))
    return render_template("preview.html", batch=batch, active_page="preview")


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)


@app.route("/uploads/<path:filename>/download")
def download_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
