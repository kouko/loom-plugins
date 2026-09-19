"""Adversarial probes against the version-only JSON bump branch of
`reviewers.reviewer_floor_for_paths` (loom_checker/reviewers.py).

Each probe asks the same question: can a `.json` change that is NOT a
version-only bump be classified as one (floor 1 instead of 2)? Probes
marked `xfail(strict=True)` are the ones that broke -- they assert the
safe outcome and are expected to fail today.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from loom_checker import reviewers


CHANGE = "2026-09-08-example"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A", ".")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def repo_with_content(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.parent.mkdir(parents=True, exist_ok=True)
    kickoff.write_text("- package-tests: python3 -m pytest -q — fixture (2026-09-08)\n")
    commit(repo, "initial")
    return repo


def bump(tmp_path: Path, before: str, after: str, name: str = "loom-code/plugin.json") -> Path:
    """Commit `before` on trunk and `after` on a feature branch, as raw text."""
    repo = repo_with_content(tmp_path)
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(before, encoding="utf-8")
    commit(repo, "manifest")
    git(repo, "switch", "-q", "-c", "feature")
    path.write_text(after, encoding="utf-8")
    commit(repo, "change the manifest")
    return repo


# --- breaks -----------------------------------------------------------------


def test_int_to_bool_flip_is_not_a_version_only_bump(tmp_path: Path) -> None:
    """Fixed: `_json_scalar_equal` checks `type(a) is type(b)` before comparing,
    so `0` and `False` no longer read as the same value."""
    repo = bump(
        tmp_path,
        json.dumps({"name": "p", "version": "9.9.0", "strict": 0}) + "\n",
        json.dumps({"name": "p", "version": "9.9.1", "strict": False}) + "\n",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_int_to_float_retype_is_not_a_version_only_bump(tmp_path: Path) -> None:
    """Fixed: same type-check as the bool/int case, above."""
    repo = bump(
        tmp_path,
        json.dumps({"name": "p", "version": "9.9.0", "retries": 3}) + "\n",
        json.dumps({"name": "p", "version": "9.9.1", "retries": 3.0}) + "\n",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_added_duplicate_key_is_not_a_version_only_bump(tmp_path: Path) -> None:
    """Fixed: `_reject_duplicate_keys` (an `object_pairs_hook`) fails the parse
    on either side rather than silently keeping the last of a repeated key."""
    repo = bump(
        tmp_path,
        '{"name": "p", "version": "9.9.0", "entry": "safe.js"}\n',
        '{"name": "p", "version": "9.9.1", "entry": "evil.js", "entry": "safe.js"}\n',
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


@pytest.mark.xfail(
    strict=True,
    reason="BREAK: `version` is popped whatever it means -- a schema/API version "
           "field is a behaviour change, not a release-number bump",
)
def test_semantic_version_field_is_not_a_low_risk_bump(tmp_path: Path) -> None:
    repo = bump(
        tmp_path,
        json.dumps({"version": "v1", "endpoint": "/data"}) + "\n",
        json.dumps({"version": "v2", "endpoint": "/data"}) + "\n",
        name="config/protocol.json",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_version_retyped_to_an_object_is_not_a_bump(tmp_path: Path) -> None:
    """Fixed: `version` must be a `str`/`int`/`float` (not `bool`) on both
    sides, or the exemption does not fire."""
    repo = bump(
        tmp_path,
        json.dumps({"name": "p", "version": "9.9.0"}) + "\n",
        json.dumps({"name": "p", "version": {"major": 9, "hooks": "x.sh"}}) + "\n",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


# --- held -------------------------------------------------------------------


def test_nested_version_key_change_still_needs_two(tmp_path: Path) -> None:
    """Only the TOP-level `version` is popped; a nested one keeps floor 2."""
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0", "dep": {"version": "1", "url": "a"}}) + "\n",
        json.dumps({"version": "9.9.1", "dep": {"version": "2", "url": "a"}}) + "\n",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_nested_value_change_under_a_version_bump_still_needs_two(tmp_path: Path) -> None:
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0", "dep": {"url": "a"}}) + "\n",
        json.dumps({"version": "9.9.1", "dep": {"url": "evil"}}) + "\n",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_array_element_change_under_a_version_bump_still_needs_two(tmp_path: Path) -> None:
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0", "allow": ["read", "write"]}) + "\n",
        json.dumps({"version": "9.9.1", "allow": ["read", "exec"]}) + "\n",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_array_reorder_under_a_version_bump_still_needs_two(tmp_path: Path) -> None:
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0", "allow": ["read", "write"]}) + "\n",
        json.dumps({"version": "9.9.1", "allow": ["write", "read"]}) + "\n",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_top_level_array_json_still_needs_two(tmp_path: Path) -> None:
    repo = bump(tmp_path, '["a"]\n', '["b"]\n')
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_protected_directory_beats_the_version_bump(tmp_path: Path) -> None:
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0"}) + "\n",
        json.dumps({"version": "9.9.1"}) + "\n",
        name="loom-code/hooks/config.json",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_version_bump_mixed_with_a_code_change_still_needs_two(tmp_path: Path) -> None:
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0"}) + "\n",
        json.dumps({"version": "9.9.1"}) + "\n",
    )
    (repo / "src.py").write_text("VALUE = 2\n", encoding="utf-8")
    commit(repo, "and a code change")
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_rename_plus_edit_still_needs_two(tmp_path: Path) -> None:
    """`--no-renames` splits a rename into add+delete; both answer False."""
    repo = repo_with_content(tmp_path)
    old = repo / "a.json"
    old.write_text(json.dumps({"version": "9.9.0", "x": 1}) + "\n", encoding="utf-8")
    commit(repo, "manifest")
    git(repo, "switch", "-q", "-c", "feature")
    old.unlink()
    (repo / "b.json").write_text(
        json.dumps({"version": "9.9.1", "x": 2}) + "\n", encoding="utf-8"
    )
    commit(repo, "rename and edit")
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_deleted_json_still_needs_two(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    path = repo / "a.json"
    path.write_text(json.dumps({"version": "9.9.0"}) + "\n", encoding="utf-8")
    commit(repo, "manifest")
    git(repo, "switch", "-q", "-c", "feature")
    path.unlink()
    commit(repo, "delete the manifest")
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_symlinked_json_still_needs_two(tmp_path: Path) -> None:
    """A symlink's blob is its target path, which does not parse as JSON."""
    repo = repo_with_content(tmp_path)
    (repo / "real-a.json").write_text('{"version": "9.9.0"}\n', encoding="utf-8")
    (repo / "link.json").symlink_to("real-a.json")
    commit(repo, "manifest and link")
    git(repo, "switch", "-q", "-c", "feature")
    (repo / "link.json").unlink()
    (repo / "link.json").symlink_to("real-b.json")
    (repo / "real-b.json").write_text('{"version": "9.9.1"}\n', encoding="utf-8")
    commit(repo, "repoint the link")
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_colon_in_path_does_not_confuse_git_show(tmp_path: Path) -> None:
    """`git show <rev>:<path>` splits on the FIRST colon, so a later one is data."""
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0", "x": 1}) + "\n",
        json.dumps({"version": "9.9.1", "x": 2}) + "\n",
        name="od:d/na:me.json",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_colon_in_path_version_only_bump_is_still_recognized(tmp_path: Path) -> None:
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0", "x": 1}) + "\n",
        json.dumps({"version": "9.9.1", "x": 1}) + "\n",
        name="od:d/na:me.json",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 1


