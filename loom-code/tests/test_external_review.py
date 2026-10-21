from __future__ import annotations

import errno
import json
import re
import subprocess

import external_review as review
import pytest
from prose_pin import affirms


def consent(executor="codex", scope="/repo", model=None, effort="high"):
    model = model or {"codex": "gpt-6.1-sol", "claude": "sonnet",
                      "agy": "gemini-2.5-pro"}[executor]
    return {
        "approved": True, "executor": executor, "review_root": scope,
        "authorization_source": {
            "kind": "direct-user-request", "quote": f"Use {executor} to review this change",
            "target": "this change", "selected_executor": executor,
        },
        "model": model, "effort": effort,
        "disclosures": {"cost": True, "vendor_egress": True,
                        "local_execution": True,
                        "filesystem_access_outside_root": True,
                        "filesystem_write_not_guaranteed": True},
    }


def completed(argv, stdout, stderr="", rc=0):
    return subprocess.CompletedProcess(argv, rc, stdout, stderr)


@pytest.mark.parametrize("record", [None, {}, consent(scope="/other"),
    {**consent(), "approved": False},
    {**consent(), "disclosures": {"cost": True}}])
def test_consent_blocks_all_subprocesses(record):
    calls = []

    def runner(*args, **kwargs):
        calls.append(args)
        raise AssertionError("external process started")

    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                            "review", record, runner=runner)
    assert result["status"] == "failed"
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


@pytest.mark.parametrize("source", [None, {},
    {"kind": "direct-user-request", "quote": "", "target": "this change"},
    {"kind": "direct-user-request", "quote": "review this", "target": ""},
    {"kind": "direct-user-request", "quote": "review this change", "target": "this change"},
    {"kind": "direct-user-request", "quote": "Use Codex to review this change", "target": "this change"},
    {"kind": "direct-user-request", "quote": "Use Claude to review this change", "target": "this change", "selected_executor": "codex"},
    {"kind": "suggestion", "quote": "Use codex", "target": "this change"},
    {"kind": "accepted-selection", "selection": "", "target": "this change"},
])
def test_authorization_source_requires_complete_owner_record(source):
    record = consent()
    if source is None:
        del record["authorization_source"]
    else:
        record["authorization_source"] = source
    calls = []

    def runner(*args, **kwargs):
        calls.append(args)
        raise AssertionError("outside process started")

    result = review.discover("codex", "/repo", record, runner=runner)
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_accepted_selection_source_allows_discovery():
    record = consent()
    record["authorization_source"] = {
        "kind": "accepted-selection", "selection": "codex", "target": "this change",
    }
    result = review.discover(
        "codex", "/repo", record,
        runner=lambda argv, **kwargs: completed(
            argv, json.dumps({"id": 2, "result": {"data": []}})),
    )
    assert result["status"] == "completed"


def test_accepted_selection_source_allows_execution():
    record = consent()
    record["authorization_source"] = {
        "kind": "accepted-selection", "selection": "codex", "target": "this change",
    }
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv[:2] == ["codex", "app-server"]:
            return completed(argv, json.dumps({"id": 2, "result": {
                "data": [{"id": "gpt-6.1-sol"}]}}))
        return completed(argv, "ok" if len(calls) == 2 else "review verdict",
                         "model: gpt-6.1-sol\nreasoning effort: high\n")

    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                            "review", record, runner=runner)
    assert result["status"] == "completed"
    assert len(calls) == 3


@pytest.mark.parametrize("quote, owner_selection", [
    ("Use Codex? Actually use Claude to review this change.", "claude"),
    ("Please use Claude instead of Codex to review this change.", "claude"),
    ("Use Codex to review this change. Actually, cancel all outside reviews.", None),
    ("Maybe Codex can review this change.", None),
])
def test_owner_excludes_codex_before_discovery_or_execution(quote, owner_selection):
    record = consent("codex")
    record["authorization_source"]["quote"] = quote
    if owner_selection is None:
        record["approved"] = False
    else:
        record["authorization_source"]["selected_executor"] = owner_selection
    no_spawn = lambda *a, **k: pytest.fail("spawned")
    discovered = review.discover("codex", "/repo", record, runner=no_spawn)
    executed = review.execute("codex", record["model"], "high", "openai",
                              "/repo", "review", record, runner=no_spawn)
    assert discovered["reason"] == "consent-missing-or-stale"
    assert executed["reason"] == "consent-missing-or-stale"


@pytest.mark.parametrize("executor, quote", [
    ("codex", "Use Codex to review this change"),
    ("claude", "請用 Claude 審查這個變更"),
    ("agy", "Agy を使ってこの変更をレビューして"),
    ("claude", "Can you use Claude to review this change?"),
    ("codex", "I want Codex to review this change"),
    ("codex", "Use Claude? No, use Codex to review this change."),
    ("codex", "Please review with Codex, not Claude."),
    ("codex", "不要用 Claude，改用 Codex 審查這個變更"),
    ("codex", "Can you use Codex to review this change?"),
    ("codex", "Use Claude? Actually use Codex to review this change."),
    ("codex", "Do not use Codex. Actually, please use Codex to review this change."),
    ("codex", "Do not use any external coding agent. Actually, use Codex to review this change."),
    ("codex", "Use Codex to review this change, no need to ask again."),
    ("codex", "Use Codex to review this change. No need to use Claude."),
    ("codex", "Use Codex to review this change. Wait for the result."),
])
def test_owner_selected_direct_request_remains_valid(executor, quote, tmp_path):
    scope = str(tmp_path)
    record = consent(executor, scope)
    record["authorization_source"]["quote"] = quote
    if executor == "claude":
        runner = lambda *a, **k: pytest.fail("Claude discovery must be local")
    else:
        runner = lambda argv, **kwargs: completed(
            argv, json.dumps({"id": 2, "result": {"data": []}})
            if executor == "codex" else "[]")
    assert review.discover(executor, scope, record, runner=runner)["status"] == "completed"


