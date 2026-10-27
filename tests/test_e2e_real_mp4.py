"""End-to-end test using real FFmpeg-generated MP4 clips; no GPU or AI model."""
import hashlib
import json
import shutil
import subprocess
import uuid
import pytest
from studio import storage, pipeline, assembly

@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"),
                    reason="FFmpeg and ffprobe required")
def test_real_mp4_attach_and_assemble(tmp_path, monkeypatch):
    monkeypatch.setenv("STUDIO_HOME", str(tmp_path))
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    pid = str(uuid.uuid4())
    scene_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    storage.save({"id": pid, "title": "Real MP4 E2E", "characters": [],
                  "scenes": [{"id": sid, "description": "Cảnh thử", "duration": 1,
                              "character_ids": []} for sid in scene_ids]})
    for index, sid in enumerate(scene_ids):
        name = f"scene_{index}.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
                        "-f", "lavfi", "-i", f"color=c={'red' if index == 0 else 'blue'}:s=320x240:r=24:d=1",
                        "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-y", str(outputs / name)], check=True, timeout=90)
        linked = pipeline.verify_and_attach(pid, sid, name)
        assert linked["media"]["sha256"] == hashlib.sha256((outputs/name).read_bytes()).hexdigest()
    result = assembly.assemble(pid, width=1280, height=720, fps=24)
    assert result["scene_count"] == 2
    rendered = tmp_path / "renders" / result["filename"]
    assert rendered.exists() and rendered.stat().st_size > 0
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration:stream=codec_type,width,height",
                            "-of", "json", str(rendered)],
                           capture_output=True, text=True, check=True, timeout=30)
    info = json.loads(probe.stdout)
    assert 1.8 <= float(info["format"]["duration"]) <= 2.2
    assert any(s.get("codec_type") == "video" and s.get("width") == 1280
               and s.get("height") == 720 for s in info["streams"])
