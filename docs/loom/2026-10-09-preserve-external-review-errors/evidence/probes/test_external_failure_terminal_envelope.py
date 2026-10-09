# concern: Nonterminal Claude JSON must not impersonate a trusted API failure.
"""Only a terminal CLI result may establish a failure reason."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review  # noqa: E402


def test_claude_assistantenvelope_unknown():
    """An assistant message carrying error-like keys is not CLI error evidence."""
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
        output = {"type": "assistant", "is_error": True,
                  "terminal_reason": "api_error", "api_error_status": 429,
                  "result": "session limit"}
        return subprocess.CompletedProcess(argv, 1, json.dumps(output), "")

    result = external_review.execute("claude", "sonnet", "high", "anthropic",
                                     "/repo", "review", consent, runner=runner)
    assert result["status"] == "failed"
    assert result["reason"] == "probe-exit-1: unknown error"
