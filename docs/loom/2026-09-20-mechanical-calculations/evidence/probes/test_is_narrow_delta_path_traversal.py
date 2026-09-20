"""Adversarial probe: is_narrow_delta rejects path traversal outside repo.

The function must reject paths that escape via '..' components or absolute paths,
as such paths indicate either hostile input or confusion about the repository
boundary, and must keep the reviewer floor at 2 (default) to prevent unsafe
auto-skip of spec/plan/blind-run.
"""
from __future__ import annotations

import pytest

from loom_checker.reviewers import is_narrow_delta


def test_is_narrow_delta_rejects_double_dot_escape() -> None:
    """A path containing '..' must NOT be considered narrow, even if it
    appears to point inside docs/loom/ after normalization.

    This is a unit test of the function's internal logic - it must reject
    any path with '..' in its parts because such paths indicate either
    hostile input or confusion about the repository boundary.
    """
    paths = {
        "docs/loom/intent/2026-09-20-mechanical-calculations.md",
        "docs/loom/2026-09-20-mechanical-calculations/plan.md",
        "docs/loom/../outside.txt",  # escaped path with '..'
    }
    assert is_narrow_delta(paths, "2026-09-20-mechanical-calculations") is False, (
        "Path with '..' must not be considered narrow"
    )


def test_is_narrow_delta_rejects_absolute_path() -> None:
    """An absolute path must NOT be considered narrow."""
    paths = {
        "docs/loom/intent/2026-09-20-mechanical-calculations.md",
        "docs/loom/2026-09-20-mechanical-calculations/plan.md",
        "/absolute/path/to/file.txt",
    }
    assert is_narrow_delta(paths, "2026-09-20-mechanical-calculations") is False, (
        "Absolute path must not be considered narrow"
    )


def test_is_narrow_delta_allows_legitimate_low_risk_doc_outside_docs_loom() -> None:
    """A low-risk doc file OUTSIDE docs/loom/ (e.g., project README) should be allowed."""
    paths = {
        "docs/loom/intent/2026-09-20-mechanical-calculations.md",
        "docs/loom/2026-09-20-mechanical-calculations/plan.md",
        "README.md",  # low-risk doc outside docs/loom/
    }
    assert is_narrow_delta(paths, "2026-09-20-mechanical-calculations") is True, (
        "Low-risk doc outside docs/loom/ must be considered narrow"
    )


def test_is_narrow_delta_rejects_paths_with_dot_in_parts() -> None:
    """A path with '.' in its parts must NOT be considered narrow."""
    paths = {
        "docs/loom/intent/2026-09-20-mechanical-calculations.md",
        "docs/loom/2026-09-20-mechanical-calculations/plan.md",
        "docs/loom/./file.md",  # '.' in path
    }
    assert is_narrow_delta(paths, "2026-09-20-mechanical-calculations") is False, (
        "Path with '.' must not be considered narrow"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])