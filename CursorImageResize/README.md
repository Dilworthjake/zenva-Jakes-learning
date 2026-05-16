<<<<<<< HEAD
# JakeIMGResizer

A small **Flask** web app for batch-resizing **PNG** and **JPEG** images locally. It uses **Pillow** for image work, **Jinja2** templates with a dark cyberpunk-style UI (system fonts only), and serves processed files from an `uploads/` directory via `send_from_directory`.

There is **no authentication**, **no CORS configuration**, and **no security headers** hardening—this is intended as a simple local or trusted-network tool.

## Features

- Upload **up to five** images per run (`.png`, `.jpg`, `.jpeg` only; validation is **by file extension**).
- Set **target width**, **height**, and **quality** (1–100). Output dimensions are exact after processing.
- Optional **clockwise rotation** in steps of **90°** (applied **before** resize, with `expand=True` so nothing is cropped at rotation time).
- Optional **text watermark** (Pillow **default bitmap font** only): custom text, size, **#RRGGBB** colour, **opacity %**, **margin** / **padding**, **text rotation** (clockwise, −180…180°), and **position** (center, corners, or **custom** % with drag preview on the first selected photo).
- Optional **image watermark** (logo/mark): upload a second **PNG or JPEG** (up to **6 MB**), set **scale** (% of output width), **opacity**, **rotation**, **margin** / **padding**, and **position** (independent of text). The image layer is drawn **first**, then text, so text stays on top when both are enabled.
- After a successful run, you are sent to a **Preview** page with thumbnails and **per-file download** links.
- Shared **header and footer** across Upload and Preview; processed files are stored with **`secure_filename`** plus a short random prefix.

## Requirements

- **Python 3.9+** (3.10+ recommended; type hints assume a recent interpreter).
- Dependencies are listed in `requirements.txt` (Flask, Pillow, Werkzeug).

## Setup

```bash
cd path/to/CursorImageResize
python -m venv .venv
```

Activate the virtual environment (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install packages:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open **http://127.0.0.1:5000/** in your browser.

By default the app runs with **Flask’s debug server** on port **5000**. For anything beyond local experimentation, use a production WSGI server and your own configuration.

## How to use

1. Open **Upload**, choose photos, set output size/quality/rotation. Optionally enable **text** and/or **image** watermarks and adjust their options; use **Custom** position and drag the overlays on the preview when needed.
2. Submit **Resize & preview**. Each file is written under `uploads/` and the result list is stored in the session.
3. On **Preview**, inspect thumbnails and use **Download** for each file. Use **New batch** to return to the upload form.
4. The **Preview** nav link only works after a successful batch; otherwise you are redirected to Upload with a message.

## Project layout

| Path | Role |
|------|------|
| `app.py` | Flask application, resize/rotate/watermark logic, routes |
| `requirements.txt` | Python dependencies |
| `templates/base.html` | Layout, global styles, site header/footer |
| `templates/index.html` | Upload form (optional text + image watermarks) |
| `templates/preview.html` | Preview grid and downloads |
| `static/js/watermark-preview.js` | Drag/preview helpers for watermarks |
| `uploads/` | Processed images (created automatically; safe to clear manually) |

## Limits and behavior

- **Request body** size is capped at **32 MB** (`MAX_CONTENT_LENGTH` in `app.py`).
- **JPEG** output uses the given quality; **PNG** maps quality to compression level. Semi-transparent watermarks are flattened onto **white** when saving JPEG.
- The Flask **`SECRET_KEY`** in `app.py` is a **development placeholder**. Change it if you expose the app beyond localhost or care about session integrity.

=======
Just a repo to store a lot of basic python tasks while I learn new libraries and keep my skills fresh
>>>>>>> 8dd128827ae37b1439f7dce7e9c8a16bf5effe3d
