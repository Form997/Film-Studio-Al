import pytest
from studio.experiment import experiment_plan, evaluate_observations

def project():
    return {"id": "demo", "characters": [], "scenes": [
        {"id": "scene1", "description": "Toàn cảnh dòng sông", "duration": 5, "character_ids": []}]}

def test_repeatable():
    a = experiment_plan(project(), seeds=[11, 23])
    b = experiment_plan(project(), seeds=[11, 23])
    assert a["experiment_sha256"] == b["experiment_sha256"]
    assert len(a["requests"]) == 2
    assert a["status"] == "planned_only"
    assert a["requests"][0]["request_sha256"] != a["requests"][1]["request_sha256"]

@pytest.mark.parametrize("seeds", [[1,1], [-1], [], [True]])
def test_bad_seeds(seeds):
    with pytest.raises(ValueError):
        experiment_plan(project(), seeds=seeds)

def test_bad_language():
    with pytest.raises(ValueError):
        experiment_plan(project(), language="fr")

def test_evaluation():
    obs = [{"request_sha256": "a"*64, "scores": {
        "identity_consistency": 4, "motion_smoothness": 3,
        "prompt_alignment": 5, "visual_quality": 4}}]
    result = evaluate_observations(obs)
    assert result["overall_mean"] == 4
    assert result["sample_size"] == 1

def test_no_fabricated_scores():
    with pytest.raises(ValueError):
        evaluate_observations([])
    with pytest.raises(ValueError):
        evaluate_observations([{"request_sha256": "a"*64, "scores": {}}])
