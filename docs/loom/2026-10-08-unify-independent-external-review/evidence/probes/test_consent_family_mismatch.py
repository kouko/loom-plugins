# concern: A contradictory consented provider family must block execution.
"""Reject an exact selection outside the consented provider family."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review  # noqa: E402


def test_consent_conflict_rejected():
    """Do not let exact model and effort override a recorded family bound."""
    record = {
        "approved": True, "executor": "codex", "review_root": "/repo",
        "model": "gpt-6.1-sol", "effort": "high", "family": "google",
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        raise AssertionError("outside process started")

    result = external_review.execute("codex", "gpt-6.1-sol", "high", "openai",
                                     "/repo", "review", record, runner=runner)
    assert result["status"] == "failed"
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []
