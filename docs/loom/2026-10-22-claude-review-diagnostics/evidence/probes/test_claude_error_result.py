# concern: A zero exit code must not turn a structured Claude error into a completed review.
"""Exercise a synthetic Claude error with a successful process exit."""

import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[5] / "loom-code/scripts/external_review.py"
SPEC = importlib.util.spec_from_file_location("external_review", SCRIPT)
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


class ClaudeErrorResultTest(unittest.TestCase):
    def test_claude_error_rejected(self):
        """A structured error cannot be returned as a completed review."""
        scope = "/synthetic-review-root"
        consent = {
            "approved": True, "executor": "claude", "review_root": scope,
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
        marker = "SYNTHETIC_PRIVATE_MARKER"
        response = json.dumps({
            "type": "result", "is_error": True,
            "result": marker + " authentication failed",
            "modelUsage": {"claude-sonnet-4-5": {}},
        })
        calls = []

        def runner(argv, **kwargs):
            calls.append(argv)
            return subprocess.CompletedProcess(argv, 0, response, "")

        result = review.execute("claude", "sonnet", "high", "anthropic", scope,
                                marker, consent, runner=runner)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["status"], "failed")
        self.assertIsNone(result["review_output"])
        self.assertNotIn(marker, json.dumps(result))