@pytest.mark.parametrize("quote", [
    "Do not use Codex. Actually, please use Codex to review this change.",
    "Do not use any external coding agent. Actually, use Codex to review this change.",
    "Use Codex to review this change, no need to ask again.",
    "Use Codex to review this change. No need to use Claude.",
    "Use Codex to review this change. Wait for the result.",
])
def test_final_reselection_allows_discovery(quote):
    record = consent("codex")
    record["authorization_source"]["quote"] = quote
    result = review.discover(
        "codex", "/repo", record,
        runner=lambda argv, **kwargs: completed(
            argv, json.dumps({"id": 2, "result": {"data": []}})),
    )
    assert result["status"] == "completed"


@pytest.mark.parametrize("quote", [
    "Do not use Codex. Actually, can you use Codex to review this change?",
    "Actually, don't use Claude; use Codex to review this change.",
    "Actually, use the Codex CLI to review this change.",
])
def test_owner_final_codex_choice_allows_discovery_and_execution(quote):
    record = consent("codex")
    record["authorization_source"]["quote"] = quote
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv[:2] == ["codex", "app-server"]:
            return completed(argv, json.dumps({"id": 2, "result": {
                "data": [{"id": "gpt-6.1-sol"}]}}))
        return completed(argv, "ok" if len(calls) == 3 else "review verdict",
                         "model: gpt-6.1-sol\nreasoning effort: high\n")

    assert review.discover("codex", "/repo", record, runner=runner)["status"] == "completed"
    assert review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                          "review", record, runner=runner)["status"] == "completed"
    assert len(calls) == 4


def test_direct_request_selected_executor_must_match_dispatch():
    record = consent("claude")
    record["authorization_source"]["selected_executor"] = "codex"
    no_spawn = lambda *a, **k: pytest.fail("spawned")
    assert review.discover("claude", "/repo", record, runner=no_spawn)["reason"] == "consent-missing-or-stale"
    assert review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                          "review", record, runner=no_spawn)["reason"] == "consent-missing-or-stale"


def test_missing_host_read_disclosure_blocks_discovery():
    record = consent()
    del record["disclosures"]["filesystem_access_outside_root"]
    result = review.discover("codex", "/repo", record,
                             runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_missing_host_write_disclosure_blocks_discovery():
    record = consent()
    del record["disclosures"]["filesystem_write_not_guaranteed"]
    result = review.discover("codex", "/repo", record,
                             runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_old_readable_scope_field_is_not_treated_as_confinement_consent():
    record = consent()
    record["readable_scope"] = record.pop("review_root")
    result = review.discover("codex", "/repo", record,
                             runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_codex_discovery_probe_and_review_observe_exact_profile():
    calls = []
    model_list = {"id": 2, "result": {"data": [{"id": "gpt-6.1-sol"}]}}
    header = "model: gpt-6.1-sol\nreasoning effort: high\n"

    def runner(argv, **kwargs):
        calls.append((argv, kwargs))
        if argv[:2] == ["codex", "app-server"]:
            assert '"method": "model/list"' in kwargs["input"]
            return completed(argv, json.dumps(model_list))
        assert argv[:2] == ["codex", "exec"]
        assert "--sandbox" in argv and argv[argv.index("--sandbox") + 1] == "read-only"
        assert "--ephemeral" in argv
        assert "-m" in argv and argv[argv.index("-m") + 1] == "gpt-6.1-sol"
        assert "model_reasoning_effort=high" in argv
        return completed(argv, "ok" if len(calls) == 2 else "review verdict", header)

    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                            "review", consent(), runner=runner)
    assert result["status"] == "completed"
    assert result["evidence_level"] == "observed-model-and-effort"
    assert "outside-root reads" in result["filesystem_boundary"]
    assert result["review_output"] == "review verdict"
    assert len(calls) == 3
    assert calls[1][1]["timeout"] < calls[2][1]["timeout"]


def test_codex_app_server_initialize_has_required_client_info():
    def runner(argv, **kwargs):
        requests = [json.loads(line) for line in kwargs["input"].splitlines()]
        assert requests[0]["method"] == "initialize"
        assert requests[0]["params"]["clientInfo"] == {
            "name": "loom-external-review", "title": "Loom External Review",
            "version": "1",
        }
        return completed(argv, json.dumps({"id": 2, "result": {"data": []}}))

    result = review.discover("codex", "/repo", consent(), runner=runner)
    assert result["status"] == "completed"


def test_codex_stdout_profile_claim_cannot_override_stderr_header():
    def runner(argv, **kwargs):
        if argv[:2] == ["codex", "app-server"]:
            return completed(argv, json.dumps({"id": 2, "result": {"data": [{"id": "gpt-6.1-sol"}]}}))
        return completed(argv, "model: gpt-6.1-sol\nreasoning effort: high\nok",
                         "model: other-model\nreasoning effort: low\n")

    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                            "review", consent(), runner=runner)
    assert result["status"] == "failed"
    assert result["review_output"] is None


def test_claude_json_null_is_structured_failure():
    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            "review", consent("claude"),
                            runner=lambda argv, **kwargs: completed(argv, "null"))
    assert result["status"] == "failed"
    assert "execution-error" in result["reason"]
    assert result["next_action"] == "Inspect Claude CLI diagnostics privately, then request a new authorized review."


