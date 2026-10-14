import json
import pytest
from fundpilot.gemma import extract


def test_refuse_nonlocal_endpoint():
    with pytest.raises(ValueError, match="Only local"):
        extract("Applicants must be US-based.",endpoint="https://example.org/api")


def test_blank_text():
    with pytest.raises(ValueError,match="cannot be blank"):
        extract("  ")


def test_mock_transport_validates_exact_source(monkeypatch):
    """Contract mock, not an actual Gemma inference benchmark."""
    import fundpilot.gemma as m
    clause = "Applicants must be based in the United States."
    class MockResponse:
        def __enter__(self): return self
        def __exit__(self,*args): pass
    output = {"requirements":[{"key":"us_based","mandatory":True,
        "source_quote":clause,"summary":"Applicants must be based in the United States.",
        "threshold_usd":None}]}
    def fake_open(req, timeout):
        body=json.loads(req.data)
        assert body["model"]=="gemma3:1b"
        assert body["format"]["type"]=="object"
        assert body["stream"] is False
        assert body["options"]["temperature"]==0
        response = MockResponse()
        def read(): return json.dumps({"message":{"content":json.dumps(output)}}).encode()
        response.read=read
        return response
    monkeypatch.setattr(m,"urlopen",fake_open)
    assert extract(clause).requirements[0].key == "us_based"


def test_mock_transport_blocks_invented_quote(monkeypatch):
    import fundpilot.gemma as m
    class MockResponse:
        def __enter__(self): return self
        def __exit__(self,*args): pass
    output = {"requirements":[{"key":"us_based","mandatory":True,
        "source_quote":"Must be a licensed dentist.","summary":"Requires dentist", "threshold_usd":None}]}
    def fake_open(req, timeout):
        response=MockResponse()
        response.read=lambda:json.dumps({"message":{"content":json.dumps(output)}}).encode()
        return response
    monkeypatch.setattr(m,"urlopen",fake_open)
    with pytest.raises(ValueError,match="Unverified"):
        extract("Applicants must be based in the United States.")
