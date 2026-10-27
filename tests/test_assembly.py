import uuid
import pytest
from studio.assembly import build_manifest, assemble
from studio import storage

def project():
    return {"id":str(uuid.uuid4()),"characters":[],"scenes":[
        {"id":"s1","description":"Toàn cảnh","duration":5,"character_ids":[],
         "verified_media":{"filename":"one.mp4","sha256":"a"*64}},
        {"id":"s2","description":"Cận cảnh","duration":5,"character_ids":[],
         "verified_media":{"filename":"two.mp4","sha256":"b"*64}}]}

def test_order_and_hash():
    p=project()
    m=build_manifest(p)
    assert [c["scene_id"] for c in m["clips"]]==["s1","s2"]
    assert build_manifest(p)["manifest_sha256"]==m["manifest_sha256"]

def test_missing_media():
    p=project()
    del p["scenes"][0]["verified_media"]
    with pytest.raises(ValueError):
        build_manifest(p)

def test_export_preset(tmp_path,monkeypatch):
    monkeypatch.setenv("STUDIO_HOME",str(tmp_path))
    p=project()
    storage.save(p)
    with pytest.raises(ValueError):
        assemble(p["id"],width=123,height=456)
