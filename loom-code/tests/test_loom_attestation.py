# concern: Protected rule documents must not receive narrow-change waivers.
from __future__ import annotations

import subprocess
import hashlib
import json
import os
import sys
import yaml
from io import StringIO
from pathlib import Path

import external_review
import pytest
from loom_checker import attestation as attestation_module
from loom_checker import digest, probes, reviewers
from loom_checker.command_handlers import finalize, reviewer_count


CHANGE = "2026-09-08-example"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def commit(repo: Path, message: str) -> str:
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def repo_with_content(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.parent.mkdir(parents=True, exist_ok=True)
    kickoff.write_text("- package-tests: python3 -m pytest -q — fixture (2026-09-08)\n")
    commit(repo, "initial")
    return repo


def manifest() -> dict:
    return {"publication_only_paths": ["docs/loom/<change-id>/attestation.json"]}


PROBE = f"docs/loom/{CHANGE}/evidence/probes/test_probe.py"


def commit_probe(repo: Path) -> str:
    """Commit a probe program where the protocol puts one.

    `finalize-review` runs only an artifact committed there, so that every
    program it executes is one `adversarial.proportionate` has counted.
    """
    path = repo / PROBE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# concern: the fixture's own adversarial run\nprint('probe')\n",
        encoding="utf-8",
    )
    commit(repo, "probe program")
    return PROBE


