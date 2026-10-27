"""Dựng MP4 minh họa bằng thẻ cảnh, KHÔNG sinh cảnh video bằng AI."""
from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import textwrap
from PIL import Image, ImageDraw, ImageFont


def _font():
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for location in candidates:
        if Path(location).is_file():
            return ImageFont.truetype(location, 37)
    return ImageFont.load_default()


def _still(scene: dict, path: Path):
    image = Image.new("RGB", (1280, 720), (19, 31, 52))
    draw = ImageDraw.Draw(image)
    draw.text((82, 90), scene.get("title", "Cảnh phim"), fill=(255, 199, 108), font=_font())
    text = scene.get("description", "")
    rows = textwrap.wrap(text, width=48)[:8]
    for idx, row in enumerate(rows):
        draw.text((82, 190 + 52 * idx), row, fill="white", font=_font())
    image.save(path)


def render(project: dict) -> Path:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("Máy chưa có FFmpeg trong PATH")
    scenes = project.get("scenes", [])
    if not scenes:
        raise ValueError("Chưa có phân cảnh")
    out_dir = Path(os.getenv("STUDIO_HOME", "./data")).resolve() / "renders"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / (project["id"] + ".mp4")
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        clips = []
        for i, scene in enumerate(scenes):
            seconds = max(1.0, min(float(scene.get("duration", 5)), 30.0))
            still = folder / f"scene_{i:04}.png"
            clip = folder / f"clip_{i:04}.mp4"
            _still(scene, still)
            args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-loop", "1", "-framerate", "24", "-i", str(still),
                    "-t", str(seconds), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-vf", "scale=1280:720", str(clip)]
            subprocess.run(args, check=True, timeout=180)
            clips.append(clip)
        concat = folder / "concat.txt"
        concat.write_text("".join("file '" + str(p).replace("'", "'\\''") + "'\n" for p in clips), encoding="utf-8")
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                        "-f", "concat", "-safe", "0", "-i", str(concat),
                        "-c", "copy", str(target)], check=True, timeout=600)
    return target
