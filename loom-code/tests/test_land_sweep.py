"""`land --cleanup <branch>` and `land --sweep [--confirm <token>]`
(plan W3-02; spec REQ-9, REQ-10).

Worktrees, refs, fetches and pushes run against real temporary repositories:
a bare `origin.git`, a main worktree `repo` on `main`, and linked worktrees
beside it. `land.run_land_external` passes git argv to the real subprocess
and scripts gh from a list of merged PRs.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from io import StringIO
from pathlib import Path

from loom_checker.command_handlers import land

GIT = shutil.which("git") or "/usr/bin/git"
GH = "/usr/local/bin/gh"


def git(where: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(where), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def ref_exists(where: Path, ref: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(where), "rev-parse", "--verify", "--quiet", ref],
        capture_output=True, text=True,
    ).returncode == 0


class Repo:
    def __init__(self, tmp_path: Path) -> None:
        self.root = tmp_path.resolve()
        self.origin = self.root / "origin.git"
        self.repo = self.root / "repo"
        git(self.root, "init", "-q", "--bare", "-b", "main", str(self.origin))
        git(self.root, "init", "-q", "-b", "main", str(self.repo))
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "remote", "add", "origin", str(self.origin))
        (self.repo / "file.txt").write_text("content\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "initial")
        git(self.repo, "push", "-q", "-u", "origin", "main")
        self.merged: list[dict] = []

    def branch(self, name: str, *, worktree: str | None = None, merged: bool = True,
               local: bool = True) -> tuple[str, Path | None]:
        """A pushed branch one commit ahead of main; returns (tip, worktree)."""
        git(self.repo, "branch", name, "main")
        path = self.root / worktree if worktree else None
        where = self.repo
        if path is not None:
            git(self.repo, "worktree", "add", "-q", str(path), name)
            where = path
        else:
            git(self.repo, "switch", "-q", name)
        (where / f"{name.replace('/', '-')}.txt").write_text(name + "\n", encoding="utf-8")
        git(where, "add", ".")
        git(where, "commit", "-q", "-m", name)
        git(where, "push", "-q", "-u", "origin", name)
        tip = git(where, "rev-parse", "HEAD")
        if path is None:
            git(self.repo, "switch", "-q", "main")
            if not local:
                git(self.repo, "update-ref", "-d", f"refs/heads/{name}", tip)
        if merged:
            self.merged.append(
                {"number": len(self.merged) + 1, "headRefName": name, "headRefOid": tip}
            )
        return tip, path

    def intact(self, name: str, path: Path | None = None) -> bool:
        return (
            ref_exists(self.repo, f"refs/heads/{name}")
            and ref_exists(self.origin, f"refs/heads/{name}")
            and (path is None or path.is_dir())
        )

    def gone(self, name: str, path: Path | None = None) -> bool:
        return (
            not ref_exists(self.repo, f"refs/heads/{name}")
            and not ref_exists(self.origin, f"refs/heads/{name}")
            and (path is None or not path.exists())
        )


class Calls:
    def __init__(self, layout: Repo) -> None:
        self.layout = layout
        self.calls: list[list[str]] = []
        self.merged_override: list[dict] | None = None
        self.refuse_push_for: set[str] = set()
        self.after_remove = None  # called with the removed worktree path

    def argvs(self, *words: str) -> list[list[str]]:
        return [argv for argv in self.calls if all(word in argv for word in words)]

    def __call__(self, argv, timeout, **kwargs):
        argv = [str(value) for value in argv]
        self.calls.append(argv)
        merged = self.layout.merged if self.merged_override is None else self.merged_override
        if argv[0] == GH:
            assert argv[1:3] != ["pr", "merge"], argv
            if argv[1:3] == ["repo", "view"]:
                return subprocess.CompletedProcess(argv, 0, "main\n", "")
            if argv[1:3] == ["pr", "list"]:
                assert argv[argv.index("--state") + 1] == "merged", argv
                if "--head" in argv:
                    head = argv[argv.index("--head") + 1]
                    rows = [dict(pr, mergedAt="2026-09-14T00:00:00Z")
                            for pr in merged if pr["headRefName"] == head]
                else:
                    assert argv[argv.index("--limit") + 1] == "1000", argv
                    rows = merged
                return subprocess.CompletedProcess(argv, 0, json.dumps(rows), "")
            if argv[1:3] == ["pr", "view"] and "state,headRefOid" in argv:
                [pr] = [pr for pr in merged if str(pr["number"]) == argv[3]]
                payload = {"state": "MERGED", "headRefOid": pr["headRefOid"]}
                return subprocess.CompletedProcess(argv, 0, json.dumps(payload), "")
            raise AssertionError(argv)
        assert argv[0] == GIT, argv
        assert "--force" not in argv and "-f" not in argv, argv
        cwd = Path(kwargs["cwd"]).resolve()
        assert cwd == self.layout.root or self.layout.root in cwd.parents, argv
        if "push" in argv and any(argv[-1] == f":refs/heads/{b}" for b in self.refuse_push_for):
            return subprocess.CompletedProcess(argv, 1, "", "! [remote rejected] refused")
        result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, **kwargs)
        if self.after_remove and argv[3:5] == ["worktree", "remove"] and result.returncode == 0:
            self.after_remove(Path(argv[-1]))
        return result


def run(monkeypatch, layout: Repo, *args: str, cwd: Path | None = None, configure=None):
    calls = Calls(layout)
    if configure:
        configure(calls)
    monkeypatch.chdir(cwd or layout.repo)
    monkeypatch.setattr(land, "run_land_external", calls)
    monkeypatch.setattr(
        land, "resolve_publish_executable", lambda name: GIT if name == "git" else GH
    )
    monkeypatch.setattr(land, "github_repo_from_origin", lambda repo: "github.com/example/project")
    out, err = StringIO(), StringIO()
    rc = land.cmd_land(list(args), out, err)
    return rc, out.getvalue(), err.getvalue(), calls


def token_of(out: str) -> str:
    removes = sorted(line for line in out.splitlines() if line.startswith("remove "))
    return hashlib.sha256("\n".join(removes).encode("utf-8")).hexdigest()[:12]


# A9 positive: cleanup-named-merged-branch
def test_cleanup_named_merged_branch(tmp_path: Path, monkeypatch) -> None:
    layout = Repo(tmp_path)
    _tip, wt = layout.branch("feat/x", worktree="wt-x")
    main_before = git(layout.repo, "rev-parse", "main")

    rc, out, err, calls = run(monkeypatch, layout, "--cleanup", "feat/x")

    assert rc == 0, err
    assert err == ""
    assert out.splitlines() == [
        f"Worktree for feat/x: {wt}",
        f"Removed worktree {wt}",
        "Deleted local branch feat/x",
        "Deleted remote branch feat/x",
        f"next: cd '{layout.repo}'",
    ]
    assert layout.gone("feat/x", wt)
    assert not calls.argvs("pr", "merge")
    assert not calls.argvs("merge", "--ff-only")
    assert git(layout.repo, "rev-parse", "main") == main_before


# A9 negative: reused-branch-name-refuses
def test_reused_branch_name_refuses(tmp_path: Path, monkeypatch) -> None:
    layout = Repo(tmp_path)
    tip, wt = layout.branch("feat/x", worktree="wt-x", merged=False)
    old = git(layout.repo, "rev-parse", "main")
    layout.merged = [{"number": 3, "headRefName": "feat/x", "headRefOid": old}]

    rc, out, err, calls = run(monkeypatch, layout, "--cleanup", "feat/x")

    assert rc == 1
    assert err == f"BLOCK land.cleanup: local branch tip {tip[:7]} is not PR head {old[:7]}\n"
    assert layout.intact("feat/x", wt)
    assert not calls.argvs("worktree", "remove") and not calls.argvs("update-ref")

    layout.merged.append({"number": 4, "headRefName": "feat/x", "headRefOid": "b" * 40})
    rc, out, err, calls = run(monkeypatch, layout, "--cleanup", "feat/x")

    assert rc == 1
    assert err == (
        "BLOCK land.cleanup: no merged PR for feat/x has its local or remote tip as head\n"
    )
    assert layout.intact("feat/x", wt)
    assert "Worktree for" not in out


def test_cleanup_without_merged_pr_refuses(tmp_path: Path, monkeypatch) -> None:
    layout = Repo(tmp_path)
    _tip, wt = layout.branch("feat/x", worktree="wt-x", merged=False)

    rc, out, err, _calls = run(monkeypatch, layout, "--cleanup", "feat/x")

    assert rc == 1
    assert err == "BLOCK land.cleanup: no merged PR for feat/x\n"
    assert out == ""
    assert layout.intact("feat/x", wt)


def sweep_layout(tmp_path: Path):
    layout = Repo(tmp_path)
    a, wt_a = layout.branch("feat/a", worktree="wt-a")
    _, wt_similar = layout.branch("feat/a-2", worktree="wt-a-2", merged=False)
    (wt_similar / "draft.txt").write_text("unmerged work\n", encoding="utf-8")
    b, _ = layout.branch("feat/b")
    _, wt_dirty = layout.branch("feat/dirty", worktree="wt-dirty")
    (wt_dirty / "notes.txt").write_text("uncommitted\n", encoding="utf-8")
    r, _ = layout.branch("feat/r", local=False)
    return layout, {"a": (a, wt_a), "similar": wt_similar, "b": b, "dirty": wt_dirty, "r": r}


# A10 positive: sweep-lists-then-confirm-removes
def test_sweep_lists_then_confirm_removes(tmp_path: Path, monkeypatch) -> None:
    layout, s = sweep_layout(tmp_path)
    a, wt_a = s["a"]

    rc, out, err, calls = run(monkeypatch, layout, "--sweep")

    assert rc == 0, err
    listed = [
        f"remove feat/a {a[:7]} — worktree {wt_a}, local, remote",
        f"remove feat/b {s['b'][:7]} — no worktree, local, remote",
        f"skip feat/dirty — worktree {s['dirty']} has untracked files",
        f"remove feat/r {s['r'][:7]} — no worktree, no local, remote",
    ]
    token = token_of(out)
    assert out.splitlines() == listed + [f"confirm with: land --sweep --confirm {token}"]
    assert layout.intact("feat/a", wt_a) and layout.intact("feat/b")
    assert ref_exists(layout.origin, "refs/heads/feat/r")
    assert not calls.argvs("worktree", "remove") and not calls.argvs("update-ref")
    assert not calls.argvs("push")
    assert len(calls.argvs("fetch", "--prune", "origin")) == 1

    rc, out, err, calls = run(monkeypatch, layout, "--sweep", "--confirm", token)

    assert rc == 0, err
    assert f"Removed worktree {wt_a}\n" in out
    assert "Deleted local branch feat/b\n" in out
    assert "Deleted remote branch feat/r\n" in out
    assert out.endswith(f"next: cd '{layout.repo}'\n"), out
    assert layout.gone("feat/a", wt_a) and layout.gone("feat/b") and layout.gone("feat/r")
    assert layout.intact("feat/dirty", s["dirty"])
    assert (s["dirty"] / "notes.txt").exists()
    assert layout.intact("feat/a-2", s["similar"])
    assert (s["similar"] / "draft.txt").exists()
    assert not calls.argvs("pr", "merge")


# A10 negative: changed-list-token-removes-nothing
def test_changed_list_token_removes_nothing(tmp_path: Path, monkeypatch) -> None:
    layout, s = sweep_layout(tmp_path)
    a, wt_a = s["a"]
    _rc, out, _err, _calls = run(monkeypatch, layout, "--sweep")
    token = token_of(out)

    git(layout.repo, "switch", "-q", "feat/b")
    (layout.repo / "later.txt").write_text("after the list\n", encoding="utf-8")
    git(layout.repo, "add", "later.txt")
    git(layout.repo, "commit", "-q", "-m", "after the list")
    git(layout.repo, "switch", "-q", "main")

    rc, out, err, calls = run(monkeypatch, layout, "--sweep", "--confirm", token)

    assert rc == 1
    assert err == (
        "BLOCK land.cleanup: the sweep list differs from the one confirmed; "
        "run land --sweep again\n"
    )
    assert "Removed" not in out and "Deleted" not in out
    assert layout.intact("feat/a", wt_a) and layout.intact("feat/b")
    assert ref_exists(layout.origin, "refs/heads/feat/r")
    assert not calls.argvs("worktree", "remove") and not calls.argvs("update-ref")
    assert not calls.argvs("push")


def test_sweep_confirm_continues_past_refusal(tmp_path: Path, monkeypatch) -> None:
    layout, s = sweep_layout(tmp_path)
    _rc, out, _err, _calls = run(monkeypatch, layout, "--sweep")
    token = token_of(out)

    def configure(calls: Calls) -> None:
        calls.refuse_push_for = {"feat/b"}

    rc, out, err, _calls = run(monkeypatch, layout, "--sweep", "--confirm", token,
                               configure=configure)

    assert rc == 1
    assert "BLOCK land.cleanup: feat/b: remote branch feat/b not deleted: " in err
    assert layout.gone("feat/a", s["a"][1]) and layout.gone("feat/r")
    assert ref_exists(layout.origin, "refs/heads/feat/b")


def test_sweep_confirm_replans_before_each_removal(tmp_path: Path, monkeypatch) -> None:
    layout = Repo(tmp_path)
    (layout.repo / ".gitignore").write_text(".env\n", encoding="utf-8")
    git(layout.repo, "add", ".gitignore")
    git(layout.repo, "commit", "-q", "-m", "ignore .env")
    git(layout.repo, "push", "-q", "origin", "main")
    _, wt_a = layout.branch("feat/a", worktree="wt-a")
    _, wt_c = layout.branch("feat/c", worktree="wt-c")
    _rc, out, _err, _calls = run(monkeypatch, layout, "--sweep")
    token = token_of(out)
    assert len([line for line in out.splitlines() if line.startswith("remove ")]) == 2

    def configure(calls: Calls) -> None:
        def drop_env(removed: Path) -> None:
            if removed == wt_a:
                (wt_c / ".env").write_text("SECRET=1\n", encoding="utf-8")
        calls.after_remove = drop_env

    rc, out, err, calls = run(monkeypatch, layout, "--sweep", "--confirm", token,
                              configure=configure)

    assert rc == 1
    assert (
        f"BLOCK land.cleanup: feat/c: worktree {wt_c} has ignored files outside "
        "the regenerable set: .env\n"
    ) in err, err
    assert layout.gone("feat/a", wt_a)
    assert layout.intact("feat/c", wt_c)
    assert (wt_c / ".env").read_text(encoding="utf-8") == "SECRET=1\n"
    assert all(str(wt_c) not in argv for argv in calls.argvs("worktree", "remove"))


def test_sweep_no_candidates(tmp_path: Path, monkeypatch) -> None:
    layout = Repo(tmp_path)
    _, wt = layout.branch("feat/x-2", worktree="wt-x-2", merged=False)

    rc, out, err, calls = run(monkeypatch, layout, "--sweep")

    assert rc == 0, err
    assert out == "No merged changes to clean up\n"
    assert layout.intact("feat/x-2", wt)


def test_sweep_skips_invoking_worktree(tmp_path: Path, monkeypatch) -> None:
    layout = Repo(tmp_path)
    _, wt = layout.branch("feat/x", worktree="wt-x")

    rc, out, err, calls = run(monkeypatch, layout, "--sweep", cwd=wt)

    assert rc == 0, err
    assert out.splitlines() == [
        "skip feat/x — current working directory",
        "No merged changes to clean up",
    ]
    assert layout.intact("feat/x", wt)


def test_sweep_reports_unexamined_older_prs(tmp_path: Path, monkeypatch) -> None:
    layout = Repo(tmp_path)

    def configure(calls: Calls) -> None:
        calls.merged_override = [
            {"number": n, "headRefName": f"old/{n}", "headRefOid": "c" * 40}
            for n in range(1000)
        ]

    rc, out, err, _calls = run(monkeypatch, layout, "--sweep", configure=configure)

    assert rc == 0, err
    assert "older merged PRs were not examined" in out
