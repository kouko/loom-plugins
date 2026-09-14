"""`land --accepted-by` trunk fast-forward and change cleanup
(plan W3-01; spec REQ-5..REQ-8).

Worktrees, refs, fetches and pushes run against real temporary repositories:
a bare `origin.git`, a main worktree `repo`, and linked worktrees beside it.
The merge stages are stubbed; `land.run_land_external` passes git argv to
the real subprocess and scripts gh.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from io import StringIO
from pathlib import Path

from loom_checker.command_handlers import land

GIT = shutil.which("git") or "/usr/bin/git"
GH = "/usr/local/bin/gh"
MERGE_OID = "a1b2c3d" + "0" * 33


def git(where: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(where), *args], check=check, capture_output=True, text=True
    )
    return result.stdout.strip()


def ref_exists(where: Path, ref: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(where), "rev-parse", "--verify", "--quiet", ref],
        capture_output=True, text=True,
    ).returncode == 0


class Layout:
    """origin.git (bare), repo (main worktree, trunk `main`), and feat/x
    pushed with upstream; origin/main is one commit ahead of local main."""

    def __init__(self, tmp_path: Path, *, main_branch: str = "main", linked: bool = True):
        self.root = tmp_path.resolve()
        self.origin = self.root / "origin.git"
        self.repo = self.root / "repo"
        self.wt = self.root / "wt-x"
        self.root.mkdir(parents=True, exist_ok=True)
        git(self.root, "init", "-q", "--bare", "-b", "main", str(self.origin))
        git(self.root, "init", "-q", "-b", "main", str(self.repo))
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "remote", "add", "origin", str(self.origin))
        (self.repo / "file.txt").write_text("content\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "initial")
        git(self.repo, "push", "-q", "-u", "origin", "main")

        git(self.repo, "switch", "-q", "-c", "feat/x")
        (self.repo / ".gitignore").write_text(".env\n__pycache__/\n", encoding="utf-8")
        (self.repo / "feature.txt").write_text("feature\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "feature")
        git(self.repo, "push", "-q", "-u", "origin", "feat/x")
        self.head = git(self.repo, "rev-parse", "HEAD")

        # The squash merge lands on origin's main, not on the local main.
        self.merged = git(
            self.repo, "commit-tree", "HEAD^{tree}", "-p", "main", "-m", "Land (#7)"
        )
        git(self.repo, "push", "-q", "origin", f"{self.merged}:refs/heads/main")
        git(self.repo, "fetch", "-q", "origin")
        self.old_main = git(self.repo, "rev-parse", "refs/heads/main")

        if main_branch != "feat/x":
            git(self.repo, "switch", "-q", "-C", main_branch, "main")
        if linked:
            git(self.repo, "worktree", "add", "-q", str(self.wt), "feat/x")

    def add_worktree(self, path: Path, branch: str) -> None:
        git(self.repo, "worktree", "add", "-q", "-b", branch, str(path), "main")

    def remote_has(self, branch: str) -> bool:
        return ref_exists(self.origin, f"refs/heads/{branch}")


class Calls:
    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.calls: list[tuple[list[str], int]] = []
        self.pr = {"state": "MERGED", "headRefOid": layout.head}
        self.interrupt_removal = False

    def git_calls(self, *words: str) -> list[list[str]]:
        return [argv for argv, _ in self.calls
                if argv[0] == GIT and all(word in argv for word in words)]

    def __call__(self, argv, timeout, **kwargs):
        argv = [str(value) for value in argv]
        self.calls.append((argv, timeout))
        if argv[0] == GH:
            if argv[1:3] == ["pr", "view"] and "state,headRefOid" in argv:
                return subprocess.CompletedProcess(argv, 0, json.dumps(self.pr), "")
            raise AssertionError(argv)
        assert argv[0] == GIT, argv
        assert "--force" not in argv and "-f" not in argv, argv
        cwd = Path(kwargs["cwd"]).resolve()
        assert cwd == self.layout.root or self.layout.root in cwd.parents, argv
        if self.interrupt_removal and argv[3:5] == ["worktree", "remove"]:
            raise subprocess.TimeoutExpired(argv, timeout)
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout, **kwargs)


def run_land(monkeypatch, layout: Layout, *, cwd: Path | None = None, configure=None):
    calls = Calls(layout)
    if configure:
        configure(calls)
    target = land.LandTarget(
        repo=layout.wt if layout.wt.exists() else layout.repo,
        head=layout.head, branch="feat/x", base="main",
        identity="github.com/example/project", number=7,
        trusted_git=GIT, trusted_gh=GH, env=dict(os.environ),
    )
    monkeypatch.chdir(cwd or layout.root)
    monkeypatch.setattr(land, "run_land_external", calls)
    monkeypatch.setattr(land, "_merge_preconditions", lambda *a, **k: target)
    monkeypatch.setattr(land, "_squash_merge", lambda *a, **k: (MERGE_OID, "Land", "body"))
    monkeypatch.setattr(land, "_verify_merge", lambda *a, **k: 0)
    monkeypatch.setattr(
        land, "resolve_publish_executable", lambda name: GIT if name == "git" else GH
    )
    out, err = StringIO(), StringIO()
    rc = land.cmd_land(["--accepted-by", "kouko"], out, err)
    return rc, out.getvalue(), err.getvalue(), calls


def nothing_removed(layout: Layout, calls: Calls) -> None:
    assert layout.wt.is_dir()
    assert ref_exists(layout.repo, "refs/heads/feat/x")
    assert layout.remote_has("feat/x")
    assert not calls.git_calls("worktree", "remove")
    assert not calls.git_calls("update-ref")
    assert not calls.git_calls("push")


# A5 positive: clean-trunk-fast-forwards
def test_clean_trunk_fast_forwards(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 0, err
    assert f"Trunk main fast-forwarded to {layout.merged[:7]}\n" in out
    assert git(layout.repo, "rev-parse", "refs/heads/main") == layout.merged
    assert calls.git_calls("merge", "--ff-only", "origin/main")


# A5 negative: dirty-trunk-skipped
def test_dirty_trunk_skipped(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)
    (layout.repo / "file.txt").write_text("local edit\n", encoding="utf-8")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 0, err
    assert f"trunk not updated: {layout.repo} has local changes\n" in out
    assert git(layout.repo, "rev-parse", "refs/heads/main") == layout.old_main
    assert not calls.git_calls("merge")
    assert (layout.repo / "file.txt").read_text(encoding="utf-8") == "local edit\n"
    assert f"Removed worktree {layout.wt}\n" in out
    assert not layout.wt.exists()


# A6 positive: merged-change-refs-worktree-removed
def test_merged_change_refs_worktree_removed(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)
    assert git(layout.repo, "config", "--get", "branch.feat/x.remote") == "origin"

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 0, err
    assert err == ""
    assert out.splitlines() == [
        "Merged PR #7 as a1b2c3d",
        f"Trunk main fast-forwarded to {layout.merged[:7]}",
        f"Removed worktree {layout.wt}",
        "Deleted local branch feat/x",
        "Deleted remote branch feat/x",
        f"next: cd '{layout.repo}'",
    ]
    assert not layout.wt.exists()
    assert not ref_exists(layout.repo, "refs/heads/feat/x")
    assert not layout.remote_has("feat/x")
    assert git(layout.repo, "config", "--get-regexp", r"^branch\.feat/x\.", check=False) == ""
    [remove] = calls.git_calls("worktree", "remove")
    assert remove[-1] == str(layout.wt)
    assert calls.git_calls("update-ref", "-d", "refs/heads/feat/x", layout.head)
    [push] = calls.git_calls("push")
    assert f"--force-with-lease=refs/heads/feat/x:{layout.head}" in push
    assert push[-2:] == ["origin", ":refs/heads/feat/x"]
    timeouts = {tuple(argv): timeout for argv, timeout in calls.calls}
    assert timeouts[tuple(remove)] == 300 and timeouts[tuple(push)] == 300


# A6 boundary: cwd-inside-worktree-prints-next-cd
def test_cwd_inside_worktree_prints_next_cd(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)

    rc, out, err, _ = run_land(monkeypatch, layout, cwd=layout.wt)

    assert rc == 0, err
    assert not layout.wt.exists()
    assert Path.cwd().resolve() == layout.repo
    assert out.endswith(f"next: cd '{layout.repo}'\n"), out


# A7 positive: untracked-file-refuses
def test_untracked_file_refuses(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)
    (layout.wt / "notes.txt").write_text("uncommitted\n", encoding="utf-8")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 1
    assert err == f"BLOCK land.cleanup: worktree {layout.wt} has untracked files\n"
    assert "next:" not in out
    nothing_removed(layout, calls)
    assert (layout.wt / "notes.txt").exists()


# A7 negative: ignored-env-refuses
def test_ignored_env_refuses(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path / "env")
    (layout.wt / ".env").write_text("SECRET=1\n", encoding="utf-8")

    rc, _, err, calls = run_land(monkeypatch, layout)

    assert rc == 1
    assert err.startswith(
        f"BLOCK land.cleanup: worktree {layout.wt} has ignored files outside the regenerable set"
    ), err
    assert ".env" in err
    nothing_removed(layout, calls)
    assert (layout.wt / ".env").exists()

    caches = Layout(tmp_path / "caches")
    (caches.wt / "pkg" / "__pycache__").mkdir(parents=True)
    (caches.wt / "pkg" / "__pycache__" / "mod.cpython-312.pyc").write_bytes(b"\0")

    rc, out, err, _ = run_land(monkeypatch, caches)

    assert rc == 0, err
    assert f"Removed worktree {caches.wt}\n" in out
    assert not caches.wt.exists()


# A8 positive: similar-named-dirty-worktree-untouched
def test_similar_named_dirty_worktree_untouched(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)
    sibling = layout.root / "wt-x-2"
    layout.add_worktree(sibling, "feat/x-2")
    (sibling / "file.txt").write_text("sibling edit\n", encoding="utf-8")
    (sibling / "draft.txt").write_text("sibling draft\n", encoding="utf-8")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 0, err
    assert not layout.wt.exists()
    assert (sibling / "file.txt").read_text(encoding="utf-8") == "sibling edit\n"
    assert (sibling / "draft.txt").read_text(encoding="utf-8") == "sibling draft\n"
    assert ref_exists(layout.repo, "refs/heads/feat/x-2")
    assert str(sibling) in git(layout.repo, "worktree", "list", "--porcelain")
    assert all(str(sibling) not in argv for argv in calls.git_calls("worktree", "remove"))


# A8 negative: moved-tip-update-ref-refuses
def test_moved_tip_update_ref_refuses(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)
    git(layout.wt, "config", "user.email", "test@example.com")
    (layout.wt / "later.txt").write_text("after review\n", encoding="utf-8")
    git(layout.wt, "add", "later.txt")
    git(layout.wt, "commit", "-q", "-m", "after review")
    moved = git(layout.wt, "rev-parse", "HEAD")

    rc, _, err, calls = run_land(monkeypatch, layout)

    assert rc == 1
    assert err == (
        f"BLOCK land.cleanup: local branch tip {moved[:7]} is not PR head {layout.head[:7]}\n"
    )
    nothing_removed(layout, calls)
    assert git(layout.repo, "rev-parse", "refs/heads/feat/x") == moved


def test_remote_already_deleted(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)
    git(layout.origin, "update-ref", "-d", "refs/heads/feat/x")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 0, err
    assert "remote branch already deleted\n" in out
    assert "Deleted remote branch" not in out
    assert not calls.git_calls("push")
    assert not ref_exists(layout.repo, "refs/heads/feat/x")


def test_no_trunk_checkout_fetches_trunk_ref(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path, main_branch="dev")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 0, err
    assert calls.git_calls("fetch", "origin", "main:main")
    assert not calls.git_calls("merge")
    assert f"Trunk main fast-forwarded to {layout.merged[:7]}\n" in out
    assert git(layout.repo, "rev-parse", "refs/heads/main") == layout.merged
    assert out.endswith(f"next: cd '{layout.repo}'\n"), out


def test_branch_in_main_worktree_switches_to_trunk(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path, main_branch="feat/x", linked=False)

    rc, out, err, calls = run_land(monkeypatch, layout, cwd=layout.repo)

    assert rc == 0, err
    assert layout.repo.is_dir()
    assert git(layout.repo, "symbolic-ref", "--short", "HEAD") == "main"
    assert not calls.git_calls("worktree", "remove")
    assert not ref_exists(layout.repo, "refs/heads/feat/x")
    assert not layout.remote_has("feat/x")
    assert "Removed worktree" not in out and "next:" not in out


def test_pr_not_merged_refuses(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)

    def configure(calls: Calls) -> None:
        calls.pr = {"state": "OPEN", "headRefOid": layout.head}

    rc, _, err, calls = run_land(monkeypatch, layout, configure=configure)

    assert rc == 1
    assert err == "BLOCK land.cleanup: PR #7 is not merged (OPEN)\n"
    nothing_removed(layout, calls)


def test_interrupted_worktree_removal_keeps_branches(tmp_path: Path, monkeypatch) -> None:
    layout = Layout(tmp_path)

    def configure(calls: Calls) -> None:
        calls.interrupt_removal = True

    rc, out, err, calls = run_land(monkeypatch, layout, configure=configure)

    assert rc == 1
    assert err.endswith(
        f"BLOCK land.cleanup: worktree removal interrupted at {layout.wt}; "
        "run git worktree prune after checking the directory\n"
    ), err
    assert ref_exists(layout.repo, "refs/heads/feat/x")
    assert layout.remote_has("feat/x")
    assert not calls.git_calls("update-ref")
    assert "Removed worktree" not in out
