"""Regression coverage for Codex Desktop worktree-aware direct merges."""

from __future__ import annotations

import io
import subprocess
from pathlib import Path

import pytest

from loom_checker.command_handlers import land
from loom_checker.command_handlers import push as loom_checker


SHIP = Path(__file__).resolve().parents[1] / "skills" / "ship" / "SKILL.md"


def test_ship_accepted_land_renders_absolute_worktree_in_command() -> None:
    text = SHIP.read_text(encoding="utf-8")

    assert "cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py land" in text
    assert "never rely on the Bash tool's workdir" in text


PUSH_MERGE_BLOCK = (
    "BLOCK push.merge: merge through loom_checker.py land --accepted-by <name>"
)


def _merge_hook(tmp_path: Path, monkeypatch, command: str) -> tuple[int, str, list]:
    main = tmp_path / "main"
    main.mkdir(exist_ok=True)
    payload = {
        "cwd": str(main),
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }
    called: list = []
    monkeypatch.setattr(loom_checker, "read_hook_payload", lambda: payload)
    monkeypatch.setattr(
        loom_checker,
        "_cmd_push",
        lambda *_args: called.append(Path.cwd()) or 0,
    )
    monkeypatch.chdir(tmp_path)
    err = io.StringIO()
    rc = loom_checker.cmd_push(["--hook"], io.StringIO(), err)
    return rc, err.getvalue(), called


# hook-blocks-absolute-cd-merge-with-push-merge (A11 positive): the absolute
# `cd` form allowed before, plus bare, relative and nested forms, are refused
# before any repository selection; `land` is the only merge path.
def test_hook_blocks_absolute_cd_merge_with_push_merge(
    tmp_path: Path, monkeypatch,
) -> None:
    feature = tmp_path / "feature"
    feature.mkdir()

    rc, err, called = _merge_hook(
        tmp_path, monkeypatch, f"cd '{feature}' && gh pr merge 808 --squash"
    )

    assert rc == 2
    assert err.splitlines() == [PUSH_MERGE_BLOCK]
    assert called == []


@pytest.mark.parametrize("command", [
    "gh pr merge 1",
    "gh pr merge 808 --squash",
    "cd feature && gh pr merge 808 --squash",
    "bash -c 'gh pr merge 1'",
    "zsh -c 'cd /tmp && gh pr merge 1'",
    "eval 'gh pr merge 1'",
    "env GH_TOKEN=x gh pr merge 1",
    "Gh pr merge 1",
])
def test_hook_blocks_every_merge_form_with_push_merge(
    tmp_path: Path, monkeypatch, command: str,
) -> None:
    rc, err, called = _merge_hook(tmp_path, monkeypatch, command)

    assert rc == 2
    assert err.splitlines() == [PUSH_MERGE_BLOCK]
    assert called == []


# hook-merge-text-rule-fails-closed (A11): hand-typed merges hidden behind
# wrapper options, combined shell flags, shell grammar or a backslash-newline
# split are refused by the textual rule, which also refuses mere mentions.
@pytest.mark.parametrize("command", [
    "(gh pr merge 7)",
    "bash -lc 'gh pr merge 7'",
    "sh -ec 'gh pr merge 7'",
    "sudo -u me gh pr merge 7",
    "nice -n 5 gh pr merge 7",
    "time -p gh pr merge 7",
    "command -p gh pr merge 7",
    "echo 7 | xargs -n1 gh pr merge",
    "exec -a x gh pr merge 7",
    "{ gh pr merge 7; }",
    "if true; then gh pr merge 7; fi",
    "for n in 7; do gh pr merge $n; done",
    "! gh pr merge 7",
    "gh pr \\\nmerge 7",
    "gh \\\npr merge 7",
    "'gh' 'pr' 'merge' 7",
    "/opt/homebrew/bin/GH -R o/r PR Merge 7",
    "gh pr $'merge' 5",
    'gh pr $"merge" 5',
])
def test_hook_blocks_hand_typed_merge_forms(
    tmp_path: Path, monkeypatch, command: str,
) -> None:
    rc, err, called = _merge_hook(tmp_path, monkeypatch, command)

    assert rc == 2
    assert err.splitlines() == [PUSH_MERGE_BLOCK]
    assert called == []


@pytest.mark.parametrize("command", [
    "gh pr view 7",
    "gh pr list --search merge",
    "git merge main",
    "ghx pr merge 7",
    # Naming a merge is not running one. The rule used to be a text match over
    # the whole command, so each of these was refused: a printed string, a
    # search for the words, a commit message describing one, and a document
    # written through a heredoc. Recognition is structural now, so they run.
    "echo gh pr merge",
    'rg -n "SEGMENT_SPLIT|publisher&&gh pr create|gh pr merge" loom-code -g \'*.py\'',
    "git commit -m 'docs: explain gh pr merge --squash'",
    "man gh | grep -A2 'pr merge'",
    "cat > notes.md <<'EOF'\nTo land it run gh pr merge --squash\nEOF\n",
])
def test_hook_leaves_commands_that_only_name_a_merge_alone(
    tmp_path: Path, monkeypatch, command: str,
) -> None:
    _rc, err, _called = _merge_hook(tmp_path, monkeypatch, command)

    assert "BLOCK push.merge" not in err


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
        return 0

    monkeypatch.setattr(loom_checker, "read_hook_payload", lambda: payload)
    monkeypatch.setattr(loom_checker, "_cmd_push", unexpected)

    assert loom_checker.cmd_push(["--hook"], io.StringIO(), io.StringIO()) == 0
    assert called is False


def test_cmd_push_noncanonical_git_push_remains_blocked(
    tmp_path: Path, monkeypatch,
) -> None:
    feature = tmp_path / "feature"
    feature.mkdir()
    payload = {
        "cwd": str(feature),
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": f"cd '{feature}' && git push --force origin main"},
    }
    err = io.StringIO()

    monkeypatch.setattr(loom_checker, "read_hook_payload", lambda: payload)

    assert loom_checker.cmd_push(["--hook"], io.StringIO(), err) == 2
    assert "canonical quote-all rendering" in err.getvalue()


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
