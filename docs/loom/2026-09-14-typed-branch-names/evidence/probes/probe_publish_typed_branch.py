"""Adversarial probes: slash-bearing branch names through publish-side helpers
(no network: every case stops before `gh` would be called).

Run from repo root:
    python3 -m pytest docs/loom/2026-09-14-typed-branch-names/evidence/probes/probe_publish_typed_branch.py -q
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import pytest

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from loom_checker.rule_checks.push import check_pr_create_remote_head  # noqa: E402

PUBLISH = REPO / "loom-code/scripts/loom_checker/command_handlers/publish.py"
PUSH = REPO / "loom-code/scripts/loom_checker/rule_checks/push.py"
CID = "2026-09-14-demo"


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=check)


@pytest.mark.parametrize("name", [f"feat/{CID}", f"fix/scope/{CID}", f"docs/{CID}"])
def test_checkrefformat_typedname_accepted(tmp_path: Path, name: str) -> None:
    """publish.py:398 gates on `check-ref-format --branch`; typed names pass."""
    assert git(tmp_path, "check-ref-format", "--branch", name, check=False).returncode == 0


@pytest.mark.parametrize("name", ["feat/", "feat//x", f"feat/.{CID}", f"feat/{CID}.lock", "feat/a..b", "/feat"])
def test_checkrefformat_malformedtypedname_rejected(tmp_path: Path, name: str) -> None:
    """One character off a typed name is refused by the same gate."""
    assert git(tmp_path, "check-ref-format", "--branch", name, check=False).returncode != 0


def test_publishquery_slashbranch_encodedonce() -> None:
    """publish.py builds `head=quote(f'{owner}:{branch}', safe='')`; the slash
    is percent-encoded exactly once (GitHub decodes %2F -- verified live
    against actions/checkout `releases%2Fv1` returning 200 during the probe)."""
    src = PUBLISH.read_text(encoding="utf-8")
    assert "head={quote(f'{owner}:{branch}', safe='')}" in src
    assert quote(f"o:feat/{CID}", safe="") == f"o%3Afeat%2F{CID}"
    assert "%25" not in quote(f"o:feat/{CID}", safe="")


def test_pushrefpath_slashbranch_encodedonce() -> None:
    """push.py builds `git/ref/heads/{quote(branch, safe='')}`."""
    assert "git/ref/heads/{quote(branch, safe='')}" in PUSH.read_text(encoding="utf-8")
    assert quote(f"fix/scope/{CID}", safe="") == f"fix%2Fscope%2F{CID}"


@pytest.fixture()
def typed_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "a").write_text("a\n", encoding="utf-8")
    git(repo, "add", "a")
    git(repo, "-c", "commit.gpgsign=false", "commit", "-q", "-m", "seed")
    git(repo, "switch", "-q", "-c", f"fix/scope/{CID}")
    return repo


@pytest.mark.parametrize("flag", ["--head {b}", "--head={b}", "-H {b}", "-H{b}"])
def test_prcreatehead_typedbranch_matchescurrent(typed_repo: Path, flag: str) -> None:
    """Every head spelling of a nested typed branch equals the current branch
    (the guard proceeds to the origin check, not the head-mismatch refusal)."""
    cmd = f"gh pr create --base main {flag.format(b=f'fix/scope/{CID}')} --title t"
    reason = check_pr_create_remote_head(typed_repo, cmd)
    assert reason is not None and "trusted GitHub origin" in reason, reason


@pytest.mark.parametrize("head", [f"fix/{CID}", f"scope/{CID}", f"owner:fix/scope/{CID}", f"refs/heads/fix/scope/{CID}"])
def test_prcreatehead_partialtypedbranch_refused(typed_repo: Path, head: str) -> None:
    """A prefix-stripped, fork-qualified or full-ref head is not the branch."""
    reason = check_pr_create_remote_head(typed_repo, f"gh pr create --base main --head {head} --title t")
    assert reason is not None and "PR head must be the current branch" in reason, reason
