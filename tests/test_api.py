import uuid
from fastapi.testclient import TestClient
from studio.api import app


def test_health():
    c = TestClient(app)
    assert c.get("/api/health").json()["status"] == "ok"


def test_project_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setenv("STUDIO_HOME", str(tmp_path))
    monkeypatch.delenv("STUDIO_TOKEN", raising=False)
    c = TestClient(app)
    p = c.post("/api/projects", json={"title": "Phim thử"}).json()
    assert p["title"] == "Phim thử"
    scene = c.post("/api/projects/" + p["id"] + "/scenes/from-script",
                   json={"script": "Bến sông\n\nCánh đồng"}).json()
    assert len(scene["scenes"]) == 2
    assert c.get("/api/projects/" + p["id"] + "/shotlist").status_code == 200
    assert c.get("/api/projects/" + str(uuid.uuid4())).status_code == 404
