"""Versioned, engine-independent contracts. Python stdlib only."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import hashlib
import json

SCHEMA_VERSION = "0.4.0"
FORMATS = {"landscape": (1280, 720), "vertical": (720, 1280), "square": (1080, 1080)}
LANGUAGES = {"vi", "en", "zh"}

def canonical_hash(data: Any) -> str:
    encoded = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

@dataclass(frozen=True)
class RenderSpec:
    aspect: str = "landscape"
    fps: int = 24
    language: str = "vi"

    def __post_init__(self):
        if self.aspect not in FORMATS:
            raise ValueError("Unsupported aspect")
        if self.language not in LANGUAGES:
            raise ValueError("Unsupported language")
        if not 1 <= self.fps <= 120:
            raise ValueError("FPS out of range")

    def export(self) -> dict:
        return {"schema_version": SCHEMA_VERSION, **asdict(self), "resolution": list(FORMATS[self.aspect])}

def validate_project(project: dict) -> dict:
    issues = []
    if not isinstance(project, dict):
        return {"valid": False, "issues": ["project must be an object"]}
    characters = project.get("characters", [])
    scenes = project.get("scenes", [])
    if not isinstance(characters, list) or not isinstance(scenes, list):
        return {"valid": False, "issues": ["characters and scenes must be arrays"]}
    ids = [c.get("id") for c in characters if isinstance(c, dict)]
    if len(ids) != len(characters) or len(set(ids)) != len(ids) or any(not x for x in ids):
        issues.append("character IDs must be unique and nonempty")
    scene_ids = [s.get("id") for s in scenes if isinstance(s, dict)]
    if len(scene_ids) != len(scenes) or len(set(scene_ids)) != len(scene_ids) or any(not x for x in scene_ids):
        issues.append("scene IDs must be unique and nonempty")
    for scene in scenes:
        if not isinstance(scene, dict):
            continue
        if not isinstance(scene.get("character_ids", []), list):
            issues.append("scene character_ids must be an array")
        elif any(cid not in ids for cid in scene.get("character_ids", [])):
            issues.append(f"scene {scene.get('id')} references missing character")
        try:
            duration = float(scene.get("duration", 5))
            if not 0 < duration <= 3600:
                issues.append(f"scene {scene.get('id')} duration invalid")
        except (ValueError, TypeError):
            issues.append(f"scene {scene.get('id')} duration invalid")
    return {"valid": not issues, "issues": issues, "schema_version": SCHEMA_VERSION}
