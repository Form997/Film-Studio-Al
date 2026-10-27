import json
import subprocess
import pytest
from studio.media_audit import audit_mp4

def test_probe_metadata(tmp_path, monkeypatch):
    (tmp_path / "clip.mp4").write_bytes(b"fake mp4 for mocked ffprobe")
    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, json.dumps({
            "format": {"duration": "2.5"},
            "streams": [{"codec_type": "video", "codec_name": "h264", "width": 1280, "height": 720}]
        }), "")
    monkeypatch.setattr("studio.media_audit.subprocess.run", fake_run)
    result = audit_mp4(str(tmp_path), "clip.mp4")
    assert result["verified"] is True
    assert result["duration_seconds"] == 2.5
    assert len(result["sha256"]) == 64

@pytest.mark.parametrize("name", ["../clip.mp4", "/tmp/clip.mp4", "bad.mov", "..", "missing.mp4"])
def test_reject_paths(tmp_path, name):
    with pytest.raises((ValueError, FileNotFoundError)):
        audit_mp4(str(tmp_path), name)

def test_reject_nonvideo(tmp_path, monkeypatch):
    (tmp_path / "clip.mp4").write_bytes(b"data")
    monkeypatch.setattr("studio.media_audit.subprocess.run", lambda *a, **k:
        subprocess.CompletedProcess(a[0], 0, json.dumps({"format":{"duration":"1"}, "streams":[]}), ""))
    with pytest.raises(ValueError):
        audit_mp4(str(tmp_path), "clip.mp4")
