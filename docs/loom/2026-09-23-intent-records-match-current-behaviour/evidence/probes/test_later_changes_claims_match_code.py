"""Adversarial probe: each "## Later changes" note describes the code as it is.

Every claim about current behaviour in the notes this change added is
re-derived from the code: the agy adapter, the publication hook,
`publication_kind`, the selection-store guard, `publish`, `land`,
`committed_branch_paths`, the deleted heredoc tests and every cited path.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-23-intent-records-match-current-behaviour/evidence/probes/test_later_changes_claims_match_code.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import inspect
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.command_handlers import land as land_handler  # noqa: E402
from loom_checker.command_handlers import publish as publish_handler  # noqa: E402
from loom_checker.reviewers import committed_branch_paths  # noqa: E402
from loom_checker.rule_checks import push as push_rules  # noqa: E402
from loom_checker.rule_checks import selection_guard  # noqa: E402

INTENT_DIR = REPO / "docs" / "loom" / "intent"
EDITED = [
    "2026-09-14-antigravity-cli-compatibility",
    "2026-09-14-expert-mode-step-selection",
    "2026-09-14-land-merged-changes",
    "2026-09-18-blocked-publish-names-the-legal-routes",
    "2026-09-19-expert-mode-skip-friction",
    "2026-09-19-publication-hook-false-positives",
    "2026-09-20-mechanical-calculations",
]
DELETED_BY_43 = "loom-code/scripts/test_adversarial_heredoc_carve_out.py"


def later_changes(change_id: str) -> str:
    text = (INTENT_DIR / f"{change_id}.md").read_text(encoding="utf-8")
    match = re.search(r"^## Later changes\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    assert match, f"{change_id} has no Later changes section"
    return match.group(1)


def temp_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    for args in (["init", "-q", "-b", "main"], ["config", "user.email", "p@example.com"],
                 ["config", "user.name", "probe"], ["commit", "-q", "--allow-empty", "-m", "init"],
                 ["switch", "-q", "-c", "fix/probe"]):
        subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
    return repo


def agy(command: str, cwd: Path) -> dict:
    payload = {"toolCall": {"args": {"CommandLine": command, "Cwd": str(cwd)}},
               "workspacePaths": [str(cwd)]}
    result = subprocess.run(
        [sys.executable, str(REPO / "loom-code/hooks/agy_adapter.py"), "push-gate"],
        input=json.dumps(payload), capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def hook(command: str, cwd: Path) -> subprocess.CompletedProcess:
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": command}, "cwd": str(cwd)}
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "loom_checker.py"), "push", "--hook"],
        input=json.dumps(payload), capture_output=True, text=True, cwd=str(cwd), timeout=60,
    )


# --- 2026-09-14-antigravity-cli-compatibility --------------------------------

@pytest.mark.parametrize("command", ["git push origin HEAD", "gh pr create --fill",
                                     "gh pr merge 1 --squash", "GIT push"])
def test_agyadapter_unattestedpublication_allowed(tmp_path: Path, command: str) -> None:
    """agy no longer blocks an unattested push, PR create or merge."""
    assert agy(command, temp_repo(tmp_path))["decision"] == "allow"


@pytest.mark.parametrize("command", ["cat .git/loom/selections/x.json",
                                     "rm -rf loom/selections/"])
def test_agyadapter_selectionstore_denied(tmp_path: Path, command: str) -> None:
    """agy still denies a command that touches the selection record store."""
    decision = agy(command, temp_repo(tmp_path))
    assert decision["decision"] == "deny"
    assert "selection.guard" in decision.get("reason", "")


# --- 2026-09-14-land-merged-changes -------------------------------------------

def test_pushhook_handtypedmerge_allowed(tmp_path: Path) -> None:
    """A hand-typed `gh pr merge` exits 0 with a reminder, never a BLOCK."""
    result = hook("gh pr merge 43 --squash", temp_repo(tmp_path))
    assert result.returncode == 0, result.stderr
    assert "BLOCK" not in result.stderr
    assert "merg" in result.stderr or "allowing" in result.stderr


def test_land_missingacceptance_refused() -> None:
    """`land` still refuses a missing acceptance and a malformed PR body."""
    source = inspect.getsource(land_handler)
    assert re.search(r"if accepted_by not in names:\s*\n\s*return _block\(ACCEPTANCE_NOT_RECORDED", source)
    assert re.search(r"fault = validate_contextual_pr_body\(body\)\s*\n\s*if fault:\s*\n\s*return _block", source)
    assert "merged anyway" in source


def test_prfloor_workflow_present() -> None:
    """The `loom-pr-floor` CI check the note names exists."""
    assert (REPO / ".github/workflows/loom-pr-floor.yml").is_file()


# --- 2026-09-14-expert-mode-step-selection / blocked-publish ------------------

def test_publish_nonvalidstatus_publishesanyway() -> None:
    """`publish` discloses a non-valid status and continues."""
    source = inspect.getsource(publish_handler)
    assert re.search(r'if status != "valid":[\s\S]{0,300}publishing anyway', source)


# --- 2026-09-19-publication-hook-false-positives ------------------------------

@pytest.mark.parametrize("command", [
    "cat <<EOF | bash\ngh pr merge 1\nEOF",
    "bash -lc 'git push origin HEAD'",
    "bash -euxc 'gh pr create'",
    "sudo git push",
    "echo run git push later",
])
def test_publicationkind_nonleadingshape_none(command: str) -> None:
    """Only a leading literal command is recognised: heredocs and `-c` scripts are not."""
    assert push_rules.publication_kind(command) is None


@pytest.mark.parametrize("command,kind", [
    ("git push origin HEAD", "push"),
    ("GH_TOKEN=x gh pr create --fill", "create"),
    ("gh pr merge 1 --squash", "merge"),
])
def test_publicationkind_leadingcommand_recognised(command: str, kind: str) -> None:
    """A direct push, PR create or merge is still recognised (for the reminder)."""
    assert push_rules.publication_kind(command) == kind


def test_selectionguard_shellsegments_reused() -> None:
    """The heredoc reading survives in `_shell_segments`, used by the selection guard."""
    assert selection_guard._shell_segments is push_rules._shell_segments
    assert "_shell_segments(command)" in inspect.getsource(selection_guard)


def test_heredoctests_pr43_deleted() -> None:
    """The heredoc carve-out tests existed before #43 and were deleted by it."""
    def exists(rev: str) -> bool:
        return subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"{rev}:{DELETED_BY_43}"],
                              capture_output=True).returncode == 0
    assert exists("b568ba1a~1")
    assert not exists("b568ba1a")
    assert not (REPO / DELETED_BY_43).exists()


