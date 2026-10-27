"""Deterministic story-graph and editing diagnostics. No LLM, no model weights."""
from __future__ import annotations
import re
from .contracts import validate_project, canonical_hash

LEXICON = {
    "vi": {"establish": ("toàn cảnh", "bối cảnh", "mở đầu"), "detail": ("cận cảnh", "ánh mắt", "bàn tay"), "action": ("chạy", "bước", "đuổi", "đánh"), "dialogue": ("nói", "hỏi", "đáp")},
    "en": {"establish": ("wide shot", "establishing", "landscape"), "detail": ("close-up", "close up", "eyes", "hands"), "action": ("run", "walk", "chase", "fight"), "dialogue": ("say", "ask", "reply")},
    "zh": {"establish": ("全景", "远景", "开场"), "detail": ("特写", "眼神", "手部"), "action": ("奔跑", "走", "追逐"), "dialogue": ("说", "问", "回答")},
}
SHOTS = {"vi": {"establish": "Toàn cảnh", "detail": "Cận cảnh", "action": "Trung cảnh động", "dialogue": "Trung cảnh", "neutral": "Trung cảnh"},
         "en": {"establish": "Wide shot", "detail": "Close-up", "action": "Moving medium shot", "dialogue": "Medium shot", "neutral": "Medium shot"},
         "zh": {"establish": "全景", "detail": "特写", "action": "运动中景", "dialogue": "中景", "neutral": "中景"}}
TRANSITIONS = {"vi": {"cut": "Cắt thẳng", "dissolve": "Hòa hình"},
               "en": {"cut": "Cut", "dissolve": "Dissolve"},
               "zh": {"cut": "硬切", "dissolve": "叠化"}}

def classify_scene(scene, language="vi"):
    if language not in LEXICON:
        raise ValueError("Unsupported language")
    description = str(scene.get("description", "")).casefold()
    scores = {key: sum(1 for term in terms if term in description)
              for key, terms in LEXICON[language].items()}
    if str(scene.get("dialogue", "")).strip():
        scores["dialogue"] += 1
    priority = ("detail", "establish", "action", "dialogue")
    kind = max(priority, key=lambda key: (scores[key], -priority.index(key)))
    return kind if scores[kind] else "neutral"

def analyze_story(project, language="vi"):
    if language not in LEXICON:
        raise ValueError("Unsupported language")
    validation = validate_project(project)
    if not validation["valid"]:
        raise ValueError("; ".join(validation["issues"]))
    scenes = project.get("scenes", [])
    nodes = []
    edges = []
    issues = []
    total_duration = 0.0
    previous_ids = set()
    previous_kind = None
    for i, scene in enumerate(scenes):
        kind = classify_scene(scene, language)
        characters = set(scene.get("character_ids", []))
        duration = float(scene.get("duration", 5))
        total_duration += duration
        transition = "dissolve" if previous_kind == "establish" and kind == "establish" else "cut"
        nodes.append({
            "id": scene["id"], "order": i + 1, "kind": kind,
            "recommended_camera": SHOTS[language][kind],
            "duration_seconds": duration,
            "characters_entering": sorted(characters - previous_ids),
            "characters_leaving": sorted(previous_ids - characters),
            "transition_from_previous": None if i == 0 else TRANSITIONS[language][transition],
            "transition_code": None if i == 0 else transition,
        })
        if i:
            edges.append({"from": scenes[i - 1]["id"], "to": scene["id"],
                          "transition": transition})
        if not str(scene.get("description", "")).strip():
            issues.append({"scene_id": scene["id"], "code": "empty_description"})
        if duration < 2:
            issues.append({"scene_id": scene["id"], "code": "very_short_scene"})
        previous_ids, previous_kind = characters, kind
    if not nodes:
        issues.append({"scene_id": None, "code": "no_scenes"})
    data = {"version": "0.6.0", "language": language, "nodes": nodes,
            "edges": edges, "duration_seconds": round(total_duration, 3),
            "issues": issues, "method": "explainable_rule_based_planner"}
    return {**data, "plan_sha256": canonical_hash(data)}