def test_codex_discovery_ignores_non_object_json_lines():
    result = review.discover("codex", "/repo", consent(),
                             runner=lambda argv, **kwargs: completed(argv, "null\n[]\n"))
    assert result["status"] == "failed"
    assert result["reason"].startswith("discovery-error:")


@pytest.mark.parametrize("error_type, expected", [
    (OSError, "unknown error"),
    (FileNotFoundError, "executor-not-installed"),
])
def test_discovery_and_execution_exceptions_do_not_echo_private_text(
        error_type, expected, tmp_path):
    secret = "PRIVATE_DIAGNOSTIC_DO_NOT_ECHO"
    scope = str(tmp_path)

    def runner(*args, **kwargs):
        raise error_type(secret)

    discovered = review.discover("codex", scope, consent(scope=scope), runner=runner)
    executed = review.execute("claude", "sonnet", "high", "anthropic", scope,
                              "review", consent("claude", scope), runner=runner)
    assert discovered["reason"] == f"discovery-error: {expected}"
    assert executed["reason"] == f"execution-error: {expected}"
    assert executed["next_action"]
    assert secret not in json.dumps(discovered)
    assert secret not in json.dumps(executed)


@pytest.mark.parametrize("executor", ["codex", "agy"])
def test_discovery_missing_review_root_reports_root_without_leaking_path(
        executor, tmp_path):
    scope = str(tmp_path / "PRIVATE_MISSING_REVIEW_ROOT")
    secret = "PRIVATE_DIAGNOSTIC_DO_NOT_ECHO"

    def runner(argv, **kwargs):
        assert kwargs["cwd"] == scope
        raise FileNotFoundError(errno.ENOENT, secret, scope)

    result = review.discover(executor, scope, consent(executor, scope), runner=runner)
    assert result["status"] == "failed"
    assert result["reason"] == "discovery-error: review-root-not-found"
    assert result["candidates"] == []
    assert scope not in json.dumps(result)
    assert secret not in json.dumps(result)


@pytest.mark.parametrize("executor", ["codex", "agy"])
def test_missing_root_is_rejected_before_real_discovery_spawn(executor, tmp_path,
                                                              monkeypatch):
    scope = str(tmp_path / "PRIVATE_MISSING_REVIEW_ROOT")
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: pytest.fail("spawned"))
    result = review.discover(executor, scope, consent(executor, scope))
    assert result["reason"] == "discovery-error: review-root-not-found"
    assert result["status"] == "failed"
    assert scope not in json.dumps(result)


@pytest.mark.parametrize("executor, family", [
    ("codex", "openai"), ("agy", "google"), ("claude", "anthropic"),
])
def test_missing_root_is_rejected_before_real_execution_spawn(
        executor, family, tmp_path, monkeypatch):
    scope = str(tmp_path / "PRIVATE_MISSING_REVIEW_ROOT")
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: pytest.fail("spawned"))
    record = consent(executor, scope)
    result = review.execute(executor, record["model"], "high", family, scope,
                            "review", record)
    assert result["reason"] == "execution-error: review-root-not-found"
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert scope not in json.dumps(result)


@pytest.mark.parametrize("executor", ["codex", "agy"])
@pytest.mark.parametrize("filename", ["executable", "unspecified"])
def test_discovery_rechecks_root_after_enoent(executor, filename, tmp_path):
    scope_dir = tmp_path / "review-root"
    scope_dir.mkdir()
    scope = str(scope_dir)

    def runner(argv, **kwargs):
        scope_dir.rmdir()
        raise FileNotFoundError(errno.ENOENT, "private diagnostic",
                                argv[0] if filename == "executable" else None)

    result = review.discover(executor, scope, consent(executor, scope), runner=runner)
    assert result["reason"] == "discovery-error: review-root-not-found"
    assert result["status"] == "failed"
    assert "private diagnostic" not in json.dumps(result)


@pytest.mark.parametrize("executor, family", [
    ("codex", "openai"), ("agy", "google"), ("claude", "anthropic"),
])
@pytest.mark.parametrize("filename", ["executable", "unspecified"])
def test_execution_rechecks_root_after_enoent(executor, family, filename, tmp_path):
    scope_dir = tmp_path / "review-root"
    scope_dir.mkdir()
    scope = str(scope_dir)

    def runner(argv, **kwargs):
        scope_dir.rmdir()
        raise FileNotFoundError(errno.ENOENT, "private diagnostic",
                                argv[0] if filename == "executable" else None)

    record = consent(executor, scope)
    result = review.execute(executor, record["model"], "high", family, scope,
                            "review", record, runner=runner)
    assert result["reason"] == "execution-error: review-root-not-found"
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert "private diagnostic" not in json.dumps(result)


