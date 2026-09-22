"""Prompt capture hook on both hosts (plan W2-01; Acceptance 1, 2, 9).

Spec decisions 3, 4, 6 and 13 of 2026-09-14-expert-mode-step-selection:
`selection capture --hook` runs only from a UserPromptSubmit payload that
carries the host's prompt reference, binds the newest unconfirmed proposal
whose code the entry-point prompt names, records a user-typed cancel for a
withdraw token, tells the user through `systemMessage`, and never blocks the
prompt. Both host manifests run the same capture, so the outcome is the same.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from loom_checker import selection

SCRIPTS = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS.parent
CHECKER = SCRIPTS / "loom_checker.py"
HOOKS = PLUGIN_ROOT / "hooks"
CHANGE = "2026-09-14-example"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def commit(repo: Path, name: str) -> None:
    (repo / name).write_text(name, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", name)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    commit(repo, "base.txt")
    git(repo, "checkout", "-q", "-b", "feature")
    commit(repo, "work.txt")
    return repo


HOST_ENV = ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT")


@pytest.fixture(autouse=True)
def no_host_session(monkeypatch):
    """Tests never inherit the real Claude Code session running the suite."""
    for name in HOST_ENV:
        monkeypatch.delenv(name, raising=False)


def checker(repo: Path, *args: str, stdin: str = "", env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "selection", *args],
        capture_output=True, text=True, cwd=str(repo), input=stdin,
        env=dict(os.environ, **(env or {})),
    )


def propose(repo: Path, skip: str = "reviewers,adversarial", change: str = CHANGE,
            env: dict | None = None) -> str:
    result = checker(repo, "propose", change, "--origin", "user", "--skip", skip, env=env)
    assert result.returncode == 0, result.stderr
    return [e for e in selection.read_events(repo, change) if e["event"] == "proposal"][-1]["code"]


def claude_payload(prompt: str, **extra) -> dict:
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": prompt,
               "session_id": "sess-1", "prompt_id": "prompt-1"}
    payload.update(extra)
    return payload


def codex_payload(prompt: str) -> dict:
    return {"hook_event_name": "UserPromptSubmit", "prompt": prompt,
            "session_id": "sess-2", "turn_id": "turn-7"}


def capture(repo: Path, payload, env: dict | None = None) -> subprocess.CompletedProcess:
    stdin = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    return checker(repo, "capture", "--hook", stdin=stdin, env=env)


def events(repo: Path, kind: str, change: str = CHANGE) -> list[dict]:
    return [e for e in selection.read_events(repo, change) if e["event"] == kind]


def show(repo: Path, change: str = CHANGE, env: dict | None = None) -> dict:
    result = checker(repo, "show", change, env=env)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def system_message(result: subprocess.CompletedProcess) -> str:
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["systemMessage"]


def manifest_command(name: str) -> str:
    hooks = json.loads((HOOKS / name).read_text(encoding="utf-8"))["hooks"]
    (entry,) = hooks["UserPromptSubmit"]
    (hook,) = entry["hooks"]
    return hook["command"]


def run_manifest(name: str, repo: Path, payload: dict, plugin_root: Path = PLUGIN_ROOT):
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(plugin_root), PLUGIN_ROOT=str(plugin_root))
    return subprocess.run(
        manifest_command(name), shell=True, cwd=str(repo), env=env, text=True,
        capture_output=True, input=json.dumps(payload, ensure_ascii=False),
    )


# --- Acceptance 1 -----------------------------------------------------------

def test_user_prompt_with_code_binds_and_returns_system_message(repo):
    code = propose(repo)
    prompt = f"/loom-code:expert-mode 確認 {code}"
    result = capture(repo, claude_payload(prompt))
    message = system_message(result)

    (confirmation,) = events(repo, "confirmation")
    (proposal,) = events(repo, "proposal")
    assert confirmation["source"] == "user-typed"
    assert confirmation["proposal_id"] == proposal["id"]
    assert confirmation["code"] == code
    assert confirmation["prompt_text"] == prompt
    assert confirmation["prompt_sha256"] == hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    assert confirmation["session_id"] == "sess-1"
    assert confirmation["prompt_ref"] == "prompt-1"
    assert (confirmation["branch"], confirmation["merge_base"]) == (
        proposal["branch"], proposal["merge_base"])
    assert confirmation["at"]

    effective = show(repo)
    assert effective["bound"] is True and effective["source"] == "user-typed"
    assert CHANGE in message
    assert ", ".join(effective["run"]) in message
    assert ", ".join(effective["skip"]) in message


def test_withdraw_token_records_cancel_not_binding(repo):
    code = propose(repo)
    message = system_message(capture(repo, claude_payload(f"/expert-mode cancel {code}")))
    assert events(repo, "confirmation") == []
    (cancel,) = events(repo, "cancel")
    assert cancel["source"] == "user-typed" and cancel["prompt_ref"] == "prompt-1"
    assert show(repo)["bound"] is False
    assert "withdrawn" in message and "full process" in message


def test_only_word_withdraw_token_cancels_a_bound_selection(repo):
    code = propose(repo)
    system_message(capture(repo, claude_payload(f"/expert-mode {code}")))
    assert show(repo)["bound"] is True
    message = system_message(capture(repo, claude_payload("/loom-code:expert-mode 取消")))
    assert show(repo)["bound"] is False
    assert CHANGE in message and "withdrawn" in message


def test_withdraw_word_with_other_words_starts_no_record(repo):
    """`取消 review` is a new selection for the skill, not a withdrawal."""
    code = propose(repo)
    result = capture(repo, claude_payload("/expert-mode 取消 review"))
    assert result.returncode == 0 and result.stdout == ""
    assert events(repo, "cancel") == [] and events(repo, "confirmation") == []
    assert code  # the pending proposal stays pending


# --- Acceptance 2 -----------------------------------------------------------

@pytest.mark.parametrize("payload", [
    {"hook_event_name": "UserPromptSubmit", "prompt": "/expert-mode {code}", "session_id": "s"},
    {"hook_event_name": "PreToolUse", "prompt": "/expert-mode {code}", "session_id": "s",
     "prompt_id": "p"},
    "not json",
])
def test_payload_without_prompt_ref_refused(repo, payload):
    code = propose(repo)
    if isinstance(payload, dict):
        payload = {k: v.format(code=code) for k, v in payload.items()}
    result = capture(repo, payload)
    assert result.returncode == 0
    assert result.stdout == ""
    assert events(repo, "confirmation") == [] and events(repo, "cancel") == []
    assert show(repo)["bound"] is False


def test_capture_refuses_to_run_without_hook_flag(repo):
    code = propose(repo)
    result = checker(repo, "capture", stdin=json.dumps(claude_payload(f"/expert-mode {code}")))
    assert result.returncode == 2
    assert "--hook" in result.stderr
    assert events(repo, "confirmation") == []


@pytest.mark.parametrize("prompt", ["yes", "{code}", "yes {code}", "ok /expert-mode {code}",
                                    "/expert-mode yes", "/expert-mode {code}X"])
def test_plain_yes_binds_nothing(repo, prompt):
    code = propose(repo)
    result = capture(repo, claude_payload(prompt.format(code=code)))
    assert result.returncode == 0 and result.stdout == ""
    assert events(repo, "confirmation") == []
    assert show(repo)["bound"] is False


def test_proposal_from_another_branch_is_not_bound(repo):
    code = propose(repo)
    git(repo, "checkout", "-q", "-b", "other")
    result = capture(repo, claude_payload(f"/expert-mode {code}"))
    assert result.returncode == 0 and result.stdout == ""
    assert events(repo, "confirmation") == []


# --- Session identity (spec decision 18) -----------------------------------

SESSION = "11111111-2222-3333-4444-555555555555"
NESTED = "99999999-8888-7777-6666-555555555555"
ATTENDED = {"CLAUDE_CODE_SESSION_ID": SESSION, "CLAUDE_CODE_SESSION_ATTENDED": "1",
            "CLAUDE_CODE_ENTRYPOINT": "cli"}

# Wrappers a text guard missed; each nested session's hook sees a new
# session_id and re-stamps ATTENDED=0 / ENTRYPOINT=sdk-cli.
NESTED_WRAPPERS = [
    'timeout 60 claude -p "/expert-mode {code}"',
    'script -q /dev/null claude -p "/expert-mode {code}"',
    'npx @anthropic-ai/claude-code -p "/expert-mode {code}"',
]


def test_propose_records_host_session_id(repo):
    propose(repo, env=ATTENDED)
    propose(repo, skip="reviewers")
    first, second = events(repo, "proposal")
    assert first["session_id"] == SESSION
    assert second["session_id"] is None


@pytest.mark.parametrize("wrapper", NESTED_WRAPPERS)
def test_nested_session_prompt_binds_nothing(repo, wrapper):
    code = propose(repo, env=ATTENDED)
    prompt = wrapper.format(code=code).split('"')[1]  # what the nested hook receives
    nested_env = {"CLAUDE_CODE_SESSION_ID": NESTED, "CLAUDE_CODE_SESSION_ATTENDED": "0",
                  "CLAUDE_CODE_ENTRYPOINT": "sdk-cli"}
    result = capture(repo, claude_payload(prompt, session_id=NESTED), env=nested_env)
    assert result.returncode == 0 and result.stdout == ""
    assert events(repo, "confirmation") == []
    assert show(repo, env=ATTENDED)["bound"] is False


def test_unattended_process_binds_nothing_even_with_same_session(repo):
    code = propose(repo, env=ATTENDED)
    result = capture(repo, claude_payload(f"/expert-mode {code}", session_id=SESSION),
                     env=dict(ATTENDED, CLAUDE_CODE_SESSION_ATTENDED="0"))
    assert result.returncode == 0 and result.stdout == ""
    assert events(repo, "confirmation") == []


def test_payload_from_another_session_binds_nothing(repo):
    code = propose(repo, env=ATTENDED)
    result = capture(repo, claude_payload(f"/expert-mode {code}", session_id=NESTED), env=ATTENDED)
    assert result.returncode == 0 and result.stdout == ""
    assert events(repo, "confirmation") == []


def test_same_attended_session_binds_and_show_follows_the_session(repo):
    code = propose(repo, env=ATTENDED)
    system_message(capture(repo, claude_payload(f"/expert-mode {code}", session_id=SESSION),
                           env=ATTENDED))
    (confirmation,) = events(repo, "confirmation")
    assert confirmation["session_id"] == SESSION
    assert show(repo, env=ATTENDED)["bound"] is True
    assert show(repo, env={"CLAUDE_CODE_SESSION_ID": NESTED})["bound"] is False
    assert show(repo)["bound"] is True  # no session variable: prior behaviour


def test_proposal_without_session_keeps_prior_binding(repo):
    """Codex exports no session variable: any payload session binds."""
    code = propose(repo)
    system_message(capture(repo, codex_payload(f"$expert-mode {code}")))
    assert show(repo)["bound"] is True


def test_cancel_still_works_when_unattended(repo):
    code = propose(repo, env=ATTENDED)
    system_message(capture(repo, claude_payload(f"/expert-mode {code}", session_id=SESSION),
                           env=ATTENDED))
    unattended = dict(ATTENDED, CLAUDE_CODE_SESSION_ATTENDED="0")
    message = system_message(capture(repo, claude_payload("/expert-mode 取消", prompt_id="p3"),
                                     env=unattended))
    assert "withdrawn" in message
    assert show(repo, env=ATTENDED)["bound"] is False


def test_non_entry_prompt_runs_no_git_outside_a_repository(tmp_path):
    """The entry-point token is checked before any git subprocess."""
    outside = tmp_path / "not-a-repo"
    outside.mkdir()
    result = subprocess.run(
        [sys.executable, str(CHECKER), "selection", "capture", "--hook"],
        input=json.dumps(claude_payload("hello there")), capture_output=True, text=True,
        cwd=str(outside), env=dict(os.environ, GIT_CEILING_DIRECTORIES=str(tmp_path)))
    assert result.returncode == 0
    assert result.stdout == "" and result.stderr == ""


def assert_no_longer_valid(result: subprocess.CompletedProcess) -> None:
    message = system_message(result)
    assert "no longer valid" in message and "table again" in message


def test_code_of_withdrawn_proposal_says_no_longer_valid(repo):
    code = propose(repo)
    system_message(capture(repo, claude_payload(f"/expert-mode {code}")))
    checker(repo, "cancel", CHANGE)
    assert_no_longer_valid(capture(repo, claude_payload(f"/expert-mode {code}", prompt_id="p2")))
    assert len(events(repo, "confirmation")) == 1
    assert show(repo)["bound"] is False


def test_code_of_cancelled_unconfirmed_proposal_does_not_bind(repo):
    code = propose(repo)
    checker(repo, "cancel", CHANGE)
    assert_no_longer_valid(capture(repo, claude_payload(f"/expert-mode {code}")))
    assert events(repo, "confirmation") == []


def test_code_of_lapsed_proposal_says_no_longer_valid(repo):
    code = propose(repo)
    git(repo, "checkout", "-q", "main")
    commit(repo, "trunk.txt")
    git(repo, "checkout", "-q", "feature")
    git(repo, "rebase", "-q", "main")
    assert_no_longer_valid(capture(repo, claude_payload(f"/expert-mode {code}")))
    assert events(repo, "confirmation") == []


def test_capture_binds_the_newest_unconfirmed_proposal(repo):
    code = propose(repo)
    system_message(capture(repo, claude_payload(f"/expert-mode {code}")))
    checker(repo, "cancel", CHANGE)
    propose(repo)  # same lists -> same code, a new proposal id
    system_message(capture(repo, claude_payload(f"/expert-mode {code}", prompt_id="prompt-2")))
    proposals = events(repo, "proposal")
    first, second = events(repo, "confirmation")
    assert first["proposal_id"] == proposals[0]["id"]
    assert second["proposal_id"] == proposals[1]["id"]
    assert show(repo)["bound"] is True


# --- Acceptance 9 -----------------------------------------------------------

def test_codex_turn_id_payload_binds_same_record(repo):
    code = propose(repo)
    prompt = f"$loom-code:expert-mode {code}"
    result = run_manifest("hooks-codex.json", repo, codex_payload(prompt))
    message = system_message(result)
    (codex_confirmation,) = events(repo, "confirmation")
    assert codex_confirmation["prompt_ref"] == "turn-7"
    assert codex_confirmation["source"] == "user-typed"
    codex_view = show(repo)

    # The same prompt through the Claude Code manifest, on a fresh proposal.
    checker(repo, "cancel", CHANGE)
    propose(repo)
    message_claude = system_message(
        run_manifest("hooks.json", repo, claude_payload(prompt, prompt_id="p9")))
    claude_confirmation = events(repo, "confirmation")[-1]
    assert set(claude_confirmation) == set(codex_confirmation)
    assert claude_confirmation["prompt_ref"] == "p9"
    claude_view = show(repo)
    for key in ("bound", "run", "skip", "code", "source"):
        assert claude_view[key] == codex_view[key], key
    assert message_claude == message


@pytest.mark.parametrize("token", ["$expert-mode", "/expert-mode", "$loom-code:expert-mode",
                                   "/loom-code:expert-mode"])
def test_bare_expert_mode_token_matches(repo, token):
    code = propose(repo)
    system_message(capture(repo, codex_payload(f"{token} {code.lower()}")))
    assert show(repo)["bound"] is True


def test_codex_hook_never_blocks_when_checker_is_missing(repo, tmp_path):
    code = propose(repo)
    result = run_manifest("hooks-codex.json", repo, codex_payload(f"$expert-mode {code}"),
                          plugin_root=tmp_path / "gone")
    assert result.returncode == 0
    assert events(repo, "confirmation") == []
