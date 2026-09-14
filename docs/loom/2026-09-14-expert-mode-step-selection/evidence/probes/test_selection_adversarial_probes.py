"""Adversarial probes for the expert-mode step-selection change.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-14-expert-mode-step-selection/evidence/probes/test_selection_adversarial_probes.py -q

Two families, selectable by keyword:

  -k "survives or boundary"    attempts the change SURVIVES and accepted
                               design boundaries; these PASS.
  -k defect                    attempts that EXPOSE a defect; these FAIL on
                               purpose. Do not weaken them.

The probes drive the real checker modules (loom_checker.selection,
loom_checker.attestation, loom_checker.rule_checks.*) that this change adds.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

# The change under test lives in loom-code/scripts; put it on the path the
# same way the repo's own package tests are run (they run with that cwd).
REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = REPO_ROOT / "loom-code" / "scripts"
assert (SCRIPTS / "loom_checker" / "selection.py").is_file(), SCRIPTS
sys.path.insert(0, str(SCRIPTS))

from loom_checker import attestation as att  # noqa: E402
from loom_checker import selection  # noqa: E402
from loom_checker.rule_checks import selection_guard  # noqa: E402
from loom_checker.rule_checks.publish import (  # noqa: E402
    render_selection_disclosure,
    validate_selection_disclosure,
)

CHANGE = "2026-09-14-example"
CHECKER = str(SCRIPTS / "loom_checker.py")
HOST_VARS = ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT")
SESSION = "sess-attended"
NESTED = "sess-nested"


@pytest.fixture(autouse=True)
def no_host_session(monkeypatch):
    """Probes never inherit the real Claude Code session running them."""
    for name in HOST_VARS:
        monkeypatch.delenv(name, raising=False)


def clean_env(**host: str) -> dict:
    """An explicit subprocess env with no inherited host-session variables."""
    env = {k: v for k, v in os.environ.items() if k not in HOST_VARS}
    env.update(host)
    return env


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True,
        env=clean_env(),
    ).stdout.strip()


def make_repo(tmp_path: Path, *, with_package: bool = False) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    if with_package:
        kickoff = repo / "docs/loom/KICKOFF-DEFAULTS.md"
        kickoff.parent.mkdir(parents=True)
        kickoff.write_text(
            "- package-tests: python3 -c pass — fixture (2026-09-14)\n", encoding="utf-8"
        )
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "checkout", "-q", "-b", "feature")
    (repo / "feature.py").write_text("ENABLED = True\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "feature")
    return repo


def add_proposal(repo: Path, skip: list[str], at: str) -> tuple[str, str]:
    branch, base = selection.current_scope(repo)
    names = [s["name"] for s in selection.step_vocabulary()]
    sk = [n for n in names if n in skip]
    run = [n for n in names if n not in sk]
    code = selection.selection_code(CHANGE, run, sk)
    pid = uuid.uuid4().hex
    selection.append_event(repo, CHANGE, {
        "event": "proposal", "id": pid, "code": code, "origin": "user",
        "run": run, "skip": sk, "branch": branch, "merge_base": base, "created_at": at,
    })
    return pid, code


def add_confirmation(repo: Path, pid: str, code: str, at: str, *, tamper: bool = False) -> None:
    branch, base = selection.current_scope(repo)
    text = f"/loom-code:expert-mode 確認 {code}"
    selection.append_event(repo, CHANGE, {
        "event": "confirmation", "proposal_id": pid, "code": code, "source": "user-typed",
        "session_id": "s1", "prompt_ref": "p1",
        "prompt_text": text + (" tampered" if tamper else ""),
        "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "branch": branch, "merge_base": base, "at": at,
    })


def add_cancel(repo: Path, at: str) -> None:
    branch, base = selection.current_scope(repo)
    selection.append_event(repo, CHANGE, {
        "event": "cancel", "source": "user-typed", "prompt_ref": "p1",
        "branch": branch, "merge_base": base, "at": at,
    })


def finalize_via_cli(repo: Path, tmp_path: Path, **host: str) -> subprocess.CompletedProcess:
    review = tmp_path / "review-input.json"
    review.write_text(json.dumps({"verdicts": [], "findings": [], "adversarial": []}), "utf-8")
    return subprocess.run(
        [sys.executable, CHECKER, "finalize-review", CHANGE, "--input", str(review)],
        capture_output=True, text=True, cwd=str(repo), env=clean_env(**host),
    )


def capture_via_cli(repo: Path, prompt: str, session_id: str, **host: str):
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": prompt,
               "session_id": session_id, "prompt_id": "prompt-1"}
    return subprocess.run(
        [sys.executable, CHECKER, "selection", "capture", "--hook"],
        input=json.dumps(payload), capture_output=True, text=True, cwd=str(repo),
        env=clean_env(**host),
    )


def confirmations(repo: Path) -> list[dict]:
    return [e for e in selection.read_events(repo, CHANGE) if e["event"] == "confirmation"]


# ===========================================================================
# NESTED-SESSION ATTACKS (round-2 bypass) — must bind nothing; these PASS.
# ===========================================================================

@pytest.mark.parametrize("wrapper", [
    'timeout 60 claude -p "/expert-mode {code}"',
    'script -q /dev/null claude -p "/expert-mode {code}"',
    'npx @anthropic-ai/claude-code -p "/expert-mode {code}"',
])
def test_capture_survives_nested_session_confirmation_binds_nothing(
    tmp_path: Path, wrapper: str,
) -> None:
    """The agent launches a nested headless session through a wrapper the text
    guard misses. That session's prompt hook sees a new session_id and runs
    with CLAUDE_CODE_SESSION_ATTENDED=0, so its `/expert-mode <code>` prompt
    must record no confirmation and nothing may bind."""
    repo = make_repo(tmp_path)
    _pid, code = add_proposal(repo, ["reviewers", "adversarial"], "2026-09-14T00:00:00Z")
    command = wrapper.format(code=code)
    nested_prompt = command.split('"')[1]
    result = capture_via_cli(repo, nested_prompt, NESTED, CLAUDE_CODE_SESSION_ID=NESTED,
                             CLAUDE_CODE_SESSION_ATTENDED="0",
                             CLAUDE_CODE_ENTRYPOINT="sdk-cli")
    assert result.returncode == 0, result.stderr
    assert confirmations(repo) == [], command
    assert att.selection_evidence(repo, CHANGE, None) is None


def test_capture_survives_same_session_unattended_binds_nothing(tmp_path: Path) -> None:
    """Even a payload carrying the attended session's id binds nothing when the
    capturing process is unattended (ATTENDED=0)."""
    repo = make_repo(tmp_path)
    _pid, code = add_proposal(repo, ["reviewers"], "2026-09-14T00:00:00Z")
    result = capture_via_cli(repo, f"/expert-mode {code}", SESSION,
                             CLAUDE_CODE_SESSION_ID=SESSION,
                             CLAUDE_CODE_SESSION_ATTENDED="0")
    assert result.returncode == 0, result.stderr
    assert confirmations(repo) == []


def test_finalize_survives_other_session_keeps_full_floor(tmp_path: Path) -> None:
    """A confirmation genuinely captured in the attended session must not waive
    anything for a finalize running in a different Claude Code session."""
    repo = make_repo(tmp_path, with_package=True)
    _pid, code = add_proposal(repo, ["reviewers", "adversarial"], "2026-09-14T00:00:00Z")
    captured = capture_via_cli(repo, f"/expert-mode {code}", SESSION,
                               CLAUDE_CODE_SESSION_ID=SESSION)
    assert captured.returncode == 0, captured.stderr
    assert len(confirmations(repo)) == 1, "precondition: the attended capture bound"
    result = finalize_via_cli(repo, tmp_path, CLAUDE_CODE_SESSION_ID=NESTED)
    assert result.returncode != 0, "finalize in another session waived the floor"
    assert "finalize.verdicts" in result.stderr, result.stderr
    assert not (repo / f"docs/loom/{CHANGE}/attestation.json").exists()


# ===========================================================================
# SURVIVED ATTEMPTS — the change withstands these; they PASS.
# ===========================================================================

@pytest.mark.parametrize("command", [
    "python3 loom_checker.py selection capture --hook",
    "tee $(git rev-parse --git-common-dir)/loom/selections/x.jsonl < e",
    "echo x >> .git/loom/selections/2026-09-14-example.jsonl",
    "cd \"$(git rev-parse --git-common-dir)/loom\" && tee selections/x < e",
    "python3 -c 'open(\"x\",\"w\")' --git-dir=/tmp/g",
])
def test_bash_guard_survives_known_write_shortcuts(command: str) -> None:
    """The guard denies every write form the design claims to recognise."""
    assert selection_guard.bash_guard_reason(command) is not None


def test_file_tool_guard_survives_write_under_loom_dir(tmp_path: Path) -> None:
    """A Write whose target resolves under <git common dir>/loom is denied."""
    repo = make_repo(tmp_path)
    common = git(repo, "rev-parse", "--git-common-dir")
    common_abs = (repo / common).resolve() if not Path(common).is_absolute() else Path(common)
    target = common_abs / "loom" / "selections" / f"{CHANGE}.jsonl"
    reason = selection_guard.guard_reason({
        "tool_name": "Write", "cwd": str(repo),
        "tool_input": {"file_path": str(target), "content": "forged"},
    })
    assert reason is not None


def test_capture_survives_and_never_blocks_garbage_stdin() -> None:
    """The capture hook exits 0 (never blocks the prompt) on junk input."""
    result = subprocess.run(
        [sys.executable, CHECKER, "selection", "capture", "--hook"],
        input="not json at all", capture_output=True, text=True, env=clean_env(),
    )
    assert result.returncode == 0


def test_validate_survives_forged_confirmation_with_tampered_text(tmp_path: Path) -> None:
    """A confirmation whose prompt_text no longer hashes to its sha binds nothing."""
    repo = make_repo(tmp_path)
    pid, code = add_proposal(repo, ["reviewers", "adversarial"], "2026-09-14T00:00:00Z")
    add_confirmation(repo, pid, code, "2026-09-14T00:00:01Z", tamper=True)
    assert att.selection_evidence(repo, CHANGE, None) is None


def test_validate_survives_reviewers_skip_without_waiving_package_or_adversarial(
    tmp_path: Path,
) -> None:
    """Skipping only reviewers must NOT waive package-tests or adversarial.

    Build a real tree so the digest matches, then present a v2 attestation
    with empty executions and skip=[reviewers]: the executions floor must
    still fire because reviewers-only skip does not cover
    {package-tests, adversarial}.
    """
    from loom_checker.digest import functional_content_digest

    repo = make_repo(tmp_path, with_package=True)
    pid, code = add_proposal(repo, ["reviewers"], "2026-09-14T00:00:00Z")
    add_confirmation(repo, pid, code, "2026-09-14T00:00:01Z")
    head = git(repo, "rev-parse", "HEAD")
    digest = functional_content_digest(repo, head, CHANGE, None)
    bound = att.selection_evidence(repo, CHANGE, None)
    assert bound["skip"] == ["reviewers"], bound
    attestation = {
        "schema": att.ATTESTATION_SCHEMA, "change_id": CHANGE,
        "content_digest": digest, "executions": [],
        "verdicts": [], "findings": [], "selection": bound,
    }
    findings = att.validate_attestation(repo, head, CHANGE, attestation, None)
    # It is rejected for a missing execution, NOT waived: package-tests and
    # adversarial are outside a reviewers-only skip.
    assert any("no successful functional executions" in reason
               for _rule, reason in findings), findings


def test_disclosure_survives_missing_skipped_steps_line() -> None:
    """publish rejects a body that omits the required skipped-steps line."""
    attestation = {"selection": {
        "confirmations": [{"code": "K7Q2", "skip": ["reviewers"],
                           "source": "user-typed", "at": "2026-09-14T00:00:00Z"}],
        "skip": ["reviewers"], "source": "user-typed", "prior_failures": []}}
    body = (
        "## Summary\nx\n## Motivation\nx\n## Reversibility\nx\n## Alternatives\nx\n"
        "## Risks\nx\n## Verification\nnothing disclosed here\n## Rollout\nx\n"
        "## Follow-ups\nx\n## Links\nx\n"
    )
    assert validate_selection_disclosure(body, attestation) is not None


def test_disclosure_survives_false_line_with_null_selection() -> None:
    """publish rejects a skipped-steps line when the attestation has no selection."""
    body = (
        "## Summary\nx\n## Motivation\nx\n## Reversibility\nx\n## Alternatives\nx\n"
        "## Risks\nx\n## Verification\nSkipped steps: reviewers — authority: user-typed (K7Q2, 2026-09-14)\n"
        "## Rollout\nx\n## Follow-ups\nx\n## Links\nx\n"
    )
    assert validate_selection_disclosure(body, {"selection": None}) is not None


# ===========================================================================
# DEFECT PROBES — these FAIL on purpose, exposing a real defect. Do NOT weaken.
# ===========================================================================

def test_prior_failure_defect_branch_rename_sheds_recorded_failure(tmp_path: Path) -> None:
    """A recorded reviewer failure must survive a branch rename.

    Failures are scoped by the branch NAME only. Renaming the branch
    (`git branch -m`) — the same tree, the same change — drops every prior
    failure, so an author can shed recorded failures and then rebind a fresh
    selection and publish with no `Prior failure:` disclosure.
    """
    repo = make_repo(tmp_path)
    selection.append_event(repo, CHANGE, {
        "event": "failure", "step": "reviewers", "rule": "finalize.verdicts",
        "head_sha": git(repo, "rev-parse", "HEAD"), "branch": "feature",
        "at": "2026-09-14T00:00:00Z",
    })
    git(repo, "branch", "-m", "feature-clean")
    surviving = selection.effective_selection(repo, CHANGE)["failures"]
    assert len(surviving) == 1, (
        "branch rename erased the recorded prior failure: "
        f"{len(surviving)} of 1 survived"
    )


def test_boundary_fresh_clone_refuses_bound_selection_loudly(tmp_path: Path) -> None:
    """Accepted boundary (spec decision 9): publication re-reads the untracked
    local selection records instead of trusting the committed `selection`
    field. Where those records are absent (a fresh clone, CI), a bound
    selection is refused, and the refusal must be loud and name the
    local-records mismatch rather than pass silently.
    """
    repo = make_repo(tmp_path, with_package=True)
    pid, code = add_proposal(
        repo, ["reviewers", "adversarial", "package-tests"], "2026-09-14T00:00:00Z"
    )
    add_confirmation(repo, pid, code, "2026-09-14T00:00:01Z")
    result = finalize_via_cli(repo, tmp_path)
    assert result.returncode == 0, result.stderr
    attestation = json.loads(
        (repo / f"docs/loom/{CHANGE}/attestation.json").read_text("utf-8")
    )
    head = git(repo, "rev-parse", "HEAD")
    # Simulate a clean clone / CI: the untracked selection records are gone.
    selection.store_path(repo, CHANGE).unlink()
    findings = att.validate_attestation(repo, head, CHANGE, attestation, None)
    assert findings, "fresh clone silently accepted a bound selection"
    assert any(rule == "push.attestation" and "local selection records" in reason
               for rule, reason in findings), findings


def test_boundary_hand_edited_selection_field_refused_without_record(tmp_path: Path) -> None:
    """A hand-edited attestation.json whose `selection` claims reviewers were
    skipped (with empty verdicts) must be refused when no matching user-typed
    confirmation record exists — the committed field alone waives nothing.
    """
    from loom_checker.digest import functional_content_digest

    repo = make_repo(tmp_path, with_package=True)
    head = git(repo, "rev-parse", "HEAD")
    forged = {
        "schema": att.ATTESTATION_SCHEMA, "change_id": CHANGE,
        "content_digest": functional_content_digest(repo, head, CHANGE, None),
        "executions": [
            {"kind": "package-tests", "command": "python3 -c pass", "artifact": "",
             "result": "pass", "command_digest": att._command_digest("python3 -c pass")},
        ],
        "verdicts": [], "findings": [],
        "selection": {
            "confirmations": [{"code": "K7Q2", "skip": ["reviewers"],
                               "source": "user-typed", "at": "2026-09-14T00:00:00Z"}],
            "skip": ["reviewers"], "source": "user-typed", "prior_failures": [],
        },
    }
    assert att.selection_evidence(repo, CHANGE, None) is None
    findings = att.validate_attestation(repo, head, CHANGE, forged, None)
    assert any("local selection records" in reason for _rule, reason in findings), findings


def test_disclosure_defect_cancelled_confirmation_claims_reviewers_skipped(tmp_path: Path) -> None:
    """A withdrawn selection must not appear in the PR disclosure as a skip.

    Confirm skip=reviewers, cancel it, then confirm skip=adversarial. Reviewers
    actually RAN (effective skip is only adversarial), yet the rendered
    disclosure the publish gate requires still states `Skipped steps:
    reviewers`, forcing a false statement into the pull request.
    """
    repo = make_repo(tmp_path)
    p1, c1 = add_proposal(repo, ["reviewers"], "2026-09-14T00:00:00Z")
    add_confirmation(repo, p1, c1, "2026-09-14T00:00:01Z")
    add_cancel(repo, "2026-09-14T00:00:02Z")
    p2, c2 = add_proposal(repo, ["adversarial"], "2026-09-14T00:00:03Z")
    add_confirmation(repo, p2, c2, "2026-09-14T00:00:04Z")
    evidence = att.selection_evidence(repo, CHANGE, None)
    disclosed = {step for c in evidence["confirmations"] for step in c["skip"]}
    assert disclosed == set(evidence["skip"]), (
        "disclosure claims steps skipped that actually ran: "
        f"disclosed={sorted(disclosed)} effective_skip={evidence['skip']}"
    )


def test_bash_guard_defect_false_positive_on_unrelated_selections_dir() -> None:
    """An ordinary write to a project directory that merely ends in
    `selections/` (nothing to do with the loom store) must be allowed. The
    bare-`selections/` rule matches any such path, so a repo with an
    application `selections/` folder cannot write into it while loom-code is
    installed.
    """
    reason = selection_guard.bash_guard_reason("echo cfg > app/selections/config.json")
    assert reason is None, f"ordinary write to app/selections/ denied: {reason!r}"
