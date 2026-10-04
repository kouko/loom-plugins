"""W0-05 — loom-code host hooks: hooks.json wires exactly one deterministic
entry (concept-model §7, §7a).

The old mechanism (git-guard, ask-triage, the router card, the family
reception/relay prose, language-stop-check) is deleted; what remains is
SessionStart -> hooks/session-start, PreToolUse(Bash) -> the single
loom checker, PostToolUse(Skill) -> language-anchor (host hygiene, not a
loom flow mechanism — plan W0-05 risk note).

External surfaces grounded:
- Claude Code hook config shape (``hooks.<Event>[].matcher`` +
  ``hooks[].{type,command}``, ``${CLAUDE_PLUGIN_ROOT}`` expansion): the
  file itself is the in-repo evidence, source-(d).
- PreToolUse blocking is by hook exit status (non-zero from the checker),
  not by a hooks.json field; the matcher is a regex over the TOOL NAME,
  so the ``git push`` / ``gh pr create`` / ``gh pr merge`` discrimination
  lives inside ``scripts/loom_checker.py push``, not here.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HOOKS_DIR = REPO / "loom-code" / "hooks"
HOOKS_JSON = HOOKS_DIR / "hooks.json"
CODEX_HOOKS_JSON = HOOKS_DIR / "hooks-codex.json"

REMOVED_HOOK_FILES = [
    "git-guard.py",
    "ask-triage.py",
    "language-stop-check.py",
    "router-card.md",
    "family-reception.md",
    "family-relay.md",
    "plain-relay.md",
]
KEPT_HOOK_FILES = ["session-start", "language-anchor.py", "lang_detect.py", "hooks.json"]


@pytest.fixture(scope="module")
def hooks() -> dict:
    return json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]


@pytest.fixture(scope="module")
def codex_hooks() -> dict:
    return json.loads(CODEX_HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]


def _matchers(entries) -> set[str]:
    return {e.get("matcher", "") for e in entries}


def _commands(entries) -> list[str]:
    return [h["command"] for e in entries for h in e["hooks"]]


def test_event_set_is_exact(hooks):
    assert set(hooks) == {"SessionStart", "PreToolUse", "PostToolUse"}


def test_codex_event_set_is_session_start_and_publication_interception(codex_hooks):
    assert set(codex_hooks) == {"SessionStart", "PreToolUse"}
    (command,) = _commands(codex_hooks["SessionStart"])
    assert command == '"${PLUGIN_ROOT}/hooks/session-start"'


def test_session_start_runs_the_rewritten_script(hooks):
    (entry,) = [e for e in hooks["SessionStart"] if e["matcher"] == "startup|clear|compact"]
    (command,) = _commands([entry])
    assert command.endswith('/hooks/session-start"')


def test_session_start_reanchors_language_after_compact_or_resume(hooks):
    (entry,) = [e for e in hooks["SessionStart"] if e["matcher"] == "compact|resume"]
    (command,) = _commands([entry])
    assert "/hooks/language-anchor.py" in command


def test_pre_tool_use_matcher_set_is_bash_only(hooks):
    """`push --hook` reads only shell commands, so no host runs it on a
    file-editing tool."""
    assert _matchers(hooks["PreToolUse"]) == {"Bash"}
    opencode = json.loads((HOOKS_DIR / "hooks-opencode.json").read_text(encoding="utf-8"))
    assert _matchers(opencode["hooks"]["PreToolUse"]) == {"Bash"}


def test_codex_pre_tool_use_uses_native_root_and_bash_matcher(codex_hooks):
    assert _matchers(codex_hooks["PreToolUse"]) == {"Bash"}
    for command in _commands(codex_hooks["PreToolUse"]):
        assert "${PLUGIN_ROOT}" in command
        assert "${CLAUDE_PLUGIN_ROOT}" not in command


def test_pre_tool_use_runs_the_single_checker_push_rule(hooks):
    """``--hook`` is what puts the checker in hook mode. Without it the
    checker reads no stdin at all, so the flag is not decoration: a hook
    entry that omits it would judge nothing."""
    (command,) = _commands(hooks["PreToolUse"])
    assert 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py" push --hook' in command


def _claude_pre_tool_use(hooks, payload: dict, plugin_root: Path):
    """Run the Claude Code PreToolUse command as Claude Code does (``sh -c``)."""
    (command,) = _commands(hooks["PreToolUse"])
    return subprocess.run(["sh", "-c", command], input=json.dumps(payload),
                          capture_output=True, text=True, timeout=30,
                          env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(plugin_root)})


PUSH = "git" + " push"  # concatenated so this file's own text is no push


def test_pre_tool_use_checker_missing_allows_and_says_so(hooks, tmp_path):
    """REQ-4 on Claude Code: a stale plugin root (checker absent) never
    refuses a publication command; it allows with the failure line."""
    missing = tmp_path / "removed-version"
    result = _claude_pre_tool_use(
        hooks, {"tool_name": "Bash", "tool_input": {"command": f"{PUSH} -u origin feat"}}, missing)
    assert result.returncode == 0, result.stderr
    assert "loom: publication hook failed (" in result.stderr
    assert "; allowing." in result.stderr
    assert str(missing / "scripts" / "loom_checker.py") in result.stderr


def _fallback_program(command: str) -> str:
    """The checker-missing branch of a hook command, host and root normalised."""
    program = command.split("; else ", 1)[1]
    return program.replace("restart Claude Code", "restart <host>").replace(
        "restart Codex", "restart <host>").replace("${CLAUDE_PLUGIN_ROOT}", "${PLUGIN_ROOT}")


def test_checker_missing_fallback_programs_are_identical(hooks, codex_hooks):
    """The Claude Code fallback and the Codex fallback run one program."""
    programs = [_fallback_program(c) for c in _commands(hooks["PreToolUse"])]
    programs += [_fallback_program(c) for c in _commands(codex_hooks["PreToolUse"])]
    assert len(programs) == 2
    assert len(set(programs)) == 1


def test_post_tool_use_keeps_language_anchor(hooks):
    assert _matchers(hooks["PostToolUse"]) == {"Skill|Agent"}
    (command,) = _commands(hooks["PostToolUse"])
    assert "/hooks/language-anchor.py" in command


def test_no_removed_hook_is_referenced(hooks):
    text = HOOKS_JSON.read_text(encoding="utf-8")
    for name in REMOVED_HOOK_FILES:
        assert name not in text, name
    # No host captures prompts or guards the selection record store.
    for path in [HOOKS_JSON, CODEX_HOOKS_JSON, HOOKS_DIR / "hooks-opencode.json",
                 HOOKS_DIR / "agy_adapter.py", REPO / "scripts" / "opencode" / "loader.js"]:
        host_text = path.read_text(encoding="utf-8")
        for needle in ("selection capture", "selections/", "selection.guard"):
            assert needle not in host_text, (path.name, needle)


def test_removed_hook_files_are_gone():
    for name in REMOVED_HOOK_FILES:
        assert not (HOOKS_DIR / name).exists(), name


def test_kept_hook_files_still_present():
    for name in KEPT_HOOK_FILES:
        assert (HOOKS_DIR / name).is_file(), name


def test_hook_dir_commands_resolve_to_existing_files(hooks):
    """Commands under ``hooks/`` must exist here; the checker under
    ``scripts/`` is owned by a parallel task and is not asserted."""
    for entries in hooks.values():
        for command in _commands(entries):
            rel = command.split("${CLAUDE_PLUGIN_ROOT}/", 1)[1].rstrip('" ')
            if not rel.startswith("hooks/"):
                continue
            assert (REPO / "loom-code" / rel).is_file(), command


AGY_HOOKS_JSON = REPO / "loom-code" / "hooks.json"
AGY_EVENTS = {"PreToolUse", "PostToolUse", "PreInvocation", "PostInvocation", "Stop"}
AGY_GROUPED_EVENTS = {"PreToolUse", "PostToolUse"}


@pytest.fixture(scope="module")
def agy_hooks() -> dict:
    """Antigravity CLI reads ``<plugin-root>/hooks.json``: top level keyed by
    hook name, then event; commands run via ``sh -c`` from the plugin root."""
    return json.loads(AGY_HOOKS_JSON.read_text(encoding="utf-8"))


def _agy_handlers(agy_hooks: dict):
    for events in agy_hooks.values():
        for event, entries in events.items():
            for entry in entries:
                handlers = entry["hooks"] if event in AGY_GROUPED_EVENTS else [entry]
                yield event, entry, handlers


def test_agy_hooks_use_agy_schema(agy_hooks):
    assert "hooks" not in agy_hooks
    for events in agy_hooks.values():
        assert set(events) <= AGY_EVENTS
        for event, entries in events.items():
            for entry in entries:
                if event in AGY_GROUPED_EVENTS:
                    assert set(entry) == {"matcher", "hooks"}
                else:
                    assert entry["type"] == "command"


def test_agy_hooks_wire_push_gate_and_pre_invocation(agy_hooks):
    wired = {
        (event, entry.get("matcher", ""), handler["command"])
        for event, entry, handlers in _agy_handlers(agy_hooks)
        for handler in handlers
    }
    assert wired == {
        ("PreToolUse", "run_command", "python3 ./hooks/agy_adapter.py push-gate"),
        ("PreInvocation", "", "python3 ./hooks/agy_adapter.py pre-invocation"),
    }


def test_agy_hooks_carry_no_host_root_variable(agy_hooks):
    text = AGY_HOOKS_JSON.read_text(encoding="utf-8")
    assert "${CLAUDE_PLUGIN_ROOT}" not in text
    assert "${PLUGIN_ROOT}" not in text


def test_agy_hook_commands_resolve_to_existing_files(agy_hooks):
    for _event, _entry, handlers in _agy_handlers(agy_hooks):
        for handler in handlers:
            rel = handler["command"].split("./", 1)[1].split()[0]
            assert (REPO / "loom-code" / rel).is_file(), handler["command"]


def test_codex_manifest_selects_only_codex_hooks():
    manifest = json.loads(
        (REPO / "loom-code/.codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    assert manifest["hooks"] == "./hooks/hooks-codex.json"
