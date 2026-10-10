# concern: A superseded executor must not reach vendor discovery or execution.
"""An explicit replacement choice must block every outside runner entry point."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import external_review  # noqa: E402


def _record():
    return {
        "approved": True,
        "executor": "codex",
        "review_root": "/repo",
        "authorization_source": {
            "kind": "direct-user-request",
            "quote": "Please use Claude instead of Codex to review this change",
            "target": "this change",
            "selected_executor": "codex",
        },
        "model": "gpt-6.1-sol",
        "effort": "high",
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }


def _runner(calls):
    def run(argv, **kwargs):
        calls.append(argv)
        if argv[:2] == ["codex", "app-server"]:
            listing = {"id": 2, "result": {"data": [{"id": "gpt-6.1-sol"}]}}
            return subprocess.CompletedProcess(argv, 0, json.dumps(listing), "")
        return subprocess.CompletedProcess(
            argv, 0, "outside response", "model: gpt-6.1-sol\nreasoning effort: high\n")
    return run


def test_discovery_excluded_blocks():
    """Reject a superseded Codex choice before model discovery."""
    calls = []
    result = external_review.discover("codex", "/repo", _record(), runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_execution_excluded_blocks():
    """Reject a superseded Codex choice before any execution stage."""
    calls = []
    result = external_review.execute("codex", "gpt-6.1-sol", "high", "openai",
                                     "/repo", "review", _record(), runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_discovery_corrected_blocks():
    """Reject a later choice of Claude after Codex was only proposed."""
    record = _record()
    record["authorization_source"]["quote"] = (
        "Use Codex? Actually use Claude to review this change")
    calls = []
    result = external_review.discover("codex", "/repo", record, runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_discovery_suggestion_blocks():
    """A tentative suggestion is not a direct request to run Codex."""
    record = _record()
    record["authorization_source"]["quote"] = "Maybe Codex can review this change"
    calls = []
    result = external_review.discover("codex", "/repo", record, runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_later_blanket_cancellation_blocks_discovery_and_execution():
    """A later cancellation of every outside agent revokes a named request."""
    record = _record()
    record["authorization_source"]["quote"] = (
        "Use Codex to review this change. Actually, do not use any external coding agent.")
    calls = []
    discovered = external_review.discover("codex", "/repo", record,
                                          runner=_runner(calls))
    executed = external_review.execute("codex", "gpt-6.1-sol", "high", "openai",
                                       "/repo", "review", record,
                                       runner=_runner(calls))
    assert discovered["reason"] == "consent-missing-or-stale"
    assert executed["reason"] == "consent-missing-or-stale"
    assert calls == []


@pytest.mark.parametrize("quote", [
    "Use Codex to review this change. Actually, cancel all outside reviews.",
    "I refuse to use Codex for this change; use Claude instead.",
    "Use Codex to review this change. Wait, use Claude instead.",
])
def test_later_refusal_or_replacement_blocks_discovery_and_execution(quote):
    record = _record()
    record["authorization_source"]["quote"] = quote
    calls = []
    discovered = external_review.discover("codex", "/repo", record,
                                          runner=_runner(calls))
    executed = external_review.execute("codex", "gpt-6.1-sol", "high", "openai",
                                       "/repo", "review", record,
                                       runner=_runner(calls))
    assert discovered["reason"] == "consent-missing-or-stale"
    assert executed["reason"] == "consent-missing-or-stale"
    assert calls == []
