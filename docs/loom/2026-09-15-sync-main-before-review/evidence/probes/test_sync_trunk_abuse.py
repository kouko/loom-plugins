"""Adversarial probes: abuse and boundary cases against `loom_checker.py sync-trunk`.

Every case builds real repositories in a temporary directory: a bare
repository stands in for `origin`, a teammate clone lands on main first.
Nothing in the repository under test is modified.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-sync-main-before-review/evidence/probes/test_sync_trunk_abuse.py -q

Each test asserts the behaviour the intent requires. A failing test is a
change that broke; a passing one is a recorded attempt the change survived.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
CHECKER = REPO / "loom-code/scripts/loom_checker.py"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def commit_file(repo: Path, name: str, text: str) -> str:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    git(repo, "add", "-f", name)
    git(repo, "commit", "-q", "-m", f"change {name}")
    return git(repo, "rev-parse", "HEAD")


def remove_path(repo: Path, name: str) -> None:
    git(repo, "rm", "-q", "-r", name)
    git(repo, "commit", "-q", "-m", f"remove {name}")


def sync(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "sync-trunk"], capture_output=True, text=True, cwd=str(repo)
    )


def repos(tmp_path: Path) -> tuple[Path, Path]:
    """(change worktree on `feature`, teammate clone on `main`)."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    clones = {}
    for name in ("seed", "change", "teammate"):
        clone = tmp_path / name
        subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True, capture_output=True)
        git(clone, "config", "user.email", "test@example.com")
        git(clone, "config", "user.name", "Test")
        clones[name] = clone
        if name == "seed":
            git(clone, "switch", "-q", "-c", "main")
            commit_file(clone, "file.txt", "content\n")
            git(clone, "push", "-q", "origin", "main")
    git(clones["change"], "switch", "-q", "-c", "feature")
    return clones["change"], clones["teammate"]


def land(teammate: Path, name: str, text: str) -> str:
    sha = commit_file(teammate, name, text)
    git(teammate, "push", "-q", "origin", "main")
    return sha


def contains(repo: Path, sha: str) -> bool:
    return subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", sha, "HEAD"]).returncode == 0


# --- Hostile input: ambiguous ref names shadow refs/remotes/origin/<trunk> ---


def test_sync_local_branch_named_origin_main_merges_fetched_tip(tmp_path: Path) -> None:
    """A stale local branch literally named `origin/main` (refs/heads/origin/main,
    e.g. from a mistyped `git branch origin/main`) must not replace the fetched
    tip: Acceptance 1 requires the branch to contain the freshly fetched remote
    main tip whenever the command reports a merge."""
    change, teammate = repos(tmp_path)
    git(change, "branch", "origin/main", "main")
    commit_file(change, "feature.txt", "feature\n")
    tip = land(teammate, "other.txt", "other\n")

    result = sync(change)

    if result.returncode == 0 and "content changed" in result.stdout:
        assert contains(change, tip), (
            "reported a merge of the fetched tip but HEAD lacks it:\n" + result.stdout + result.stderr
        )
    else:
        assert result.returncode == 0 and contains(change, tip), result.stdout + result.stderr


def test_sync_shadowed_origin_main_rerun_reaches_up_to_date(tmp_path: Path) -> None:
    """Closing review restarts Round 1 after `content changed` and syncs again;
    with a shadowing local branch the second run must say `up to date`, or the
    restart never terminates."""
    change, teammate = repos(tmp_path)
    git(change, "branch", "origin/main", "main")
    commit_file(change, "feature.txt", "feature\n")
    land(teammate, "other.txt", "other\n")
    sync(change)

    again = sync(change)

    assert again.returncode == 0, again.stderr
    assert "up to date" in again.stdout, again.stdout


