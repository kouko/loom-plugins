# concern: Malformed model discovery must fail as a structured result.
"""Treat an invalid app-server response as a failed candidate observation."""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review  # noqa: E402


def test_discovery_null_failed():
    """Do not crash when a JSON-RPC response line is JSON null."""
    record = {
        "approved": True, "executor": "codex", "review_root": "/repo",
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }

    def runner(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 0, "null\n", "")

    result = external_review.discover("codex", "/repo", record, runner=runner)
    assert result["status"] == "failed"
    assert result["reason"].startswith("discovery-error:")
