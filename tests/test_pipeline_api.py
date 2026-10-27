import uuid
from fastapi.testclient import TestClient
from studio.api import app
from studio import storage

def test_pipeline_auth_and_preview(tmp_path, monkeypatch):
    monkeypatch.setenv("STUDIO_HOME", str(tmp_path))
    monkeypatch.setenv("STUDIO_TOKEN", "local-secret")
    pid, sid = str(uuid.uuid4()), str(uuid.uuid4())
    storage.save({"id": pid, "title": "Film", "characters": [],
                  "scenes": [{"id": sid, "description": "Toàn cảnh", "duration": 5, "character_ids": []}]})
    client = TestClient(app)
    assert client.get(f"/api/projects/{pid}/pipeline-preview").status_code == 200
    url = f"/api/projects/{pid}/scenes/{sid}/attach-verified"
    assert client.post(url, json={"filename": "clip.mp4"}).status_code == 401
    assert client.post(url, headers={"X-Studio-Token": "wrong"}, json={"filename": "clip.mp4"}).status_code == 401
    assert client.post(url, headers={"X-Studio-Token": "local-secret"}, json={"filename": "../bad.mp4"}).status_code == 422
    assert client.post(f"/api/projects/{pid}/scenes/{uuid.uuid4()}/submit-workflow",
                       headers={"X-Studio-Token": "local-secret"},
                       json={"workflow": {"1": {"class_type": "A", "inputs": {}}}}).status_code == 422

def test_pipeline_requires_token_configuration(tmp_path, monkeypatch):
    monkeypatch.setenv("STUDIO_HOME", str(tmp_path))
    monkeypatch.delenv("STUDIO_TOKEN", raising=False)
    client = TestClient(app)
    pid, sid = str(uuid.uuid4()), str(uuid.uuid4())
    assert client.post(f"/api/projects/{pid}/scenes/{sid}/submit-workflow",
                       json={"workflow": {}}).status_code == 403
