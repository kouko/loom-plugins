# concern: `init` must refuse a hostile store path with a clean LoomMemoryError
# and no traceback — every other refusal path prints the "nothing was created"
# banner and `validate` handles the same shapes cleanly — but a target whose
# parent is a file (NotADirectoryError) or a broken symlink (FileExistsError)
# crashes with an uncaught traceback instead.
"""Adversarial probe — `init` crashes with an uncaught traceback on hostile
store paths instead of refusing cleanly.

Two reachable shapes, no intent required:
- the store path's parent is a regular file  -> NotADirectoryError
- the store path is a broken symlink         -> FileExistsError

`validate` on the same paths reports a clean `store-missing` violation and
exits 1; `init`'s own contract says a refusal exits 1 naming the offender
with "nothing was created". This probe runs the real CLI on both shapes and
requires a non-zero exit WITHOUT a traceback.

RED today: both shapes print a Python traceback — the probe's assertion
fails.
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[5]
SCRIPT_REL = "loom-workflow/skills/loom-memory/scripts/loom_memory.py"


def _run_init(store: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / SCRIPT_REL), "init", str(store)],
        capture_output=True,
        text=True,
    )


def test_init_hostile_path_refusal_clean() -> None:
    """Init refusal on hostile paths must be a clean LoomMemoryError exit, no
    traceback; both shapes crash today, so this probe is RED."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="loom-adv-d-"))
    try:
        # shape 1 — the store's parent is a regular file
        (tmp / "afile").write_text("x", encoding="utf-8")
        result = _run_init(tmp / "afile" / "memory")
        assert result.returncode != 0, "init on a file-parented path must not succeed"
        assert "Traceback" not in result.stderr, (
            "init on a parent-is-a-file path crashed with a traceback instead of "
            f"a clean refusal:\n{result.stderr.strip()}"
        )

        # shape 2 — the store target is a broken symlink
        (tmp / "brokenlink").symlink_to(tmp / "nowhere")
        result = _run_init(tmp / "brokenlink")
        assert result.returncode != 0, "init on a broken-symlink target must not succeed"
        assert "Traceback" not in result.stderr, (
            "init on a broken-symlink target crashed with a traceback instead of "
            f"a clean refusal:\n{result.stderr.strip()}"
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