def test_functional_digest_ignores_declared_publication_paths(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    before = git(repo, "rev-parse", "HEAD")
    evidence = repo / f"docs/loom/{CHANGE}/attestation.json"
    evidence.parent.mkdir(parents=True)
    evidence.write_text('{"content_digest":"old"}\n', encoding="utf-8")
    after = commit(repo, "publication evidence")

    assert digest.functional_content_digest(repo, before, CHANGE, manifest()) == \
        digest.functional_content_digest(repo, after, CHANGE, manifest())


def test_functional_mutation_invalidates_digest(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    before = git(repo, "rev-parse", "HEAD")
    (repo / "src.py").write_text("VALUE = 2\n", encoding="utf-8")
    after = commit(repo, "functional change")

    assert digest.functional_content_digest(repo, before, CHANGE, manifest()) != \
        digest.functional_content_digest(repo, after, CHANGE, manifest())


def test_another_changes_attestation_is_functional_content(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    before = git(repo, "rev-parse", "HEAD")
    other = repo / "docs/loom/another-change/attestation.json"
    other.parent.mkdir(parents=True)
    other.write_text("{}\n", encoding="utf-8")
    after = commit(repo, "other evidence")

    assert digest.functional_content_digest(repo, before, CHANGE, manifest()) != \
        digest.functional_content_digest(repo, after, CHANGE, manifest())


def matching_attestation(repo: Path) -> dict:
    command = "python3 -m pytest -q"
    adversarial = "python3 src.py"
    return {
        "schema": "loom-attestation/v1",
        "change_id": CHANGE,
        "content_digest": digest.functional_content_digest(
            repo, git(repo, "rev-parse", "HEAD"), CHANGE, manifest()
        ),
        "executions": [{
            "kind": "package-tests", "command": command, "artifact": "",
            "result": "pass", "command_digest": hashlib.sha256(command.encode()).hexdigest(),
        }, {
            "kind": "adversarial", "command": adversarial, "artifact": "src.py",
            "result": "pass", "command_digest": hashlib.sha256(adversarial.encode()).hexdigest(),
        }],
        "verdicts": [{
            "reviewer": "reviewer-1", "vendor": "openai", "model": "test",
            "lens": "code", "verdict": "PASS", "findings": [],
        }, {
            "reviewer": "reviewer-2", "vendor": "other", "model": "test",
            "lens": "code", "verdict": "PASS", "findings": [],
        }],
        "findings": [],
    }


def test_matching_attestation_validates_without_executing_commands(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    failures = attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, matching_attestation(repo), manifest()
    )
    assert failures == []


def test_well_formed_forged_attestation_fails_closed(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    attestation = matching_attestation(repo)
    attestation["executions"][0]["command_digest"] = "0" * 64
    failures = attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    )
    assert any("command digest" in reason for _, reason in failures)


def test_package_execution_must_match_declared_command(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    attestation = matching_attestation(repo)
    attestation["executions"][0]["command"] = "true"
    attestation["executions"][0]["command_digest"] = hashlib.sha256(b"true").hexdigest()
    failures = attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    )
    assert any("declared package command" in reason for _, reason in failures)


def test_attestation_requires_two_reviewers_and_adversarial_execution(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    attestation = matching_attestation(repo)
    attestation["verdicts"] = attestation["verdicts"][:1]
    failures = attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    )
    assert any("two distinct reviewers" in reason for _, reason in failures)
    attestation = matching_attestation(repo)
    attestation["executions"] = attestation["executions"][:1]
    failures = attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    )
    assert any("adversarial execution" in reason for _, reason in failures)


def test_reviewer_floor_is_one_only_for_narrow_low_risk_paths() -> None:
    change_paths = {
        f"docs/loom/intent/{CHANGE}.md",
        f"docs/loom/{CHANGE}/plan.md",
        "loom-code/scripts/test_example.py",
        "docs/guide.md",
    }
    assert reviewers.reviewer_floor_for_paths(change_paths, CHANGE) == 1
    # Adding a test is low risk, so the floor is one; it is still a file the
    # suite executes, so the delta is not narrow and skips no step.
    assert reviewers.is_narrow_delta(change_paths, CHANGE) is False
    assert reviewers.is_narrow_delta(
        change_paths - {"loom-code/scripts/test_example.py"}, CHANGE
    ) is True

    for protected in (
        "src.py",
        "loom-code/skills/closing-review/SKILL.md",
        "loom-code/agents/reviewer.md",
        "loom-code/contract/manifest.yaml",
        "loom-code/hooks/hooks.json",
        "docs/loom/KICKOFF-DEFAULTS.md",
        "AGENTS.md",
        "CLAUDE.md",
        "DESIGN.md",
        "PRINCIPLES.md",
        "ARCHITECTURE.md",
        "docs/architecture.md",
        "unknown.bin",
        f"docs/loom/{CHANGE}/../../src.py",
        "tests/skills/SKILL.md",
        "tests/hooks/hooks.json",
        "tests/contract/manifest.yaml",
    ):
        assert reviewers.reviewer_floor_for_paths(
            change_paths | {protected}, CHANGE
        ) == 2
        assert reviewers.is_narrow_delta(change_paths | {protected}, CHANGE) is False
        assert reviewers.is_narrow_delta({protected}, CHANGE) is False


def test_reviewer_floor_is_two_when_the_delta_removes_a_test() -> None:
    """Adding a check is low risk; removing one changes what the repository
    can still catch, so it keeps the default two reviewers."""
    change_paths = {
        f"docs/loom/intent/{CHANGE}.md",
        "loom-code/scripts/test_example.py",
        "docs/guide.md",
    }
    removed = {"loom-code/scripts/test_example.py"}
    assert reviewers.reviewer_floor_for_paths(change_paths, CHANGE, removed) == 2
    assert reviewers.is_narrow_delta(change_paths, CHANGE, removed) is False
    assert reviewers.reviewer_floor_for_paths(change_paths, CHANGE) == 1


def test_is_narrow_delta_returns_false_for_mixed_delta() -> None:
    """A delta with code changes is not narrow."""
    change_paths = {
        f"docs/loom/intent/{CHANGE}.md",
        f"docs/loom/{CHANGE}/plan.md",
        "loom-code/scripts/some_code.py",
    }
    assert reviewers.is_narrow_delta(change_paths, CHANGE) is False
    assert reviewers.reviewer_floor_for_paths(change_paths, CHANGE) == 2


def test_matching_low_risk_attestation_accepts_one_reviewer(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    git(repo, "switch", "-q", "-c", "feature")
    guide = repo / "docs/guide.md"
    guide.parent.mkdir(parents=True, exist_ok=True)
    guide.write_text("Clarified usage.\n", encoding="utf-8")
    commit(repo, "docs")
    attestation = matching_attestation(repo)
    attestation["verdicts"] = attestation["verdicts"][:1]

    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    ) == []


def test_selected_outside_review_raises_narrow_floor_and_requires_both_families(
    tmp_path: Path, monkeypatch,
) -> None:
    repo = repo_with_content(tmp_path)
    git(repo, "switch", "-q", "-c", "feature")
    plan = repo / f"docs/loom/{CHANGE}/plan.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text(
        "## Risks\nuser-decided — second-vendor selection-confirmed: claude\n",
        encoding="utf-8",
    )
    commit(repo, "select outside reviewer")
    monkeypatch.chdir(repo)
    out, err = StringIO(), StringIO()
    assert reviewer_count.cmd_reviewer_count([CHANGE], out, err) == 0
    assert out.getvalue() == "2\n"

    evidence = matching_attestation(repo)
    evidence["verdicts"] = evidence["verdicts"][:1]
    assert any("two distinct reviewers" in reason for _, reason in
               attestation_module.validate_attestation(repo, git(repo, "rev-parse", "HEAD"),
                                                       CHANGE, evidence, manifest()))
    evidence["verdicts"].append({**evidence["verdicts"][0],
                                 "reviewer": "reviewer-2", "vendor": "openai"})
    review_input = tmp_path / "review-input.json"
    review_input.write_text(json.dumps({"verdicts": evidence["verdicts"],
                                        "findings": [], "adversarial": []}),
                            encoding="utf-8")
    assert any("outside" in reason for _, reason in
               finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()))
    assert any("outside" in reason for _, reason in
               attestation_module.validate_attestation(repo, git(repo, "rev-parse", "HEAD"),
                                                       CHANGE, evidence, manifest()))
    evidence["verdicts"][1]["vendor"] = "anthropic"
    evidence["verdicts"][1]["lens"] = "docs"
    assert any("same review lens" in reason for _, reason in
               attestation_module.validate_attestation(repo, git(repo, "rev-parse", "HEAD"),
                                                       CHANGE, evidence, manifest()))
    evidence["verdicts"][1]["lens"] = "code"
    assert any("outside execution" in reason for _, reason in
               attestation_module.validate_attestation(repo, git(repo, "rev-parse", "HEAD"),
                                                       CHANGE, evidence, manifest()))


