"""Skipped-review ledger and store change-id safety (plan W2-04).

Spec 2026-09-14-expert-mode-step-selection REQ-8, decision 14:
`selection skipped-review` reads `docs/loom/*/attestation.json` in the
remote default branch tree and lists each merged change whose attestation
records reviewers as skipped.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from loom_checker import selection
from loom_checker.helpers import UsageError

CHECKER = Path(__file__).with_name("loom_checker.py")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "base")
    return repo


def attestation(change_id: str, skip: list[str] | None) -> dict:
    selected = None if skip is None else {
        "confirmations": [{"code": "AB2C", "skip": skip, "source": "user-typed",
                           "at": "2026-09-14T00:00:00Z"}],
        "skip": skip, "source": "user-typed", "prior_failures": [],
    }
    return {"schema": "loom-attestation/v2", "change_id": change_id, "content_digest": "d",
            "executions": [], "verdicts": [], "findings": [], "selection": selected}


def merge_change(repo: Path, change_id: str, skip: list[str] | None) -> str:
    """Deliver one change to main through a merge commit; return its short sha."""
    git(repo, "checkout", "-q", "-b", change_id)
    target = repo / "docs/loom" / change_id / "attestation.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(attestation(change_id, skip)), encoding="utf-8")
    git(repo, "add", str(target.relative_to(repo)))
    git(repo, "commit", "-q", "-m", f"attest {change_id}")
    git(repo, "checkout", "-q", "main")
    git(repo, "merge", "-q", "--no-ff", "-m", f"Merge {change_id}", change_id)
    return git(repo, "log", "-1", "--format=%h", "HEAD")


def publish_remote_default(repo: Path) -> None:
    git(repo, "update-ref", "refs/remotes/origin/main", git(repo, "rev-parse", "HEAD"))
    git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")


def ledger(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "selection", "skipped-review"],
        capture_output=True, text=True, cwd=str(repo),
    )


# --- Acceptance 8 -----------------------------------------------------------

def test_merged_change_skipping_reviewers_listed(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    skipper = merge_change(repo, "2026-09-01-skipper", ["reviewers", "adversarial"])
    merge_change(repo, "2026-09-02-full", None)
    merge_change(repo, "2026-09-03-tests-only", ["package-tests"])
    publish_remote_default(repo)
    # A local-only change on main is not on the remote default branch yet.
    merge_change(repo, "2026-09-04-unpushed", ["reviewers"])

    result = ledger(repo)

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == [
        f"2026-09-01-skipper {skipper} skipped: reviewers, adversarial"
    ]


def test_none_prints_no_merged_change_skipped_review(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    merge_change(repo, "2026-09-02-full", None)
    publish_remote_default(repo)

    result = ledger(repo)

    assert result.returncode == 0, result.stderr
    assert result.stdout == "no merged change skipped review\n"


def test_indeterminate_remote_default_is_a_clear_refusal(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    merge_change(repo, "2026-09-01-skipper", ["reviewers"])

    result = ledger(repo)

    assert result.returncode != 0
    assert result.stdout == ""
    assert "remote default" in result.stderr
    assert "refs/remotes/origin/HEAD" in result.stderr


# --- store change-id safety -------------------------------------------------

@pytest.mark.parametrize("change_id", [
    "../escape", "2026-09-14-a/b", "2026-09-14-UPPER", "not-a-date", "", "_",
    "2026-09-14-ok\n", "/abs",
])
def test_store_refuses_change_id_that_is_not_one_safe_segment(
    tmp_path: Path, change_id: str
) -> None:
    repo = make_repo(tmp_path)
    with pytest.raises(UsageError):
        selection.store_path(repo, change_id)
    with pytest.raises(UsageError):
        selection.append_event(repo, change_id, {"event": "failure"})
    # A read of an unsafe id binds nothing: the full process applies.
    assert selection.read_events(repo, change_id) == []
    assert not (Path(git(repo, "rev-parse", "--absolute-git-dir")) / "loom").exists()


def test_store_accepts_dated_change_id(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    selection.append_event(repo, "2026-09-14-ok-2", {"event": "failure"})
    assert selection.read_events(repo, "2026-09-14-ok-2") == [{"event": "failure"}]
