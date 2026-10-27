import pytest
from studio.film_brain import direct, compare_character_snapshots

def fixture():
    return {
        "id": "demo",
        "characters": [{"id": "a", "name": "An", "appearance": "tóc đen", "costume": "áo nâu"}],
        "scenes": [
            {"id": "s1", "description": "Cận cảnh An đi bộ", "character_ids": ["a"]},
            {"id": "s2", "description": "Toàn cảnh bến sông", "character_ids": []},
        ],
    }

@pytest.mark.parametrize("language", ["vi", "en", "zh"])
def test_languages(language):
    result = direct(fixture(), language)
    assert len(result["shots"]) == 2
    assert result["shots"][0]["character_locks"][0]["id"] == "a"
    assert result["shots"][1]["continuity"]["characters_leaving"] == ["a"]
    assert result["shots"][0]["prompt"]

def test_bad_language():
    with pytest.raises(ValueError):
        direct(fixture(), "fr")

def test_missing_reference():
    p = fixture()
    p["scenes"][0]["character_ids"] = ["unknown"]
    assert direct(p)["shots"][0]["continuity"]["missing_character_ids"] == ["unknown"]

def test_snapshot_diff():
    a = fixture()
    b = fixture()
    b["characters"][0]["costume"] = "áo xanh"
    assert compare_character_snapshots(a, b)["changed"] == ["a"]
