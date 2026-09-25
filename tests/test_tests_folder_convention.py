"""The tests-folder convention is stated, and CI follows it.
concern: a test file placed outside every test root the suite runs (root
scripts/, .claude/hooks/, a plugin's hooks or contract folder, a tests folder
under any of those, a new plugin not yet in `TEST_ROOTS`) is neither
collected by the package suite nor refused by any guard, so it goes dark.

Tests live in `tests/` folders apart from the code they test. Four things keep
that true after the move: the contributor guidance (AGENTS.md) says so, every
CI workflow is triggered by edits under the test folders it runs and runs them
through the shared inventory (`scripts/run_package_tests.py --loom-family`),
neither the guidance nor the workflows still names an old test location, and
no test file in the working tree sits outside the runner's `TEST_ROOTS`.

Bound of the repository-wide guard: it reads `repo_files.repository_files`
(tracked plus untracked, non-ignored files; a plain walk without git), matches
file names `test_*.py`, `*_test.py` and `test-*.sh`, and allows a match only
when it sits under one of the runner's `TEST_ROOTS` or under `docs/loom/`
(change evidence and probes). A root's `local/` folder is allowed although the
suite skips it. A test named any other way is outside this guard.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from run_package_tests import TEST_ROOTS, loom_family_commands  # noqa: E402
from repo_files import repository_files  # noqa: E402  (on sys.path via the runner)
WORKFLOWS = REPO / ".github" / "workflows"
GROUPS = {"code", "design", "workflow-python", "workflow-shell", "workflow-mermaid"}

# An old test location: a test beside production code or inside a skill folder.
OLD_TEST_PATH = re.compile(
    r"(loom-code|loom-design|loom-workflow)/scripts/[^ ]*test_"
    r"|skills/[a-z-]*/(scripts|probes)/test_"
    r"|(^|[^/])scripts/test_"
    r"|\.claude/hooks/test_",
    re.MULTILINE,
)

# The path each CI workflow must be triggered by: a test file in every folder
# it runs, and the inventory that decides what it runs.
REQUIRED_TRIGGERS = {
    "loom-code-ci.yml": [
        "tests/test_new.py",
        "tests/hooks/test_new.py",
        "loom-code/tests/test_new.py",
        "scripts/run_package_tests.py",
    ],
    "loom-design-ci.yml": [
        "loom-design/tests/spec/test_new.py",
        "scripts/run_package_tests.py",
    ],
    "loom-workflow-ci.yml": [
        "loom-workflow/tests/test_new.py",
        "loom-workflow/tests/loom-memory/test_new.py",
        "scripts/run_package_tests.py",
    ],
}


# A test file by name: pytest's two default patterns and the shell-test prefix.
TEST_FILE = re.compile(r"(^|/)(test_[^/]*\.py|[^/]*_test\.py|test-[^/]*\.sh)\Z")


def _tracked_strays(root: Path) -> list[str]:
    """Test files of the repository outside every test root the suite runs and outside `docs/loom/`."""
    allowed = tuple(f"{r}/" for r in TEST_ROOTS) + ("docs/loom/",)
    return sorted(
        rel
        for rel in (path.relative_to(root).as_posix() for path in repository_files(root))
        if TEST_FILE.search(rel) and not rel.startswith(allowed)
    )


def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """GitHub path-filter glob: `**` spans folders, `*` stays inside one."""
    out = ""
    for token in re.split(r"(\*\*/?|\*)", pattern):
        if token in ("**", "**/"):
            out += ".*"
        elif token == "*":
            out += "[^/]*"
        else:
            out += re.escape(token)
    return re.compile(out + r"\Z")


def _missed(filters: list[str], paths: list[str]) -> list[str]:
    compiled = [_glob_to_regex(f) for f in filters]
    return [p for p in paths if not any(c.match(p) for c in compiled)]


def _triggers(workflow: Path) -> dict[str, list[str]]:
    data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    on = data.get("on", data.get(True))
    return {event: on[event]["paths"] for event in ("pull_request", "push")}


def test_agents_md_states_tests_folders() -> None:
    text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    for phrase in (
        "`<plugin>/tests/`",
        "`loom-workflow/tests/<skill>/`",
        "root `tests/`",
        "`tests/local/`",
        "`tests/<skill>/`",
    ):
        assert phrase in text, f"AGENTS.md does not state {phrase}"


def test_ci_path_filters_cover_the_tests_folders() -> None:
    for name, paths in REQUIRED_TRIGGERS.items():
        for event, filters in _triggers(WORKFLOWS / name).items():
            assert _missed(filters, paths) == [], f"{name} {event}"


def test_workflow_shell_ci_is_triggered_by_every_test_root() -> None:
    """A `test-*.sh` in any root runs in the shell group, so editing it must fire that job."""
    shell = [
        w for w in sorted(WORKFLOWS.glob("*.yml"))
        if "--loom-family --only workflow-shell" in w.read_text(encoding="utf-8")
    ]
    assert len(shell) == 1, shell
    paths = [f"{root}/sub/test-new.sh" for root in TEST_ROOTS]
    for event, filters in _triggers(shell[0]).items():
        assert _missed(filters, paths) == [], f"{shell[0].name} {event}"


def test_ci_path_filter_missing_tests_is_detected() -> None:
    assert _missed(["loom-code/scripts/**", "scripts/**"], ["loom-code/tests/test_new.py"]) == [
        "loom-code/tests/test_new.py"
    ]
    assert _missed(["loom-code/**", "tests/**"], ["loom-code/tests/test_new.py"]) == []


def test_ci_runs_the_same_groups_as_the_inventory() -> None:
    groups = set()
    for name in REQUIRED_TRIGGERS:
        text = (WORKFLOWS / name).read_text(encoding="utf-8")
        groups |= set(re.findall(r"run_package_tests\.py --loom-family --only (\S+)", text))
        assert not re.search(r"-m pytest\b|run:\s*pytest\b", text), name
    assert groups == GROUPS


def test_guidance_and_workflows_name_no_old_test_path() -> None:
    documents = [REPO / "AGENTS.md", *sorted(WORKFLOWS.glob("*.yml"))]
    stale = [
        f"{doc.relative_to(REPO)}: {m.group(0)}"
        for doc in documents
        for m in OLD_TEST_PATH.finditer(doc.read_text(encoding="utf-8"))
    ]
    assert stale == []


def test_old_test_path_in_a_document_is_detected() -> None:
    for text in (
        "# scripts/test_state_anchor_carrier_inventory.py scans loom-*/",
        "see loom-code/scripts/test_check_mechanisms.py",
        "loom-code/skills/build/probes/test_recovery_rules.py",
        ".claude/hooks/test_remind_memory_mirror.py",
    ):
        assert OLD_TEST_PATH.search(text), text
    assert not OLD_TEST_PATH.search("tests/test_state_anchor_carrier_inventory.py")


def _planted_repo(root: Path, rel: str) -> Path:
    planted = root / rel
    planted.parent.mkdir(parents=True, exist_ok=True)
    planted.write_text("def test_planted():\n    assert False\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", rel], cwd=root, check=True)
    return root


def test_no_test_file_sits_outside_a_tests_folder() -> None:
    assert _tracked_strays(REPO) == []


@pytest.mark.parametrize(
    "rel",
    [
        "scripts/test_zz_planted_stray.py",
        ".claude/hooks/test_zz_planted_stray.py",
        "loom-code/hooks/test_zz_planted_stray.py",
        "loom-new/contract/zz_planted_test.py",
        "loom-new/scripts/test-zz-planted.sh",
        # A folder named tests that the package suite does not run.
        "scripts/tests/test_zz.py",
        ".claude/hooks/tests/test_zz.py",
        "loom-code/hooks/tests/test_zz.py",
        "loom-new/tests/test_zz_planted_stray.py",
        "loom-code/skills/build/tests/test_zz.py",
        # The cases the per-plugin and root-level guards covered.
        "scripts/test_stray.py",
        ".claude/hooks/test-stray.sh",
        "loom-code/scripts/test_stray.py",
        "loom-code/skills/build/probes/test_recovery_rules.py",
        "loom-design/scripts/interface/test_stray.py",
        "loom-design/skills/write-spec/test_stray.py",
        "loom-workflow/skills/handoff/scripts/test_stray.py",
        "loom-workflow/scripts/test_stray.py",
        "loom-workflow/.claude-plugin/test_stray.py",
    ],
)
def test_planted_stray_outside_tests_folders_is_refused(tmp_path: Path, rel: str) -> None:
    assert _tracked_strays(_planted_repo(tmp_path, rel)) == [rel]


def test_stray_is_refused_without_git(tmp_path: Path) -> None:
    """The listing comes from `repository_files`, which walks a tree git does not own."""
    stray = tmp_path / "scripts" / "test_zz.py"
    stray.parent.mkdir(parents=True)
    stray.write_text("", encoding="utf-8")
    assert _tracked_strays(tmp_path) == ["scripts/test_zz.py"]


@pytest.mark.parametrize(
    "rel",
    [
        "tests/test_zz_planted_stray.py",
        "tests/hooks/test_zz_planted_stray.py",
        "loom-design/tests/spec/test_zz_planted_stray.py",
        "loom-workflow/tests/loom-memory/test-zz-planted.sh",
        "loom-code/tests/sub/test-zz-planted.sh",
        "loom-code/tests/local/test-zz-local.sh",
        "docs/loom/some-change/evidence/probes/test_zz_planted_stray.py",
    ],
)
def test_planted_test_in_a_tests_folder_or_docs_loom_is_allowed(
    tmp_path: Path, rel: str
) -> None:
    repo = _planted_repo(tmp_path, rel)
    assert _tracked_strays(repo) == []
    if rel.endswith(".sh") and "/local/" not in rel:
        shell = loom_family_commands(repo, verbosity="-q", only="workflow-shell")
        assert ["bash", (repo / rel).as_posix()] in shell, "allowed but never run"
