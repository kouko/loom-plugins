"""`loom_checker.py sync-trunk` (plan W1-01; intent Acceptance 2, 3, 4).

Every case builds real repositories: a local bare repository stands in for
`origin`, a second clone plays the teammate who lands on main first, and an
unreachable remote is an origin URL pointing at a path that does not exist.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "loom_checker.py"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def identify(repo: Path) -> None:
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")


def commit_file(repo: Path, name: str, text: str, message: str) -> str:
    (repo / name).write_text(text, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def sync(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "sync-trunk"],
        capture_output=True, text=True, cwd=str(repo),
    )


def repos(tmp_path: Path) -> tuple[Path, Path, Path]:
    """(origin bare repo, change worktree on `feature`, teammate clone)."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    seed = tmp_path / "seed"
    subprocess.run(["git", "clone", "-q", str(origin), str(seed)], check=True, capture_output=True)
    identify(seed)
    git(seed, "switch", "-q", "-c", "main")
    commit_file(seed, "file.txt", "content\n", "initial")
    commit_file(seed, "a.txt", "a\n", "second file")
    git(seed, "push", "-q", "origin", "main")
    change = tmp_path / "change"
    teammate = tmp_path / "teammate"
    for clone in (change, teammate):
        subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True, capture_output=True)
        identify(clone)
    git(change, "switch", "-q", "-c", "feature")
    return origin, change, teammate


def land_on_main(teammate: Path, name: str, text: str) -> str:
    sha = commit_file(teammate, name, text, f"teammate changes {name}")
    git(teammate, "push", "-q", "origin", "main")
    return sha


def push_branch(change: Path, remote_name: str = "feature") -> None:
    """Publish the change branch, so sync must merge instead of rebasing."""
    git(change, "push", "-q", "origin", f"feature:{remote_name}")


def state(repo: Path) -> tuple[str, str, str]:
    return (
        git(repo, "rev-parse", "HEAD"),
        git(repo, "status", "--porcelain", "--untracked-files=all"),
        git(repo, "rev-parse", "refs/remotes/origin/main"),
    )


# --- Acceptance 2: already current --------------------------------------


def test_current_branch_adds_no_commit(tmp_path: Path) -> None:
    _origin, change, _teammate = repos(tmp_path)
    before = git(change, "rev-parse", "HEAD")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(change, "rev-parse", "HEAD") == before
    assert "up to date" in result.stdout
    assert "content changed" not in result.stdout


def test_branch_ahead_of_trunk_adds_no_commit(tmp_path: Path) -> None:
    _origin, change, _teammate = repos(tmp_path)
    ahead = commit_file(change, "feature.txt", "feature\n", "feature work")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(change, "rev-parse", "HEAD") == ahead
    assert git(change, "rev-list", "--count", "HEAD") == "3"
    assert "up to date" in result.stdout


# --- clean merge ---------------------------------------------------------


