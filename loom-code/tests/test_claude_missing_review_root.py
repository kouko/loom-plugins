# concern: Claude discovery must not report completion for a missing review root.
"""Exercise the path that lists documented aliases without spawning a CLI."""

from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import external_review as review  # noqa: E402


def test_claude_discovery_reports_missing_review_root(tmp_path: Path) -> None:
    scope = str(tmp_path / "PRIVATE_MISSING_REVIEW_ROOT")
    record = {
        "approved": True,
        "executor": "claude",
        "review_root": scope,
        "authorization_source": {
            "kind": "direct-user-request",
            "quote": "Use Claude to review this change",
            "target": "this change", "selected_executor": "claude",
        },
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }

    def no_spawn(*args: object, **kwargs: object) -> None:
        raise AssertionError("model discovery should not spawn a CLI")

    result = review.discover("claude", scope, record, runner=no_spawn)

    assert result["status"] == "failed"
    assert result["reason"] == "discovery-error: review-root-not-found"
    assert result["candidates"] == []
    assert scope not in json.dumps(result)
