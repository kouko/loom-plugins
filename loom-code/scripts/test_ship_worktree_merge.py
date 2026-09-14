"""Regression coverage for Codex Desktop worktree-aware direct merges."""

from __future__ import annotations

import io
from pathlib import Path

import pytest

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