# --- false negatives (safe direction, documented) ---------------------------


def test_non_ascii_path_version_bump_fails_closed(tmp_path: Path) -> None:
    """core.quotePath escapes the diff path, so `git show` misses and floor stays 2."""
    repo = bump(
        tmp_path,
        json.dumps({"version": "9.9.0", "x": 1}) + "\n",
        json.dumps({"version": "9.9.1", "x": 1}) + "\n",
        name="設定/plugin.json",
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_nan_value_does_not_defeat_a_real_version_only_bump(tmp_path: Path) -> None:
    """NaN != NaN would have broken this, but json reuses one NaN object and
    dict equality compares values by identity first, so the bump still reads
    as version-only. Probed because it was the obvious false-negative risk."""
    repo = bump(
        tmp_path,
        '{"version": "9.9.0", "x": NaN}\n',
        '{"version": "9.9.1", "x": NaN}\n',
    )
    assert reviewers.required_reviewer_count(repo, CHANGE) == 1


def test_lockfile_style_nested_version_defeats_a_real_bump(tmp_path: Path) -> None:
    """The npm case: package.json + package-lock.json, the lock nests `version`."""
    repo = repo_with_content(tmp_path)
    pkg = repo / "package.json"
    lock = repo / "package-lock.json"
    pkg.write_text(json.dumps({"name": "p", "version": "9.9.0"}) + "\n", encoding="utf-8")
    lock.write_text(
        json.dumps({"name": "p", "version": "9.9.0", "packages": {"": {"version": "9.9.0"}}})
        + "\n",
        encoding="utf-8",
    )
    commit(repo, "package and lock")
    git(repo, "switch", "-q", "-c", "feature")
    pkg.write_text(json.dumps({"name": "p", "version": "9.9.1"}) + "\n", encoding="utf-8")
    lock.write_text(
        json.dumps({"name": "p", "version": "9.9.1", "packages": {"": {"version": "9.9.1"}}})
        + "\n",
        encoding="utf-8",
    )
    commit(repo, "bump both")
    assert reviewers.required_reviewer_count(repo, CHANGE) == 2
