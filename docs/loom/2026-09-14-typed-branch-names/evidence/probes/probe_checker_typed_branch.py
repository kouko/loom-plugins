"""Adversarial probes: typed / slash-bearing branch names through checker
commands that resolve the branch base (`intent`, `reviewer-count`).

Run from repo root:
    python3 -m pytest docs/loom/2026-09-14-typed-branch-names/evidence/probes/probe_checker_typed_branch.py -q

Scratch repositories live under pytest's tmp_path (system temp), never the worktree.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
CHECKER = REPO / "loom-code/scripts/loom_checker.py"
CID = "2026-09-14-demo"
INTENT = """# A change
originator: tester
kind: engineering
needs-design: no — internal only
status: open

## Problem
The thing is slow and the people who use it wait too long.
"""


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=check)


def make_repo(tmp_path: Path, trunk: str = "main") -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", trunk)
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    git(repo, "config", "commit.gpgsign", "false")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    git(repo, "add", "seed.txt")
    git(repo, "commit", "-q", "-m", "seed")
    return repo


def commit_src(repo: Path) -> Path:
    target = repo / "src/cli/main.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("x\n", encoding="utf-8")
    git(repo, "add", "src/cli/main.py")
    git(repo, "commit", "-q", "-m", "add src")
    intent = repo / f"docs/loom/intent/{CID}.md"
    intent.parent.mkdir(parents=True, exist_ok=True)
    intent.write_text(INTENT, encoding="utf-8")
    return intent


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECKER), *args], cwd=cwd, capture_output=True, text=True)


def _assert_base_resolved(result: subprocess.CompletedProcess) -> None:
    assert "git switch -c" not in result.stderr, result.stderr
    assert "no branch base resolves" not in result.stderr, result.stderr
    assert "HEAD is the trunk" not in result.stderr, result.stderr


@pytest.mark.parametrize("branch", [f"feat/{CID}", f"fix/scope/{CID}", f"chore/a/b/c/{CID}"])
def test_intentcmd_typedbranch_resolvesbase(tmp_path: Path, branch: str) -> None:
    """Typed and deeply nested branch names resolve the base in `intent`."""
    repo = make_repo(tmp_path)
    git(repo, "switch", "-q", "-c", branch)
    intent = commit_src(repo)
    result = run("intent", str(intent), cwd=repo)
    _assert_base_resolved(result)
    assert result.returncode == 1 and "intent.needs-design-recompute" in result.stderr


def test_reviewercount_typedbranch_resolvesbase(tmp_path: Path) -> None:
    """`reviewer-count` on a nested typed branch exits 0 and prints a count.
    Observed: it also exits 0 on the trunk, so this case records that the
    name is accepted; it cannot discriminate a trunk refusal."""
    repo = make_repo(tmp_path)
    git(repo, "switch", "-q", "-c", f"fix/scope/{CID}")
    commit_src(repo)
    git(repo, "add", "docs")
    git(repo, "commit", "-q", "-m", "intent")  # reviewer-count needs a clean tree
    result = run("reviewer-count", CID, cwd=repo)
    _assert_base_resolved(result)
    assert result.returncode == 0, (result.returncode, result.stderr)
    assert result.stdout.strip().isdigit(), result.stdout


def test_gitswitch_trunkprefixedname_refusedbygit(tmp_path: Path) -> None:
    """`main/<id>` cannot coexist with a `main` branch (ref D/F conflict), so
    the trunk-prefixed typed name never reaches the checker in a main repo."""
    repo = make_repo(tmp_path, trunk="main")
    assert git(repo, "switch", "-c", f"main/{CID}", check=False).returncode != 0


def test_intentcmd_trunkprefixedbranchonmaster_notmistakenfortrunk(tmp_path: Path) -> None:
    """On a `master` repo, a branch literally named `main/<id>` is not the trunk."""
    repo = make_repo(tmp_path, trunk="master")
    git(repo, "switch", "-q", "-c", f"main/{CID}")
    intent = commit_src(repo)
    result = run("intent", str(intent), cwd=repo)
    _assert_base_resolved(result)
    assert result.returncode == 1


def test_gitswitch_flattypebranchexists_refusedbygit(tmp_path: Path) -> None:
    """Boundary the Step 6 text never mentions: an existing flat `feat` branch
    makes `git switch -c feat/<id>` fail (D/F conflict)."""
    repo = make_repo(tmp_path)
    git(repo, "branch", "feat")
    result = git(repo, "switch", "-c", f"feat/{CID}", check=False)
    assert result.returncode != 0


def test_intentcmd_typedbranchshadowedbytag_resolvesbase(tmp_path: Path) -> None:
    """A tag spelled like the typed branch makes `--abbrev-ref HEAD` print
    `heads/feat/<id>`; the base must still resolve."""
    repo = make_repo(tmp_path)
    git(repo, "switch", "-q", "-c", f"feat/{CID}")
    intent = commit_src(repo)
    git(repo, "tag", f"feat/{CID}")
    result = run("intent", str(intent), cwd=repo)
    _assert_base_resolved(result)
    assert result.returncode == 1


@pytest.mark.xfail(
    strict=True,
    reason="pre-existing: trunk guard reads --abbrev-ref; out of scope for 2026-09-14-typed-branch-names",
)
def test_intentcmd_ontrunkwithtagmain_failsclosed(tmp_path: Path) -> None:
    """Pre-existing (not introduced here): on `main` with a tag also named
    `main`, `--abbrev-ref HEAD` prints `heads/main`, escaping the trunk-name
    set; the checker must still refuse with the typed-branch hint."""
    repo = make_repo(tmp_path)
    intent = commit_src(repo)
    git(repo, "tag", "main")
    result = run("intent", str(intent), cwd=repo)
    assert result.returncode == 2, (result.returncode, result.stderr)
    assert "git switch -c <type>/<change-id>" in result.stderr
