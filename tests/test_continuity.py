import pytest
from studio.continuity import validate_pose, pose_distance, motion_report, compare_attributes

def test_identical_pose():
    p = {"nose": [0.5, 0.5], "left_wrist": [0.3, 0.5]}
    assert pose_distance(p, p)["distance"] == 0

def test_jump():
    frames = [{"nose": [0, 0]}, {"nose": [0.1, 0]}, {"nose": [0.9, 0]}]
    report = motion_report(frames, jump_threshold=0.2)
    assert report["possible_jump_count"] == 1
    assert report["median_displacement"] == 0.45

def test_missing_common_joint():
    assert pose_distance({"nose": [0, 0]}, {"wrist": [0, 0]})["status"] == "insufficient_data"

@pytest.mark.parametrize("bad", [
    {"nose": [-1, 0]}, {"nose": [float("nan"), 0]}, {"nose": [True, 0]},
    {"nose": [1, 2]}, {}, {"nose": [0]},
])
def test_bad_pose(bad):
    with pytest.raises(ValueError):
        validate_pose(bad)

def test_invalid_frames():
    with pytest.raises(ValueError):
        motion_report([{"nose": [0, 0]}])

def test_metadata():
    result = compare_attributes({"costume": "brown"}, {"costume": "blue"})
    assert result["changed_fields"] == ["costume"]
