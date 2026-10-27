import pytest
from studio.contracts import RenderSpec, canonical_hash, validate_project
from studio.engine_contract import GenerationRequest, DryRunEngine, NoEngineConfigured

def test_render_spec():
    assert RenderSpec(language="zh", aspect="vertical").export()["resolution"] == [720, 1280]
    with pytest.raises(ValueError):
        RenderSpec(fps=0)
    with pytest.raises(ValueError):
        RenderSpec(language="fr")

def test_stable_hash():
    assert canonical_hash({"b": 2, "a": 1}) == canonical_hash({"a": 1, "b": 2})

def test_validation():
    p = {"characters": [{"id": "a"}], "scenes": [{"id": "s", "character_ids": ["a"], "duration": 5}]}
    assert validate_project(p)["valid"]
    p["scenes"][0]["character_ids"] = ["missing"]
    assert not validate_project(p)["valid"]

def test_request_manifest():
    req = GenerationRequest("s", "scene", RenderSpec(), seed=7)
    assert len(req.manifest()["request_sha256"]) == 64
    with pytest.raises(NoEngineConfigured):
        DryRunEngine().generate(req)

def test_invalid_request():
    with pytest.raises(ValueError):
        GenerationRequest("", "", RenderSpec())
