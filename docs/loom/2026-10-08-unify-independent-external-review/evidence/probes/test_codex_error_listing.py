# concern: A Codex model/list JSON-RPC error must not be reported as successful discovery.
"""Reject a model-list error response without treating it as an empty list."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review


def test_model_list_error_is_failed_discovery():
    record = {
        "approved": True, "executor": "codex", "review_root": "/repo",
        "disclosures": {key: True for key in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }

    def runner(argv, **kwargs):
        response = {"jsonrpc": "2.0", "id": 2,
                    "error": {"code": -32000, "message": "not initialized"}}
        return subprocess.CompletedProcess(argv, 0, json.dumps(response), "")

    result = external_review.discover("codex", "/repo", record, runner=runner)
    assert result["status"] == "failed"
    assert result["reason"].startswith("discovery-error:")