def test_finalize_binds_selected_outside_runner_output_to_verdict(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.write_text("- package-tests: python3 -c pass — fixture (2026-09-08)\n")
    commit(repo, "declare fast suite")
    git(repo, "switch", "-q", "-c", "feature")
    plan = repo / f"docs/loom/{CHANGE}/plan.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text("## Risks\nuser-decided — second-vendor selection-confirmed: claude\n")
    commit(repo, "select outside review")
    raw = (
        "verdict: PASS\nlens: docs\nreviewed_sha: HEAD\n"
        "dimension_scores:\n"
        "  omission: PASS\n  ambiguity: PASS\n  inconsistency: PASS\n"
        "  incorrect-fact: PASS\n  missing-population: PASS\n"
        "  deletion-first: PASS\nfindings: []\nnotes: []\n"
    )
    review_input = tmp_path / "review-input.json"
    review_input.write_text(json.dumps({
        "verdicts": [
            {"reviewer": "native", "vendor": "openai", "model": "test",
             "lens": "docs", "verdict": "PASS", "findings": []},
            {"reviewer": "outside-1", "vendor": "anthropic", "model": "sonnet",
             "lens": "docs", "reviewed_sha": "HEAD", "verdict": "PASS", "findings": [],
             "external_review": {
                 "status": "completed", "reason": None, "executor": "claude",
                 "requested_model": "sonnet", "requested_effort": "high",
                 "requested_family": "anthropic", "evidence_level": "accepted-explicit-settings",
                 "observed_model": "claude-sonnet-4-5", "observed_effort": None,
                 "review_output": raw,
             }},
        ], "findings": [], "adversarial": [],
    }), encoding="utf-8")
    output = StringIO()
    assert finalize._finalize(repo, CHANGE, ["--input", str(review_input)], output) == []
    attestation = json.loads((repo / f"docs/loom/{CHANGE}/attestation.json").read_text())
    receipt = attestation["verdicts"][1]["external_review"]
    assert receipt["output_digest"] == hashlib.sha256(raw.encode()).hexdigest()
    assert "review_output" not in receipt
    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    ) == []
    receipt["reviewer"] = "native"
    assert any("outside execution" in reason for _, reason in
               attestation_module.validate_attestation(repo, git(repo, "rev-parse", "HEAD"),
                                                       CHANGE, attestation, manifest()))


