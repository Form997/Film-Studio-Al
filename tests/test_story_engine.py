import pytest
from studio.story_engine import classify_scene, analyze_story

def project():
    return {"id": "p", "characters": [{"id": "a", "name": "An"}],
            "scenes": [
                {"id": "1", "description": "Toàn cảnh bến sông", "duration": 5, "character_ids": ["a"]},
                {"id": "2", "description": "Cận cảnh ánh mắt", "duration": 3, "character_ids": []},
            ]}

@pytest.mark.parametrize("language,description,expected", [
    ("vi", "Toàn cảnh bến sông", "establish"),
    ("en", "Close-up of hands", "detail"),
    ("zh", "奔跑在田野", "action"),
])
def test_classification(language, description, expected):
    assert classify_scene({"description": description}, language) == expected

def test_story_graph():
    result = analyze_story(project())
    assert len(result["nodes"]) == 2
    assert len(result["edges"]) == 1
    assert result["nodes"][1]["characters_leaving"] == ["a"]
    assert result["duration_seconds"] == 8
    assert len(result["plan_sha256"]) == 64
    assert analyze_story(project())["plan_sha256"] == result["plan_sha256"]

def test_missing_character():
    p = project()
    p["scenes"][0]["character_ids"] = ["unknown"]
    with pytest.raises(ValueError):
        analyze_story(p)

def test_language():
    with pytest.raises(ValueError):
        analyze_story(project(), "fr")

def test_empty():
    result = analyze_story({"scenes": [], "characters": []})
    assert result["issues"][0]["code"] == "no_scenes"
