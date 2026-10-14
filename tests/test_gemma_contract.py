"""Adapter contracts with mocked transport. These are NOT live Gemma benchmarks."""

import io
import json
import pytest
from fundpilot.gemma import extract


def test_refuse_nonlocal_endpoint():
    with pytest.raises(ValueError, match="Only local"):
        extract("Applicants must be US-based.", endpoint="https://example.org/api")


def test_blank_text():
    with pytest.raises(ValueError, match="cannot be blank"):
        extract("  ")


def test_mock_transport_attaches_exact_input_sentence(monkeypatch):
    import fundpilot.gemma as module

    clause = "Applicants must be based in the United States."
    output = {"key": "us_based", "mandatory": True, "threshold_usd": None}

    def fake_open(req, timeout):
        body = json.loads(req.data)
        assert body["model"] == "gemma3:1b"
        assert body["format"]["type"] == "object"
        assert body["stream"] is False
        assert body["options"]["temperature"] == 0
        assert body["prompt"].endswith(clause + "\nOutput:")
        return io.BytesIO(json.dumps({"response": json.dumps(output)}).encode())

    monkeypatch.setattr(module, "urlopen", fake_open)
    actual = extract(clause).requirements[0]
    assert actual.key == "us_based"
    assert actual.source_quote == clause


def test_mock_transport_blocks_model_supplied_quote(monkeypatch):
    import fundpilot.gemma as module

    output = {
        "key": "us_based",
        "mandatory": True,
        "threshold_usd": None,
        "source_quote": "Must be a licensed dentist.",
    }
    monkeypatch.setattr(
        module, "urlopen", lambda *a, **kw: io.BytesIO(json.dumps({"response": json.dumps(output)}).encode())
    )
    with pytest.raises(RuntimeError, match="incompatible schema"):
        extract("Applicants must be based in the United States.")
