"""Nonblocking introduction and manual, bounded local-model availability check."""
import json
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request

from .gemma import DEFAULT_MODEL, DEFAULT_OLLAMA, urlopen
from .logic import safe_text

INITIAL_STATUS = 'Model not checked yet. You can check whether local Ollama and Gemma are available.'
SAMPLE_STATUS = ('**CNS excerpt loaded.** Sample defaults are fictional and editable. One public excerpt, not a full eligibility '
                 'assessment. Click Analyze for a new local model request; no result is preloaded.')
INTRO = '''**Check the funding rules before writing the application.** Paste a public award announcement or load a short example. FundPilot highlights supported conditions, possible contradictions and questions to verify. **It cannot certify eligibility or guarantee an award.**

1. **Add the rules:** Include exceptions and deadlines—or load the CNS sample.
2. **Add your facts:** Answer Yes, No or Unknown. Unknown is safer than guessing.
3. **Review and verify:** Run local Gemma, check source quotations and resolve questions with the organizer.

Only public award text goes to local Gemma; applicant answers are evaluated in Python. Do not paste confidential or proprietary grant materials.'''
TUTORIAL = '''### Understand your results

- **MATCH:** A supported condition agrees with a fact you entered. It is not an overall eligibility decision.
- **NOT MATCH:** A supported condition conflicts with a fact you entered. Verify the contradiction and any published exceptions.
- **UNKNOWN:** Information is missing, the source is conditional, or the analysis cannot safely decide. Follow the verification question.
- **INFO:** A date, award benefit or other detail to review; not a confirmed eligibility condition.

### How evidence and privacy work

Live analysis runs through local Ollama. Only the public funding text goes to the model; applicant answers are evaluated in Python. Python attaches exact original source passages. Exact quotations do not prove that every condition was understood.

Downloaded reports are plain local temporary files, not encrypted secure storage. Do not paste confidential, proprietary or institutional grant documents.

Check the full official announcement, linked policies, current application cycle and deadlines. The URL you enter is for attribution; FundPilot does not automatically fetch or validate the page. A future deadline does not establish that applications are open.

### Local setup

Use **Check local model** when you want to check availability. It does not install or run a model. Start Ollama and download `gemma3:1b` separately if needed; initial installation needs internet. Viewing this tutorial makes no model request.

You may explicitly choose **Rule baseline (NO AI)** without Ollama. Failed live inference never silently switches to that mode.'''


def check_local_model():
    """Only a button calls this. No startup probe, downloads, redirects or proxies."""
    try:
        p = urlparse(DEFAULT_OLLAMA)
        if (p.scheme != 'http' or p.hostname not in ('localhost', '127.0.0.1', '::1')
            or p.port != 11434 or p.username or p.password or p.path not in ('', '/')
            or p.query or p.fragment or ':cloud' in DEFAULT_MODEL):
            return 'Model status unknown: diagnostic requires the local Ollama service on port 11434 and a downloaded model.'
        with urlopen(Request(DEFAULT_OLLAMA+'/api/tags', method='GET'), timeout=2.5) as response:
            body = response.read(1024 * 1024 + 1)
        if len(body) > 1024 * 1024:
            raise ValueError('Oversized local response')
        data = json.loads(body)
        if not isinstance(data, dict) or not isinstance(data.get('models'), list):
            raise ValueError('Invalid local response')
        tags = set()
        for entry in data['models']:
            if not isinstance(entry, dict) or not isinstance(entry.get('name'), str):
                raise ValueError('Invalid model entry')
            tags.add(entry['name'])
        model = safe_text(DEFAULT_MODEL)
        if DEFAULT_MODEL in tags:
            return f'✓ Local Gemma is available: {model} found in Ollama. This checks installation, not inference success.'
        return f'Ollama is available, but {model} is missing. Run: `ollama pull {model}`. No download was started.'
    except HTTPError:
        return 'Unable to confirm local model status. Ollama returned an HTTP error or redirect; no redirect was followed.'
    except (TimeoutError, socket.timeout):
        return 'Unable to confirm local model status: the local check timed out. Check Ollama and try again.'
    except URLError as exc:
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            return 'Unable to confirm local model status: the local check timed out. Check Ollama and try again.'
        return 'Ollama is not reachable locally. Start Ollama, then check again.'
    except (ValueError, TypeError, OSError):
        return 'Unable to confirm local model status. Check Ollama and try again.'