@pytest.mark.parametrize("selected,executor,model,family,level,observed_model,observed_effort", [
    ("claude", "claude", "sonnet", "anthropic", "accepted-explicit-settings", "claude-sonnet-4-5", None),
    ("codex", "codex", "gpt-6.1-sol", "openai", "observed-model-and-effort", "gpt-6.1-sol", "high"),
    ("gemini", "agy", "gemini-2.5-pro", "google", "accepted-explicit-settings", None, None),
])
def test_outside_receipt_rejects_impossible_field_combinations(
    tmp_path: Path, selected: str, executor: str, model: str, family: str,
    level: str, observed_model: str | None, observed_effort: str | None,
) -> None:
    repo = repo_with_content(tmp_path)
    git(repo, "switch", "-q", "-c", "feature")
    plan = repo / f"docs/loom/{CHANGE}/plan.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text(f"## Risks\nuser-decided — second-vendor selection-confirmed: {selected}\n")
    commit(repo, "select outside review")
    evidence = matching_attestation(repo)
    outside = evidence["verdicts"][1]
    outside.update(vendor=family, model=model)
    evidence["verdicts"][0]["vendor"] = "anthropic" if family != "anthropic" else "openai"
    receipt = {
        "status": "completed", "executor": executor, "model": model,
        "effort": "high", "family": family, "evidence_level": level,
        "observed_model": observed_model, "observed_effort": observed_effort,
        "output_digest": "a" * 64, "reviewer": outside["reviewer"],
    }
    outside["external_review"] = receipt
    head = git(repo, "rev-parse", "HEAD")
    assert attestation_module.validate_attestation(repo, head, CHANGE, evidence, manifest()) == []

    alien_model = "sonnet" if family != "anthropic" else "gpt-6.1-sol"
    impossible = [
        {"evidence_level": "accepted-explicit-settings" if executor == "codex"
         else "observed-model-and-effort"},
        {"observed_model": None if executor != "agy" else "gemini-2.5-pro"},
        {"observed_effort": None if executor == "codex" else "high"},
        {"model": alien_model},
        {"effort": "unsupported"},
        {"executor": "claude" if executor != "claude" else "codex"},
    ]
    if executor == "claude":
        impossible.append({"model": "claude-opus-4", "observed_model": "claude-sonnet-4-5"})
        impossible.append({"observed_model": "claude-opus-4-1"})
    for fields in impossible:
        receipt.update(fields)
        outside["model"] = receipt["model"]
        assert any("outside execution" in reason for _, reason in
                   attestation_module.validate_attestation(repo, head, CHANGE, evidence, manifest()))
        receipt.update(model=model, effort="high", executor=executor, evidence_level=level,
                       observed_model=observed_model, observed_effort=observed_effort)
        outside["model"] = model


