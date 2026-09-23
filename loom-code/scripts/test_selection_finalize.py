"""Finalization and attestation v2 under a bound step selection (plan W2-03).

Spec 2026-09-14-expert-mode-step-selection REQ-2, REQ-3, REQ-7, REQ-11 and
decisions 3, 6, 8, 9: finalize-review waives exactly the checks of steps a
user-typed confirmation skipped, records a failure event on every non-zero
exit, and the v2 attestation carries a `selection` the validator re-reads
from the local records.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from loom_checker import attestation as attestation_module
from loom_checker import intent_state
from loom_checker import selection

import pytest

CHECKER = Path(__file__).with_name("loom_checker.py")
CHANGE = "2026-09-14-example"


@pytest.fixture(autouse=True)
def no_host_session(monkeypatch):
    """Tests never inherit the real Claude Code session running the suite."""
    for name in ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT"):
        monkeypatch.delenv(name, raising=False)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def commit_all(repo: Path, message: str) -> str:
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def make_repo(tmp_path: Path, package: str = "python3 -c pass") -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.parent.mkdir(parents=True)
    kickoff.write_text(f"- package-tests: {package} — fixture (2026-09-14)\n", encoding="utf-8")
    commit_all(repo, "base")
    git(repo, "checkout", "-q", "-b", "feature")
    (repo / "feature.py").write_text("ENABLED = True\n", encoding="utf-8")
    commit_all(repo, "feature")
    return repo


def make_narrow_repo(tmp_path: Path) -> Path:
    """A repo whose branch delta is mechanically narrow: one low-risk doc."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.parent.mkdir(parents=True)
    kickoff.write_text("- package-tests: python3 -c pass — fixture (2026-09-23)\n", encoding="utf-8")
    commit_all(repo, "base")
    git(repo, "checkout", "-q", "-b", "feature")
    guide = repo / "docs/guide.md"
    guide.write_text("# guide\n", encoding="utf-8")
    commit_all(repo, "doc")
    return repo


def propose(repo: Path, skip: str) -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER), "selection", "propose", CHANGE,
         "--origin", "user", "--skip", skip],
        capture_output=True, text=True, cwd=str(repo),
    )
    assert result.returncode == 0, result.stderr


def confirm(repo: Path, at: str, source: str = "user-typed", tamper: bool = False) -> dict:
    """Stand in for the W2-01 capture hook: bind the newest proposal."""
    proposal = [e for e in selection.read_events(repo, CHANGE) if e["event"] == "proposal"][-1]
    text = f"/loom-code:expert-mode 確認 {proposal['code']}"
    event = {
        "event": "confirmation", "proposal_id": proposal["id"], "code": proposal["code"],
        "source": source, "session_id": "s1", "prompt_ref": "p1",
        "prompt_text": text + (" extra" if tamper else ""),
        "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "branch": proposal["branch"], "merge_base": proposal["merge_base"], "at": at,
    }
    selection.append_event(repo, CHANGE, event)
    return event


def review_input(tmp_path: Path, verdicts: list, adversarial: list) -> Path:
    path = tmp_path / "review-input.json"
    path.write_text(json.dumps(
        {"verdicts": verdicts, "findings": [], "adversarial": adversarial}
    ), encoding="utf-8")
    return path


def finalize(repo: Path, input_path: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "finalize-review", CHANGE, "--input", str(input_path)],
        capture_output=True, text=True, cwd=str(repo), env=dict(os.environ, **(env or {})),
    )


def written(repo: Path) -> dict:
    return json.loads((repo / f"docs/loom/{CHANGE}/attestation.json").read_text(encoding="utf-8"))


def validate(repo: Path, attestation: dict) -> list:
    return attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, None
    )


def failures(repo: Path) -> list[dict]:
    return [e for e in selection.read_events(repo, CHANGE) if e["event"] == "failure"]


