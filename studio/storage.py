"""Lưu dự án local-first bằng JSON nguyên tử. Chỉ dùng trên một máy."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import uuid


def root() -> Path:
    path = Path(os.getenv("STUDIO_HOME", "./data")).resolve() / "projects"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _path(project_id: str) -> Path:
    valid_id = str(uuid.UUID(project_id))
    return root() / (valid_id + ".json")


def save(project: dict) -> dict:
    location = _path(project["id"])
    payload = json.dumps(project, ensure_ascii=False, indent=2)
    fd, tempname = tempfile.mkstemp(dir=location.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        os.replace(tempname, location)
    finally:
        if os.path.exists(tempname):
            os.unlink(tempname)
    return project


def load(project_id: str) -> dict:
    location = _path(project_id)
    if not location.is_file():
        raise FileNotFoundError(project_id)
    return json.loads(location.read_text(encoding="utf-8"))


def all_projects() -> list[dict]:
    items = []
    for p in root().glob("*.json"):
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
            items.append({"id": doc["id"], "title": doc.get("title", ""), "scene_count": len(doc.get("scenes", []))})
        except (ValueError, KeyError, OSError):
            continue
    return sorted(items, key=lambda x: x["title"].lower())
