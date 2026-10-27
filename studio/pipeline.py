"""V1.0 local-first integration: planning, submission, verification, and scene linkage."""
from __future__ import annotations
import uuid
from pathlib import Path
from . import storage, runner, media_audit, story_engine
from .contracts import validate_project

def scene_in_project(project, scene_id):
    return next((s for s in project.get("scenes", []) if s.get("id") == scene_id), None)

def validate_scene(project_id, scene_id):
    project = storage.load(project_id)
    issues = validate_project(project)
    if not issues["valid"]:
        raise ValueError("; ".join(issues["issues"]))
    if scene_in_project(project, scene_id) is None:
        raise ValueError("Scene does not belong to project")
    return project

def preview(project_id, *, language="vi"):
    project = storage.load(project_id)
    return story_engine.analyze_story(project, language)

async def submit(project_id, scene_id, workflow, *, model_label="unverified"):
    validate_scene(project_id, scene_id)
    return await runner.submit_local(workflow, project_id=project_id,
                                     scene_id=scene_id, model_label=model_label)

def verify_and_attach(project_id, scene_id, filename, *, output_dir=None):
    project = validate_scene(project_id, scene_id)
    base = Path(output_dir) if output_dir is not None else storage.root().parent / "outputs"
    report = media_audit.audit_mp4(str(base), filename)
    scene = scene_in_project(project, scene_id)
    # Only store metadata and basename, never arbitrary paths or fabricated AI provenance.
    scene["verified_media"] = {
        "filename": report["filename"], "sha256": report["sha256"],
        "duration_seconds": report["duration_seconds"],
        "video_streams": report["video_streams"],
        "verification": report["verification"],
        "source": "user_supplied_local_file",
    }
    storage.save(project)
    return {"project_id": project_id, "scene_id": scene_id, "media": scene["verified_media"],
            "note": "Technical metadata verified; no claim of AI generation or visual quality."}