def test_external_dispatch_gate_integrates_runner_verdict_and_attestation(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.write_text("- package-tests: python3 -c pass — fixture (2026-09-08)\n")
    commit(repo, "declare fast suite")
    git(repo, "switch", "-q", "-c", "feature")
    plan = repo / f"docs/loom/{CHANGE}/plan.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text("## Risks\nuser-decided — second-vendor selection-confirmed: codex\n")
    commit(repo, "select outside provider")
    packet = ("lens: docs\nreviewed_sha: HEAD\nchanged paths: docs/loom/"
              f"{CHANGE}/plan.md\nground truth: intent and plan\n"
              "dimensions: loom-code/skills/closing-review/references/lenses.md\n"
              "output: agents/reviewer.md YAML contract\n")
    raw = "verdict: PASS\nlens: docs\nfindings: []\n"
    header = "model: gpt-6.1-sol\nreasoning effort: high\n"
    calls = []

    def runner(argv, **kwargs):
        calls.append(argv)
        if argv[:2] == ["codex", "app-server"]:
            return subprocess.CompletedProcess(
                argv, 0, json.dumps({"id": 2, "result": {"data": [{"id": "gpt-6.1-sol"}]}}), ""
            )
        assert argv[:2] == ["codex", "exec"]
        assert argv[argv.index("-m") + 1] == "gpt-6.1-sol"
        assert "model_reasoning_effort=high" in argv
        if len(calls) == 3:
            assert kwargs["input"] == packet
            return subprocess.CompletedProcess(argv, 0, raw, header)
        return subprocess.CompletedProcess(argv, 0, "ok", header)

    consent = {
        "approved": True, "executor": "codex", "review_root": str(repo),
        "authorization_source": {"kind": "direct-user-request", "quote": "Use Codex to review this change", "target": "this change"},
        "model": "gpt-6.1-sol", "effort": "high",
        "disclosures": {
            "cost": True, "vendor_egress": True, "local_execution": True,
            "filesystem_access_outside_root": True,
            "filesystem_write_not_guaranteed": True,
        },
    }
    stale = dict(consent, review_root=str(tmp_path))
    assert external_review.execute(
        "codex", "gpt-6.1-sol", "high", "openai", str(repo), packet, stale,
        runner=runner,
    )["status"] == "failed"
    assert external_review.execute(
        "codex", "gpt-6.1-sol", "medium", "openai", str(repo), packet, consent,
        runner=runner,
    )["status"] == "failed"
    assert calls == []
    result = external_review.execute(
        "codex", "gpt-6.1-sol", "high", "openai", str(repo), packet, consent,
        runner=runner,
    )
    assert result["status"] == "completed"
    assert result["evidence_level"] == "observed-model-and-effort"
    assert len(calls) == 3

    verdicts = [
        {"reviewer": "native", "vendor": "anthropic", "model": "sonnet",
         "lens": "docs", "verdict": "PASS", "findings": []},
        {"reviewer": "outside", "vendor": "openai", "model": "gpt-6.1-sol",
         "lens": "docs", "reviewed_sha": "HEAD", "verdict": "PASS",
         "findings": [], "external_review": result},
    ]
    review_input = tmp_path / "review-input.json"
    review_input.write_text(json.dumps({"verdicts": verdicts, "findings": [],
                                        "adversarial": []}), encoding="utf-8")
    assert any("required reviewer YAML" in reason for _, reason in
               finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()))

    raw = (
        "verdict: PASS\nlens: docs\nreviewed_sha: HEAD\n"
        "dimension_scores:\n"
        "  omission: PASS\n  ambiguity: PASS\n  inconsistency: PASS\n"
        "  incorrect-fact: PASS\n  missing-population: PASS\n"
        "  deletion-first: PASS\nfindings: []\nnotes: []\n"
    )
    result["review_output"] = raw
    review_input.write_text(json.dumps({"verdicts": verdicts, "findings": [],
                                        "adversarial": []}), encoding="utf-8")
    assert finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()) == []
    attestation = json.loads((repo / f"docs/loom/{CHANGE}/attestation.json").read_text())
    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    ) == []
    receipt = attestation["verdicts"][1]["external_review"]
    assert receipt["output_digest"] == hashlib.sha256(raw.encode()).hexdigest()
    assert "review_output" not in receipt

    (repo / f"docs/loom/{CHANGE}/attestation.json").unlink()
    verdicts[1]["lens"] = "skill"
    review_input.write_text(json.dumps({"verdicts": verdicts, "findings": [],
                                        "adversarial": []}), encoding="utf-8")
    assert any("output differs from its verdict" in reason for _, reason in
               finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()))
    verdicts[1]["lens"] = "docs"
    for malformed in (
        raw.replace("  deletion-first: PASS\n", ""),
        raw.replace("  omission: PASS", "  omission: UNKNOWN"),
        raw.replace("reviewed_sha: HEAD", "reviewed_sha: OTHER"),
    ):
        result["review_output"] = malformed
        review_input.write_text(json.dumps({"verdicts": verdicts, "findings": [],
                                            "adversarial": []}), encoding="utf-8")
        assert any("required reviewer YAML" in reason for _, reason in
                   finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()))
    finding = {"severity": "important", "dimension": "omission", "anchor": "",
               "text": "issue: missing fact", "fix": "add it"}
    verdicts[1]["findings"] = [finding]
    result["review_output"] = raw.replace("findings: []", yaml.safe_dump({"findings": [finding]}).strip())
    review_input.write_text(json.dumps({"verdicts": verdicts, "findings": [],
                                        "adversarial": []}), encoding="utf-8")
    assert any("malformed reviewer findings" in reason for _, reason in
               finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()))
    verdicts[1]["findings"] = []
    result["review_output"] = raw.replace("  omission: PASS", "  omission: NEEDS_REVISION")
    review_input.write_text(json.dumps({"verdicts": verdicts, "findings": [],
                                        "adversarial": []}), encoding="utf-8")
    assert any("overall verdict" in reason for _, reason in
               finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()))
    for severities in (("fatal",), ("important", "important")):
        findings = [
            {"severity": severity, "dimension": "omission",
             "anchor": f"docs/guide.md:{index}", "text": "issue: missing fact",
             "fix": "add the fact"}
            for index, severity in enumerate(severities, 1)
        ]
        verdicts[1]["findings"] = findings
        result["review_output"] = raw.replace(
            "findings: []", yaml.safe_dump({"findings": findings}).strip()
        )
        review_input.write_text(json.dumps({"verdicts": verdicts, "findings": [],
                                            "adversarial": []}), encoding="utf-8")
        assert any("overall verdict" in reason for _, reason in
                   finalize._finalize(repo, CHANGE, ["--input", str(review_input)], StringIO()))


