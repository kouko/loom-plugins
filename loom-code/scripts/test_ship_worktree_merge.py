"""Regression coverage for Codex Desktop worktree-aware direct merges."""

from __future__ import annotations

import io
import subprocess
from pathlib import Path

from loom_checker.command_handlers import land
from loom_checker.command_handlers import push as loom_checker


SHIP = Path(__file__).resolve().parents[1] / "skills" / "ship" / "SKILL.md"


def test_ship_accepted_land_renders_absolute_worktree_in_command() -> None:
    text = SHIP.read_text(encoding="utf-8")

    assert "cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py land" in text
    assert "never rely on the Bash tool's workdir" in text


def test_cmd_push_non_publication_command_still_passes(monkeypatch) -> None:
    payload = {
        "cwd": "/does/not/matter",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "ls -la"},
    }
    called = False

    def unexpected(*_args):
        nonlocal called
        called = True
        return "unexpected"

    monkeypatch.setattr(loom_checker, "read_hook_payload", lambda: payload)
    monkeypatch.setattr(loom_checker, "_reminder", unexpected)

    assert loom_checker.cmd_push(["--hook"], io.StringIO(), io.StringIO()) == 0
    assert called is False


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def _land_without_attestation(
    tmp_path: Path, monkeypatch, *, attestations: int = 0,
) -> tuple[int, str, list]:
    """`land --accepted-by` on a branch that carries a committed intent and
    `attestations` attested changes. Every gh and git call goes through
    `run_land_external`, which records here and fails as if offline, so
    nothing reaches GitHub."""
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "branch", "-M", "main")
    _git(repo, "switch", "-q", "-c", "feature")
    _git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    intent = repo / "docs" / "loom" / "intent" / "change.md"
    intent.parent.mkdir(parents=True)
    intent.write_text(
        "# Change\noriginator: kouko\nstatus: confirmed 2026-09-14\n"
        "\n## Proposed outcome\nLand it.\n",
        encoding="utf-8",
    )
    for index in range(attestations):
        target = repo / "docs" / "loom" / f"change-{index}" / "attestation.json"
        target.parent.mkdir(parents=True)
        target.write_text(f'{{"change_id": "change-{index}"}}', encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "change")

    calls: list = []

    def offline(argv, _timeout, **_kwargs):
        calls.append(list(argv))
        return subprocess.CompletedProcess(argv, 1, "", "offline")

    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", offline)
    monkeypatch.setattr(
        land, "resolve_publish_executable",
        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh",
    )
    err = io.StringIO()
    rc = land.cmd_land(["--accepted-by", "kouko"], io.StringIO(), err)
    return rc, err.getvalue(), calls


# With no attestation `land` identifies the change from its one intent and
# goes on to GitHub (spec REQ-6): the refusal it used to give here, with its
# two routes, is gone, and nothing tells the caller to hand a command over.
def test_merge_without_attestation_reaches_github(tmp_path: Path, monkeypatch) -> None:
    rc, err, calls = _land_without_attestation(tmp_path, monkeypatch)

    assert rc == 1
    assert calls and calls[0][1:3] == ["repo", "view"]
    assert err == "BLOCK land.merge: default branch lookup failed: offline\n"


# Two attested changes disagree with the change the branch carries: `land`
# cannot identify the change, refuses on one line naming the fix, and reaches
# nothing on GitHub.
def test_merge_with_two_attested_changes_is_unidentified(
    tmp_path: Path, monkeypatch
) -> None:
    rc, err, calls = _land_without_attestation(tmp_path, monkeypatch, attestations=2)

    assert rc == 1
    assert calls == []
    lines = err.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("BLOCK land.merge: the branch identifies change 'change'")
    assert "rename the branch to <type>/<change-id>" in lines[0]


def _land_on_a_branch_that_adds_nothing(tmp_path: Path, monkeypatch) -> tuple[int, str, list]:
    """`land --accepted-by` on a branch that adds nothing to a base which
    already attests a change and which the published trunk contains -- the
    landed shape. The merge route reads the same empty-delta state the push
    route does, so it owes the same tail."""
    repo = tmp_path / "landed-repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    intent = repo / "docs" / "loom" / "intent" / "change.md"
    intent.parent.mkdir(parents=True)
    intent.write_text(
        "# Change\noriginator: kouko\nstatus: confirmed 2026-09-14\n"
        "\n## Proposed outcome\nLand it.\n",
        encoding="utf-8",
    )
    target = repo / "docs" / "loom" / "change-0" / "attestation.json"
    target.parent.mkdir(parents=True)
    target.write_text('{"change_id": "change-0"}', encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "landed change")
    # The change landed, so the remote's default branch carries the base. Both
    # refs are what `git clone` writes: the branch is the snapshot, and
    # `refs/remotes/origin/HEAD` is what says the remote calls that branch its
    # default. Without them the state cannot be told from a finished branch
    # nobody published, and `nothing_left_to_publish` answers False on that
    # doubt.
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")
    _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    _git(repo, "switch", "-q", "-c", "feature")
    _git(repo, "remote", "add", "origin", "git@github.com:example/project.git")

    calls: list = []
    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", lambda argv, _t, **_k: calls.append(list(argv)))
    monkeypatch.setattr(
        land, "resolve_publish_executable",
        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh",
    )
    err = io.StringIO()
    rc = land.cmd_land(["--accepted-by", "kouko"], io.StringIO(), err)
    return rc, err.getvalue(), calls


# Empty delta over an attesting base, on a branch that does not name the
# change: nothing identifies it, so `land` refuses on one line naming the fix
# and reaches nothing on GitHub.
def test_merge_on_a_branch_that_adds_nothing_is_unidentified(
    tmp_path: Path, monkeypatch
) -> None:
    rc, err, calls = _land_on_a_branch_that_adds_nothing(tmp_path, monkeypatch)

    assert rc == 1
    assert calls == []
    lines = err.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith("BLOCK land.merge: cannot identify the change")
    assert "rename the branch to <type>/<change-id>" in lines[0]
