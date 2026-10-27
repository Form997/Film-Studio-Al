"""Chuẩn hóa mô tả cảnh/nhân vật do studio tự viết, không ràng buộc model."""
from __future__ import annotations


def compose_prompt(scene: dict, characters: list[dict], style: str = "cinematic") -> str:
    """Tạo prompt có cấu trúc cho engine ngoài; không bảo đảm nhận diện mặt."""
    indexed = {x.get("id"): x for x in characters}
    parts = [f"Visual style: {style}", f"Shot: {scene.get('camera', 'medium shot')}",
             f"Action and location: {scene.get('description', '')}"]
    for ident in scene.get("character_ids", []):
        character = indexed.get(ident)
        if character:
            parts.append(
                "Character: " + character.get("name", "") +
                "; appearance: " + character.get("appearance", "") +
                "; costume: " + character.get("costume", "")
            )
    if scene.get("dialogue"):
        parts.append("Vietnamese dialogue: " + scene["dialogue"])
    return "\n".join(parts)
