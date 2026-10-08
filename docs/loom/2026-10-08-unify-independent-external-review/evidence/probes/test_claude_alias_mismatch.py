# concern: A Claude alias must not accept a different observed model tier.
"""The observed Claude tier must agree with the selected alias."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review
from loom_checker import reviewers


def test_sonnet_alias_cannot_accept_opus_observation():
    record = {
        "approved": True, "executor": "claude", "review_root": "/repo",
        "model": "sonnet", "effort": "high",
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        output = {"result": "ok", "modelUsage": {"claude-opus-4-1": {}}}
        return subprocess.CompletedProcess(argv, 0, json.dumps(output), "")

    result = external_review.execute("claude", "sonnet", "high", "anthropic",
                                     "/repo", "review", record, runner=runner)
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert len(calls) == 1


def test_sonnet_alias_receipt_cannot_claim_opus_observation():
    verdicts = [
        {"vendor": "openai", "lens": "code"},
        {"vendor": "anthropic", "lens": "code", "model": "sonnet",
         "reviewer": "outside-1", "external_review": {
             "status": "completed", "executor": "claude", "model": "sonnet",
             "effort": "high", "family": "anthropic",
             "evidence_level": "accepted-explicit-settings",
             "observed_model": "claude-opus-4-1", "observed_effort": None,
             "output_digest": "a" * 64, "reviewer": "outside-1"}},
    ]
    failure = reviewers.outside_verdict_failure(verdicts, "anthropic")
    assert failure is not None
