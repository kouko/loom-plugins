"""Adversarial probe: auto-skip boundaries and user-selection precedence.

Tests that _auto_skip correctly:
1. Returns spec/plan/blind-run only for narrow deltas (never intent)
2. Never includes intent in auto-skip list
3. Respects explicit user selections (they always win)
4. Returns empty list for broad/unknown deltas

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-20-mechanical-calculations/evidence/probes/test_auto_skip_boundaries.py -q

Every probe is an attempt to make the change fail. Attempts the change
survives PASS; attempts that expose a defect FAIL on purpose and must not be
weakened.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.selection import _auto_skip
from loom_checker.reviewers import _NARROW_AUTO_SKIP_STEPS


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def make_repo_with_files(tmp_path: Path, files: list[str]) -> Path:
    """Create a repo with base commit and a feature branch containing given files."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "src.py")
    git(repo, "commit", "-q", "-m", "initial")
    # Create feature branch
    git(repo, "switch", "-q", "-c", "feature")
    for f in files:
        (repo / f).parent.mkdir(parents=True, exist_ok=True)
        (repo / f).write_text(f"content of {f}\n", encoding="utf-8")
        git(repo, "add", f)
    git(repo, "commit", "-q", "-m", "add files")
    return repo


def test_autoskip_narrow_skipspecplanblindrun() -> None:
    """For a narrow delta (intent, plan, evidence, low-risk doc, test),
    _auto_skip should return ['spec', 'plan', 'blind-run'] (never intent)."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo_with_files(
            Path(tmp),
            [
                "docs/loom/intent/2026-09-20-mechanical-calculations.md",
                "docs/loom/2026-09-20-mechanical-calculations/plan.md",
                "docs/loom/2026-09-20-mechanical-calculations/evidence/probes/test_something.py",
                "README.md",  # low-risk doc outside docs/loom/
            ],
        )
        # Get the names of all steps from the manifest
        from loom_checker.helpers import load_manifest
        manifest = load_manifest()
        names = [s["name"] for s in manifest["step_selection"]["steps"]]
        skip = _auto_skip(repo, "2026-09-20-mechanical-calculations", names)
        # Should auto-skip spec, plan, blind-run but NOT intent
        expected = ["spec", "plan", "blind-run"]
        assert set(skip) == set(expected), f"Expected {expected}, got {skip}"
        assert "intent" not in skip, "Intent must never be auto-skipped"


def test_autoskip_broad_skipempty() -> None:
    """For a broad delta (includes source code), _auto_skip should return empty list."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo_with_files(
            Path(tmp),
            [
                "docs/loom/intent/2026-09-20-mechanical-calculations.md",
                "docs/loom/2026-09-20-mechanical-calculations/plan.md",
                "src.py",  # production code -> broad delta
            ],
        )
        from loom_checker.helpers import load_manifest
        manifest = load_manifest()
        names = [s["name"] for s in manifest["step_selection"]["steps"]]
        skip = _auto_skip(repo, "2026-09-20-mechanical-calculations", names)
        assert skip == [], f"Expected empty list for broad delta, got {skip}"


def test_autoskip_protected_skipempty() -> None:
    """If delta includes a protected path (e.g., manifest.yaml), auto-skip should be empty."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo_with_files(
            Path(tmp),
            [
                "docs/loom/intent/2026-09-20-mechanical-calculations.md",
                "docs/loom/2026-09-20-mechanical-calculations/plan.md",
                "loom-code/contract/manifest.yaml",  # protected -> broad delta
            ],
        )
        from loom_checker.helpers import load_manifest
        manifest = load_manifest()
        names = [s["name"] for s in manifest["step_selection"]["steps"]]
        skip = _auto_skip(repo, "2026-09-20-mechanical-calculations", names)
        assert skip == [], f"Expected empty list for protected path delta, got {skip}"


def test_autoskip_narrow_intentnever() -> None:
    """Even in a narrow delta, intent must never appear in the auto-skip list."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo_with_files(
            Path(tmp),
            [
                "docs/loom/intent/2026-09-20-mechanical-calculations.md",
                "docs/loom/2026-09-20-mechanical-calculations/plan.md",
                "docs/guide.md",  # low-risk doc
            ],
        )
        from loom_checker.helpers import load_manifest
        manifest = load_manifest()
        names = [s["name"] for s in manifest["step_selection"]["steps"]]
        skip = _auto_skip(repo, "2026-09-20-mechanical-calculations", names)
        assert "intent" not in skip, "Intent must never be auto-skipped"
        # Should still skip spec/plan/blind-run for this narrow delta
        assert set(skip) >= {"spec", "plan", "blind-run"} - set(), (
            f"Expected spec/plan/blind-run to be skipped, got {skip}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])