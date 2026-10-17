"""finalize-review and the attestation validator decide an adversarial
execution by its runner row: a listed runner in its accepted form attests by
the passing tests its own output shows, an argv no row claims (or output its
row cannot read) attests only with a verdict reviewer's confirmation bound to
the content and quoting this run's output, and pytest/shell/direct execution
keeps today's rules.

The `go` and `mvn` runners are fakes on PATH that print a fixed output, so
these tests need neither toolchain; real runs belong to acceptance testing.
"""
# concern: A probe whose tests never ran must not be attested as having run.
from __future__ import annotations

import os
import sys
from pathlib import Path

from test_selection_finalize import CHANGE
from test_selection_finalize import PASSING
from test_selection_finalize import commit_all
from test_selection_finalize import finalize
from test_selection_finalize import git
from test_selection_finalize import make_repo
from test_selection_finalize import review_input
from test_selection_finalize import validate
from test_selection_finalize import written

from loom_checker.attestation import _command_digest

PROBES = f"docs/loom/{CHANGE}/evidence/probes"
GO = f"{PROBES}/attack_test.go"
JAVA = f"{PROBES}/AttackTest.java"
GO_PASS = (
    '{"Action":"start","Package":"example"}\n'
    '{"Action":"run","Package":"example","Test":"TestAttack"}\n'
    '{"Action":"pass","Package":"example","Test":"TestAttack","Elapsed":0}\n'
    '{"Action":"pass","Package":"example","Elapsed":0.01}\n'
)
GO_SKIP = GO_PASS.replace('"pass","Package":"example","Test"', '"skip","Package":"example","Test"')
MAVEN_LINE = "[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.02 s -- in AttackTest"
MAVEN_OUTPUT = f"[INFO] Running AttackTest\n{MAVEN_LINE}\n[INFO] BUILD SUCCESS\n"


