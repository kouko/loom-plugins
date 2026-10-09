# concern: Failed Claude probe output must not expose unrelated private material.
"""Failed external review must return a bounded diagnostic without raw secrets."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review  # noqa: E402


def test_claude_failedprobe_sanitized():
    """A CLI error can echo private text even when its API status is useful."""
    secret = "PRIVATE_REVIEW_MATERIAL_DO_NOT_ECHO"
    consent = {
        "approved": True, "executor": "claude", "review_root": "/repo",
        "authorization_source": {"kind": "direct-user-request",
                                 "quote": "Use Claude to review this change",
                                 "target": "this change"},
        "model": "sonnet", "effort": "high",
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }

    def runner(argv, **kwargs):
        output = {"type": "result", "is_error": True,
                  "terminal_reason": "api_error", "api_error_status": 429,
                  "result": f"Session limit reached. {secret}"}
        return subprocess.CompletedProcess(argv, 1, json.dumps(output), secret)

    result = external_review.execute("claude", "sonnet", "high", "anthropic",
                                     "/repo", "review", consent, runner=runner)
    assert result["status"] == "failed"
    assert result["reason"] == "probe-exit-1: Claude session limit (HTTP 429)"
    assert secret not in json.dumps(result)
