from __future__ import annotations

import errno
import json
import subprocess

import external_review as review
import pytest


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


@pytest.mark.parametrize("source", [{},
    {"kind": "direct-user-request", "quote": "", "target": "this change"},
    {"kind": "direct-user-request", "quote": "review this", "target": ""},
    {"kind": "direct-user-request", "quote": "review this change", "target": "this change"},
    {"kind": "direct-user-request", "quote": "Use Codex to review this change", "target": "this change"},
    {"kind": "suggestion", "quote": "Use codex", "target": "this change"},
    {"kind": "accepted-selection", "selection": "", "target": "this change"},
])
def test_authorization_source_must_name_real_request_or_selection(source):
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


@pytest.mark.parametrize("executor, quote", [
    ("claude", "Do not use Claude to review this change"),
    ("codex", "Don't use Codex to review this change"),
    ("agy", "Never use Agy to review this change"),
    ("claude", "不要用 Claude 審查這個變更"),
    ("codex", "別用 Codex 審查這個變更"),
    ("claude", "Claude を使わないで、この変更を確認して"),
    ("claude", "Do not review with Claude"),
    ("claude", "I don't want Claude"),
    ("claude", "Claude can review this change"),
    ("claude", "I did not say to use Claude"),
    ("claude", "Use Claude? No, use Codex to review this change."),
    ("claude", "Please review with Codex, not Claude."),
    ("claude", "不要用 Claude，改用 Codex 審查這個變更"),
    ("codex", "Please use Claude instead of Codex to review this change"),
    ("codex", "Use Codex? Actually use Claude to review this change"),
    ("codex", "Maybe Codex can review this change"),
])
def test_refusal_or_ambiguous_quote_cannot_authorize_discovery_or_execution(
        executor, quote):
    record = consent(executor)
    record["authorization_source"]["quote"] = quote
    no_spawn = lambda *a, **k: pytest.fail("spawned")
    discovered = review.discover(executor, "/repo", record, runner=no_spawn)
    executed = review.execute(executor, record["model"], "high",
                              {"claude": "anthropic", "codex": "openai", "agy": "google"}[executor],
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
])
def test_affirmative_direct_request_remains_valid(executor, quote):
    record = consent(executor)
    record["authorization_source"]["quote"] = quote
    assert review._authorization_valid(record["authorization_source"], executor)


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
    assert stderr not in json.dumps(result)


def test_nonzero_empty_diagnostic_is_explicitly_unknown():
    result = review.execute("claude", "sonnet", "high", "anthropic", "/repo",
                            "review", consent("claude"),
                            runner=lambda argv, **kwargs: completed(argv, "", rc=2))
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert result["reason"] == "probe-exit-2: unknown error"
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