def test_claude_discovery_returns_documented_aliases_for_existing_root(tmp_path):
    scope = str(tmp_path)
    result = review.discover("claude", scope, consent("claude", scope),
                             runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["status"] == "completed"
    assert result["reason"] is None
    assert result["candidates"] == ["opus", "sonnet", "haiku"]


def test_execution_missing_review_root_reports_root_without_completing(tmp_path):
    scope = str(tmp_path / "PRIVATE_MISSING_REVIEW_ROOT")
    secret = "PRIVATE_DIAGNOSTIC_DO_NOT_ECHO"

    def runner(argv, **kwargs):
        assert kwargs["cwd"] == scope
        raise FileNotFoundError(errno.ENOENT, secret, scope)

    result = review.execute("claude", "sonnet", "high", "anthropic", scope,
                            "review", consent("claude", scope), runner=runner)
    assert result["status"] == "failed"
    assert result["reason"] == "execution-error: review-root-not-found"
    assert result["review_output"] is None
    assert result["evidence_level"] == "none"
    assert scope not in json.dumps(result)
    assert secret not in json.dumps(result)


def test_valid_review_root_with_missing_executable_keeps_cli_reason(tmp_path):
    scope = str(tmp_path)

    def runner(argv, **kwargs):
        assert kwargs["cwd"] == scope
        raise FileNotFoundError(errno.ENOENT, "PRIVATE_DIAGNOSTIC_DO_NOT_ECHO", argv[0])

    discovered = review.discover("codex", scope, consent(scope=scope), runner=runner)
    executed = review.execute("claude", "sonnet", "high", "anthropic", scope,
                              "review", consent("claude", scope), runner=runner)
    assert discovered["status"] == executed["status"] == "failed"
    assert discovered["reason"] == "discovery-error: executor-not-installed"
    assert executed["reason"] == "execution-error: executor-not-installed"
    assert executed["review_output"] is None
    assert "PRIVATE_DIAGNOSTIC_DO_NOT_ECHO" not in json.dumps((discovered, executed))


def test_discovery_json_rpc_error_does_not_echo_private_text():
    secret = "PRIVATE_JSON_RPC_ERROR_DO_NOT_ECHO"
    response = {"id": 2, "error": {"code": -32000, "message": secret}}
    result = review.discover("codex", "/repo", consent(),
                             runner=lambda argv, **kwargs: completed(argv, json.dumps(response)))
    assert result["reason"] == "discovery-error: codex model/list error: unknown error"
    assert secret not in json.dumps(result)


def test_claude_alias_uses_explicit_flags_and_reports_accepted_level():
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        assert argv[:2] == ["claude", "-p"]
        assert argv[argv.index("--permission-mode") + 1] == "plan"
        assert argv[argv.index("--tools") + 1] == "Read,Glob,Grep"
        assert argv[argv.index("--permission-prompts") + 1] == "none"
        assert argv[argv.index("--model") + 1] == "sonnet"
        assert argv[argv.index("--effort") + 1] == "high"
        output = {"result": "ok" if len(calls) == 1 else "verdict: PASS",
                  "modelUsage": {"claude-sonnet-4-5": {"inputTokens": 2}}}
        return completed(argv, json.dumps(output))

    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            "review", consent("claude"), runner=runner)
    assert result["status"] == "completed"
    assert result["evidence_level"] == "accepted-explicit-settings"
    assert result["observed_model"] == "claude-sonnet-4-5"
    assert result["observed_effort"] is None
    assert json.loads(result["probe"]["stdout"])["result"] == "ok"
    assert len(calls) == 2


@pytest.mark.parametrize("http_status, message, expected", [
    (429, "You've hit your session limit · resets 4am (Asia/Taipei)",
     "Claude session limit (HTTP 429)"),
    (503, "Service unavailable", "Claude API HTTP 503"),
])
def test_claude_structured_api_error_reports_bounded_reason_without_review_material(
        http_status, message, expected):
    secret = "private review prompt and verdict: PASS"
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        failure = {"type": "result", "is_error": True,
                   "api_error_status": http_status, "terminal_reason": "api_error",
                   "result": message}
        return completed(argv, json.dumps(failure), rc=1)

    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            secret, consent("claude"), runner=runner)
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert result["reason"] == f"probe-exit-1: {expected}"
    action = ("Wait for the Claude session limit to reset, then request a new authorized review."
              if http_status == 429 else
              "Check Claude API status locally, then request a new authorized review.")
    assert result["next_action"] == action
    assert result["probe"] == {"returncode": 1, "timeout_seconds": 45}
    assert secret not in json.dumps(result)
    assert len(calls) == 1


def test_nonzero_untrusted_stdout_does_not_become_failure_reason():
    prompt = "secret prompt"
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if len(calls) == 1:
            return completed(argv, json.dumps({"result": "ok " + prompt, "modelUsage":
                                               {"claude-sonnet-4-5": {}}}))
        return completed(argv, json.dumps({"type": "assistant", "is_error": True,
                                           "terminal_reason": "api_error",
                                           "api_error_status": 429,
                                           "result": "session limit " + prompt}),
                         prompt, rc=1)

    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            prompt, consent("claude"), runner=runner)
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert result["reason"] == "review-exit-1: unknown error"
    assert result["next_action"] == "Run claude doctor locally; inspect CLI diagnostics privately, then request a new authorized review."
    assert result["diagnostic"] == {"stage": "review", "exit_code": 1,
                                    "stdout_present": True, "stderr_present": True,
                                    "stdout_json_parseable": True}
    assert prompt not in json.dumps(result)


@pytest.mark.parametrize("stderr, expected", [
    ("Error: unsupported effort high", "unsupported effort"),
    ("Error: authentication required", "authentication error"),
    ("Error: You've hit your session limit · resets 4am", "Claude session limit"),
    ("unrecognized diagnostic", "unknown error"),
])
def test_claude_empty_stdout_classifies_only_known_stderr(stderr, expected):
    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            "review", consent("claude"),
                            runner=lambda argv, **kwargs: completed(argv, "", stderr, rc=2))
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert result["reason"] == f"probe-exit-2: {expected}"
    assert result["next_action"]
    assert stderr not in json.dumps(result)


