# concern: A superseded executor must not reach vendor discovery or execution.
"""Owner records excluding Codex block every outside runner entry point."""

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
            "selected_executor": "claude",
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
    """Reject an owner record selecting Claude before model discovery."""
    calls = []
    result = external_review.discover("codex", "/repo", _record(), runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_execution_excluded_blocks():
    """Reject an owner record selecting Claude before any execution stage."""
    calls = []
    result = external_review.execute("codex", "gpt-6.1-sol", "high", "openai",
                                     "/repo", "review", _record(), runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_discovery_corrected_blocks():
    """The owner records the final Claude choice after a correction."""
    record = _record()
    record["authorization_source"]["quote"] = (
        "Use Codex? Actually use Claude to review this change")
    calls = []
    result = external_review.discover("codex", "/repo", record, runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_discovery_suggestion_blocks():
    """The owner leaves a tentative suggestion unapproved."""
    record = _record()
    record["authorization_source"]["quote"] = "Maybe Codex can review this change"
    record["approved"] = False
    calls = []
    result = external_review.discover("codex", "/repo", record, runner=_runner(calls))
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_later_blanket_cancellation_blocks_discovery_and_execution():
    """The owner removes authorization after a blanket cancellation."""
    record = _record()
    record["authorization_source"]["quote"] = (
        "Use Codex to review this change. Actually, do not use any external coding agent.")
    record["approved"] = False
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
    "Use Codex? Actually, use Claude to review this change; Codex can wait.",
])
def test_later_refusal_or_replacement_blocks_discovery_and_execution(quote):
    record = _record()
    record["authorization_source"]["quote"] = quote
    if "cancel all" in quote:
        record["approved"] = False
    calls = []
    discovered = external_review.discover("codex", "/repo", record,
                                          runner=_runner(calls))
    executed = external_review.execute("codex", "gpt-6.1-sol", "high", "openai",
                                       "/repo", "review", record,
                                       runner=_runner(calls))
    assert discovered["reason"] == "consent-missing-or-stale"
    assert executed["reason"] == "consent-missing-or-stale"
    assert calls == []
