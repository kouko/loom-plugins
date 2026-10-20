# concern: progress lines leak onto stdout and corrupt the single JSON result when the error stream is closed
"""Run the real external_review.py with its error stream closed (`2>&-`).

Python then starts with `sys.stderr` set to None, and
`print(..., file=sys.stderr)` falls back to stdout, so the progress and
closing lines land in front of the JSON result. Before this change the
script wrote nothing to stderr and stdout was exactly one JSON document.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = (Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
          / "external_review.py")
FAKE_CLAUDE = """#!{python}
import json, sys
sys.stdin.read()
print(json.dumps({{"result": "REVIEW-TEXT", "modelUsage": {{"claude-sonnet-4-5": {{}}}}}}))
"""


def _run_review(tmp_path: Path, shell_suffix: str, **kwargs):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "claude"
    fake.write_text(FAKE_CLAUDE.format(python=sys.executable))
    fake.chmod(0o755)
    scope = tmp_path / "scope"
    scope.mkdir()
    record = tmp_path / "consent.json"
    record.write_text(json.dumps({
        "approved": True, "executor": "claude", "review_root": str(scope),
        "authorization_source": {
            "kind": "direct-user-request", "quote": "Use claude to review this change",
            "target": "this change", "selected_executor": "claude"},
        "model": "sonnet", "effort": "high",
        "disclosures": {k: True for k in (
            "cost", "vendor_egress", "local_execution",
            "filesystem_access_outside_root", "filesystem_write_not_guaranteed")},
    }))
    env = {k: v for k, v in os.environ.items()
           if k not in ("FORCE_COLOR", "CLAUDE_CODE_SESSION_ID")}
    env["PATH"] = f"{bin_dir}:/usr/bin:/bin"
    cmd = ["/bin/sh", "-c", f'exec "$0" "$@" {shell_suffix}', sys.executable,
           str(SCRIPT), "--executor", "claude", "--scope", str(scope),
           "--consent-record", str(record), "--model", "sonnet", "--effort",
           "high", "--family", "anthropic"]
    return subprocess.run(cmd, input="PACKET", stdout=subprocess.PIPE, text=True,
                          env=env, timeout=60, **kwargs)


def test_external_review_closed_stderr_stdout_is_one_json_result(tmp_path):
    """With stderr closed, stdout must still be exactly one JSON result."""
    proc = _run_review(tmp_path, "2>&-", stderr=subprocess.DEVNULL)
    assert "external-review:" not in proc.stdout, proc.stdout
    result = json.loads(proc.stdout)
    assert result["status"] == "completed", result
