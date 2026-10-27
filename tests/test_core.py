import io
import json
import subprocess
from pathlib import Path
from PIL import Image
from fastapi.testclient import TestClient
import pytest
from studio import api as server
from studio import comfy
from studio.storage import split_script
from studio.render import srt_for_scenes


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(server, "HOME", tmp_path)
    monkeypatch.delenv("STUDIO_TOKEN", raising=False)
    monkeypatch.delenv("COMFYUI_ALLOW_REMOTE", raising=False)
    return TestClient(server.app)


def make_project(client):
    r = client.post("/api/projects", json={"title": "Phim miền Tây"})
    assert r.status_code == 201, r.text
    p = r.json()
    s = client.post(f"/api/projects/{p['id']}/scenes", json={
        "title": "Cảnh mở đầu", "dialogue": "Xin chào miền Tây!", "duration": 1
    })
    assert s.status_code == 201, s.text
    return p, s.json()


def test_script_segments_and_unicode():
    parts = split_script("Cảnh 1: Bình minh\nGhe nhỏ\n\nCảnh 2: Chợ nổi\nNắng lên")
    assert len(parts) == 2
    subtitles = srt_for_scenes([{"duration": 1.5, "dialogue": "Đất Mũi Cà Mau"},
                               {"duration": 2, "dialogue": "Tiếng đờn kìm"}])
    assert "00:00:01,500 --> 00:00:03,500" in subtitles
    assert "Đất Mũi Cà Mau" in subtitles


def test_end_to_end_crud(client):
    p, s = make_project(client)
    char = client.post(f"/api/projects/{p['id']}/characters", json={"name": "Ông Bảy", "identity": "khăn rằn"})
    assert char.status_code == 201
    update = client.patch(f"/api/projects/{p['id']}/scenes/{s['id']}",
                          json={"character_ids": [char.json()["id"]], "description": "Cà Mau"})
    assert update.status_code == 200
    prompt = client.get(f"/api/projects/{p['id']}/scenes/{s['id']}/prompt").json()
    assert "Ông Bảy" in prompt["positive"] and "khăn rằn" in prompt["positive"]
    bad = client.patch(f"/api/projects/{p['id']}/scenes/{s['id']}", json={"character_ids": ["fake"]})
    assert bad.status_code == 400
    assert len(client.get("/api/projects").json()) == 1


def test_upload_rights_and_png(client):
    p, s = make_project(client)
    image = Image.new("RGB", (20, 20), "teal")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    route = f"/api/projects/{p['id']}/scenes/{s['id']}/asset/image"
    denied = client.post(route, files={"file": ("test.png", buffer.getvalue(), "image/png")})
    assert denied.status_code == 400
    success = client.post(route, files={"file": ("test.png", buffer.getvalue(), "image/png")},
                          data={"rights_confirmed": "true", "source_note": "Ảnh do tôi chụp"})
    assert success.status_code == 200, success.text
    assert client.get(success.json()["url"]).status_code == 200
    assert client.get(f"/media/{p['id']}/assets/secrets.txt").status_code == 404


def test_workflow_substitution(tmp_path):
    (tmp_path / "test.json").write_text(json.dumps({"1": {"class_type": "TestNode", "inputs": {
        "text": "Xin chào {{PROMPT}}", "seed": "{{SEED}}", "number": "{{WIDTH}}"}}}))
    result = comfy.load_workflow(tmp_path, "test.json", {"{{PROMPT}}": "Cà Mau", "{{SEED}}": 17, "{{WIDTH}}": 1280})
    assert result["1"]["inputs"]["seed"] == 17
    assert result["1"]["inputs"]["text"] == "Xin chào Cà Mau"
    with pytest.raises(comfy.ComfyError):
        comfy.load_workflow(tmp_path, "../../passwd", {})


def test_render_with_titlecard(client):
    if not server.ffmpeg_available():
        pytest.skip("ffmpeg unavailable")
    p, s = make_project(client)
    r = client.post(f"/api/projects/{p['id']}/export")
    assert r.status_code == 200, r.text
    output = r.json()
    assert client.get(output["video"]).status_code == 200
    assert "Xin chào miền Tây" in client.get(output["srt"]).content.decode("utf-8-sig")
    assert client.get(output["provenance"]).json()["assets"][0]["kind"] == "title_card"


def test_token_on_writes(client, monkeypatch):
    monkeypatch.setenv("STUDIO_TOKEN", "secret-key")
    assert client.post("/api/projects", json={"title": "Bí mật"}).status_code == 401
    r = client.post("/api/projects", json={"title": "Hợp lệ"}, headers={"X-Studio-Token": "secret-key"})
    assert r.status_code == 201
