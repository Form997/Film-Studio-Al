"""Reproducible video experiment protocol; evaluates supplied observations only."""
from __future__ import annotations
from math import isfinite
from .contracts import RenderSpec, canonical_hash
from .engine_contract import GenerationRequest

METRICS = ("identity_consistency", "motion_smoothness", "prompt_alignment", "visual_quality")

def experiment_plan(project, *, language="vi", aspect="landscape", seeds=(11, 23, 37)):
    from .contracts import validate_project
    from .film_brain import direct
    validation = validate_project(project)
    if not validation["valid"]:
        raise ValueError("; ".join(validation["issues"]))
    if not isinstance(seeds, (list, tuple)) or not 1 <= len(seeds) <= 20:
        raise ValueError("Expected 1..20 seeds")
    if len(set(seeds)) != len(seeds) or any(type(s) is not int or not 0 <= s <= 2**32-1 for s in seeds):
        raise ValueError("Seeds must be unique unsigned 32-bit integers")
    spec = RenderSpec(language=language, aspect=aspect)
    shots = direct(project, language, aspect)["shots"]
    requests = [
        GenerationRequest(str(shot["scene_id"]), shot["prompt"], spec, seed=seed).manifest()
        for shot in shots for seed in seeds
    ]
    data = {"protocol_version": "0.7.0", "project_id": project.get("id"),
            "language": language, "aspect": aspect, "seeds": list(seeds),
            "requests": requests, "engine": "not-configured",
            "status": "planned_only"}
    return {**data, "experiment_sha256": canonical_hash(data)}

def evaluate_observations(observations):
    """Aggregate human-supplied scores; do not claim automatic video assessment."""
    if not isinstance(observations, list) or not observations or len(observations) > 1000:
        raise ValueError("Expected 1..1000 observations")
    seen = set()
    clean = []
    for row in observations:
        if not isinstance(row, dict):
            raise ValueError("Each observation must be an object")
        request_hash = row.get("request_sha256")
        if not isinstance(request_hash, str) or len(request_hash) != 64 or any(c not in "0123456789abcdef" for c in request_hash):
            raise ValueError("Invalid request_sha256")
        if request_hash in seen:
            raise ValueError("Duplicate request_sha256")
        seen.add(request_hash)
        scores = row.get("scores")
        if not isinstance(scores, dict) or set(scores) != set(METRICS):
            raise ValueError("All four metrics are required")
        for key, value in scores.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or not 0 <= value <= 5:
                raise ValueError(f"Score {key} must be in [0,5]")
        clean.append(scores)
    means = {key: round(sum(row[key] for row in clean)/len(clean), 4) for key in METRICS}
    return {"method": "user_supplied_ratings", "sample_size": len(clean),
            "means": means, "overall_mean": round(sum(means.values())/len(means), 4),
            "disclaimer": "Human-entered scores only; no video was generated or automatically evaluated."}