def test_nonzero_empty_diagnostic_is_explicitly_unknown():
    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            "review", consent("claude"),
                            runner=lambda argv, **kwargs: completed(argv, "", rc=2))
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert result["reason"] == "probe-exit-2: unknown error"
    assert result["next_action"] == "Run claude doctor locally; inspect CLI diagnostics privately, then request a new authorized review."
    assert result["diagnostic"] == {"stage": "probe", "exit_code": 2,
                                    "stdout_present": False, "stderr_present": False,
                                    "stdout_json_parseable": False}
    assert result["probe"] == {"returncode": 2, "timeout_seconds": 45}


def test_agy_model_list_and_explicit_pair():
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv == ["agy", "models"]:
            return completed(argv, "gemini-2.5-pro\nclaude-sonnet-4-5\n")
        assert argv[:5] == ["agy", "--add-dir", "/repo", "-p",
                            review.PROBE_PROMPT if len(calls) == 2 else "review"]
        assert kwargs["input"] == ""
        assert kwargs["cwd"] == "/repo"
        assert "--sandbox" in argv
        assert "--disable-slash-commands" in argv
        assert argv[argv.index("--mode") + 1] == "plan"
        assert argv[argv.index("--effort") + 1] == "high"
        return completed(argv, "ok" if len(calls) == 2 else "verdict: PASS")

    result = review.execute("agy", "gemini-2.5-pro", "high", "google", "/repo",
                            "review", consent("agy"), runner=runner)
    assert result["status"] == "completed"
    assert result["evidence_level"] == "accepted-explicit-settings"
    assert result["observed_model"] is None
    assert len(calls) == 3


def test_agy_nonzero_stderr_reason_stays_bounded():
    def runner(argv, **kwargs):
        if argv == ["agy", "models"]:
            return completed(argv, "gemini-2.5-pro\n")
        return completed(argv, "", "Error: unsupported effort high " + "x" * 301, rc=2)

    result = review.execute("agy", "gemini-2.5-pro", "high", "google", "/repo",
                            "review", consent("agy"), runner=runner)
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert result["reason"] == "probe-exit-2: unsupported effort"
    assert "x" * 301 not in json.dumps(result)


def test_agy_relative_review_root_stops_before_discovery():
    result = review.execute("agy", "gemini-2.5-pro", "high", "google", "repo",
                            "review", consent("agy", scope="repo"),
                            runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "scope-must-be-absolute"


def test_agy_cross_family_selection_is_refused_before_probe():
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        return completed(argv, "gemini-2.5-pro\n")

    result = review.execute("agy", "gemini-2.5-pro", "high", "anthropic", "/repo",
                            "review", consent("agy"), runner=runner)
    assert result["reason"] == "selected-provider-family-mismatch-or-unknown"
    assert calls == []


def test_unaccepted_pair_blocks_discovery():
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        raise AssertionError("must not run")

    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                            "review", consent(model="gpt-6-sol"), runner=runner)
    assert result["reason"] == "consent-missing-or-stale"
    assert calls == []


def test_consented_discovery_then_bounded_pair_selection():
    calls = []
    record = consent()
    record.pop("model")
    record.pop("effort")
    record.update(selection_authorized=True, family="openai", allowed_efforts=["high"])

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv[:2] == ["codex", "app-server"]:
            return completed(argv, json.dumps({"id": 2, "result": {"data": [{"id": "gpt-6.1-sol"}]}}))
        return completed(argv, "ok", "model: gpt-6.1-sol\nreasoning effort: high\n")

    listed = review.discover("codex", "/repo", record, runner=runner)
    assert listed["status"] == "completed"
    assert listed["candidates"] == ["gpt-6.1-sol"]
    executed = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                              "review", record, runner=runner)
    assert executed["status"] == "completed"
    assert len(calls) == 4


def test_bounded_selection_rejects_effort_outside_consent():
    record = consent()
    record.pop("model")
    record.pop("effort")
    record.update(selection_authorized=True, family="openai", allowed_efforts=["medium"])
    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                            "review", record, runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_agy_consent_can_select_family_after_consented_discovery():
    record = consent("agy")
    record.pop("model")
    record.pop("effort")
    record.update(selection_authorized=True,
                  allowed_families=["anthropic", "google"],
                  allowed_efforts=["high"])
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv == ["agy", "models"]:
            return completed(argv, "gemini-2.5-pro\nclaude-sonnet-4-5\n")
        return completed(argv, "ok")

    assert review.discover("agy", "/repo", record, runner=runner)["status"] == "completed"
    result = review.execute("agy", "claude-sonnet-4-5", "high", "anthropic",
                            "/repo", "review", record, runner=runner)
    assert result["status"] == "completed"
    assert len(calls) == 4


@pytest.mark.parametrize("families", [[], ["unknown"], ["google", "unknown"],
                                      ["Google"], "google"])