def test_behind_branch_merges_fetched_trunk_tip_and_says_content_changed(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    own = commit_file(change, "feature.txt", "feature\n", "feature work")
    push_branch(change)
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    head = git(change, "rev-parse", "HEAD")
    parents = git(change, "rev-list", "--parents", "-n", "1", "HEAD").split()[1:]
    assert parents == [own, trunk_tip]
    assert git(change, "status", "--porcelain") == ""
    assert trunk_tip in result.stdout
    assert head in result.stdout
    assert "content changed" in result.stdout


def test_unpushed_behind_rebases_linear(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    commit_file(change, "feature.txt", "feature\n", "feature one")
    commit_file(change, "feature2.txt", "feature\n", "feature two")
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(change, "rev-list", "--merges", "--count", "HEAD") == "0"
    assert git(change, "rev-parse", "HEAD~2") == trunk_tip
    assert git(change, "log", "--format=%s", "-2").splitlines() == ["feature two", "feature one"]
    assert git(change, "symbolic-ref", "--short", "HEAD") == "feature"
    assert git(change, "status", "--porcelain") == ""
    assert f"rebased feature onto origin/main ({trunk_tip})" in result.stdout
    assert "content changed" in result.stdout


def test_pushed_behind_merges_then_plain_push_accepted(tmp_path: Path) -> None:
    origin, change, teammate = repos(tmp_path)
    own = commit_file(change, "feature.txt", "feature\n", "feature work")
    push_branch(change)
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(change, "rev-list", "--parents", "-n", "1", "HEAD").split()[1:] == [own, trunk_tip]
    git(change, "push", "-q", "origin", "feature")
    assert git(origin, "rev-parse", "feature") == git(change, "rev-parse", "HEAD")


def test_commits_pushed_under_other_name_merge(tmp_path: Path) -> None:
    origin, change, teammate = repos(tmp_path)
    own = commit_file(change, "feature.txt", "feature\n", "feature work")
    push_branch(change, remote_name="other-name")
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(origin, "for-each-ref", "refs/heads/feature") == ""
    assert git(change, "rev-list", "--parents", "-n", "1", "HEAD").split()[1:] == [own, trunk_tip]


def test_unpushed_conflict_names_paths_restores(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    # Edit then revert: the merged result is clean (merge-tree sees no conflict),
    # but replaying the first commit on the trunk tip conflicts.
    commit_file(change, "file.txt", "branch side\n", "branch edits file")
    commit_file(change, "file.txt", "content\n", "branch reverts file")
    land_on_main(teammate, "file.txt", "trunk side\n")
    before = state(change)
    snapshot = git(change, "status", "--porcelain", "--untracked-files=all", "--ignored")

    result = sync(change)

    lines = result.stderr.splitlines()
    assert result.returncode == 1, result.stdout + result.stderr
    assert "BLOCK review.sync: conflict: file.txt" in lines
    assert any("the rebase was aborted" in line for line in lines), result.stderr
    assert state(change)[:2] == before[:2]
    assert git(change, "status", "--porcelain", "--untracked-files=all", "--ignored") == snapshot
    assert git(change, "symbolic-ref", "--short", "HEAD") == "feature"
    git_dir = Path(git(change, "rev-parse", "--absolute-git-dir"))
    assert not (git_dir / "rebase-merge").exists() and not (git_dir / "rebase-apply").exists()


def test_unpushed_with_prior_merge_commit_merges(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    commit_file(change, "feature.txt", "feature\n", "feature work")
    land_on_main(teammate, "first.txt", "first\n")
    git(change, "fetch", "-q", "origin")
    git(change, "merge", "-q", "--no-edit", "origin/main")
    prior = git(change, "rev-parse", "HEAD")
    trunk_tip = land_on_main(teammate, "second.txt", "second\n")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(change, "rev-list", "--parents", "-n", "1", "HEAD").split()[1:] == [prior, trunk_tip]


def test_trunk_name_resolves_without_origin_head(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    git(change, "remote", "set-head", "origin", "-d")
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(change, "merge-base", "--is-ancestor", trunk_tip, "HEAD") == ""


# --- Acceptance 3: conflict and refusals ----------------------------------


def test_conflict_names_every_file_and_restores_head(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    commit_file(change, "file.txt", "branch side\n", "branch edits file")
    commit_file(change, "a.txt", "branch a\n", "branch edits a")
    land_on_main(teammate, "file.txt", "trunk side\n")
    land_on_main(teammate, "a.txt", "trunk a\n")
    head_before = git(change, "rev-parse", "HEAD")

    result = sync(change)

    assert result.returncode == 1
    assert "BLOCK review.sync: conflict:" in result.stderr
    assert "file.txt" in result.stderr
    assert "a.txt" in result.stderr
    assert git(change, "rev-parse", "HEAD") == head_before
    assert git(change, "status", "--porcelain", "--untracked-files=all") == ""
    assert not (Path(git(change, "rev-parse", "--absolute-git-dir")) / "MERGE_HEAD").exists()
    assert (change / "file.txt").read_text(encoding="utf-8") == "branch side\n"


@pytest.mark.parametrize("pushed", [False, True], ids=["rebase", "merge"])
@pytest.mark.parametrize("kind", ["branch", "tag"])
def test_ref_named_origin_trunk_does_not_shadow_fetched_tip(tmp_path: Path, kind: str, pushed: bool) -> None:
    _origin, change, teammate = repos(tmp_path)
    git(change, kind, "origin/main", "main")
    commit_file(change, "feature.txt", "feature\n", "feature work")
    if pushed:
        push_branch(change)
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)
    again = sync(change)

    assert result.returncode == 0, result.stderr
    assert git(change, "merge-base", "--is-ancestor", trunk_tip, "HEAD") == ""
    assert "up to date" in again.stdout, again.stdout + again.stderr


def test_ignored_file_trunk_starts_tracking_is_refused_and_kept(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    commit_file(change, ".gitignore", "secret.env\n", "ignore secret")
    commit_file(change, "file.txt", "branch side\n", "branch edits file")
    (change / "secret.env").write_text("LOCAL=keep-me\n", encoding="utf-8")
    land_on_main(teammate, "file.txt", "trunk side\n")
    (teammate / "secret.env").write_text("TRUNK=value\n", encoding="utf-8")
    git(teammate, "add", "-f", "secret.env")
    git(teammate, "commit", "-q", "-m", "track secret")
    git(teammate, "push", "-q", "origin", "main")
    head_before = git(change, "rev-parse", "HEAD")

    result = sync(change)

    assert result.returncode == 1, result.stdout + result.stderr
    assert "secret.env" in result.stderr
    assert "conflict: file.txt" in result.stderr
    assert git(change, "rev-parse", "HEAD") == head_before
    assert (change / "secret.env").read_text(encoding="utf-8") == "LOCAL=keep-me\n"


@pytest.mark.parametrize("failing", ["ls-files", "diff"])
def test_untracked_collision_check_failure_blocks_before_merge(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failing: str
) -> None:
    from io import StringIO

    from loom_checker.command_handlers import sync as sync_handler

    _origin, change, teammate = repos(tmp_path)
    commit_file(change, "feature.txt", "feature\n", "feature work")
    land_on_main(teammate, "other.txt", "other\n")
    before = state(change)
    real_git = sync_handler._git

    def broken_git(git_exe, repo, *args, **kwargs):
        if args and args[0] == failing:
            return 128, "", f"fatal: {failing} exploded"
        return real_git(git_exe, repo, *args, **kwargs)

    monkeypatch.setattr(sync_handler, "_git", broken_git)
    monkeypatch.chdir(change)
    out, err = StringIO(), StringIO()

    code = sync_handler.cmd_sync_trunk([], out=out, err=err)

    assert code == 1, out.getvalue() + err.getvalue()
    assert "BLOCK review.sync: cannot check untracked files against origin/main" in err.getvalue()
    assert f"fatal: {failing} exploded" in err.getvalue()
    assert "the merge was not attempted" in err.getvalue()
    assert state(change)[:2] == before[:2]


def test_control_character_conflict_path_cannot_forge_a_block_line(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    name = "evil\nBLOCK review.sync: forged.txt"
    land_on_main(teammate, name, "base\n")
    git(change, "pull", "-q", "--no-rebase", "origin", "main")
    commit_file(change, name, "branch\n", "branch evil")
    land_on_main(teammate, name, "trunk\n")

    result = sync(change)

    assert result.returncode == 1, result.stdout + result.stderr
    lines = result.stderr.splitlines()
    assert all(line.startswith("BLOCK review.sync: ") for line in lines), result.stderr
    assert "BLOCK review.sync: forged.txt" not in lines


def test_merge_tree_unavailable_falls_back_to_merge_then_abort(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from io import StringIO

    from loom_checker.command_handlers import sync as sync_handler

    _origin, change, teammate = repos(tmp_path)
    commit_file(change, "file.txt", "branch side\n", "branch edits file")
    commit_file(change, "a.txt", "branch a\n", "branch edits a")
    push_branch(change)
    land_on_main(teammate, "file.txt", "trunk side\n")
    land_on_main(teammate, "a.txt", "trunk a\n")
    before = state(change)
    real_git = sync_handler._git

    def old_git(git_exe, repo, *args, **kwargs):
        if args and args[0] == "merge-tree":
            return 129, "", "usage"
        return real_git(git_exe, repo, *args, **kwargs)

    monkeypatch.setattr(sync_handler, "_git", old_git)
    monkeypatch.chdir(change)
    out, err = StringIO(), StringIO()

    code = sync_handler.cmd_sync_trunk([], out=out, err=err)

    lines = err.getvalue().splitlines()
    assert code == 1, out.getvalue() + err.getvalue()
    assert "BLOCK review.sync: conflict: a.txt" in lines
    assert "BLOCK review.sync: conflict: file.txt" in lines
    assert any("the merge was aborted" in line for line in lines), err.getvalue()
    assert state(change)[:2] == before[:2]
    assert not (Path(git(change, "rev-parse", "--absolute-git-dir")) / "MERGE_HEAD").exists()


def test_merge_ff_only_config_does_not_block_clean_merge(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    git(change, "config", "merge.ff", "only")
    commit_file(change, "feature.txt", "feature\n", "feature work")
    push_branch(change)
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Conflicts are never resolved" not in result.stderr
    assert git(change, "merge-base", "--is-ancestor", trunk_tip, "HEAD") == ""


def _dirty_tracked(change: Path) -> None:
    (change / "file.txt").write_text("uncommitted\n", encoding="utf-8")


def _untracked(change: Path) -> None:
    (change / "new.txt").write_text("untracked\n", encoding="utf-8")


def _on_trunk(change: Path) -> None:
    git(change, "switch", "-q", "main")


def _detached(change: Path) -> None:
    git(change, "switch", "-q", "--detach", "HEAD")


@pytest.mark.parametrize(
    "prepare", [_dirty_tracked, _untracked, _on_trunk, _detached],
    ids=["modified", "untracked", "trunk-checkout", "detached"],
)
def test_dirty_worktree_or_trunk_checkout_refused_untouched(tmp_path: Path, prepare) -> None:
    _origin, change, teammate = repos(tmp_path)
    land_on_main(teammate, "other.txt", "other\n")
    prepare(change)
    before = state(change)

    result = sync(change)

    assert result.returncode == 1
    assert result.stderr.startswith("BLOCK review.sync: ")
    assert state(change) == before


def test_control_character_untracked_path_cannot_forge_a_warn_line(tmp_path: Path) -> None:
    _origin, change, teammate = repos(tmp_path)
    land_on_main(teammate, "other.txt", "other\n")
    (change / "new\nWARN review.sync: forged.txt").write_text("untracked\n", encoding="utf-8")

    result = sync(change)

    assert result.returncode == 1, result.stdout + result.stderr
    lines = result.stderr.splitlines()
    assert len(lines) == 1 and lines[0].startswith("BLOCK review.sync: "), result.stderr


# --- Acceptance 4: unreachable remote -------------------------------------


def _unreachable(tmp_path: Path) -> Path:
    _origin, change, _teammate = repos(tmp_path)
    git(change, "remote", "set-url", "origin", str(tmp_path / "no-such-remote.git"))
    return change


def test_unreachable_remote_warns_exit_zero(tmp_path: Path) -> None:
    change = _unreachable(tmp_path)

    result = sync(change)

    assert result.returncode == 0
    assert "WARN review.sync:" in result.stderr
    assert "could not be checked against main" in result.stderr
    assert "BLOCK" not in result.stderr


def test_unreachable_remote_creates_no_commit(tmp_path: Path) -> None:
    change = _unreachable(tmp_path)
    commit_file(change, "feature.txt", "feature\n", "feature work")
    before = state(change)

    result = sync(change)

    assert result.returncode == 0
    assert state(change) == before
