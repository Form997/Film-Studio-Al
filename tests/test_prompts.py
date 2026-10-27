from studio.prompts import compose_prompt


def test_prompt_contains_character():
    scene = {"description": "Dòng sông", "camera": "toàn cảnh", "character_ids": ["abc"]}
    characters = [{"id": "abc", "name": "An", "appearance": "tóc đen", "costume": "áo nâu"}]
    out = compose_prompt(scene, characters)
    assert "Dòng sông" in out
    assert "An" in out
    assert "áo nâu" in out


def test_prompt_without_characters():
    assert "Cánh đồng" in compose_prompt({"description": "Cánh đồng"}, [])