def fake_runners(tmp_path: Path, output: str) -> dict:
    """`go` and `mvn` on PATH, each printing `output` and exiting 0."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    (tmp_path / "output.txt").write_text(output, encoding="utf-8")
    for name in ("go", "mvn"):
        runner = bin_dir / name
        runner.write_text(
            f"#!{sys.executable}\nimport sys\n"
            f"sys.stdout.write(open({str(tmp_path / 'output.txt')!r}).read())\n",
            encoding="utf-8",
        )
        runner.chmod(0o755)
    return {"PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}


def probe_repo(tmp_path: Path, *artifacts: str) -> Path:
    repo = make_repo(tmp_path)
    for artifact in artifacts:
        path = repo / artifact
        path.parent.mkdir(parents=True, exist_ok=True)
        comment = "#" if artifact.endswith((".py", ".sh")) else "//"
        path.write_text(f"{comment} concern: a boundary input the code never rejects\n",
                        encoding="utf-8")
    commit_all(repo, "probes")
    return repo


def confirmation(repo: Path, quote: str = MAVEN_LINE, reviewer: str = "r1",
                 sha: str = "HEAD") -> dict:
    return {"reviewer": reviewer, "reviewed_sha": git(repo, "rev-parse", sha), "quote": quote}


def run(repo: Path, tmp_path: Path, item: dict, output: str = GO_PASS):
    return finalize(repo, review_input(tmp_path, PASSING, [item]), fake_runners(tmp_path, output))


def adversarial(attestation: dict) -> dict:
    return next(run for run in attestation["executions"] if run["kind"] == "adversarial")


def go_attestation(tmp_path: Path) -> tuple[Path, dict]:
    repo = probe_repo(tmp_path, GO)
    result = run(repo, tmp_path, {"command": f"go test -json {GO}", "artifact": GO})
    assert result.returncode == 0, result.stderr
    return repo, written(repo)


# --- Acceptance 1 -----------------------------------------------------------

def test_go_parsed_probe_finalized_and_validated(tmp_path: Path) -> None:
    repo, attestation = go_attestation(tmp_path)
    execution = adversarial(attestation)
    assert (execution["evidence"], execution["passed"]) == ("parsed", 1)
    assert "confirmation" not in execution
    assert validate(repo, attestation) == []


def test_parsed_evidence_zero_passed_invalid(tmp_path: Path) -> None:
    repo, attestation = go_attestation(tmp_path)
    for forged in ({"passed": 0}, {"passed": True}, {"evidence": None}):
        execution = adversarial(attestation)
        original = dict(execution)
        execution.update(forged)
        assert validate(repo, attestation), forged
        execution.clear()
        execution.update(original)


# --- Acceptance 3 -----------------------------------------------------------

def test_listed_zero_passed_refused_even_with_confirmation(tmp_path: Path) -> None:
    repo = probe_repo(tmp_path, GO)
    line = GO_SKIP.splitlines()[1]
    result = run(repo, tmp_path, {
        "command": f"go test -json {GO}", "artifact": GO,
        "confirmation": confirmation(repo, quote=line),
    }, GO_SKIP)
    assert result.returncode == 1
    assert "no passing, non-skipped test" in result.stderr
    assert not (repo / f"docs/loom/{CHANGE}/attestation.json").exists()


def test_claimed_but_untargeted_refused(tmp_path: Path) -> None:
    repo = probe_repo(tmp_path, GO)
    result = run(repo, tmp_path, {
        "command": f"go test {GO}", "artifact": GO,
        "confirmation": confirmation(repo, quote=GO_PASS.splitlines()[1]),
    })
    assert result.returncode == 1
    assert "not in its accepted form" in result.stderr

    (tmp_path / "second").mkdir()
    repo, attestation = go_attestation(tmp_path / "second")
    execution = adversarial(attestation)
    execution["command"] = f"go test -json -run TestNothing {GO}"
    execution["command_digest"] = _command_digest(execution["command"])
    assert any("accepted form" in reason for _, reason in validate(repo, attestation))


# --- Acceptance 4 -----------------------------------------------------------

def test_unlisted_maven_with_confirmation_attested(tmp_path: Path) -> None:
    repo = probe_repo(tmp_path, JAVA)
    item = {"command": "mvn -q test -Dtest=AttackTest", "artifact": JAVA}
    missing = run(repo, tmp_path, item, MAVEN_OUTPUT)
    assert missing.returncode == 1
    assert "reviewer confirmation" in missing.stderr
    assert MAVEN_LINE in missing.stderr  # the output tail, as on a failed run

    item["confirmation"] = confirmation(repo)
    result = run(repo, tmp_path, item, MAVEN_OUTPUT)
    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    execution = adversarial(attestation)
    assert execution["evidence"] == "reviewer"
    assert execution["confirmation"] == {
        "reviewer": "r1", "reviewed_sha": git(repo, "rev-parse", "HEAD"),
        "content_digest": attestation["content_digest"], "quote": MAVEN_LINE,
    }
    assert validate(repo, attestation) == []


def test_other_content_or_partial_line_quote_refused(tmp_path: Path) -> None:
    repo = probe_repo(tmp_path, JAVA)
    item = {"command": "mvn -q test -Dtest=AttackTest", "artifact": JAVA}
    for bad, reason in (
        (confirmation(repo, sha="HEAD~1"), "reviewed_sha"),  # reviewed other content
        (confirmation(repo, quote=MAVEN_LINE[:40]), "quote"),  # part of a line
        (confirmation(repo, quote="[INFO] BUILD SUCCESS"), "quote"),  # no file stem
        (confirmation(repo, quote=f"{MAVEN_LINE}\n "), "quote"),  # plus a blank line
        (confirmation(repo, reviewer="someone-else"), "reviewer"),  # gave no verdict
    ):
        item["confirmation"] = bad
        result = run(repo, tmp_path, item, MAVEN_OUTPUT)
        assert result.returncode == 1, bad
        assert f"the confirmation's {reason}" in result.stderr, bad

    item["confirmation"] = confirmation(repo)
    assert run(repo, tmp_path, item, MAVEN_OUTPUT).returncode == 0
    attestation = written(repo)
    recorded = adversarial(attestation)["confirmation"]
    recorded["content_digest"] = "0" * 40
    assert validate(repo, attestation)
    recorded.update(content_digest=attestation["content_digest"], reviewer="someone-else")
    assert validate(repo, attestation)
    adversarial(attestation)["evidence"] = "parsed"
    adversarial(attestation)["passed"] = 1  # an argv no row claims cannot parse
    assert validate(repo, attestation)


def test_outside_reviewer_yaml_carries_probe_confirmations() -> None:
    from loom_checker.reviewers import _review_yaml_failure

    scores = dict.fromkeys(("omission", "ambiguity", "inconsistency", "incorrect-fact",
                            "missing-population", "deletion-first"), "PASS")
    verdict = {"verdict": "PASS", "lens": "docs", "reviewed_sha": "a" * 40,
               "review_target_sha": "b" * 40, "dimension_scores": scores,
               "findings": [], "notes": []}
    entry = {"artifact": JAVA, "reviewed_sha": "a" * 40, "quote": MAVEN_LINE}
    assert _review_yaml_failure({**verdict, "probe_confirmations": [entry]}, verdict) is None
    assert _review_yaml_failure(
        {**verdict, "probe_confirmations": [{**entry, "quote": ""}]}, verdict
    ) == "selected outside execution has malformed probe confirmations"


# --- Acceptance 5 -----------------------------------------------------------

def test_pytest_shell_attestation_unchanged(tmp_path: Path) -> None:
    python, shell = f"{PROBES}/probe_0.py", f"{PROBES}/probe_1.sh"
    repo = probe_repo(tmp_path, python, shell)
    result = finalize(repo, review_input(tmp_path, PASSING, [
        {"command": f"python3 {python}", "artifact": python},
        {"command": f"bash {shell}", "artifact": shell},
    ]))
    assert result.returncode == 0, result.stderr
    attestation = written(repo)
    assert [set(run) for run in attestation["executions"]] == [
        {"kind", "command", "artifact", "result", "command_digest"}] * 3
    assert validate(repo, attestation) == []


def test_python_noop_still_refused(tmp_path: Path) -> None:
    python = f"{PROBES}/probe_0.py"
    repo = probe_repo(tmp_path, python)
    result = finalize(repo, review_input(tmp_path, PASSING, [{
        "command": f"python3 -c pass {python}", "artifact": python,
        "confirmation": {"reviewer": "r1", "reviewed_sha": git(repo, "rev-parse", "HEAD"),
                         "quote": "probe_0"},
    }]))
    assert result.returncode == 1
    assert "command must execute the artifact directly" in result.stderr