# --- 2026-09-20-mechanical-calculations ----------------------------------------

def test_committedpaths_docstring_explainsexclusion() -> None:
    """The cited function counts committed paths and its docstring gives the why."""
    doc = committed_branch_paths.__doc__ or ""
    assert "deliberately excluded" in doc and "finalize-review" in doc
    assert "committed_branch_paths(repo, change_id)" in (
        SCRIPTS / "loom_checker/selection.py").read_text(encoding="utf-8")
    plan = (REPO / "docs/loom/2026-09-20-mechanical-calculations/plan.md").read_text(encoding="utf-8")
    assert "W1-01" in plan and "committed" in plan.split("W1-01", 1)[1][:200]


# --- every note ------------------------------------------------------------------

@pytest.mark.parametrize("change_id", EDITED)
def test_notepaths_cited_exist(change_id: str) -> None:
    """Every backticked repo path a note cites exists, except the one #43 deleted."""
    note = later_changes(change_id)
    for path in re.findall(r"`([\w./-]+/[\w.-]+\.(?:py|md|yml|json))`", note):
        if path == DELETED_BY_43:
            continue
        assert (REPO / path).is_file(), f"{change_id} cites missing {path}"


@pytest.mark.parametrize("change_id", EDITED)
def test_notesections_cited_exist(change_id: str) -> None:
    """Every `<SKILL.md>` §N a note cites is a numbered heading in that file."""
    note = later_changes(change_id)
    for path, number in re.findall(r"`(loom-code/skills/[\w-]+/SKILL\.md)` §(\d+)", note):
        text = (REPO / path).read_text(encoding="utf-8")
        assert re.search(rf"^## {number}\. ", text, re.M), f"{path} has no §{number}"
