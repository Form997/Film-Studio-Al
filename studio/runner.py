"""Opt-in local ComfyUI runner. No hidden GPU execution or invented output."""
from __future__ import annotations
import hashlib
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from .contracts import canonical_hash
from . import comfy

def validate_workflow(workflow):
    if not isinstance(workflow, dict) or not workflow or len(workflow) > 500:
        raise ValueError("Workflow must contain 1..500 nodes")
    for node_id, node in workflow.items():
        if not isinstance(node_id, str) or not isinstance(node, dict):
            raise ValueError("Invalid node")
        if not isinstance(node.get("class_type"), str) or not isinstance(node.get("inputs"), dict):
            raise ValueError("Each node requires class_type and inputs")
    return {"node_count": len(workflow), "workflow_sha256": canonical_hash(workflow)}

def prepare_run(workflow, *, project_id, scene_id, model_label="unverified"):
    meta = validate_workflow(workflow)
    if not project_id or not scene_id:
        raise ValueError("Project and scene IDs are required")
    data = {"protocol_version": "0.8.0", "project_id": project_id, "scene_id": scene_id,
            "model_label": model_label, "workflow": meta,
            "provider": "comfyui-local", "state": "ready_not_submitted"}
    return {**data, "run_sha256": canonical_hash(data)}

async def submit_local(workflow, *, project_id, scene_id, model_label="unverified"):
    run = prepare_run(workflow, project_id=project_id, scene_id=scene_id, model_label=model_label)
    started = time.monotonic()
    response = await comfy.submit_workflow(workflow)
    prompt_id = response.get("prompt_id") if isinstance(response, dict) else None
    try:
        prompt_id = str(uuid.UUID(str(prompt_id)))
    except (ValueError, TypeError, AttributeError):
        raise RuntimeError("ComfyUI response did not contain a valid prompt_id")
    return {**run, "state": "submitted_not_completed", "prompt_id": prompt_id,
            "submission_seconds": round(time.monotonic()-started, 3),
            "submitted_at_utc": datetime.now(timezone.utc).isoformat(),
            "note": "Submission is not proof of video output; check ComfyUI history and files."}

async def check_local(prompt_id):
    prompt_id = str(uuid.UUID(prompt_id))
    history = await comfy.get_history(prompt_id)
    record = history.get(prompt_id) if isinstance(history, dict) else None
    if not isinstance(record, dict):
        return {"prompt_id": prompt_id, "state": "pending_or_unknown", "verified_media": False}
    outputs = record.get("outputs", {})
    return {"prompt_id": prompt_id, "state": "history_available",
            "output_node_count": len(outputs) if isinstance(outputs, dict) else 0,
            "verified_media": False,
            "note": "History exists; output media not independently validated."}
