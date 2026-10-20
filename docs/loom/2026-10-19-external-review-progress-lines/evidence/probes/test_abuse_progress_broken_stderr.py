# concern: a failed progress write (broken or full error stream) turns a completed review into a failed one
"""Run the real external_review.py with its error stream a pipe whose reader
has gone away.

The progress write raises BrokenPipeError inside `_launch`; `execute` maps
that OSError to `execution-error: unknown error`, so a review the CLI
completed is reported as failed. Before this change the same run completed.
Progress lines are diagnostics and must not change any status (REQ-4).
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


def _run_review(tmp_path: Path, **kwargs):
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
    cmd = [sys.executable, str(SCRIPT), "--executor", "claude", "--scope",
           str(scope), "--consent-record", str(record), "--model", "sonnet",
           "--effort", "high", "--family", "anthropic"]
    return subprocess.run(cmd, input="PACKET", stdout=subprocess.PIPE, text=True,
                          env=env, timeout=60, **kwargs)


def test_external_review_broken_stderr_status_stays_completed(tmp_path):
    """A broken error stream must not turn a completed review into a failure."""
    read_end, write_end = os.pipe()
    os.close(read_end)
    try:
        proc = _run_review(tmp_path, stderr=write_end)
    finally:
        os.close(write_end)
    result = json.loads(proc.stdout.splitlines()[-1])
    assert result["status"] == "completed", result
    assert proc.returncode == 0, proc.returncode