def test_reviewer_floor_fails_closed_when_branch_base_is_unknown(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)

    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_reviewer_floor_sees_both_sides_of_a_protected_file_rename(
    tmp_path: Path,
) -> None:
    repo = repo_with_content(tmp_path)
    runtime = repo / "runtime.py"
    runtime.write_text("VALUE = 1\n", encoding="utf-8")
    commit(repo, "runtime")
    git(repo, "switch", "-q", "-c", "feature")
    guide = repo / "docs/guide.md"
    guide.parent.mkdir(parents=True, exist_ok=True)
    runtime.rename(guide)
    commit(repo, "rename runtime as docs")

    assert reviewers.required_reviewer_count(repo, CHANGE) == 2


def test_reviewer_count_command_reports_the_computed_floor(
    tmp_path: Path, monkeypatch
) -> None:
    repo = repo_with_content(tmp_path)
    git(repo, "switch", "-q", "-c", "feature")
    guide = repo / "docs/guide.md"
    guide.parent.mkdir(parents=True, exist_ok=True)
    guide.write_text("Clarified usage.\n", encoding="utf-8")
    commit(repo, "docs")
    monkeypatch.chdir(repo)
    out, err = StringIO(), StringIO()

    assert reviewer_count.cmd_reviewer_count([CHANGE], out, err) == 0
    assert out.getvalue() == "1\n"
    assert err.getvalue() == ""


