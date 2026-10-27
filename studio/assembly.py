"""V2.0: assemble verified local scene MP4s in timeline order using FFmpeg."""
from __future__ import annotations
import hashlib
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from . import storage, media_audit
from .contracts import validate_project, canonical_hash

def _hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def build_manifest(project):
    result = validate_project(project)
    if not result["valid"]:
        raise ValueError("; ".join(result["issues"]))
    scenes = project.get("scenes", [])
    if not scenes or len(scenes) > 100:
        raise ValueError("Need 1..100 scenes")
    items = []
    for scene in scenes:
        media = scene.get("verified_media")
        if not isinstance(media, dict) or not media.get("filename") or not media.get("sha256"):
            raise ValueError("Every scene must have verified_media")
        items.append({"scene_id": scene["id"], "filename": media["filename"],
                      "sha256": media["sha256"]})
    data = {"version": "2.0.0-alpha", "project_id": project["id"], "clips": items}
    return {**data, "manifest_sha256": canonical_hash(data)}

def assemble(project_id, *, width=1280, height=720, fps=24):
    if (width, height) not in ((1280,720),(720,1280),(1080,1080)) or fps not in (24,25,30):
        raise ValueError("Unsupported export preset")
    project = storage.load(project_id)
    manifest = build_manifest(project)
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg missing")
    base = storage.root().parent
    outputs = base / "outputs"
    renders = base / "renders"
    renders.mkdir(parents=True, exist_ok=True)
    sources = []
    for clip in manifest["clips"]:
        path = media_audit._within(outputs, clip["filename"])
        if _hash(path) != clip["sha256"]:
            raise ValueError("Media file changed after verification")
        sources.append(path)
    destination = renders / (str(uuid.UUID(project_id)) + "-assembled.mp4")
    with tempfile.TemporaryDirectory(dir=renders) as folder:
        work = Path(folder)
        clips = []
        for index, source in enumerate(sources):
            normalized = work / f"clip_{index:03}.mp4"
            vf = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps}"
            command = ["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",
                       "-i",str(source),"-map","0:v:0","-an","-vf",vf,
                       "-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(normalized)]
            subprocess.run(command, check=True, timeout=600)
            clips.append(normalized)
        playlist = work / "list.txt"
        playlist.write_text("".join("file '"+p.name+"'\n" for p in clips),encoding="utf-8")
        temp_target = work / "assembled.mp4"
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",
                        "-f","concat","-safe","1","-i",str(playlist),
                        "-c","copy","-movflags","+faststart",str(temp_target)],check=True,timeout=600)
        if not temp_target.is_file() or temp_target.stat().st_size == 0:
            raise RuntimeError("No assembled MP4 produced")
        os.replace(temp_target, destination)
    return {"status":"assembled_not_quality_checked","filename":destination.name,
            "scene_count":len(sources),"manifest_sha256":manifest["manifest_sha256"],
            "audio":"not_included","note":"Clips joined in scene order; inspect output before publishing."}
