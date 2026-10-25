"""W0-05 — loom-code host hooks: hooks.json wires exactly one deterministic
entry (concept-model §7, §7a).

The old mechanism (git-guard, ask-triage, the router card, the family
reception/relay prose, language-stop-check) is deleted; what remains is
SessionStart -> hooks/session-start, PreToolUse(Bash) -> the single
loom checker, PostToolUse(Skill|Agent), SessionStart(compact|resume) and
UserPromptSubmit -> language-anchor (host hygiene, not a loom flow
mechanism — plan W0-05 risk note).

External surfaces grounded:
- Claude Code hook config shape (``hooks.<Event>[].matcher`` +
  ``hooks[].{type,command}``, ``${CLAUDE_PLUGIN_ROOT}`` expansion): the
  file itself is the in-repo evidence, source-(d).
- PreToolUse blocking is by hook exit status (non-zero from the checker),
  not by a hooks.json field; the matcher is a regex over the TOOL NAME,
  so the ``git push`` / ``gh pr create`` / ``gh pr merge`` discrimination
  lives inside ``scripts/loom_checker.py push``, not here.
"""
# concern: shell-reserved exit-code names can abort host hooks before checker results or fallbacks are handled.
from __future__ import annotations

import json
import os
import subprocess
import sys
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
KEPT_HOOK_FILES = ["session-start", "language-anchor.py", "hooks.json"]


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
    assert set(hooks) == {"SessionStart", "PreToolUse", "PostToolUse", "UserPromptSubmit"}


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
    assert '"${CLAUDE_PLUGIN_ROOT}/scripts/loom-python" --ready push --hook' in command


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


def test_user_prompt_submit_runs_language_anchor(hooks):
    (command,) = _commands(hooks["UserPromptSubmit"])
    assert command.startswith('"${CLAUDE_PLUGIN_ROOT}/scripts/loom-python" --ready --script ../hooks/language-anchor.py')
    assert 'exec python3 "${CLAUDE_PLUGIN_ROOT}/hooks/language-anchor.py"' in command


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
    assert {(event, matcher) for event, matcher, _ in wired} == {
        ("PreToolUse", "run_command"), ("PreInvocation", "")}
    for _, _, command in wired:
        assert command.startswith("./scripts/loom-python --ready --script ../hooks/agy_adapter.py ")


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


def _ready_env(tmp_path):
    runtime = tmp_path / "cache/loom-code/python-3.11-pyyaml-6.0.2-v1/bin"
    runtime.mkdir(parents=True)
    (runtime / "python").symlink_to(sys.executable)
    return {**os.environ, "XDG_CACHE_HOME": str(tmp_path / "cache"), "PATH": "/bin"}


@pytest.mark.parametrize("host", ["claude", "codex", "opencode", "antigravity"])
def test_host_hooks_use_ready_runtime_without_host_python(host, tmp_path):
    roots = {"claude": HOOKS_JSON, "codex": CODEX_HOOKS_JSON,
             "opencode": HOOKS_DIR / "hooks-opencode.json", "antigravity": AGY_HOOKS_JSON}
    data = json.loads(roots[host].read_text(encoding="utf-8"))
    if host == "antigravity":
        command = data["loom-code"]["PreToolUse"][0]["hooks"][0]["command"]
        payload = {"workspacePaths": [str(tmp_path)], "toolCall": {"args": {"CommandLine": "git status"}}}
    else:
        command = _commands(data["hooks"]["PreToolUse"])[0]
        payload = {"tool_name": "Bash", "tool_input": {"command": "git status"}}
    env = _ready_env(tmp_path)
    env.update(CLAUDE_PLUGIN_ROOT=str(REPO / "loom-code"), PLUGIN_ROOT=str(REPO / "loom-code"))
    result = subprocess.run(["/bin/sh", "-c", command], input=json.dumps(payload), text=True,
                            capture_output=True, cwd=REPO / "loom-code", env=env, timeout=30)
    assert result.returncode == 0, result.stderr
    if host == "antigravity":
        assert json.loads(result.stdout) == {"decision": "allow"}


@pytest.mark.parametrize("host,event,matcher", [
    ("claude", "SessionStart", "compact|resume"),
    ("claude", "PreToolUse", "Bash"),
    ("claude", "PostToolUse", "Skill|Agent"),
    ("claude", "UserPromptSubmit", ""),
    ("codex", "PreToolUse", "Bash"),
    ("opencode", "PreToolUse", "Bash"),
    ("opencode", "PostToolUse", "Skill"),
    ("antigravity", "PreToolUse", "run_command"),
    ("antigravity", "PreInvocation", ""),
])
@pytest.mark.parametrize("shell", ["/bin/sh", "/bin/zsh"])
def test_hook_exit_code_capture_avoids_readonly_shell_name(host, event, matcher, shell, tmp_path):
    if not Path(shell).is_file():
        pytest.skip(f"{shell} is unavailable")
    root = REPO / "loom-code"
    manifests = {"claude": HOOKS_JSON, "codex": CODEX_HOOKS_JSON,
                 "opencode": HOOKS_DIR / "hooks-opencode.json", "antigravity": AGY_HOOKS_JSON}
    data = json.loads(manifests[host].read_text(encoding="utf-8"))
    if host == "antigravity":
        entries = data["loom-code"][event]
        (entry,) = [item for item in entries if item.get("matcher", "") == matcher]
        command = (entry["hooks"][0] if event == "PreToolUse" else entry)["command"]
        payload = {"workspacePaths": [str(tmp_path)], "toolCall": {"args": {"CommandLine": "git status"}},
                   "conversationId": "readonly", "invocationNum": 0, "initialNumSteps": 1}
    else:
        entries = data["hooks"][event]
        (entry,) = [item for item in entries if item.get("matcher", "") == matcher]
        (command,) = _commands([entry])
        payload = {"hook_event_name": event, "tool_name": "Bash",
                   "tool_input": {"command": "git status"}}
    if shell == "/bin/sh":
        command = "readonly status; " + command
    env = {**os.environ, "XDG_CACHE_HOME": str(tmp_path / "empty"), "TMPDIR": str(tmp_path),
           "CLAUDE_PLUGIN_ROOT": str(root), "PLUGIN_ROOT": str(root)}
    result = subprocess.run([shell, "-c", command], input=json.dumps(payload), text=True,
                            capture_output=True, cwd=root, env=env, timeout=30)
    assert result.returncode == 0, (host, event, shell, result.stderr)