def test_unknown_or_empty_allowed_families_fail_before_subprocess(families):
    record = consent("agy")
    record.pop("model")
    record.pop("effort")
    record.update(selection_authorized=True, allowed_families=families,
                  allowed_efforts=["high"])
    result = review.execute("agy", "gemini-2.5-pro", "high", "google", "/repo",
                            "review", record,
                            runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_selected_family_outside_consented_set_fails_before_subprocess():
    record = consent("agy")
    record.pop("model")
    record.pop("effort")
    record.update(selection_authorized=True, allowed_families=["anthropic"],
                  allowed_efforts=["high"])
    result = review.execute("agy", "gemini-2.5-pro", "high", "google", "/repo",
                            "review", record,
                            runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_exact_pair_does_not_override_an_invalid_allowed_families_list():
    record = consent("agy")
    record["allowed_families"] = ["unknown"]
    result = review.execute("agy", "gemini-2.5-pro", "high", "google", "/repo",
                            "review", record,
                            runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_exact_pair_does_not_override_a_conflicting_family_bound():
    record = consent()
    record["family"] = "google"
    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo",
                            "review", record,
                            runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_allowed_families_cannot_override_a_conflicting_single_family():
    record = consent("agy")
    record.pop("model")
    record.pop("effort")
    record.update(selection_authorized=True, family="anthropic",
                  allowed_families=["google"], allowed_efforts=["high"])
    result = review.execute("agy", "gemini-2.5-pro", "high", "google", "/repo",
                            "review", record,
                            runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_malformed_single_family_fails_before_discovery():
    record = consent()
    record["family"] = []
    result = review.discover("codex", "/repo", record,
                             runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_invalid_allowed_families_blocks_network_discovery():
    record = consent("agy")
    record["allowed_families"] = []
    result = review.discover("agy", "/repo", record,
                             runner=lambda *a, **k: pytest.fail("spawned"))
    assert result["reason"] == "consent-missing-or-stale"


def test_claude_model_usage_family_mismatch_rejects_review():
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        return completed(argv, json.dumps({"result": "ok", "modelUsage": {"gpt-6": {}}}))

    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            "review", consent("claude"), runner=runner)
    assert result["status"] == "failed"
    assert "family mismatch" in result["reason"]
    assert len(calls) == 1


def test_claude_explicit_id_must_be_observed_exactly():
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        return completed(argv, json.dumps({"result": "ok", "modelUsage": {"claude-other": {}}}))

    result = review.execute("claude", "claude-sonnet-4-5", "high", "anthropic", "/repo",
                            "review", consent("claude", model="claude-sonnet-4-5"), runner=runner)
    assert result["status"] == "failed"
    assert "model mismatch" in result["reason"]
    assert len(calls) == 1


@pytest.mark.parametrize("case", ["missing", "mismatch", "timeout", "rejected", "header-mismatch"])
def test_failed_selection_or_execution_never_falls_back(case):
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv[:2] == ["codex", "app-server"]:
            models = [] if case == "missing" else [{"id": "gpt-6.1-sol"}]
            return completed(argv, json.dumps({"id": 2, "result": {"data": models}}))
        if case == "timeout":
            raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
        if case == "rejected":
            return completed(argv, "", "unsupported effort high PRIVATE_CODEX_ERROR", 2)
        model = "other-model" if case == "header-mismatch" else "gpt-6.1-sol"
        return completed(argv, "ok", f"model: {model}\nreasoning effort: high\n")

    family = "google" if case == "mismatch" else "openai"
    result = review.execute("codex", "gpt-6.1-sol", "high", family, "/repo",
                            "review", consent(), runner=runner)
    assert result["status"] == "failed"
    assert result["review_output"] is None
    if case == "rejected":
        assert result["reason"] == "probe-exit-2: unsupported effort"
        assert "PRIVATE_CODEX_ERROR" not in json.dumps(result)
    assert len(calls) <= 2


_FAKE_CODEX = """#!{python}
import json, os, select, sys, time
open({pidfile!r}, "w").write(str(os.getpid()))
for _ in range(3):
    sys.stdin.readline()
if {mode!r} == "hang":
    time.sleep(60)
ready, _, _ = select.select([sys.stdin], [], [], 0.3)
if ready and sys.stdin.readline() == "":
    sys.exit(0)  # real app-server: stdin EOF before model/list answer
print(json.dumps({{"jsonrpc": "2.0", "id": 1, "result": {{}}}}))
print(json.dumps({{"jsonrpc": "2.0", "method": "note", "params": {{}}}}))
print("not json")
print(json.dumps({{"id": 2, "result": {{"data": [{{"id": "gpt-a"}}, {{"id": "gpt-b"}}]}}}}), flush=True)
time.sleep(60)
"""


def _fake_codex(tmp_path, monkeypatch, mode):
    import sys
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pidfile = tmp_path / "pid"
    script = bin_dir / "codex"
    script.write_text(_FAKE_CODEX.format(python=sys.executable, pidfile=str(pidfile), mode=mode))
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    return pidfile


def _assert_reaped(pidfile):
    import os
    pid = int(pidfile.read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


def test_codex_discovery_keeps_stdin_open_for_model_list(tmp_path, monkeypatch):
    pidfile = _fake_codex(tmp_path, monkeypatch, "answer")
    result = review.discover("codex", str(tmp_path), consent(scope=str(tmp_path)))
    assert result["candidates"] == ["gpt-a", "gpt-b"], result
    _assert_reaped(pidfile)


def test_codex_discovery_times_out_when_app_server_never_answers(tmp_path, monkeypatch):
    pidfile = _fake_codex(tmp_path, monkeypatch, "hang")
    monkeypatch.setattr(review, "CODEX_DISCOVERY_TIMEOUT", 1)
    result = review.discover("codex", str(tmp_path), consent(scope=str(tmp_path)))
    assert result["reason"] == "discovery-timeout: 1s"
    _assert_reaped(pidfile)


_FAKE_CLI = """#!{python}
import json, os, subprocess, sys, time
mode = {mode!r}
if mode == "codex-exit":
    sys.exit(3)
if mode == "codex-exit0":
    sys.exit(0)
if mode == "codex-exit-orphan":
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    open({pidfile!r}, "w").write(str(child.pid))
    sys.exit(3)
text = sys.stdin.read()
if mode == "claude" and "single word ok" in text:
    print(json.dumps({{"result": "ok", "modelUsage": {{"claude-sonnet-4-5": {{}}}}}}))
    sys.exit(0)
print("gemini-2.5-pro", flush=True)
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(5)"])
open({pidfile!r}, "w").write(str(child.pid))
if mode != "exit-early":
    time.sleep(5)
"""


def _fake_cli(tmp_path, monkeypatch, name, mode):
    import sys
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pidfile = tmp_path / "pid"
    script = bin_dir / name
    script.write_text(_FAKE_CLI.format(python=sys.executable, pidfile=str(pidfile), mode=mode))
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    return pidfile


def _assert_descendant_gone(pidfile):
    import os
    import time
    pid = int(pidfile.read_text())
    for _ in range(50):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.05)
    pytest.fail("descendant still running")


def test_agy_discovery_times_out_when_descendant_holds_stdout(tmp_path, monkeypatch):
    import time
    pidfile = _fake_cli(tmp_path, monkeypatch, "agy", "hang")
    monkeypatch.setattr(review, "AGY_DISCOVERY_TIMEOUT", 1)
    start = time.monotonic()
    result = review.discover("agy", str(tmp_path), consent("agy", scope=str(tmp_path)))
    assert result["reason"] == "discovery-timeout: 1s"
    assert time.monotonic() - start < 4
    _assert_descendant_gone(pidfile)


def test_agy_discovery_exit_with_lingering_descendant_is_not_timeout(tmp_path, monkeypatch):
    import time
    pidfile = _fake_cli(tmp_path, monkeypatch, "agy", "exit-early")
    start = time.monotonic()
    result = review.discover("agy", str(tmp_path), consent("agy", scope=str(tmp_path)))
    assert result["candidates"] == ["gemini-2.5-pro"], result
    assert time.monotonic() - start < 4
    _assert_descendant_gone(pidfile)


def test_review_stage_times_out_when_descendant_holds_stdout(tmp_path, monkeypatch):
    import time
    pidfile = _fake_cli(tmp_path, monkeypatch, "claude", "claude")
    start = time.monotonic()
    result = review.execute("claude", "sonnet", "high", "anthropic", str(tmp_path),
                            "review", consent("claude", scope=str(tmp_path)),
                            probe_timeout=1, review_timeout=2)
    assert result["reason"] == "execution-timeout: 2s", result
    assert time.monotonic() - start < 4.5
    _assert_descendant_gone(pidfile)


@pytest.mark.parametrize("mode,code", [("codex-exit", 3), ("codex-exit0", 0),
                                       ("codex-exit-orphan", 3)])
def test_codex_exit_before_answer_reports_exit_code(tmp_path, monkeypatch, mode, code):
    import time
    pidfile = _fake_cli(tmp_path, monkeypatch, "codex", mode)
    start = time.monotonic()
    result = review.discover("codex", str(tmp_path), consent(scope=str(tmp_path)))
    assert result["reason"] == f"discovery-error: codex model/list failed: exit {code}"
    executed = review.execute("codex", "gpt-a", "high", "openai", str(tmp_path), "review",
                              consent(scope=str(tmp_path), model="gpt-a"))
    assert executed["reason"] == f"execution-error: codex model/list failed: exit {code}"
    assert time.monotonic() - start < review.CODEX_DISCOVERY_TIMEOUT
    if pidfile.exists():  # an exited codex's lingering descendant is killed too
        _assert_descendant_gone(pidfile)


def test_review_timeout_default_is_thirty_minutes(monkeypatch):
    timeouts = []

    def runner(argv, **kwargs):
        timeouts.append(kwargs["timeout"])
        if argv[:2] == ["codex", "app-server"]:
            return completed(argv, json.dumps({"id": 2, "result": {"data": [{"id": "gpt-6.1-sol"}]}}))
        return completed(argv, "ok", "model: gpt-6.1-sol\nreasoning effort: high\n")

    result = review.execute("codex", "gpt-6.1-sol", "high", "openai", "/repo", "review",
                            consent(), runner=runner)
    assert result["status"] == "completed", result
    assert timeouts[-1] == 1800
    execute, seen = review.execute, {}
    monkeypatch.setattr(review, "execute", lambda *a, **k: seen.update(k) or {"status": "failed"})
    review.main(["--executor", "codex", "--scope", "/repo", "--consent-record", "/nonexistent",
                 "--model", "m", "--effort", "high", "--family", "openai"],
                stdin=__import__("io").StringIO(""), out=__import__("io").StringIO())
    assert seen["review_timeout"] == 1800
    result = execute("codex", "gpt-6.1-sol", "high", "openai", "/repo", "review",
                            consent(), runner=lambda *a, **k: pytest.fail("spawned"),
                            review_timeout=1801)
    assert result["reason"] == "invalid-explicit-profile"


def _progress_lines(text):
    return [line for line in text.splitlines() if line.startswith("external-review:")]


_FAKE_CLAUDE_STEPS = """#!{python}
import json, sys
text = sys.stdin.read()
exec({probe!r} if "single word ok" in text else {review!r})
print(json.dumps({{"result": "ok", "modelUsage": {{"claude-sonnet-4-5": {{}}}}}}), flush=True)
"""


def _execute_claude(tmp_path, monkeypatch, *, probe_code="", review_code="",
                    probe_timeout=45, review_timeout=60):
    """Run review.execute against a fake `claude` CLI; each step runs its code first."""
    import sys
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    script = bin_dir / "claude"
    script.write_text(_FAKE_CLAUDE_STEPS.format(python=sys.executable, probe=probe_code,
                                                review=review_code))
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    return review.execute("claude", "sonnet", "high", "anthropic", str(tmp_path),
                          "REVIEW-PACKET", consent("claude", scope=str(tmp_path)),
                          probe_timeout=probe_timeout, review_timeout=review_timeout)


def _closing_seconds(line, outcome):
    """(total, longest silence) in seconds from one step's closing line."""
    match = re.fullmatch(rf"external-review: {outcome} after (\d+)s · longest silence (\d+)s",
                         line)
    assert match, line
    return int(match.group(1)), int(match.group(2))


def test_review_step_prints_progress_each_interval(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(review, "PROGRESS_INTERVAL", 0.3)
    result = _execute_claude(tmp_path, monkeypatch,
                             review_code="import time; time.sleep(1.1)")
    assert result["status"] == "completed", result
    lines = _progress_lines(capsys.readouterr().err)
    running = [line for line in lines if "review still running" in line]
    assert len(running) >= 2, lines
    assert all(re.fullmatch(r"external-review: review still running · \d+s elapsed"
                            r" · (last output \d+s ago|no output yet)", line)
               for line in running), running


def test_step_shorter_than_interval_prints_no_progress(tmp_path, monkeypatch, capsys):
    result = _execute_claude(tmp_path, monkeypatch)
    assert result["status"] == "completed", result
    lines = _progress_lines(capsys.readouterr().err)
    assert not [line for line in lines if "still running" in line], lines
    assert [line.split(" after ")[0] for line in lines] == [
        "external-review: probe exited 0", "external-review: review exited 0"], lines


def test_closing_line_reports_longest_silence(tmp_path, monkeypatch, capsys):
    result = _execute_claude(tmp_path, monkeypatch, review_code=(
        "import time; print('a', flush=True); time.sleep(1.3);"
        " print('b', flush=True); sys.exit(3)"))
    assert result["reason"].startswith("review-exit-3"), result
    lines = _progress_lines(capsys.readouterr().err)
    closing = [line for line in lines if line.startswith("external-review: review ")]
    assert len(closing) == 1, lines
    total, silence = _closing_seconds(closing[0], "review exited 3")
    assert total >= 1 and 1 <= silence <= total, closing


def test_timeout_prints_timed_out_closing_line(tmp_path, monkeypatch, capsys):
    result = _execute_claude(tmp_path, monkeypatch, probe_code="import time; time.sleep(10)",
                             probe_timeout=1, review_timeout=2)
    assert result["reason"] == "execution-timeout: 1s", result
    lines = _progress_lines(capsys.readouterr().err)
    assert len(lines) == 1, lines
    total, silence = _closing_seconds(lines[0], "probe timed out")
    assert total >= 1 and 1 <= silence <= total, lines


_FAKE_CLAUDE_OK = """#!{python}
import json, sys
sys.stdin.read()
print(json.dumps({{"result": "SECRET-REVIEW-TEXT", "modelUsage": {{"claude-sonnet-4-5": {{}}}}}}))
"""


def test_json_result_unchanged_with_progress(tmp_path, monkeypatch, capsys):
    import io
    import sys
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    script = bin_dir / "claude"
    script.write_text(_FAKE_CLAUDE_OK.format(python=sys.executable))
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    record = tmp_path / "consent.json"
    record.write_text(json.dumps(consent("claude", scope=str(tmp_path))))
    out = io.StringIO()
    code = review.main(["--executor", "claude", "--scope", str(tmp_path),
                        "--consent-record", str(record), "--model", "sonnet",
                        "--effort", "high", "--family", "anthropic"],
                       stdin=io.StringIO("PACKET-TEXT"), out=out)
    result = json.loads(out.getvalue())
    assert code == 0 and result["status"] == "completed", result
    assert result["review_output"] == "SECRET-REVIEW-TEXT"
    assert "external-review:" not in out.getvalue()
    err = capsys.readouterr().err
    lines = _progress_lines(err)
    assert [line.split(" after ")[0] for line in lines] == [
        "external-review: probe exited 0", "external-review: review exited 0"], lines
    assert "PACKET-TEXT" not in err and "SECRET-REVIEW-TEXT" not in err


def test_discovery_prints_no_progress(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(review, "PROGRESS_INTERVAL", 0.1)
    _fake_cli(tmp_path, monkeypatch, "agy", "exit-early")
    result = review.discover("agy", str(tmp_path), consent("agy", scope=str(tmp_path)))
    assert result["candidates"] == ["gemini-2.5-pro"], result
    assert _progress_lines(capsys.readouterr().err) == []


def _execute_section():
    from pathlib import Path
    skill = (Path(review.__file__).resolve().parents[1] / "skills"
             / "external-review" / "SKILL.md").read_text()
    match = re.search(r"^## Execute$.*?(?=^## |\Z)", skill, re.M | re.S)
    assert match, "## Execute missing"
    return " ".join(match.group(0).lower().split())


def _affirms_relay(text):
    return affirms(text, "relay", "progress line", "user", "visible")


def _affirms_one_json_stdout(text):
    return affirms(text, "stdout", "one json result")


def test_execute_section_names_progress_relay():
    assert _affirms_relay(_execute_section())


def test_execute_section_still_names_one_json_result():
    assert _affirms_one_json_stdout(_execute_section())


def test_execute_section_pins_reject_negated_samples():
    assert _affirms_relay("keep the error stream visible and relay each progress line"
                          " to the user.")
    assert not _affirms_relay("keep the error stream visible but do not relay progress"
                              " lines to the user; wait silently.")
    assert _affirms_one_json_stdout("stdout remains the one json result.")
    assert not _affirms_one_json_stdout("stdout no longer remains the one json result.")
