"""`pr-floor`: the read-only CI check on a pull request (plan W1-05).

Spec 2026-09-22-publication-floor-moves-to-github REQ-1, REQ-3, Design
decisions "Verification status — CI depth" and "Status is published by the
check, not read from the body". A bad body fails naming the heading; every
verification status passes and is published to the job summary and a
`::notice`; nothing is read from the body but its structure.
"""

from __future__ import annotations

import io
import os
from pathlib import Path

import pytest

from loom_checker.command_handlers.pr_floor import cmd_pr_floor
from loom_checker.rule_checks.publish import CONTEXTUAL_PR_HEADINGS
from test_verification_status import CHANGE
from test_verification_status import attestation
from test_verification_status import branch_repo
from test_verification_status import commit
from test_verification_status import commit_attestation
from test_verification_status import confirmed_intent
from test_verification_status import git


def body(skip_heading: str | None = None, extra_verification: str = "") -> str:
    parts = []
    for heading in CONTEXTUAL_PR_HEADINGS:
        if heading == skip_heading:
            continue
        text = f"The {heading.lower()} section says something concrete here."
        if heading == "Verification":
            text += extra_verification
        parts.append(f"## {heading}\n\n{text}\n")
    return "\n".join(parts)


def run(repo: Path, body_text: str, monkeypatch, tmp_path: Path, *extra: str):
    body_file = tmp_path / "body.md"
    body_file.write_text(body_text, encoding="utf-8")
    summary = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    monkeypatch.chdir(repo)
    base = git(repo, "rev-parse", "main")
    head = git(repo, "rev-parse", "HEAD")
    out, err = io.StringIO(), io.StringIO()
    code = cmd_pr_floor(
        ["--body-file", str(body_file), "--base", base, "--head", head, *extra], out, err
    )
    written = summary.read_text(encoding="utf-8") if summary.exists() else ""
    return code, out.getvalue(), err.getvalue(), written


def identified_repo(tmp_path: Path) -> Path:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    return repo


# --- A1: the body floor -----------------------------------------------------


def test_bad_body_exit_1_names_heading(tmp_path: Path, monkeypatch) -> None:
    repo = identified_repo(tmp_path)
    code, _out, err, _summary = run(repo, body("Scope"), monkeypatch, tmp_path)
    assert code == 1
    assert err.startswith("BLOCK ci.pr-floor: ")
    assert 'heading "Scope" is missing' in err


def test_good_body_exit_0(tmp_path: Path, monkeypatch) -> None:
    repo = identified_repo(tmp_path)
    code, _out, err, _summary = run(repo, body(), monkeypatch, tmp_path)
    assert code == 0, err


# --- A3: status published by the check ---------------------------------------


def test_status_in_summary_and_notice(tmp_path: Path, monkeypatch) -> None:
    repo = identified_repo(tmp_path)
    commit_attestation(repo, attestation(repo, skip=["adversarial"]))
    code, out, _err, summary = run(repo, body(), monkeypatch, tmp_path)
    assert code == 0
    assert "verification: valid (skipped: adversarial)" in summary
    assert "::notice title=verification::valid (skipped: adversarial)" in out


def test_body_status_text_ignored(tmp_path: Path, monkeypatch) -> None:
    repo = identified_repo(tmp_path)
    claim = "\n\nVerification status: valid\n"
    code, out, _err, summary = run(repo, body(extra_verification=claim), monkeypatch, tmp_path)
    assert code == 0
    assert "verification: absent" in summary
    assert "::notice title=verification::absent" in out
    assert "valid" not in summary


@pytest.mark.parametrize("branch", [None, "wip"])
def test_unidentified_change_is_stale_and_passes(tmp_path: Path, monkeypatch, branch) -> None:
    repo = branch_repo(tmp_path, "wip")
    (repo / "src.py").write_text("VALUE = 3\n", encoding="utf-8")
    commit(repo, "no intent")
    extra = ("--branch", branch) if branch else ()
    code, out, _err, summary = run(repo, body(), monkeypatch, tmp_path, *extra)
    assert code == 0
    assert "::notice title=verification::stale (change not identified: " in out
    assert "verification: stale (change not identified: " in summary


def test_branch_flag_names_the_change(tmp_path: Path, monkeypatch) -> None:
    # A detached CI checkout: the branch comes from the event, not HEAD.
    repo = identified_repo(tmp_path)
    confirmed_intent(repo, "2026-09-21-other")
    commit(repo, "second intent")
    git(repo, "checkout", "-q", "--detach")
    code, out, _err, _summary = run(
        repo, body(), monkeypatch, tmp_path, "--branch", f"feat/{CHANGE}"
    )
    assert code == 0
    assert "::notice title=verification::absent" in out


def test_notice_escapes_workflow_command_text(tmp_path: Path, monkeypatch) -> None:
    # Status text can carry PR-controlled strings; a newline must not start a
    # second workflow command.
    from loom_checker.command_handlers import pr_floor

    monkeypatch.setattr(
        pr_floor, "verification_status", lambda *_a, **_k: "stale (a%b\r\n::error::x)"
    )
    repo = identified_repo(tmp_path)
    code, out, _err, _summary = run(repo, body(), monkeypatch, tmp_path)
    assert code == 0
    assert out == "::notice title=verification::stale (a%25b%0D%0A::error::x)\n"


def test_no_summary_env_still_prints_notice(tmp_path: Path, monkeypatch) -> None:
    repo = identified_repo(tmp_path)
    body_file = tmp_path / "body.md"
    body_file.write_text(body(), encoding="utf-8")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.chdir(repo)
    out = io.StringIO()
    code = cmd_pr_floor(
        ["--body-file", str(body_file), "--base", git(repo, "rev-parse", "main"),
         "--head", "HEAD"], out, io.StringIO(),
    )
    assert code == 0
    assert "::notice title=verification::absent" in out.getvalue()
    assert "GITHUB_STEP_SUMMARY" not in os.environ
