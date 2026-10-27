"""Local MP4 audit: allowlisted path, ffprobe metadata, SHA-256. No AI scoring."""
from __future__ import annotations
import hashlib
import json
import math
import subprocess
from pathlib import Path

MAX_BYTES = 8 * 1024**3

def _within(root: Path, filename: str) -> Path:
    if not isinstance(filename, str) or not filename or Path(filename).name != filename or filename in (".", ".."):
        raise ValueError("Filename must be a plain basename")
    if not filename.lower().endswith(".mp4"):
        raise ValueError("Only MP4 files supported")
    base = root.resolve(strict=True)
    path = (base / filename).resolve(strict=True)
    if not path.is_relative_to(base) or not path.is_file():
        raise ValueError("File is outside output directory or not a file")
    return path

def audit_mp4(output_dir: str, filename: str, *, timeout=15):
    path = _within(Path(output_dir), filename)
    size = path.stat().st_size
    if not 0 < size <= MAX_BYTES:
        raise ValueError("File size out of range")
    cmd = ["ffprobe", "-v", "error", "-show_entries",
           "format=duration,format_name:stream=codec_type,codec_name,width,height",
           "-of", "json", str(path)]
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=True)
        info = json.loads(completed.stdout)
    except (OSError, subprocess.SubprocessError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError("ffprobe could not validate media") from exc
    streams = info.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    fmt = info.get("format", {})
    try:
        duration = float(fmt["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("Missing duration") from exc
    if not videos or not math.isfinite(duration) or duration <= 0 or not all(
        isinstance(s.get("width"), int) and s["width"] > 0 and
        isinstance(s.get("height"), int) and s["height"] > 0 for s in videos
    ):
        raise ValueError("No valid video stream or duration")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"verified": True, "verification": "ffprobe_metadata_only",
            "filename": filename, "bytes": size, "sha256": digest.hexdigest(),
            "duration_seconds": round(duration, 3),
            "video_streams": [{"codec": s.get("codec_name"), "width": s["width"],
                               "height": s["height"]} for s in videos],
            "warning": "Valid container metadata does not prove all frames decode or video quality."}
