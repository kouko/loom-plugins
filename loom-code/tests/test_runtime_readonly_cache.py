# concern: A read-only cache must report the write barrier instead of a stale lock.
"""Exercise repair when an existing runtime cache is not writable."""

import os
import subprocess
from pathlib import Path


LAUNCHER = Path(__file__).resolve().parents[1] / "scripts" / "loom-python"


def test_repair_readonly_cache_reports_write_barrier(tmp_path: Path) -> None:
    """Report the actionable cache permission problem before lock timeout."""
    cache = tmp_path / "cache" / "loom-code"
    cache.mkdir(parents=True)
    tools = tmp_path / "tools"
    tools.mkdir()
    for name in ("uv", "sleep"):
        tool = tools / name
        tool.write_text("#!/bin/sh\nexit 0\n")
        tool.chmod(0o755)
    cache.chmod(0o555)
    try:
        result = subprocess.run(
            ["/bin/sh", str(LAUNCHER), "--repair", "--list-rules"],
            env={**os.environ, "XDG_CACHE_HOME": str(cache.parent),
                 "PATH": f"{tools}:/usr/bin:/bin"},
            capture_output=True, text=True, timeout=10,
        )
    finally:
        cache.chmod(0o755)
    assert result.returncode == 2
    assert "write" in result.stderr.lower() or "permission" in result.stderr.lower(), result.stderr
    assert "lock did not clear" not in result.stderr, result.stderr
