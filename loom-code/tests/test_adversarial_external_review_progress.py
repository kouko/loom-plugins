"""Adversarial programs for external-review progress lines on stderr.

concern: a progress write leaks onto stdout and corrupts the single JSON
result when the error stream is closed, or a failed write (broken or full
error stream) turns a completed review into a failed one.

Graduated from the 2026-10-19-external-review-progress-lines change store.
Both run the real external_review.py against a fake `claude` CLI: one with
its error stream closed (`2>&-`, so Python starts with `sys.stderr` None
and `print` falls back to stdout), one with its error stream a pipe whose
reader has gone away (the write raises BrokenPipeError).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "external_review.py"
FAKE_CLAUDE = """#!{python}
import json, sys
sys.stdin.read()
print(json.dumps({{"result": "REVIEW-TEXT", "modelUsage": {{"claude-sonnet-4-5": {{}}}}}}))
"""
ARGS = ["--executor", "claude", "--model", "sonnet", "--effort", "high",
        "--family", "anthropic"]


def _run_review(tmp_path: Path, shell_suffix: str | None, **kwargs):
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
    review = [str(SCRIPT), "--scope", str(scope), "--consent-record", str(record), *ARGS]
    if shell_suffix is None:
        cmd = [sys.executable, *review]
    else:
        cmd = ["/bin/sh", "-c", f'exec "$0" "$@" {shell_suffix}', sys.executable, *review]
    return subprocess.run(cmd, input="PACKET", stdout=subprocess.PIPE, text=True,
                          env=env, timeout=60, **kwargs)


def test_external_review_closed_stderr_stdout_is_one_json_result(tmp_path):
    """With stderr closed, stdout must still be exactly one JSON result."""
    proc = _run_review(tmp_path, "2>&-", stderr=subprocess.DEVNULL)
    assert "external-review:" not in proc.stdout, proc.stdout
    result = json.loads(proc.stdout)
    assert result["status"] == "completed", result


def test_external_review_broken_stderr_status_stays_completed(tmp_path):
    """A broken error stream must not turn a completed review into a failure."""
    read_end, write_end = os.pipe()
    os.close(read_end)
    try:
        proc = _run_review(tmp_path, None, stderr=write_end)
    finally:
        os.close(write_end)
    result = json.loads(proc.stdout.splitlines()[-1])
    assert result["status"] == "completed", result
    assert proc.returncode == 0, proc.returncode
