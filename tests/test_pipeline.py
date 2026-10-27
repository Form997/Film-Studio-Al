import asyncio
import uuid
import pytest
from studio import pipeline, storage

def make_project(tmp_path, monkeypatch):
    monkeypatch.setenv("STUDIO_HOME", str(tmp_path))
    pid, sid = str(uuid.uuid4()), str(uuid.uuid4())
    storage.save({"id": pid, "title": "Test", "characters": [],
                  "scenes": [{"id": sid, "description": "Toàn cảnh", "duration": 5, "character_ids": []}]})
    return pid, sid

def test_preview(tmp_path, monkeypatch):
    pid, sid = make_project(tmp_path, monkeypatch)
    result = pipeline.preview(pid)
    assert result["nodes"][0]["id"] == sid

def test_reject_foreign_scene(tmp_path, monkeypatch):
    pid, sid = make_project(tmp_path, monkeypatch)
    with pytest.raises(ValueError):
        pipeline.validate_scene(pid, str(uuid.uuid4()))

def test_submit_mock(tmp_path, monkeypatch):
    pid, sid = make_project(tmp_path, monkeypatch)
    async def fake(workflow, **kwargs):
        return {"state": "submitted_not_completed", **kwargs}
    monkeypatch.setattr("studio.pipeline.runner.submit_local", fake)
    result = asyncio.run(pipeline.submit(pid, sid, {"1": {"class_type": "A", "inputs": {}}}))
    assert result["state"] == "submitted_not_completed"

def test_attach_mock(tmp_path, monkeypatch):
    pid, sid = make_project(tmp_path, monkeypatch)
    def fake_audit(directory, filename):
        return {"filename": filename, "sha256": "a"*64, "duration_seconds": 2,
                "video_streams": [{"codec": "h264", "width": 720, "height": 1280}],
                "verification": "ffprobe_metadata_only"}
    monkeypatch.setattr("studio.pipeline.media_audit.audit_mp4", fake_audit)
    report = pipeline.verify_and_attach(pid, sid, "clip.mp4")
    assert report["scene_id"] == sid
    assert storage.load(pid)["scenes"][0]["verified_media"]["filename"] == "clip.mp4"