def test_stale_attestation_fails_closed(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    attestation = matching_attestation(repo)
    (repo / "src.py").write_text("VALUE = 3\n", encoding="utf-8")
    head = commit(repo, "new behavior")
    failures = attestation_module.validate_attestation(repo, head, CHANGE, attestation, manifest())
    assert any("functional content digest" in reason for _, reason in failures)


def test_adversarial_execution_must_name_a_committed_artifact(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    attestation = matching_attestation(repo)
    command = "python3 missing.py"
    attestation["executions"].append({
        "kind": "adversarial", "command": command, "artifact": "missing.py",
        "result": "pass", "command_digest": hashlib.sha256(command.encode()).hexdigest(),
    })
    failures = attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    )
    assert any("committed artifact" in reason for _, reason in failures)


def test_adversarial_wrapper_cannot_fake_execution(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    attestation = matching_attestation(repo)
    command = "true src.py"
    attestation["executions"][1].update({
        "command": command,
        "command_digest": hashlib.sha256(command.encode()).hexdigest(),
    })
    failures = attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    )
    assert any("execute the artifact directly" in reason for _, reason in failures)


def test_pytest_runner_directly_executes_named_artifact() -> None:
    assert probes.command_executes_artifact(
        "python3 -m pytest tests/probe.py -q", "tests/probe.py"
    )
    for command in ("python3 -m pytest -q -x tests/probe.py",
                    "uv run --with x python -m pytest -q tests/probe.py",
                    "python3 -m pytest -pno:cacheprovider tests/probe.py",
                    "python3 -m pytest --tb=short tests/probe.py"):
        assert probes.command_executes_artifact(command, "tests/probe.py")
    for command in ("python3 -m pytest -q tests/other.py",
                    "python3 -m pytest --help tests/probe.py",
                    "python3 -m pytest --version tests/probe.py",
                    "python3 -m pytest tests/probe.py --collect-only",
                    "python3 -m pytest --junitxml tests/probe.py tests/other.py"):
        assert not probes.command_executes_artifact(command, "tests/probe.py")


def bare_repo(tmp_path: Path) -> Path:
    """A repository with no test-command marker and no KICKOFF-DEFAULTS, so
    that `declared_test_command` falls through to the test-file scan."""
    repo = tmp_path / "adopting"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    commit(repo, "initial")
    return repo


def test_test_command_ignores_nested_worktree(tmp_path: Path) -> None:
    """Files inside a linked worktree checked out under the repository are
    another repository's; a test file there is not this repo's test suite."""
    repo = bare_repo(tmp_path)
    git(repo, "worktree", "add", "-q", "-b", "side", str(repo / "wt"))
    (repo / "wt" / "test_someone_elses.py").write_text(
        "def test_x():\n    assert True\n", encoding="utf-8"
    )

    assert probes.declared_test_command(repo) == (None, "")


def test_test_command_still_detects_own_tests(tmp_path: Path) -> None:
    repo = bare_repo(tmp_path)
    (repo / "test_own.py").write_text(
        "def test_x():\n    assert True\n", encoding="utf-8"
    )

    assert probes.declared_test_command(repo) == (
        "python3 -m pytest -q", "detected test_*.py files"
    )


def test_finalize_review_runs_and_writes_matching_attestation(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.write_text("- package-tests: python3 -c pass — fixture (2026-09-08)\n")
    commit(repo, "declare tests")
    probe = commit_probe(repo)
    review_input = tmp_path / "review-input.json"
    review_input.write_text(json.dumps({
        "verdicts": [{
            "reviewer": "reviewer-1", "vendor": "openai", "model": "test",
            "lens": "code", "verdict": "PASS", "findings": [],
        }, {
            "reviewer": "reviewer-2", "vendor": "other", "model": "test",
            "lens": "code", "verdict": "PASS", "findings": [],
        }],
        "findings": [],
        "adversarial": [{"command": f"python3 {probe}", "artifact": probe}],
    }), encoding="utf-8")
    checker = Path(__file__).resolve().parents[1] / "scripts" / "loom_checker.py"
    result = subprocess.run(
        [sys.executable, str(checker), "finalize-review", CHANGE, "--input", str(review_input)],
        cwd=repo, capture_output=True, text=True, env=os.environ.copy(),
    )
    assert result.returncode == 0, result.stderr
    output = repo / f"docs/loom/{CHANGE}/attestation.json"
    attestation = json.loads(output.read_text(encoding="utf-8"))
    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    ) == []
    assert [run["kind"] for run in attestation["executions"]] == [
        "package-tests", "adversarial"
    ]
    assert attestation["schema"] == "loom-attestation/v2"
    assert attestation["selection"] is None


def test_v1_attestation_still_validates_unchanged(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    attestation = matching_attestation(repo)
    assert attestation["schema"] == "loom-attestation/v1"
    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    ) == []
    attestation["selection"] = None
    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, manifest()
    ) != []


