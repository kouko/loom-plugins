"""The tests-folder convention is stated, and CI follows it.

Tests live in `tests/` folders apart from the code they test. Three things keep
that true after the move: the contributor guidance (AGENTS.md) says so, every
CI workflow is triggered by edits under the test folders it runs and runs them
through the shared inventory (`scripts/run_package_tests.py --loom-family`),
and neither the guidance nor the workflows still names an old test location.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
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
