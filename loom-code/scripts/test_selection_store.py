"""Selection store, step vocabulary and record lifetimes (plan W1-01).

Spec decisions 1, 2, 5, 6, 7 and 8 of 2026-09-14-expert-mode-step-selection:
the checker owns the step vocabulary, the append-only record store lives
under the git common dir, selection events lapse when the branch or merge
base moves, and failure events survive a rebase.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from loom_checker import selection

import pytest


@pytest.fixture(autouse=True)
def no_host_session(monkeypatch):
    """Tests never inherit the real Claude Code session running the suite."""
    for name in ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT"):
        monkeypatch.delenv(name, raising=False)

CHECKER = Path(__file__).with_name("loom_checker.py")
CHANGE = "2026-09-14-example"
FULL = ["spec", "plan", "implementer", "tdd", "reviewers",
        "adversarial", "blind-run", "package-tests"]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def checker(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "selection", *args],
        capture_output=True, text=True, cwd=str(repo),
    )


def commit(repo: Path, name: str) -> None:
    (repo / name).write_text(name, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", name)


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    commit(repo, "base.py")
    git(repo, "checkout", "-q", "-b", "feature")
    commit(repo, "work.py")
    return repo


def confirm(repo: Path, prompt: str | None = None) -> None:
    """Stand in for the W2-01 capture hook: bind the newest proposal."""
    proposal = [e for e in selection.read_events(repo, CHANGE) if e["event"] == "proposal"][-1]
    text = prompt if prompt is not None else f"/loom-code:expert-mode 確認 {proposal['code']}"
    selection.append_event(repo, CHANGE, {
        "event": "confirmation",
        "proposal_id": proposal["id"],
        "code": proposal["code"],
        "source": "user-typed",
        "session_id": "s1",
        "prompt_ref": "p1",
        "prompt_text": text,
        "prompt_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "branch": proposal["branch"],
        "merge_base": proposal["merge_base"],
        "at": "2026-09-14T00:00:00Z",
    })


def show(repo: Path) -> dict:
    result = checker(repo, "show", CHANGE)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


# --- Acceptance 1 -----------------------------------------------------------

def test_propose_prints_table_code_and_cancel_restores_full(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    result = checker(repo, "propose", CHANGE, "--origin", "user",
                     "--skip", "reviewers,adversarial")
    assert result.returncode == 0, result.stderr
    code = selection.selection_code(CHANGE, [s for s in FULL if s not in {"reviewers", "adversarial"}],
                                    ["reviewers", "adversarial"])
    assert f"code: {code}" in result.stdout
    assert any(line.split() == ["reviewers", "skip"] for line in result.stdout.splitlines())
    assert any(line.split() == ["tdd", "run"] for line in result.stdout.splitlines())

    confirm(repo)
    bound = show(repo)
    assert bound["bound"] is True
    assert bound["skip"] == ["reviewers", "adversarial"]

    cancelled = checker(repo, "cancel", CHANGE)
    assert cancelled.returncode == 0, cancelled.stderr
    after = show(repo)
    assert after["bound"] is False
    assert after["run"] == FULL and after["skip"] == []
    assert [e["source"] for e in selection.read_events(repo, CHANGE) if e["event"] == "cancel"] == ["agent-run"]


def test_steps_carry_no_requires_and_propose_refuses_unknown_and_intent(tmp_path: Path) -> None:
    raw = selection.load_manifest()["step_selection"]["steps"]
    assert [s["name"] for s in raw] == FULL
    assert all(set(s) == {"name"} for s in raw)
    assert all(set(s) == {"name"} for s in selection.step_vocabulary())
    repo = make_repo(tmp_path)
    unknown = checker(repo, "propose", CHANGE, "--origin", "agent", "--skip", "publication")
    assert unknown.returncode != 0
    assert "publication" in unknown.stderr
    intent = checker(repo, "propose", CHANGE, "--origin", "agent", "--skip", "intent")
    assert intent.returncode != 0
    assert "the intent is always kept" in intent.stderr
    assert selection.read_events(repo, CHANGE) == []


@pytest.mark.parametrize("step", FULL)
def test_skipping_any_single_step_validates(step: str) -> None:
    assert selection.validate_selection([step], []) == []


@pytest.mark.parametrize("flag", ["--skip", "--run"])
def test_propose_refuses_intent_saying_it_is_always_kept(tmp_path: Path, flag: str) -> None:
    repo = make_repo(tmp_path)
    refused = checker(repo, "propose", CHANGE, "--origin", "user", flag, "intent")
    assert refused.returncode != 0
    assert "the intent is always kept" in refused.stderr
    assert "unknown step" not in refused.stderr
    assert selection.read_events(repo, CHANGE) == []


def test_code_is_order_independent_four_base32_chars() -> None:
    a = selection.selection_code(CHANGE, ["tdd", "plan"], ["reviewers", "adversarial"])
    b = selection.selection_code(CHANGE, ["plan", "tdd"], ["adversarial", "reviewers"])
    assert a == b and len(a) == 4
    assert set(a) <= set("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")


def test_confirmation_prompt_grammar() -> None:
    ok = selection.confirmation_prompt_matches
    assert ok("/loom-code:expert-mode 確認 K7Q2", "K7Q2")
    assert ok("/expert-mode OK K7Q2", "K7Q2")
    assert ok("$expert-mode K7Q2", "K7Q2")
    assert ok("$loom-code:expert-mode go K7Q2", "K7Q2")
    assert not ok("yes K7Q2", "K7Q2")
    assert not ok("/expert-mode 確認K7Q2", "K7Q2")
    assert not ok("/expert-mode", "K7Q2")


def test_confirmation_with_tampered_prompt_text_does_not_bind(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    assert checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "tdd").returncode == 0
    confirm(repo, prompt="yes")
    assert show(repo)["bound"] is False


# --- Acceptance 6 -----------------------------------------------------------

def test_same_branch_and_base_applies(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    assert checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "blind-run").returncode == 0
    confirm(repo)
    commit(repo, "more.txt")  # new commits on the branch keep the merge base
    state = show(repo)
    assert state["bound"] is True
    assert state["skip"] == ["blind-run"]
    assert "blind-run" not in state["run"]


def test_reused_change_id_on_new_branch_inherits_nothing(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    assert checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "blind-run").returncode == 0
    confirm(repo)
    git(repo, "checkout", "-q", "main")
    git(repo, "checkout", "-q", "-b", "feature-two")
    commit(repo, "two.txt")
    state = show(repo)
    assert state["bound"] is False
    # Auto-skip activates for narrow deltas: .txt file outside docs/loom/ makes floor=1
    # so spec/plan/blind-run are auto-skipped
    assert state["skip"] == ["spec", "plan", "blind-run"]
    assert "spec" not in state["run"]
    assert "plan" not in state["run"]
    assert "blind-run" not in state["run"]


def test_store_lives_under_git_common_dir(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    assert checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "tdd").returncode == 0
    assert (repo / ".git/loom/selections" / f"{CHANGE}.jsonl").is_file()


# --- Acceptance 7 -----------------------------------------------------------

def rebase_onto_new_trunk(repo: Path) -> None:
    git(repo, "checkout", "-q", "main")
    commit(repo, "trunk.txt")
    git(repo, "checkout", "-q", "feature")
    git(repo, "rebase", "-q", "main")


def test_failure_survives_rebase(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    recorded = checker(repo, "record-failure", CHANGE, "--step", "reviewers", "--rule", "verdict.needs-revision")
    assert recorded.returncode == 0, recorded.stderr
    rebase_onto_new_trunk(repo)
    failures = show(repo)["failures"]
    assert [(f["step"], f["rule"]) for f in failures] == [("reviewers", "verdict.needs-revision")]


def test_failure_survives_branch_rename(tmp_path: Path) -> None:
    """Failures are filtered by change-id only; `branch` is informational."""
    from loom_checker.attestation import selection_evidence

    repo = make_repo(tmp_path)
    recorded = checker(repo, "record-failure", CHANGE, "--step", "reviewers", "--rule", "verdict.needs-revision")
    assert recorded.returncode == 0, recorded.stderr
    git(repo, "branch", "-m", "feature-clean")
    assert checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "reviewers").returncode == 0
    confirm(repo)
    state = show(repo)
    assert state["bound"] is True
    assert [(f["step"], f["branch"]) for f in state["failures"]] == [("reviewers", "feature")]
    prior = selection_evidence(repo, CHANGE)["prior_failures"]
    assert [(f["step"], f["rule"]) for f in prior] == [("reviewers", "verdict.needs-revision")]


def test_show_and_cancel_refuse_an_option_as_change_id(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    for sub in ("show", "cancel"):
        result = checker(repo, sub, "--help")
        assert result.returncode == 2, (sub, result.stdout, result.stderr)
        assert f"selection {sub} <change-id>" in result.stderr
        assert result.stdout == ""
    assert not selection.store_dir(repo).exists()


def test_checker_usage_lists_every_selection_subcommand(tmp_path: Path) -> None:
    result = subprocess.run([sys.executable, str(CHECKER)], capture_output=True, text=True)
    assert result.returncode == 2
    for line in ("selection skipped-review", "selection capture --hook"):
        assert line in result.stderr, line


def test_selection_lapses_after_rebase(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    assert checker(repo, "propose", CHANGE, "--origin", "user", "--skip", "reviewers,adversarial").returncode == 0
    confirm(repo)
    assert show(repo)["bound"] is True
    rebase_onto_new_trunk(repo)
    state = show(repo)
    assert state["bound"] is False
    assert state["skip"] == []
