# concern: A consent flag without a quoted request or accepted selection must not start vendor discovery.
"""Reject a consent record that has no authorization provenance."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review


def test_missing_authorization_source_blocks_discovery():
    record = {
        "approved": True, "executor": "codex", "review_root": "/repo",
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }
    calls = []

    def runner(*args, **kwargs):
        calls.append(args)
        raise AssertionError("vendor process started without authorization source")

    result = external_review.discover("codex", "/repo", record, runner=runner)
    assert result["status"] == "failed"
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []
