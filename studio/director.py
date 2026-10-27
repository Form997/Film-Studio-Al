"""Quy tắc phân cảnh tự xây dựng, độc lập với mô hình sinh video."""
from __future__ import annotations

import hashlib
import json
import re
import uuid


def split_script(script: str) -> list[dict]:
    """Tách văn bản theo đoạn trống; không tuyên bố suy luận ngữ nghĩa bằng AI."""
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", script.strip()) if part.strip()]
    return [
        {
            "id": str(uuid.uuid4()),
            "order": index + 1,
            "title": f"Cảnh {index + 1}",
            "description": part,
            "dialogue": "",
            "duration": 5,
            "camera": "Trung cảnh",
            "character_ids": [],
            "media": None,
        }
        for index, part in enumerate(paragraphs)
    ]


def character_fingerprint(character: dict) -> str:
    """Kiểm soát thay đổi hồ sơ, KHÔNG so khớp khuôn mặt thật."""
    fields = {k: character.get(k) for k in ("name", "appearance", "voice", "costume", "reference")}
    data = json.dumps(fields, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


def audit(project: dict) -> dict:
    characters = {c["id"] for c in project.get("characters", [])}
    issues: list[dict] = []
    scenes = project.get("scenes", [])
    if not scenes:
        issues.append({"level": "warning", "scene": None, "message": "Chưa có phân cảnh"})
    for scene in scenes:
        sid = scene.get("id")
        if not scene.get("description", "").strip():
            issues.append({"level": "warning", "scene": sid, "message": "Thiếu mô tả cảnh"})
        if float(scene.get("duration", 0)) <= 0:
            issues.append({"level": "error", "scene": sid, "message": "Thời lượng không hợp lệ"})
        for cid in scene.get("character_ids", []):
            if cid not in characters:
                issues.append({"level": "error", "scene": sid, "message": f"Nhân vật không tồn tại: {cid}"})
        if scene.get("media") is None:
            issues.append({"level": "info", "scene": sid, "message": "Chưa có nguồn hình/video; sẽ dùng thẻ tiêu đề"})
    return {"passed": not any(x["level"] == "error" for x in issues), "issues": issues, "scene_count": len(scenes)}


def shotlist(project: dict, aspect: str = "landscape") -> dict:
    resolutions = {"landscape": [1280, 720], "vertical": [720, 1280], "square": [1080, 1080]}
    if aspect not in resolutions:
        raise ValueError("Tỷ lệ phim không hợp lệ")
    registry = {c["id"]: c for c in project.get("characters", [])}
    return {
        "project_id": project["id"],
        "format": aspect,
        "resolution": resolutions[aspect],
        "scenes": [
            {
                "scene_id": s["id"],
                "order": i + 1,
                "description": s.get("description", ""),
                "dialogue": s.get("dialogue", ""),
                "duration": s.get("duration", 5),
                "camera": s.get("camera", "Trung cảnh"),
                "characters": [
                    {"id": cid, "fingerprint": character_fingerprint(registry[cid])}
                    for cid in s.get("character_ids", []) if cid in registry
                ],
            }
            for i, s in enumerate(project.get("scenes", []))
        ],
    }
