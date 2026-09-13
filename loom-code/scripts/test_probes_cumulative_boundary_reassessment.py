"""Rebuild frozen histories and enforce the cumulative-boundary admission bar."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/skill-dogfood/2026-09-13-cumulative-boundary-reassessment"
CASES = EVIDENCE_DIR / "cases.md"
REPORT = EVIDENCE_DIR / "report.md"
BASELINE_REVISION = "1973ff35c4919e4c40795808240249c7ee40f506"
BASELINE_SHA256 = "e4c249bae4a5badbd15c258fbfe6d4d2d920e9eba58329fa2ee05bfe573c0da4"
ALLOWED_CANDIDATE_PATHS = {
    "loom-code/skills/write-plan/SKILL.md",
    "loom-code/skills/write-plan/references/cumulative-boundary-reassessment.md",
}


def _fenced_json(path: Path, label: str) -> tuple[dict, str]:
    text = path.read_text()
    match = re.search(rf"```json {re.escape(label)}\n(.*?)\n```", text, re.S)
    assert match, f"missing ```json {label}` block in {path}"
    return json.loads(match.group(1)), match.group(1)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _frozen_rubric() -> str:
    match = re.search(
        r"<!-- BEGIN frozen-rubric -->\n(.*?)\n<!-- END frozen-rubric -->",
        CASES.read_text(),
        re.S,
    )
    assert match, "missing frozen rubric markers"
    return match.group(1)


def _run(repo: Path, *args: str, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        [*args],
        cwd=repo,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.strip()


def build_fixture(root: Path, case_id: str, case: dict, git_config: dict) -> dict:
    repo = root / case_id
    repo.mkdir()
    _run(
        repo,
        "git",
        "init",
        "-q",
        f"--initial-branch={git_config['branch']}",
        f"--object-format={git_config['object_format']}",
    )
    _run(repo, "git", "config", "user.name", git_config["author_name"])
    _run(repo, "git", "config", "user.email", git_config["author_email"])

    started = datetime.fromisoformat(git_config["start_time"])
    commits = []
    for index, revision in enumerate(case["commits"]):
        changed_paths = []
        removed_paths = []
        for relative, content in revision["changes"].items():
            target = repo / relative
            if content is None:
                if target.exists():
                    target.unlink()
                removed_paths.append(relative)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
                changed_paths.append(relative)
        if changed_paths:
            _run(repo, "git", "add", "--", *changed_paths)
        for relative in removed_paths:
            _run(repo, "git", "add", "-u", "--", relative)
        timestamp = (started + timedelta(minutes=index)).astimezone(timezone.utc).isoformat()
        env = os.environ.copy()
        env.update(
            {
                "GIT_AUTHOR_DATE": timestamp,
                "GIT_COMMITTER_DATE": timestamp,
                "LC_ALL": "C",
                "TZ": "UTC",
            }
        )
        _run(repo, "git", "commit", "-q", "-m", revision["message"], env=env)
        commits.append(_run(repo, "git", "rev-parse", "HEAD"))

    return {
        "repo": repo,
        "head": _run(repo, "git", "rev-parse", "HEAD"),
        "tree": _run(repo, "git", "rev-parse", "HEAD^{tree}"),
        "commits": commits,
    }


@pytest.fixture(scope="session")
def fixture_spec() -> tuple[dict, str]:
    return _fenced_json(CASES, "fixture-spec")


def test_fixture_spec_is_complete_and_bounded(fixture_spec):
    spec, _ = fixture_spec
    assert spec["schema"] == 1
    assert spec["git"]["object_format"] == "sha1"
    assert set(spec["cases"]) == {"L1", "L2", "L3", "L4"}
    assert all(2 <= len(case["commits"]) <= 20 for case in spec["cases"].values())
    assert all(case["feature_request"].strip() for case in spec["cases"].values())


def test_baseline_contract_matches_frozen_identity():
    baseline = subprocess.run(
        ["git", "show", f"{BASELINE_REVISION}:loom-code/skills/write-plan/SKILL.md"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    assert hashlib.sha256(baseline).hexdigest() == BASELINE_SHA256


@pytest.mark.parametrize("case_id", ["L1", "L2", "L3", "L4"])
def test_real_git_history_matches_frozen_identity(tmp_path, fixture_spec, case_id):
    spec, _ = fixture_spec
    case = spec["cases"][case_id]
    built = build_fixture(tmp_path, case_id, case, spec["git"])
    assert built["head"] == case["expected_head"]
    assert built["tree"] == case["expected_tree"]
    assert len(built["commits"]) == len(set(built["commits"]))
    assert _run(built["repo"], "git", "status", "--porcelain") == ""


@pytest.mark.parametrize("case_id", ["L1", "L2", "L3", "L4"])
def test_fixture_head_unit_tests_pass(tmp_path, fixture_spec, case_id):
    spec, _ = fixture_spec
    built = build_fixture(tmp_path, case_id, spec["cases"][case_id], spec["git"])
    _run(built["repo"], sys.executable, "-m", "unittest", "discover", "-s", "tests", "-q")


def valid_admission_example(spec: dict, fixture_spec_sha256: str) -> dict:
    fixtures = {
        case_id: {"head": case["expected_head"], "tree": case["expected_tree"]}
        for case_id, case in spec["cases"].items()
    }
    return {
        "status": "ADMITTED",
        "identities": {
            "fixture_spec_sha256": fixture_spec_sha256,
            "rubric_sha256": _sha256_text(_frozen_rubric()),
            "baseline_revision": BASELINE_REVISION,
            "baseline_contract_sha256": BASELINE_SHA256,
            "candidate_contract_sha256": "1" * 64,
            "candidate_reference_sha256": "2" * 64,
            "candidate_changed_contract_paths": sorted(ALLOWED_CANDIDATE_PATHS),
        },
        "fixtures": fixtures,
        "runner_profile": {
            "baseline": {"model": "test-model", "effort": "test-effort"},
            "candidate": {"model": "test-model", "effort": "test-effort"},
        },
        "normalizer_sha256": "3" * 64,
        "normalized_outputs": {
            case_id: {"baseline": "4" * 64, "candidate": "5" * 64}
            for case_id in ("L1", "L2", "L3", "L4")
        },
        "auditors": ["audit-one", "audit-two"],
        "cases": {
            "L1": {"baseline": ["incorrect", "incorrect"], "candidate": ["correct", "correct"]},
            "L2": {"baseline": ["correct", "correct"], "candidate": ["correct", "correct"]},
            "L3": {"baseline": ["insufficient", "insufficient"], "candidate": ["correct", "correct"]},
            "L4": {"baseline": ["correct", "correct"], "candidate": ["correct", "correct"]},
        },
        "reference_loaded": {"L1": True, "L2": False, "L3": True, "L4": False},
        "cost": {
            "baseline": {"elapsed_seconds": 1, "input_tokens": 1, "output_tokens": 1},
            "candidate": {"elapsed_seconds": 1, "input_tokens": 1, "output_tokens": 1},
        },
        "mechanism_delta": 0,
        "real_runs": {
            "L1": {
                "complete": True,
                "focused_tests_pass": True,
                "candidate_surface_clearer_or_smaller": True,
            },
            "L2": {
                "complete": True,
                "focused_tests_pass": True,
                "extraction_performed": False,
            },
        },
        "claims_scope": "frozen-four-case-corpus-only",
    }


def admission_failures(evidence: dict, spec: dict, fixture_spec_sha256: str) -> list[str]:
    failures = []
    identities = evidence.get("identities") or {}
    if evidence.get("status") != "ADMITTED":
        failures.append("status is not ADMITTED")
    if identities.get("fixture_spec_sha256") != fixture_spec_sha256:
        failures.append("fixture specification identity is missing or mismatched")
    if identities.get("rubric_sha256") != _sha256_text(_frozen_rubric()):
        failures.append("rubric identity is missing or mismatched")
    if identities.get("baseline_revision") != BASELINE_REVISION:
        failures.append("baseline revision is missing or mismatched")
    if identities.get("baseline_contract_sha256") != BASELINE_SHA256:
        failures.append("baseline contract identity is missing or mismatched")
    for field in ("candidate_contract_sha256", "candidate_reference_sha256"):
        value = identities.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            failures.append(f"{field} is missing or malformed")
    if identities.get("candidate_contract_sha256") == BASELINE_SHA256:
        failures.append("candidate contract is byte-identical to the baseline")
    if set(identities.get("candidate_changed_contract_paths") or []) != ALLOWED_CANDIDATE_PATHS:
        failures.append("candidate contract path identity is incomplete or out of scope")

    fixtures = evidence.get("fixtures") or {}
    for case_id, case in spec["cases"].items():
        observed = fixtures.get(case_id) or {}
        if observed.get("head") != case["expected_head"] or observed.get("tree") != case["expected_tree"]:
            failures.append(f"{case_id} fixture identity is missing or mismatched")

    auditors = evidence.get("auditors") or []
    if len(auditors) != 2 or len(set(auditors)) != 2:
        failures.append("two independent auditor identities are required")
    cases = evidence.get("cases") or {}
    expected = {
        "L1": {"candidate": ["correct", "correct"]},
        "L2": {"candidate": ["correct", "correct"]},
        "L3": {"candidate": ["correct", "correct"]},
        "L4": {"candidate": ["correct", "correct"]},
    }
    for case_id, arms in expected.items():
        for arm, scores in arms.items():
            if (cases.get(case_id) or {}).get(arm) != scores:
                failures.append(f"{case_id} {arm} does not meet the frozen rubric")
    if (cases.get("L1") or {}).get("baseline") not in (
        ["incorrect", "incorrect"],
        ["insufficient", "insufficient"],
    ):
        failures.append("L1 baseline does not meet the frozen non-tie requirement")

    runner_profile = evidence.get("runner_profile") or {}
    if not runner_profile.get("baseline") or runner_profile.get("baseline") != runner_profile.get("candidate"):
        failures.append("matched runner profile is missing or differs by arm")
    if not re.fullmatch(r"[0-9a-f]{64}", str(evidence.get("normalizer_sha256") or "")):
        failures.append("normalizer identity is missing or malformed")
    normalized_outputs = evidence.get("normalized_outputs") or {}
    for case_id in ("L1", "L2", "L3", "L4"):
        for arm in ("baseline", "candidate"):
            value = (normalized_outputs.get(case_id) or {}).get(arm)
            if not re.fullmatch(r"[0-9a-f]{64}", str(value or "")):
                failures.append(f"{case_id} {arm} normalized output identity is missing")
    loads = evidence.get("reference_loaded") or {}
    if loads != {"L1": True, "L2": False, "L3": True, "L4": False}:
        failures.append("conditional reference loading does not match the challenge corpus")
    cost = evidence.get("cost") or {}
    for arm in ("baseline", "candidate"):
        values = cost.get(arm) or {}
        if not all(isinstance(values.get(field), (int, float)) and values[field] >= 0
                   for field in ("elapsed_seconds", "input_tokens", "output_tokens")):
            failures.append(f"{arm} cost evidence is missing")
    if evidence.get("mechanism_delta") != 0:
        failures.append("mechanism population did not remain flat")
    real_runs = evidence.get("real_runs") or {}
    l1 = real_runs.get("L1") or {}
    if not (l1.get("complete") and l1.get("focused_tests_pass")
            and l1.get("candidate_surface_clearer_or_smaller")):
        failures.append("L1 real implementation evidence is missing or unmet")
    l2 = real_runs.get("L2") or {}
    if not (l2.get("complete") and l2.get("focused_tests_pass")
            and l2.get("extraction_performed") is False):
        failures.append("L2 real implementation evidence is missing or unmet")
    if evidence.get("claims_scope") != "frozen-four-case-corpus-only":
        failures.append("claims scope exceeds the frozen corpus")
    return failures


def test_admission_oracle_accepts_complete_evidence(fixture_spec):
    spec, raw = fixture_spec
    evidence = valid_admission_example(spec, _sha256_text(raw))
    assert admission_failures(evidence, spec, _sha256_text(raw)) == []


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        ("l1-tie", "L1 baseline"),
        ("l2-split", "L2 candidate"),
        ("l3-resplit", "L3 candidate"),
        ("l4-noise", "L4 candidate"),
        ("fixture-swap", "L1 fixture identity"),
        ("arm-path", "candidate contract path identity"),
        ("always-load", "conditional reference loading"),
        ("missing-real-run", "L1 real implementation"),
    ],
)
def test_admission_oracle_rejects_false_success(fixture_spec, mutation, expected):
    spec, raw = fixture_spec
    evidence = valid_admission_example(spec, _sha256_text(raw))
    if mutation == "l1-tie":
        evidence["cases"]["L1"]["baseline"] = ["correct", "correct"]
    elif mutation == "l2-split":
        evidence["cases"]["L2"]["candidate"] = ["incorrect", "incorrect"]
    elif mutation == "l3-resplit":
        evidence["cases"]["L3"]["candidate"] = ["incorrect", "incorrect"]
    elif mutation == "l4-noise":
        evidence["cases"]["L4"]["candidate"] = ["incorrect", "incorrect"]
    elif mutation == "fixture-swap":
        evidence["fixtures"]["L1"]["head"] = evidence["fixtures"]["L2"]["head"]
    elif mutation == "arm-path":
        evidence["identities"]["candidate_changed_contract_paths"].append("loom-code/agents/implementer.md")
    elif mutation == "always-load":
        evidence["reference_loaded"]["L2"] = True
    else:
        evidence["real_runs"]["L1"] = None
    assert any(expected in failure for failure in admission_failures(evidence, spec, _sha256_text(raw)))


def test_observed_report_meets_admission_bar(fixture_spec):
    spec, raw = fixture_spec
    evidence, _ = _fenced_json(REPORT, "evidence")
    failures = admission_failures(evidence, spec, _sha256_text(raw))
    assert failures == [], "admission evidence is incomplete:\n- " + "\n- ".join(failures)
