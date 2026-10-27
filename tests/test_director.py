import uuid
import pytest
from studio.director import split_script, audit, shotlist, character_fingerprint


def project():
    return {"id": str(uuid.uuid4()), "scenes": [], "characters": []}


def test_split():
    data = split_script("Mở đầu.\n\nKết thúc.")
    assert len(data) == 2
    assert data[0]["order"] == 1


def test_empty():
    assert split_script(" \n\n ") == []


def test_audit_warns():
    assert audit(project())["issues"]


def test_audit_bad_character():
    p = project()
    p["scenes"] = split_script("Một cảnh")
    p["scenes"][0]["character_ids"] = ["missing"]
    assert audit(p)["passed"] is False


def test_fingerprint():
    char = {"name": "An", "appearance": "Tóc ngắn"}
    assert character_fingerprint(char) == character_fingerprint(char)
    assert character_fingerprint(char) != character_fingerprint({"name": "Bình"})


def test_shotlist():
    p = project()
    p["scenes"] = split_script("Cảnh đầu")
    assert shotlist(p, "vertical")["resolution"] == [720, 1280]
    with pytest.raises(ValueError):
        shotlist(p, "bad")
