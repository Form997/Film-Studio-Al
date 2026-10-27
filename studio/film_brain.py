"""Bộ đạo diễn dựa quy tắc, tự viết; hỗ trợ vi/en/zh. Không giả nhận là LLM."""
from __future__ import annotations
import hashlib
import json
import re

LANGUAGES = {"vi", "en", "zh"}
CAMERAS = {
    "vi": {"wide": "Toàn cảnh", "medium": "Trung cảnh", "close": "Cận cảnh"},
    "en": {"wide": "Wide shot", "medium": "Medium shot", "close": "Close-up"},
    "zh": {"wide": "远景", "medium": "中景", "close": "特写"},
}
NEGATIVE = {
    "vi": "không đổi khuôn mặt, không đổi trang phục, không méo tay, không nhảy cảnh",
    "en": "no identity drift, no costume changes, no malformed hands, no jump cuts",
    "zh": "人物身份一致，服装一致，手部自然，镜头连续",
}
def _clean(value: object, limit: int = 2000) -> str:
    return re.sub(r"\\s+", " ", str(value or "")).strip()[:limit]

def _shot(scene: dict) -> str:
    text = _clean(scene.get("description")).lower()
    if any(x in text for x in ("cận cảnh", "close-up", "close up", "特写", "面部")):
        return "close"
    if any(x in text for x in ("toàn cảnh", "wide shot", "远景", "全景")):
        return "wide"
    return "medium"

def _character_signature(character: dict) -> str:
    keys = ("name", "appearance", "voice", "costume", "reference")
    payload = json.dumps({k: character.get(k, "") for k in keys}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]

def direct(project: dict, language: str = "vi", aspect: str = "landscape") -> dict:
    """Tạo kế hoạch cảnh và prompt có nguồn gốc rõ, không gọi model."""
    if language not in LANGUAGES:
        raise ValueError("Ngôn ngữ phải là vi, en hoặc zh")
    if aspect not in ("landscape", "vertical", "square"):
        raise ValueError("Tỷ lệ phim không hợp lệ")
    people = {str(c.get("id")): c for c in project.get("characters", [])}
    result = []
    previous = set()
    for index, scene in enumerate(project.get("scenes", []), 1):
        ids = list(dict.fromkeys(str(x) for x in scene.get("character_ids", [])))
        missing = [cid for cid in ids if cid not in people]
        characters = [people[cid] for cid in ids if cid in people]
        descriptions = "; ".join(
            f"{_clean(c.get('name'), 100)}: {_clean(c.get('appearance'), 400)}; "
            f"costume={_clean(c.get('costume'), 200)}; "
            f"voice={_clean(c.get('voice'), 200)}"
            for c in characters
        )
        key = _shot(scene)
        desc = _clean(scene.get("description"))
        dialogue = _clean(scene.get("dialogue"))
        prompt = (
            f"Scene {index}; aspect={aspect}; shot={CAMERAS[language][key]}; "
            f"action={desc}; dialogue={dialogue}; character bible=[{descriptions}]. "
            f"Continuity: {NEGATIVE[language]}."
        )
        result.append({
            "scene_id": scene.get("id"), "order": index,
            "language": language, "camera": CAMERAS[language][key],
            "prompt": prompt, "negative_prompt": NEGATIVE[language],
            "character_locks": [
                {"id": c.get("id"), "fingerprint": _character_signature(c)}
                for c in characters
            ],
            "continuity": {
                "characters_entering": sorted(set(ids) - previous),
                "characters_leaving": sorted(previous - set(ids)),
                "missing_character_ids": missing,
                "requires_visual_review": bool(characters),
            },
        })
        previous = set(ids)
    return {
        "version": "0.3.0", "project_id": project.get("id"),
        "language": language, "aspect": aspect, "shots": result,
        "disclaimer": "Prompt-based continuity only; no face verification or video generation.",
    }

def compare_character_snapshots(before: dict, after: dict) -> dict:
    """So sánh metadata nhân vật giữa hai lần dựng."""
    left = {str(c["id"]): _character_signature(c) for c in before.get("characters", [])}
    right = {str(c["id"]): _character_signature(c) for c in after.get("characters", [])}
    return {
        "added": sorted(right.keys() - left.keys()),
        "removed": sorted(left.keys() - right.keys()),
        "changed": sorted(k for k in left.keys() & right.keys() if left[k] != right[k]),
    }