def shift(stamp: str, seconds: int) -> str:
    moment = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return (moment + timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


PASSING = [
    {"reviewer": "r1", "vendor": "openai", "model": "m", "lens": "code", "verdict": "PASS", "findings": []},
    {"reviewer": "r2", "vendor": "other", "model": "m", "lens": "code", "verdict": "PASS", "findings": []},
]


# --- Acceptance 3 -----------------------------------------------------------

def test_bound_skip_of_reviewers_and_adversarial_validates(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    propose(repo, "reviewers,adversarial")
    event = confirm(repo, "2026-09-14T00:00:00Z")

    result = finalize(repo, review_input(tmp_path, [], []))

    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    assert attestation["schema"] == "loom-attestation/v2"
    assert attestation["verdicts"] == []
    assert [run["kind"] for run in attestation["executions"]] == ["package-tests"]
    assert attestation["selection"] == {
        "confirmations": [{"code": event["code"], "skip": ["reviewers", "adversarial"],
                           "source": "user-typed", "at": "2026-09-14T00:00:00Z"}],
        "skip": ["reviewers", "adversarial"],
        "source": "user-typed",
        "prior_failures": [],
    }
    assert validate(repo, attestation) == []
    # The merged witness shape accepts the v2 evidence too.
    assert intent_state._delivery_witness_valid(attestation, CHANGE)


def test_narrow_delta_finalizes_with_no_adversarial_artifact(tmp_path: Path) -> None:
    """A narrow delta auto-skips the adversarial step, with no typed skip."""
    repo = make_narrow_repo(tmp_path)

    result = finalize(repo, review_input(tmp_path, PASSING[:1], []))

    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    assert [run["kind"] for run in attestation["executions"]] == ["package-tests"]
    assert attestation["selection"] is None  # no typed confirmation was bound
    assert validate(repo, attestation) == []
    assert attestation_module.validate_attestation(
        repo, git(repo, "rev-parse", "HEAD"), CHANGE, attestation, None,
        claimed_selection=True,
    ) == []


def test_finalize_and_attestation_refuse_alike_with_one_message(tmp_path: Path) -> None:
    """Acceptance 10: one predicate, one message, both call sites."""
    from loom_checker.probes import missing_adversarial_execution

    reason = missing_adversarial_execution(0, set())
    assert reason and missing_adversarial_execution(1, set()) is None
    assert missing_adversarial_execution(0, {"adversarial"}) is None

    repo = make_repo(tmp_path)
    refused = finalize(repo, review_input(tmp_path, PASSING, []))
    assert refused.returncode == 1
    assert f"BLOCK finalize.adversarial: {reason}" in refused.stderr

    accepted = finalize(repo, review_input(
        tmp_path, PASSING, [{"command": "python3 src.py", "artifact": "src.py"}]
    ))
    assert accepted.returncode == 0, accepted.stderr
    attestation = written(repo)
    stripped = dict(attestation, executions=[
        run for run in attestation["executions"] if run["kind"] != "adversarial"
    ])
    assert [msg for _, msg in validate(repo, stripped)] == [reason]


def write_probes(repo: Path, count: int, concern: bool = True) -> None:
    """Commit `count` probe programs for this change, replacing any earlier set."""
    directory = repo / f"docs/loom/{CHANGE}/evidence/probes"
    if directory.is_dir():
        for stale in directory.iterdir():
            stale.unlink()
    directory.mkdir(parents=True, exist_ok=True)
    head = "# concern: a boundary input the code never rejects\n" if concern else ""
    for index in range(count):
        (directory / f"probe_{index}.py").write_text(
            f'"""Probe {index}."""\n{head}assert True\n', encoding="utf-8"
        )
    commit_all(repo, f"probes {count}")


def run_with_probes(repo: Path, tmp_path: Path) -> subprocess.CompletedProcess:
    return finalize(repo, review_input(
        tmp_path, PASSING, [{"command": "python3 src.py", "artifact": "src.py"}]
    ))


def test_five_probe_programs_pass_and_a_sixth_is_refused(tmp_path: Path) -> None:
    """Acceptance 3: at most five committed probe programs for a change."""
    repo = make_repo(tmp_path)
    write_probes(repo, 5)
    accepted = run_with_probes(repo, tmp_path)
    assert accepted.returncode == 0, accepted.stderr

    write_probes(repo, 6)
    refused = run_with_probes(repo, tmp_path)
    assert refused.returncode == 1
    assert "BLOCK adversarial.proportionate" in refused.stderr
    assert "six" in refused.stderr or "6" in refused.stderr


def test_probe_program_without_a_concern_line_is_refused(tmp_path: Path) -> None:
    """Acceptance 4: every committed probe program names what it defends against."""
    repo = make_repo(tmp_path)
    write_probes(repo, 2, concern=False)

    refused = run_with_probes(repo, tmp_path)

    assert refused.returncode == 1
    assert "BLOCK adversarial.proportionate" in refused.stderr
    assert "concern:" in refused.stderr
    assert "probe_0.py" in refused.stderr


def test_skipping_every_executed_step_allows_empty_executions(tmp_path: Path) -> None:
    repo = make_repo(tmp_path, package="python3 -c 'raise SystemExit(3)'")
    propose(repo, "reviewers,adversarial,package-tests")
    confirm(repo, "2026-09-14T00:00:00Z")

    result = finalize(repo, review_input(tmp_path, [], []))

    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    assert attestation["executions"] == []
    assert validate(repo, attestation) == []


def test_unbound_skip_refused_and_digest_mismatch_blocks(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    # A proposal alone binds nothing: today's floors apply.
    propose(repo, "reviewers,adversarial")
    refused = finalize(repo, review_input(tmp_path, [], []))
    assert refused.returncode == 1
    assert "finalize.verdicts" in refused.stderr

    # Neither an agent-recorded source nor a tampered prompt binds.
    confirm(repo, "2026-09-14T00:00:00Z", source="agent-recorded")
    assert "finalize.verdicts" in finalize(repo, review_input(tmp_path, [], [])).stderr
    confirm(repo, "2026-09-14T00:00:01Z", tamper=True)
    assert "finalize.verdicts" in finalize(repo, review_input(tmp_path, [], [])).stderr

    # A skip of reviewers does not waive the adversarial floor.
    confirm(repo, "2026-09-14T00:00:02Z")
    propose(repo, "reviewers")
    confirm(repo, "2026-09-14T00:00:03Z")
    partial = finalize(repo, review_input(tmp_path, [], []))
    assert partial.returncode == 1
    assert "finalize.adversarial" in partial.stderr

    # Bound skip validates; an attestation claiming a skip the records do not
    # hold (records cancelled) is refused, and so is a digest mismatch.
    propose(repo, "reviewers,adversarial")
    confirm(repo, "2026-09-14T00:00:04Z")
    assert finalize(repo, review_input(tmp_path, [], [])).returncode == 0
    attestation = written(repo)
    assert validate(repo, attestation) == []

    forged = dict(attestation, selection=None)
    assert any("selection" in reason for _, reason in validate(repo, forged))

    selection.append_event(repo, CHANGE, {
        "event": "cancel", "source": "agent-run", "prompt_ref": None,
        "branch": attestation_branch(repo), "merge_base": event_base(repo),
        "at": "2026-09-14T00:00:05Z",
    })
    assert any("selection" in reason for _, reason in validate(repo, attestation))

    (repo / "src.py").write_text("VALUE = 2\n", encoding="utf-8")
    commit_all(repo, "functional change")
    propose(repo, "reviewers,adversarial")
    confirm(repo, "2026-09-14T00:00:06Z")
    stale = validate(repo, attestation)
    assert any("functional content digest" in reason for _, reason in stale)


def test_v2_without_selection_keeps_every_floor(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    assert finalize(repo, review_input(
        tmp_path, PASSING, [{"command": "python3 src.py", "artifact": "src.py"}]
    )).returncode == 0
    attestation = written(repo)
    assert attestation["schema"] == "loom-attestation/v2"
    assert attestation["selection"] is None
    assert validate(repo, attestation) == []
    for mutate in (
        lambda a: a.update(verdicts=[]),
        lambda a: a.update(executions=[x for x in a["executions"] if x["kind"] != "adversarial"]),
        lambda a: a.update(executions=[x for x in a["executions"] if x["kind"] != "package-tests"]),
    ):
        broken = json.loads(json.dumps(attestation))
        mutate(broken)
        assert validate(repo, broken) != []


def attestation_branch(repo: Path) -> str:
    return git(repo, "rev-parse", "--abbrev-ref", "HEAD")


def event_base(repo: Path) -> str:
    return selection.current_scope(repo)[1]


# --- Acceptance 7 -----------------------------------------------------------

def test_finalize_failure_recorded_and_listed_as_prior(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    refused = finalize(repo, review_input(tmp_path, [], []))
    assert refused.returncode == 1

    recorded = failures(repo)
    assert len(recorded) == 1
    failure = recorded[0]
    assert failure["step"] == "reviewers"
    assert failure["rule"] == "finalize.verdicts"
    assert failure["head_sha"] == git(repo, "rev-parse", "HEAD")
    assert failure["branch"] == "feature"

    propose(repo, "reviewers,adversarial")
    confirm(repo, shift(failure["at"], 1))
    result = finalize(repo, review_input(tmp_path, [], []))

    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    assert attestation["selection"]["prior_failures"] == [
        {key: failure[key] for key in ("step", "rule", "head_sha", "branch", "at")}
    ]
    assert validate(repo, attestation) == []


def test_confirmation_from_another_session_keeps_the_full_floor(tmp_path: Path, monkeypatch) -> None:
    """Spec decision 18 (c): a confirmation recorded by a nested session
    (`timeout 60 claude -p`, `script -q /dev/null claude -p`, `npx
    @anthropic-ai/claude-code -p`) carries that session's id, so finalize in
    the attended session refuses the skip; the recording session may use it."""
    repo = make_repo(tmp_path)
    propose(repo, "reviewers,adversarial")
    confirm(repo, "2026-09-14T00:00:00Z")  # recorded with session_id "s1"

    refused = finalize(repo, review_input(tmp_path, [], []), env={"CLAUDE_CODE_SESSION_ID": "other"})
    assert refused.returncode == 1 and "finalize.verdicts" in refused.stderr

    accepted = finalize(repo, review_input(tmp_path, [], []), env={"CLAUDE_CODE_SESSION_ID": "s1"})
    assert accepted.returncode == 0, accepted.stderr
    attestation = written(repo)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "s1")
    assert validate(repo, attestation) == []
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "other")
    assert attestation_module.selection_evidence(repo, CHANGE) is None
    assert any("selection" in reason for _, reason in validate(repo, attestation))


def test_cancelled_confirmation_is_not_disclosed(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    propose(repo, "reviewers")
    confirm(repo, "2026-09-14T00:00:01Z")
    selection.append_event(repo, CHANGE, {
        "event": "cancel", "source": "agent-run", "prompt_ref": None,
        "branch": attestation_branch(repo), "merge_base": event_base(repo),
        "at": "2026-09-14T00:00:02Z",
    })
    propose(repo, "adversarial")
    second = confirm(repo, "2026-09-14T00:00:03Z")
    evidence = attestation_module.selection_evidence(repo, CHANGE)
    assert evidence["skip"] == ["adversarial"]
    assert evidence["confirmations"] == [{"code": second["code"], "skip": ["adversarial"],
                                          "source": "user-typed", "at": "2026-09-14T00:00:03Z"}]


def test_prior_failure_decided_by_record_order_not_timestamp(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    branch = attestation_branch(repo)
    same_second = "2026-09-14T00:00:05Z"
    selection.append_event(repo, CHANGE, {
        "event": "failure", "step": "reviewers", "rule": "before", "head_sha": "h",
        "branch": branch, "at": same_second})
    propose(repo, "reviewers")
    confirm(repo, same_second)
    selection.append_event(repo, CHANGE, {
        "event": "failure", "step": "reviewers", "rule": "after", "head_sha": "h",
        "branch": branch, "at": "2026-09-14T00:00:00Z"})
    prior = attestation_module.selection_evidence(repo, CHANGE)["prior_failures"]
    assert [f["rule"] for f in prior] == ["before"]


def test_non_verification_refusals_record_no_failure(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    usage = subprocess.run(
        [sys.executable, str(CHECKER), "finalize-review", CHANGE, "--bogus"],
        capture_output=True, text=True, cwd=str(repo))
    assert usage.returncode == 2
    (repo / "dirty.txt").write_text("x", encoding="utf-8")
    dirty = finalize(repo, review_input(tmp_path, [], []))
    assert dirty.returncode == 1 and "finalize.clean-tree" in dirty.stderr
    assert failures(repo) == []


def test_failure_after_confirmation_not_listed_as_prior(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    propose(repo, "reviewers")
    confirm(repo, "2026-01-01T00:00:00Z")
    refused = finalize(repo, review_input(tmp_path, [], []))
    assert refused.returncode == 1
    assert [e["rule"] for e in failures(repo)] == ["finalize.adversarial"]

    result = finalize(repo, review_input(
        tmp_path, [], [{"command": "python3 src.py", "artifact": "src.py"}]
    ))

    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    assert attestation["selection"]["prior_failures"] == []
    assert validate(repo, attestation) == []