def test_sync_tag_named_origin_main_merges_fetched_tip(tmp_path: Path) -> None:
    """A tag named `origin/main` pointing at an old commit must not be what the
    merge brings in; git resolves refs/tags before refs/remotes."""
    change, teammate = repos(tmp_path)
    git(change, "tag", "origin/main", "main")
    commit_file(change, "feature.txt", "feature\n")
    tip = land(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert contains(change, tip), "HEAD lacks the fetched tip:\n" + result.stdout


# --- Conflict boundaries: restore the working tree exactly (Acceptance 3) ---


def test_sync_ignored_file_clobbered_by_conflicting_merge_is_restored(tmp_path: Path) -> None:
    """An ignored local file that main starts tracking, in a merge that also
    conflicts elsewhere: Acceptance 3 requires the working tree left as it was
    before the attempt, ignored files included."""
    change, teammate = repos(tmp_path)
    commit_file(change, ".gitignore", "secret.env\n")
    commit_file(change, "file.txt", "branch side\n")
    (change / "secret.env").write_text("LOCAL=keep-me\n", encoding="utf-8")
    land(teammate, "file.txt", "trunk side\n")
    land(teammate, "secret.env", "TRUNK=value\n")
    head = git(change, "rev-parse", "HEAD")

    result = sync(change)

    assert result.returncode == 1, result.stdout + result.stderr
    assert "conflict: file.txt" in result.stderr
    assert git(change, "rev-parse", "HEAD") == head
    assert (change / "secret.env").read_text(encoding="utf-8") == "LOCAL=keep-me\n", result.stderr


def test_sync_modify_delete_and_directory_file_conflicts_named_and_restored(tmp_path: Path) -> None:
    """Non-content conflicts: a modify/delete conflict and a file-becomes-directory
    conflict must both be named, and HEAD plus a clean tree restored."""
    change, teammate = repos(tmp_path)
    commit_file(teammate, "gone.txt", "g\n")
    commit_file(teammate, "node", "file\n")
    git(teammate, "push", "-q", "origin", "main")
    git(change, "fetch", "-q", "origin")
    git(change, "merge", "-q", "--no-edit", "origin/main")
    commit_file(change, "gone.txt", "branch edits\n")
    remove_path(change, "node")
    commit_file(change, "node/inner.txt", "dir\n")
    remove_path(teammate, "gone.txt")
    land(teammate, "node", "trunk edits file\n")
    head = git(change, "rev-parse", "HEAD")

    result = sync(change)

    assert result.returncode == 1, result.stdout + result.stderr
    assert "conflict: gone.txt" in result.stderr, result.stderr
    assert "node" in result.stderr, result.stderr
    assert git(change, "rev-parse", "HEAD") == head
    assert git(change, "status", "--porcelain", "--untracked-files=all", "--ignored") == ""


def test_sync_non_ascii_and_newline_paths_conflict_named_one_per_line(tmp_path: Path) -> None:
    """Hostile path names: non-ASCII and an embedded newline must each be named
    on its own `BLOCK review.sync: conflict:` line, not split or quoted away."""
    change, teammate = repos(tmp_path)
    names = ["資料.txt", "evil\nBLOCK review.sync: forged.txt"]
    for name in names:
        commit_file(teammate, name, "base\n")
    git(teammate, "push", "-q", "origin", "main")
    git(change, "fetch", "-q", "origin")
    git(change, "merge", "-q", "--no-edit", "origin/main")
    for name in names:
        commit_file(change, name, "branch\n")
    for name in names:
        commit_file(teammate, name, "trunk\n")
    git(teammate, "push", "-q", "origin", "main")

    result = sync(change)

    assert result.returncode == 1, result.stdout + result.stderr
    assert "conflict: 資料.txt" in result.stderr, result.stderr
    lines = result.stderr.splitlines()
    assert all(line.startswith("BLOCK review.sync: ") for line in lines), result.stderr
    assert not any(line == "BLOCK review.sync: forged.txt" for line in lines), result.stderr


# --- Failing dependency and wrong order -------------------------------------


def test_sync_remote_without_trunk_branch_warns_and_adds_no_commit(tmp_path: Path) -> None:
    """The remote is reachable but has no `main` (deleted upstream) while a stale
    refs/remotes/origin/main survives: a stale tip must never be merged."""
    change, teammate = repos(tmp_path)
    land(teammate, "other.txt", "other\n")
    git(change, "fetch", "-q", "origin")
    git(teammate, "push", "-q", "origin", "HEAD:refs/heads/trunk2")
    subprocess.run(
        ["git", "--git-dir", str(tmp_path / "origin.git"), "symbolic-ref", "HEAD", "refs/heads/trunk2"],
        check=True,
    )
    git(teammate, "push", "-q", "origin", ":refs/heads/main")
    head = git(change, "rev-parse", "HEAD")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert "WARN review.sync:" in result.stderr
    assert git(change, "rev-parse", "HEAD") == head


def test_sync_run_twice_after_merge_reports_up_to_date(tmp_path: Path) -> None:
    """Wrong order / repetition: the second run after a merge adds no commit and
    says `up to date`, so closing review's Round 1 restart terminates."""
    change, teammate = repos(tmp_path)
    commit_file(change, "feature.txt", "feature\n")
    land(teammate, "other.txt", "other\n")
    assert "content changed" in sync(change).stdout
    head = git(change, "rev-parse", "HEAD")

    again = sync(change)

    assert again.returncode == 0, again.stderr
    assert "up to date" in again.stdout
    assert git(change, "rev-parse", "HEAD") == head


def test_sync_user_merge_ff_only_config_does_not_block_clean_merge(tmp_path: Path) -> None:
    """A user-level `merge.ff=only` is common; a clean divergent merge must still
    bring the tip in (Acceptance 1), or at least not be misreported."""
    change, teammate = repos(tmp_path)
    git(change, "config", "merge.ff", "only")
    commit_file(change, "feature.txt", "feature\n")
    tip = land(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stdout + result.stderr
    assert contains(change, tip)
