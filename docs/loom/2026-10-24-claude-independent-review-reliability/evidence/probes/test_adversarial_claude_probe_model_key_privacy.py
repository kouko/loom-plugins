# concern: A probe's untrusted modelUsage key must not leak CLI output into a failed public result.
"""Exercise the public failure boundary with a hostile probe model key."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review as review


def test_claude_hostile_probe_model_key_bounded():
    """A failed review cannot reveal a probe's arbitrary modelUsage key."""
    marker = "SYNTHETIC_PRIVATE_PACKET_TEXT"
    calls = []
    consent = {
        "approved": True, "executor": "claude", "review_root": "/repo",
        "authorization_source": {
            "kind": "direct-user-request", "quote": "Use Claude to review this change",
            "target": "this change", "selected_executor": "claude",
        },
        "model": "sonnet", "effort": "high",
        "disclosures": {
            "cost": True, "vendor_egress": True, "local_execution": True,
            "filesystem_access_outside_root": True,
            "filesystem_write_not_guaranteed": True,
        },
    }

    def runner(argv, **kwargs):
        calls.append(argv)
        if len(calls) == 1:
            output = {"type": "result", "result": "ok", "modelUsage": {
                "claude-sonnet-4-5-" + marker: {},
            }}
            return subprocess.CompletedProcess(argv, 0, json.dumps(output), "")
        output = {"type": "result", "is_error": True,
                  "terminal_reason": "rapid_refill_breaker", "result": marker}
        return subprocess.CompletedProcess(argv, 0, json.dumps(output), "")

    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            marker, consent, runner=runner)
    assert len(calls) == 2
    assert result["status"] == "failed"
    assert result["reason"] == "review-rapid-refill-breaker"
    assert marker not in json.dumps(result)
