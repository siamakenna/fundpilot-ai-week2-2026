"""Availability checks use adapter mocks, not model-accuracy evidence."""
import io
import json
import socket
from urllib.error import HTTPError, URLError

import pytest

from fundpilot import onboarding
from fundpilot.realworld import Applicant, analyze
from fundpilot.verification import queue_markdown


def reply(monkeypatch, value):
    calls = []
    def read(req, **kwargs):
        calls.append((req.full_url, req.get_method(), kwargs))
        return io.BytesIO(json.dumps(value).encode())
    monkeypatch.setattr(onboarding, 'urlopen', read)
    return calls


def test_ready_requires_exact_model_tag_and_only_bounded_local_get(monkeypatch):
    calls=reply(monkeypatch, {'models':[{'name':'gemma3:1b'}]})
    assert 'found in Ollama' in onboarding.check_local_model()
    assert calls == [('http://127.0.0.1:11434/api/tags','GET',{'timeout':2.5})]


@pytest.mark.parametrize('models',[[],[{'name':'gemma3:4b'}],[{'name':'gemma3:1b:cloud'}]])
def test_service_available_but_model_absent(monkeypatch,models):
    reply(monkeypatch,{'models':models})
    result=onboarding.check_local_model()
    assert 'missing' in result and 'No download was started' in result


@pytest.mark.parametrize('value',[{},[],{'models':None},{'models':[{}]}])
def test_invalid_response_is_not_ready(monkeypatch,value):
    reply(monkeypatch,value)
    assert 'Unable to confirm' in onboarding.check_local_model()


@pytest.mark.parametrize('error,expected',[
    (URLError(ConnectionRefusedError()),'not reachable'),
    (URLError(socket.timeout()),'timed out'),
    (socket.timeout(),'timed out'),
    (HTTPError('http://127.0.0.1:11434',302,'Redirect',{},None),'no redirect was followed'),
])
def test_transport_errors_are_truthful(monkeypatch,error,expected):
    def fail(*args,**kwargs):raise error
    monkeypatch.setattr(onboarding,'urlopen',fail)
    assert expected in onboarding.check_local_model()


@pytest.mark.parametrize('url',[
    'https://127.0.0.1:11434','http://example.com:11434','http://127.0.0.1:11434@evil.test',
    'http://127.0.0.1:80','http://127.0.0.1:11434/path','http://127.0.0.1:11434?q=x',
    'http://name:secret@127.0.0.1:11434',
])
def test_unsafe_configuration_never_makes_a_request(monkeypatch,url):
    monkeypatch.setattr(onboarding,'DEFAULT_OLLAMA',url)
    calls=reply(monkeypatch,{'models':[]})
    assert 'unknown' in onboarding.check_local_model()
    assert not calls


def test_malformed_or_oversized_json_is_unknown(monkeypatch):
    for raw in [b'invalid',b'x'*(1024*1024+1)]:
        monkeypatch.setattr(onboarding,'urlopen',lambda *a,**k:io.BytesIO(raw))
        assert 'Unable to confirm' in onboarding.check_local_model()


def test_empty_queue_has_scope_warning_without_zero_of_zero():
    report=analyze('Applicants must be the first author.',Applicant(first_author=True),mode='rules')
    text=queue_markdown(report,limit=3)
    assert 'Showing 0 of 0' not in text
    assert 'not eligibility approval' in text and 'linked policies' in text


def test_building_ui_does_not_probe_model(monkeypatch):
    import gradio as gr
    from fundpilot.real_ui import build_public_ui
    def forbidden(*args,**kwargs):raise AssertionError('Startup model request')
    monkeypatch.setattr(onboarding,'urlopen',forbidden)
    with gr.Blocks(analytics_enabled=False) as demo:
        build_public_ui()
    assert demo is not None
