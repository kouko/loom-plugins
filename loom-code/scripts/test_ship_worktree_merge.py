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
    "echo gh pr merge",
    "gh pr $'merge' 5",
    'gh pr $"merge" 5',
])
def test_hook_text_rule_blocks_hand_typed_merge_forms(
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
])
def test_hook_text_rule_leaves_other_commands_alone(
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


MERGE_UNATTESTED_REASON = (
    "BLOCK land.merge: branch must carry exactly one attested change; found 0"
)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def _land_without_attestation(
    tmp_path: Path, monkeypatch, *, attestations: int = 0,
) -> tuple[int, str, list]:
    """`land --accepted-by` on a branch that carries a committed intent and
    `attestations` attested changes. Every gh and git call goes through
    `run_land_external`, which records here instead of running, so nothing
    reaches GitHub."""
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
    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", lambda argv, _t, **_k: calls.append(list(argv)))
    monkeypatch.setattr(
        land, "resolve_publish_executable",
        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh",
    )
    err = io.StringIO()
    rc = land.cmd_land(["--accepted-by", "kouko"], io.StringIO(), err)
    return rc, err.getvalue(), calls


# A2 positive: merge-refusal-names-both-routes. With no attestation `land`
# refuses at the acceptance step, before the shared publication check, so this
# is the site a caller actually sees; it names the same two routes the
# publication refusal names, and forbids handing the command over.
def test_merge_refusal_names_both_routes(tmp_path: Path, monkeypatch) -> None:
    rc, err, calls = _land_without_attestation(tmp_path, monkeypatch)

    assert rc == 1
    assert calls == []
    reason = err.splitlines()[0]
    assert reason.startswith("BLOCK land.merge: ")
    assert "run the closing-review station" in reason
    assert "selection propose <change-id> --origin agent --skip reviewers" in reason
    assert "confirms by typing `/loom-code:expert-mode <code>`" in reason
    assert "never hand the blocked publication command to the user to run" in reason


# A2, count greater than one: the merge refusal names the routes only where
# they work. With two attested changes in the delta neither route reduces the
# count, so the same site names the action that does.
def test_merge_refusal_with_two_attested_changes_names_no_dead_route(
    tmp_path: Path, monkeypatch
) -> None:
    rc, err, calls = _land_without_attestation(tmp_path, monkeypatch, attestations=2)

    assert rc == 1
    assert calls == []
    lines = err.splitlines()
    assert len(lines) == 1
    reason = lines[0]
    assert reason.startswith(
        "BLOCK land.merge: branch must carry exactly one attested change; found 2"
    )
    assert "two legal routes" not in reason
    assert "selection propose" not in reason
    assert "the branch delta has to end at one attested change" in reason
    assert "never hand the blocked publication command to the user to run" in reason


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
    # The change landed, so the published trunk carries the base. Without this
    # ref the state cannot be told from a finished branch nobody published, and
    # `nothing_left_to_publish` answers False on that doubt.
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")
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


# A2, empty delta over an attesting base: `land` reaches the same tail the push
# route does, and it is pinned at both sites rather than at one.
def test_merge_refusal_on_a_branch_that_adds_nothing_names_no_route(
    tmp_path: Path, monkeypatch
) -> None:
    rc, err, calls = _land_on_a_branch_that_adds_nothing(tmp_path, monkeypatch)

    assert rc == 1
    assert calls == []
    lines = err.splitlines()
    assert len(lines) == 1
    assert lines[0] == f"{MERGE_UNATTESTED_REASON}{loom_checker.NOTHING_TO_PUBLISH}"


# A2 negative: merge-without-attestation-still-refused. The refusal keeps the
# rule id, the exit code and the reason it opened with, on one line.
def test_merge_without_attestation_still_refused(tmp_path: Path, monkeypatch) -> None:
    rc, err, calls = _land_without_attestation(tmp_path, monkeypatch)

    assert rc == 1
    assert calls == []
    lines = err.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith(MERGE_UNATTESTED_REASON)