def test_finalize_review_accepts_one_reviewer_for_low_risk_change(tmp_path: Path) -> None:
    repo = repo_with_content(tmp_path)
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.write_text("- package-tests: python3 -c pass — fixture (2026-09-08)\n")
    commit(repo, "declare tests")
    git(repo, "switch", "-q", "-c", "feature")
    guide = repo / "docs/guide.md"
    guide.parent.mkdir(parents=True, exist_ok=True)
    guide.write_text("Clarified usage.\n", encoding="utf-8")
    commit(repo, "docs")
    review_input = tmp_path / "review-input.json"
    review_input.write_text(json.dumps({
        "verdicts": [{
            "reviewer": "reviewer-1", "vendor": "openai", "model": "test",
            "lens": "docs", "verdict": "PASS", "findings": [],
        }],
        "findings": [],
        # The delta is one low-risk doc, so the adversarial step is auto-skipped
        # and the change records no adversarial run at all.
        "adversarial": [],
    }), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "loom_checker.py"), "finalize-review", CHANGE,
         "--input", str(review_input)],
        cwd=repo, capture_output=True, text=True, env=os.environ.copy(),
    )

    assert result.returncode == 0, result.stderr


def test_finalize_surfaces_failed_command_output(tmp_path: Path, monkeypatch) -> None:
    repo = repo_with_content(tmp_path)
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    (repo / "fail.py").write_text(
        'print("PACKAGE_SENTINEL")\nraise SystemExit(7)\n', encoding="utf-8"
    )
    kickoff.write_text(
        "- package-tests: python3 fail.py — fixture (2026-09-08)\n",
        encoding="utf-8",
    )
    commit(repo, "set failing package command")
    probe = commit_probe(repo)
    review_input = tmp_path / "review-input.json"
    review_input.write_text(json.dumps({
        "verdicts": [
            {"reviewer": "r1", "vendor": "openai", "model": "test", "lens": "code", "verdict": "PASS", "findings": []},
            {"reviewer": "r2", "vendor": "openai", "model": "test", "lens": "skill", "verdict": "PASS", "findings": []},
        ],
        "findings": [],
        "adversarial": [{"command": f"python3 {probe}", "artifact": probe}],
    }), encoding="utf-8")
    monkeypatch.chdir(repo)
    error = StringIO()
    assert finalize.cmd_finalize_review([CHANGE, "--input", str(review_input)], err=error) == 1
    assert "PACKAGE_SENTINEL" in error.getvalue()
