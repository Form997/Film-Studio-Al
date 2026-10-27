"""Explicit provider boundary: no model weights, no hidden cloud calls."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from .contracts import RenderSpec, canonical_hash

@dataclass(frozen=True)
class GenerationRequest:
    scene_id: str
    prompt: str
    spec: RenderSpec
    reference_paths: tuple[str, ...] = ()
    seed: int | None = None

    def __post_init__(self):
        if not self.scene_id or not self.prompt.strip():
            raise ValueError("scene_id and prompt required")
        if self.seed is not None and not 0 <= self.seed <= 2**32 - 1:
            raise ValueError("seed out of range")

    def manifest(self) -> dict:
        data = {
            "scene_id": self.scene_id, "prompt": self.prompt,
            "spec": self.spec.export(), "reference_paths": list(self.reference_paths),
            "seed": self.seed,
        }
        return {**data, "request_sha256": canonical_hash(data)}

@dataclass(frozen=True)
class GenerationResult:
    scene_id: str
    provider: str
    media_path: str
    request_sha256: str

class VideoEngine(Protocol):
    name: str
    def generate(self, request: GenerationRequest) -> GenerationResult: ...

class NoEngineConfigured(RuntimeError):
    pass

class DryRunEngine:
    """Validates contract; deliberately never pretends to generate a video."""
    name = "dry-run"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        raise NoEngineConfigured(
            "No video model configured. Inspect request.manifest() and install an explicit adapter."
        )
