import pytest
from studio.runner import prepare_run, validate_workflow, submit_local, check_local

WF = {"1": {"class_type": "TestNode", "inputs": {"seed": 11}}}

def test_workflow():
    assert validate_workflow(WF)["node_count"] == 1
    assert prepare_run(WF, project_id="p", scene_id="s")["state"] == "ready_not_submitted"

def test_hash_repeatable():
    a = prepare_run(WF, project_id="p", scene_id="s")
    b = prepare_run(WF, project_id="p", scene_id="s")
    assert a["run_sha256"] == b["run_sha256"]

@pytest.mark.parametrize("bad", [{}, {"1": {}}, {"1": {"class_type": "A"}}])
def test_bad_workflow(bad):
    with pytest.raises(ValueError):
        validate_workflow(bad)

@pytest.mark.asyncio
async def test_submit_mock(monkeypatch):
    async def fake(workflow):
        return {"prompt_id": "12345678-1234-1234-1234-123456789abc"}
    monkeypatch.setattr("studio.runner.comfy.submit_workflow", fake)
    result = await submit_local(WF, project_id="p", scene_id="s")
    assert result["state"] == "submitted_not_completed"

@pytest.mark.asyncio
async def test_history_mock(monkeypatch):
    async def fake(prompt_id):
        return {prompt_id: {"outputs": {"1": {}}}}
    monkeypatch.setattr("studio.runner.comfy.get_history", fake)
    result = await check_local("12345678-1234-1234-1234-123456789abc")
    assert result["verified_media"] is False
