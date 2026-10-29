# concern: a uv.lock that git ignores (so the repository commits no lockfile) still switches the detected suite to `uv run --locked`, so finalize-review records a package command its own attestation validator rejects.
"""Intent 2026-10-29-suite-runs-in-locked-env, Acceptance 2: a Python
repository that commits no uv lockfile gets the same suite command as before.

`uv run`, `uv sync` and `uv add` write `uv.lock` on their own, and projects
that do not commit it list it in `.gitignore`. finalize-review reads the
working tree, while attestation validation reads the commit, so an ignored
lock makes the two disagree.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker import attestation as attestation_module  # noqa: E402
from loom_checker import probes  # noqa: E402

CHECKER = SCRIPTS / "loom_checker.py"
CHANGE = "2026-10-29-example"
PASSING = [
    {"reviewer": "r1", "vendor": "openai", "model": "m", "lens": "code", "verdict": "PASS", "findings": []},
]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def ignored_lock_repo(tmp_path: Path) -> Path:
    """A Python repo that ignores uv.lock, with an ignored lock on disk and a doc-only delta."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "pyproject.toml").write_text("[project]\nname = 'x'\nversion = '0'\n", encoding="utf-8")
    (repo / ".gitignore").write_text("uv.lock\n.venv/\n", encoding="utf-8")
    (repo / "test_ok.py").write_text("def test_ok() -> None:\n    assert True\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "checkout", "-q", "-b", "feature")
    (repo / "docs").mkdir()
    (repo / "docs/guide.md").write_text("# guide\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "doc")
    # Written by any `uv run` on the developer's machine; git ignores it.
    (repo / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    assert git(repo, "status", "--porcelain") == ""
    return repo


def shims(tmp_path: Path) -> dict:
    """`python3` and a pass-through `uv` that both run this interpreter, which has pytest."""
    binary = tmp_path / "bin"
    binary.mkdir()
    (binary / "python3").write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n', encoding="utf-8")
    (binary / "uv").write_text(
        "#!/bin/sh\nwhile [ $# -gt 0 ]; do case \"$1\" in python*) break;; esac; shift; done\n"
        f'shift\nexec "{sys.executable}" "$@"\n', encoding="utf-8",
    )
    for shim in binary.iterdir():
        shim.chmod(0o755)
    env = dict(os.environ, PATH=f"{binary}{os.pathsep}{os.environ['PATH']}")
    for name in ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT", "FORCE_COLOR"):
        env.pop(name, None)
    return env


def test_detection_ignored_uv_lock_matches_committed_tree(tmp_path: Path) -> None:
    """The working-tree read finalize-review uses agrees with the commit read validation uses."""
    repo = ignored_lock_repo(tmp_path)
    head = git(repo, "rev-parse", "HEAD")

    assert probes.declared_test_command(repo) == probes.declared_test_command(repo, head)


def test_finalize_ignored_uv_lock_writes_attestation_that_validates(tmp_path: Path) -> None:
    """finalize-review in a repo that commits no lockfile writes an attestation that revalidates."""
    repo = ignored_lock_repo(tmp_path)
    review = tmp_path / "review-input.json"
    review.write_text(json.dumps({"verdicts": PASSING, "findings": [], "adversarial": []}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(CHECKER), "finalize-review", CHANGE, "--input", str(review)],
        capture_output=True, text=True, cwd=str(repo), env=shims(tmp_path),
    )
    assert result.returncode == 0, result.stderr
    attestation = json.loads((repo / f"docs/loom/{CHANGE}/attestation.json").read_text(encoding="utf-8"))

    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, None
    ) == []
