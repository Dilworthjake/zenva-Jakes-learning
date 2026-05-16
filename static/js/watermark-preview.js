(function () {
  "use strict";

  var maxPreviewW = 520;
  var previewFontCss = "ui-monospace, Cascadia Mono, Consolas, monospace";

  function $(id) {
    return document.getElementById(id);
  }

  function parseNum(el, fallback) {
    var v = parseFloat(el && el.value);
    return isNaN(v) ? fallback : v;
  }

  function targetSize() {
    var w = parseNum($("width"), 800);
    var h = parseNum($("height"), 600);
    return { w: Math.max(1, w), h: Math.max(1, h) };
  }

  function measureLabel(text, fontPx) {
    var s = document.createElement("span");
    s.style.cssText =
      "position:absolute;left:-9999px;top:0;white-space:pre-wrap;visibility:hidden;font-family:" +
      previewFontCss +
      ";font-size:" +
      fontPx +
      "px;line-height:1.2;";
    s.textContent = text || " ";
    document.body.appendChild(s);
    var w = s.offsetWidth;
    var h = s.offsetHeight;
    document.body.removeChild(s);
    return { w: Math.max(24, w), h: Math.max(16, h) };
  }

  function presetAnchorPct(pos, tw, th, W, H, margin, padding) {
    var inset = margin + padding;
    var ax, ay;
    if (pos === "center") {
      ax = 50;
      ay = 50;
    } else if (pos === "top-left") {
      ax = ((inset + tw / 2) / W) * 100;
      ay = ((inset + th / 2) / H) * 100;
    } else if (pos === "top-right") {
      ax = ((W - inset - tw / 2) / W) * 100;
      ay = ((inset + th / 2) / H) * 100;
    } else if (pos === "bottom-left") {
      ax = ((inset + tw / 2) / W) * 100;
      ay = ((H - inset - th / 2) / H) * 100;
    } else if (pos === "bottom-right") {
      ax = ((W - inset - tw / 2) / W) * 100;
      ay = ((H - inset - th / 2) / H) * 100;
    } else {
      ax = 50;
      ay = 50;
    }
    return {
      x: Math.max(0, Math.min(100, ax)),
      y: Math.max(0, Math.min(100, ay)),
    };
  }

  var state = {
    baseImg: null,
    wmImg: null,
    wmImgUrl: null,
    scale: 1,
    displayW: 0,
    displayH: 0,
    dragging: false,
    dragKind: null,
  };

  function previewShouldShow() {
    var files = $("images") && $("images").files;
    if (!files || !files.length || !state.baseImg) return false;
    var t = $("wm_enabled") && $("wm_enabled").checked;
    var i = $("wm_image_enabled") && $("wm_image_enabled").checked;
    return t || i;
  }

  function syncTextDrag() {
    var drag = $("wm_drag");
    if (!drag) return;
    drag.style.left = parseNum($("watermark_x_pct"), 50) + "%";
    drag.style.top = parseNum($("watermark_y_pct"), 50) + "%";
  }

  function syncImageDrag() {
    var box = $("wm_drag_img");
    var inner = $("wm_drag_img_inner");
    if (!box || !inner || !state.wmImg) return;
    box.style.left = parseNum($("watermark_img_x_pct"), 90) + "%";
    box.style.top = parseNum($("watermark_img_y_pct"), 90) + "%";
    var ts = targetSize();
    var scalePct = parseNum($("watermark_img_scale"), 22);
    var twDisp = Math.max(12, state.displayW * (scalePct / 100));
    box.style.width = twDisp + "px";
    inner.style.opacity = String(parseNum($("watermark_img_opacity"), 80) / 100);
    var rot = parseNum($("watermark_img_rotation"), 0);
    box.style.transform =
      "translate(-50%, -50%) rotate(" + rot + "deg)";
  }

  function updateTextDrag() {
    var drag = $("wm_drag");
    var txt = $("watermark_text");
    var sz = parseNum($("watermark_size"), 24);
    var col = ($("watermark_color") && $("watermark_color").value) || "#ffffff";
    var op = parseNum($("watermark_opacity"), 75) / 100;
    var rot = parseNum($("watermark_text_rotation"), 0);
    if (!drag) return;
    drag.textContent = (txt && txt.value) || "Preview";
    var ts = targetSize();
    var fontPx = Math.max(8, sz * (state.displayW / ts.w));
    drag.style.fontSize = fontPx + "px";
    drag.style.fontFamily = previewFontCss;
    drag.style.color = col;
    drag.style.opacity = String(Math.max(0.05, Math.min(1, op)));
    drag.style.transform = "translate(-50%, -50%) rotate(" + rot + "deg)";
  }

  function drawCanvas() {
    var canvas = $("wm_canvas");
    var wrap = $("wm_canvas_wrap");
    if (!canvas || !state.baseImg) return;
    var iw = state.baseImg.naturalWidth;
    var ih = state.baseImg.naturalHeight;
    var sc = Math.min(1, maxPreviewW / iw);
    state.scale = sc;
    state.displayW = Math.round(iw * sc);
    state.displayH = Math.round(ih * sc);
    canvas.width = state.displayW;
    canvas.height = state.displayH;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(state.baseImg, 0, 0, state.displayW, state.displayH);
    if (wrap) {
      wrap.style.width = state.displayW + "px";
      wrap.style.height = state.displayH + "px";
    }
    var imgBox = $("wm_drag_img");
    if (imgBox && state.wmImg && $("wm_image_enabled") && $("wm_image_enabled").checked) {
      imgBox.hidden = false;
      $("wm_drag_img_inner").src = state.wmImg.src;
      syncImageDrag();
    } else if (imgBox) {
      imgBox.hidden = true;
    }
    updateTextDrag();
    syncTextDrag();
    if ($("wm_drag")) {
      $("wm_drag").style.display =
        $("wm_enabled") && $("wm_enabled").checked ? "block" : "none";
    }
  }

  function applyPresetText() {
    var posEl = $("watermark_position");
    if (!posEl || posEl.value === "custom") return;
    var ts = targetSize();
    var margin = parseNum($("watermark_margin"), 16);
    var padding = parseNum($("watermark_padding"), 8);
    var text = ($("watermark_text") && $("watermark_text").value) || " ";
    var sz = parseNum($("watermark_size"), 24);
    var fontPx = Math.max(8, sz * (state.displayW / ts.w));
    var m = measureLabel(text, fontPx);
    var tw = m.w / state.scale;
    var th = m.h / state.scale;
    var p = presetAnchorPct(posEl.value, tw, th, ts.w, ts.h, margin, padding);
    $("watermark_x_pct").value = p.x.toFixed(2);
    $("watermark_y_pct").value = p.y.toFixed(2);
    syncTextDrag();
  }

  function applyPresetImage() {
    var posEl = $("watermark_img_position");
    if (!posEl || posEl.value === "custom" || !state.wmImg) return;
    var ts = targetSize();
    var margin = parseNum($("watermark_img_margin"), 16);
    var padding = parseNum($("watermark_img_padding"), 8);
    var scalePct = parseNum($("watermark_img_scale"), 22);
    var tw = (ts.w * scalePct) / 100;
    var aspect = state.wmImg.naturalHeight / Math.max(1, state.wmImg.naturalWidth);
    var th = tw * aspect;
    var p = presetAnchorPct(posEl.value, tw, th, ts.w, ts.h, margin, padding);
    $("watermark_img_x_pct").value = p.x.toFixed(2);
    $("watermark_img_y_pct").value = p.y.toFixed(2);
    syncImageDrag();
  }

  function onBaseFileChange(ev) {
    var files = ev.target.files;
    var section = $("wm_preview_section");
    if (!files || !files.length) {
      state.baseImg = null;
      if (section) section.hidden = true;
      return;
    }
    var f = files[0];
    if (!/^image\/(png|jpe?g)$/i.test(f.type)) {
      state.baseImg = null;
      if (section) section.hidden = true;
      return;
    }
    var reader = new FileReader();
    reader.onload = function () {
      var img = new Image();
      img.onload = function () {
        state.baseImg = img;
        refreshPreview();
      };
      img.src = reader.result;
    };
    reader.readAsDataURL(f);
  }

  function onWmImageFileChange(ev) {
    var f = ev.target.files && ev.target.files[0];
    if (state.wmImgUrl) {
      URL.revokeObjectURL(state.wmImgUrl);
      state.wmImgUrl = null;
    }
    state.wmImg = null;
    if (!f || !/^image\/(png|jpe?g)$/i.test(f.type)) {
      refreshPreview();
      return;
    }
    state.wmImgUrl = URL.createObjectURL(f);
    var img = new Image();
    img.onload = function () {
      state.wmImg = img;
      applyPresetImage();
      refreshPreview();
    };
    img.src = state.wmImgUrl;
  }

  function refreshPreview() {
    var section = $("wm_preview_section");
    if (!section) return;
    if (previewShouldShow()) {
      section.hidden = false;
      drawCanvas();
      if ($("watermark_position") && $("watermark_position").value !== "custom") {
        applyPresetText();
      } else {
        syncTextDrag();
      }
      if (
        state.wmImg &&
        $("wm_image_enabled") &&
        $("wm_image_enabled").checked &&
        $("watermark_img_position") &&
        $("watermark_img_position").value !== "custom"
      ) {
        applyPresetImage();
      } else {
        syncImageDrag();
      }
    } else {
      section.hidden = true;
    }
  }

  function moveDragFromEvent(e) {
    var wrap = $("wm_canvas_wrap");
    if (!wrap || !state.dragKind) return;
    var rect = wrap.getBoundingClientRect();
    var clientX = e.touches ? e.touches[0].clientX : e.clientX;
    var clientY = e.touches ? e.touches[0].clientY : e.clientY;
    var x = ((clientX - rect.left) / rect.width) * 100;
    var y = ((clientY - rect.top) / rect.height) * 100;
    x = Math.max(0, Math.min(100, x));
    y = Math.max(0, Math.min(100, y));
    if (state.dragKind === "text") {
      $("watermark_x_pct").value = x.toFixed(2);
      $("watermark_y_pct").value = y.toFixed(2);
      if ($("watermark_position")) $("watermark_position").value = "custom";
      syncTextDrag();
    } else {
      $("watermark_img_x_pct").value = x.toFixed(2);
      $("watermark_img_y_pct").value = y.toFixed(2);
      if ($("watermark_img_position")) $("watermark_img_position").value = "custom";
      syncImageDrag();
    }
  }

  function startDragText(ev) {
    if (!$("wm_enabled") || !$("wm_enabled").checked) return;
    ev.preventDefault();
    ev.stopPropagation();
    state.dragging = true;
    state.dragKind = "text";
    moveDragFromEvent(ev);
    bindDragUp();
  }

  function startDragImage(ev) {
    if (!$("wm_image_enabled") || !$("wm_image_enabled").checked || !state.wmImg) return;
    ev.preventDefault();
    ev.stopPropagation();
    state.dragging = true;
    state.dragKind = "image";
    moveDragFromEvent(ev);
    bindDragUp();
  }

  function bindDragUp() {
    function move(e) {
      if (!state.dragging) return;
      moveDragFromEvent(e);
    }
    function up() {
      state.dragging = false;
      state.dragKind = null;
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", up);
      window.removeEventListener("touchmove", move);
      window.removeEventListener("touchend", up);
    }
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
    window.addEventListener("touchmove", move, { passive: false });
    window.addEventListener("touchend", up);
  }

  function onTextInput() {
    updateTextDrag();
    if ($("watermark_position") && $("watermark_position").value !== "custom") {
      applyPresetText();
    }
  }

  function onImageInput() {
    if (
      state.wmImg &&
      $("watermark_img_position") &&
      $("watermark_img_position").value !== "custom"
    ) {
      applyPresetImage();
    } else {
      syncImageDrag();
    }
  }

  function init() {
    var imgInput = $("images");
    var wmImgInput = $("watermark_image");
    if (imgInput) imgInput.addEventListener("change", onBaseFileChange);
    if (wmImgInput) wmImgInput.addEventListener("change", onWmImageFileChange);

    if ($("wm_enabled")) $("wm_enabled").addEventListener("change", refreshPreview);
    if ($("wm_image_enabled")) $("wm_image_enabled").addEventListener("change", refreshPreview);

    [
      "watermark_text",
      "watermark_size",
      "watermark_color",
      "watermark_opacity",
      "watermark_text_rotation",
      "watermark_margin",
      "watermark_padding",
      "width",
      "height",
    ].forEach(function (id) {
      var el = $(id);
      if (el) el.addEventListener("input", onTextInput);
    });

    [
      "watermark_img_scale",
      "watermark_img_opacity",
      "watermark_img_rotation",
      "watermark_img_margin",
      "watermark_img_padding",
      "width",
      "height",
    ].forEach(function (id) {
      var el = $(id);
      if (el) el.addEventListener("input", onImageInput);
    });

    var posText = $("watermark_position");
    if (posText) {
      posText.addEventListener("change", function () {
        if (posText.value !== "custom") applyPresetText();
        else syncTextDrag();
      });
    }

    var posImg = $("watermark_img_position");
    if (posImg) {
      posImg.addEventListener("change", function () {
        if (posImg.value !== "custom") applyPresetImage();
        else syncImageDrag();
      });
    }

    var drag = $("wm_drag");
    if (drag) {
      drag.addEventListener("mousedown", startDragText);
      drag.addEventListener("touchstart", startDragText, { passive: false });
    }
    var dragImg = $("wm_drag_img");
    if (dragImg) {
      dragImg.addEventListener("mousedown", startDragImage);
      dragImg.addEventListener("touchstart", startDragImage, { passive: false });
    }

    updateTextDrag();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
