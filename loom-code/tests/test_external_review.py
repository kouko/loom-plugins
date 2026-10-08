from __future__ import annotations

import json
import subprocess

import external_review as review
import pytest


def consent(executor="codex", scope="/repo", model=None, effort="high"):
    model = model or {"codex": "gpt-6.1-sol", "claude": "sonnet",
                      "agy": "gemini-2.5-pro"}[executor]
    return {
        "approved": True, "executor": executor, "review_root": scope,
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
    assert len(calls) == 2


def test_agy_model_list_and_explicit_pair():
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv == ["agy", "models"]:
            return completed(argv, "gemini-2.5-pro\nclaude-sonnet-4-5\n")
        assert argv[:3] == ["agy", "-p", "--model"]
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
            return completed(argv, "", "unsupported effort", 2)
        model = "other-model" if case == "header-mismatch" else "gpt-6.1-sol"
        return completed(argv, "ok", f"model: {model}\nreasoning effort: high\n")

    family = "google" if case == "mismatch" else "openai"
    result = review.execute("codex", "gpt-6.1-sol", "high", family, "/repo",
                            "review", consent(), runner=runner)
    assert result["status"] == "failed"
    assert result["review_output"] is None
    assert len(calls) <= 2