def test_missing_ready_runtime_reports_repair_without_checker_refusal(hooks, tmp_path):
    (command,) = _commands(hooks["PreToolUse"])
    env = {**os.environ, "XDG_CACHE_HOME": str(tmp_path / "empty"), "PATH": "/bin",
           "CLAUDE_PLUGIN_ROOT": str(REPO / "loom-code")}
    result = subprocess.run(["/bin/sh", "-c", command], input=json.dumps(
        {"tool_name": "Bash", "tool_input": {"command": "git push origin feat"}}),
        text=True, capture_output=True, env=env, timeout=30)
    assert result.returncode == 0
    assert "--repair" in result.stderr and "publication hook failed" in result.stderr


@pytest.mark.parametrize("host", ["opencode", "antigravity"])
def test_json_hosts_return_failure_diagnostic_when_runtime_missing(host, tmp_path):
    root = REPO / "loom-code"
    if host == "opencode":
        data = json.loads((HOOKS_DIR / "hooks-opencode.json").read_text())
        command = _commands(data["hooks"]["PreToolUse"])[0]
        payload = {"tool_name": "Bash", "tool_input": {"command": "git push origin feat"}}
    else:
        data = json.loads(AGY_HOOKS_JSON.read_text())
        command = data["loom-code"]["PreToolUse"][0]["hooks"][0]["command"]
        payload = {"workspacePaths": [str(tmp_path)], "toolCall": {"args": {"CommandLine": "git push origin feat"}}}
    env = {**os.environ, "XDG_CACHE_HOME": str(tmp_path / "empty"), "PATH": "/bin",
           "PLUGIN_ROOT": str(root)}
    result = subprocess.run(["/bin/sh", "-c", command], input=json.dumps(payload),
                            text=True, capture_output=True, cwd=root, env=env)
    assert result.returncode == 0, result.stderr
    assert "--repair" in json.dumps(json.loads(result.stdout))


@pytest.mark.parametrize("host,event,matcher", [
    ("claude", "SessionStart", "compact|resume"),
    ("claude", "PostToolUse", "Skill|Agent"),
    ("claude", "UserPromptSubmit", ""),
    ("opencode", "PostToolUse", "Skill"),
    ("antigravity", "PreInvocation", ""),
])
def test_stdlib_hooks_keep_context_with_cold_cache(host, event, matcher, tmp_path):
    root = REPO / "loom-code"
    if host == "antigravity":
        data = json.loads(AGY_HOOKS_JSON.read_text())
        command = data["loom-code"][event][0]["command"]
        payload = {"conversationId": "cold", "workspacePaths": [str(tmp_path)],
                   "invocationNum": 0, "initialNumSteps": 1}
    else:
        manifest = HOOKS_JSON if host == "claude" else HOOKS_DIR / "hooks-opencode.json"
        entries = json.loads(manifest.read_text())["hooks"][event]
        (entry,) = [item for item in entries if item.get("matcher", "") == matcher]
        (command,) = _commands([entry])
        payload = {"hook_event_name": event, "tool_name": "Skill"}
    env = {**os.environ, "XDG_CACHE_HOME": str(tmp_path / "empty"), "TMPDIR": str(tmp_path),
           "CLAUDE_PLUGIN_ROOT": str(root), "PLUGIN_ROOT": str(root)}
    result = subprocess.run(["/bin/sh", "-c", command], input=json.dumps(payload),
                            text=True, capture_output=True, cwd=root, env=env, timeout=30)
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    if host == "antigravity":
        assert "Station order:" in output["injectSteps"][0]["ephemeralMessage"]
    else:
        assert "in the language and script" in output["hookSpecificOutput"]["additionalContext"]

    ready_env = _ready_env(tmp_path)
    ready_env.update(CLAUDE_PLUGIN_ROOT=str(root), PLUGIN_ROOT=str(root), TMPDIR=str(tmp_path))
    if host == "antigravity":
        ready_env["PATH"] = os.environ["PATH"]  # session-start also calls awk/sed
        payload["conversationId"] = "ready"
    ready = subprocess.run(["/bin/sh", "-c", command], input=json.dumps(payload),
                           text=True, capture_output=True, cwd=root, env=ready_env, timeout=30)
    assert ready.returncode == 0, ready.stderr
    ready_output = json.loads(ready.stdout)
    if host == "antigravity":
        assert "Station order:" in ready_output["injectSteps"][0]["ephemeralMessage"]
    else:
        assert "in the language and script" in ready_output["hookSpecificOutput"]["additionalContext"]
