# concern: the time limit is bypassed when the outside CLI does not read a large prompt from stdin
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "loom-code" / "scripts"))
import external_review as review  # noqa: E402


def test_launch_unreadPromptOverPipeBuffer_timesOutAtLimit(tmp_path):
    """A CLI that never reads stdin must still be stopped at the time limit.

    The prompt (1 MiB) exceeds the pipe buffer, so writing it blocks until
    the child reads or exits. The child sleeps 6 s; the limit is 0.5 s.
    """
    argv = [sys.executable, "-c", "import time; time.sleep(6)"]
    start = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired):
        review._launch(argv, input="x" * (1 << 20), timeout=0.5, cwd=str(tmp_path))
    assert time.monotonic() - start < 3
