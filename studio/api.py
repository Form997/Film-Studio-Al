"""Ứng dụng chỉ dành cho localhost; cần xác thực đầy đủ trước khi triển khai SaaS."""
from __future__ import annotations

import os
from pathlib import Path
import uuid

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import storage, director, render

app = FastAPI(title="HAI ĐẤT AI FILM STUDIO", version="0.2.0")
WEB = Path(__file__).resolve().parent.parent / "web"


def guard(token: str | None):
    expected = os.getenv("STUDIO_TOKEN", "")
    if expected and token != expected:
        raise HTTPException(status_code=401, detail="Sai mã truy cập thao tác ghi")


def get(project_id: str):
    try:
        return storage.load(project_id)
    except (FileNotFoundError, ValueError, AttributeError):
        raise HTTPException(status_code=404, detail="Không tìm thấy dự án")


class ProjectInput(BaseModel):
    title: str = Field(min_length=1, max_length=140)
    script: str = Field(default="", max_length=100000)


class ScriptInput(BaseModel):
    script: str = Field(max_length=100000)


class CharacterInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    appearance: str = Field(default="", max_length=5000)
    voice: str = Field(default="", max_length=1000)
    costume: str = Field(default="", max_length=2000)
    reference: str = Field(default="", max_length=500)


class SceneInput(BaseModel):
    description: str = Field(min_length=1, max_length=10000)
    dialogue: str = Field(default="", max_length=5000)
    duration: float = Field(default=5, ge=1, le=30)
    camera: str = Field(default="Trung cảnh", max_length=200)
    character_ids: list[str] = Field(default_factory=list)


class ReorderInput(BaseModel):
    ids: list[str]


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.2.0", "video_ai": "optional external engine"}


@app.get("/api/projects")
def list_projects():
    return storage.all_projects()


@app.post("/api/projects")
def create_project(body: ProjectInput, x_studio_token: str | None = Header(None)):
    guard(x_studio_token)
    document = {"id": str(uuid.uuid4()), "title": body.title, "script": body.script, "scenes": [], "characters": []}
    return storage.save(document)


@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    return get(project_id)


@app.put("/api/projects/{project_id}")
def update_project(project_id: str, body: ProjectInput, x_studio_token: str | None = Header(None)):
    guard(x_studio_token)
    document = get(project_id)
    document.update({"title": body.title, "script": body.script})
    return storage.save(document)


@app.post("/api/projects/{project_id}/scenes/from-script")
def split_project(project_id: str, body: ScriptInput, x_studio_token: str | None = Header(None)):
    guard(x_studio_token)
    document = get(project_id)
    document["script"] = body.script
    document["scenes"] = director.split_script(body.script)
    return storage.save(document)


@app.post("/api/projects/{project_id}/characters")
def add_character(project_id: str, body: CharacterInput, x_studio_token: str | None = Header(None)):
    guard(x_studio_token)
    document = get(project_id)
    character = {"id": str(uuid.uuid4()), **body.model_dump()}
    document["characters"].append(character)
    storage.save(document)
    return character


@app.post("/api/projects/{project_id}/scenes")
def add_scene(project_id: str, body: SceneInput, x_studio_token: str | None = Header(None)):
    guard(x_studio_token)
    document = get(project_id)
    scene = {"id": str(uuid.uuid4()), "title": f"Cảnh {len(document['scenes']) + 1}",
             "order": len(document["scenes"]) + 1, "media": None, **body.model_dump()}
    document["scenes"].append(scene)
    storage.save(document)
    return scene


@app.post("/api/projects/{project_id}/scenes/reorder")
def reorder(project_id: str, body: ReorderInput, x_studio_token: str | None = Header(None)):
    guard(x_studio_token)
    document = get(project_id)
    old = {scene["id"]: scene for scene in document["scenes"]}
    if len(body.ids) != len(old) or set(body.ids) != set(old):
        raise HTTPException(status_code=422, detail="Danh sách ID cảnh phải khớp hoàn toàn")
    document["scenes"] = [{**old[sid], "order": i + 1} for i, sid in enumerate(body.ids)]
    return storage.save(document)


@app.get("/api/projects/{project_id}/quality")
def quality(project_id: str):
    return director.audit(get(project_id))


@app.get("/api/projects/{project_id}/shotlist")
def shots(project_id: str, aspect: str = "landscape"):
    try:
        return director.shotlist(get(project_id), aspect)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@app.post("/api/projects/{project_id}/render")
def render_project(project_id: str, x_studio_token: str | None = Header(None)):
    guard(x_studio_token)
    document = get(project_id)
    try:
        result = render.render(document)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"download_url": f"/api/projects/{project_id}/render.mp4", "file": result.name}


@app.get("/api/projects/{project_id}/render.mp4")
def download(project_id: str):
    get(project_id)
    path = Path(os.getenv("STUDIO_HOME", "./data")).resolve() / "renders" / (str(uuid.UUID(project_id)) + ".mp4")
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Chưa xuất bản MP4")
    return FileResponse(path, filename="hai-dat-film-" + path.name, media_type="video/mp4")


app.mount("/", StaticFiles(directory=str(WEB), html=True), name="web")
