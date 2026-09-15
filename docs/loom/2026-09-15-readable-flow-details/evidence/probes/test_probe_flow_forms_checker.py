"""Adversary probes: do the deterministic checkers accept the forms the new
guidance tells authors to write?

The change (2026-09-15-readable-flow-details) tells capture-intent authors
that "any section may use a Markdown table or diagram" (Acceptance 6: "the
intent checker still accepts it"), and tells spec authors that several
parallel cases are "a table `case | what the user does | what they see`" and
branching states are "a Mermaid `stateDiagram-v2` or `flowchart`"
(Acceptance 2). Neither the intent checker nor `spec.ui-flows-recompute`
changed. These probes feed both checkers an artifact written exactly the way
the new text says, and expect it to be accepted.

Run from the repo root:
    python3 -m pytest docs/loom/2026-09-15-readable-flow-details/evidence/probes/test_probe_flow_forms_checker.py -q -p no:cacheprovider
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    """Walk upward until a directory holding docs/loom is found."""
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs" / "loom").is_dir() and (candidate / "loom-code").is_dir():
            return candidate
    raise RuntimeError(f"repo root not found above {start}")


ROOT = _find_repo_root(Path(__file__).parent)
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))

from loom_checker.helpers import load_manifest  # noqa: E402
from loom_checker.parsing import parse_document  # noqa: E402
from loom_checker.rule_checks.intake import check_ui_flows_recompute  # noqa: E402
from loom_checker.rule_checks.intake import flow_lines  # noqa: E402
from loom_checker.rule_checks.intent import check_intent_schema  # noqa: E402
from loom_checker.rule_checks.intent import check_product_no_identifiers  # noqa: E402


def _product_intent(problem: str) -> str:
    return (
        "# Export my tasks\n"
        "originator: kouko\n"
        "kind: product\n"
        "needs-design: yes — a new command the user types\n"
        "status: confirmed 2026-09-15\n\n"
        "## Problem\n"
        f"{problem}\n\n"
        "## Proposed outcome\n"
        "The user can back up their tasks in one step.\n\n"
        "## Value case\n"
        "kouko; losing tasks hurts now; GO.\n\n"
        "## Acceptance\n"
        "1. The user can back up their tasks in one step.\n\n"
        "## Constraints\n"
        "- none\n\n"
        "## Out of scope\n"
        "- syncing\n\n"
        "## Open questions\n"
        "- none\n"
    )


def _intent_failures(problem: str) -> list[tuple[str, str]]:
    front, sections = parse_document(_product_intent(problem))
    return check_intent_schema(load_manifest(), front, sections) + check_product_no_identifiers(
        front, sections
    )


# --- intent: forms at intent altitude (Acceptance 6) ---


def test_productIntentProblem_markdownTable_accepted() -> None:
    """A current-versus-wanted table in a product Problem passes the intent checker."""
    problem = (
        "Backing up tasks is manual today.\n\n"
        "| now | wanted |\n"
        "|---|---|\n"
        "| copy by hand, often forgotten | one step |\n"
    )
    assert _intent_failures(problem) == []


def test_productIntentProblem_mermaidFlowchartPlainIds_accepted() -> None:
    """A flowchart with plain node ids in a product Problem passes the intent checker."""
    problem = (
        "Backing up tasks is manual today.\n\n"
        "```mermaid\n"
        "flowchart LR\n"
        "  A[kouko finishes work] --> B[forgets the backup]\n"
        "  B --> C[loses tasks]\n"
        "```\n"
    )
    assert _intent_failures(problem) == []


@pytest.mark.parametrize(
    "diagram",
    [
        # who is affected, at intent altitude: people and hand-offs, no UI reactions
        "sequenceDiagram\n  kouko->>Team: shares the task list\n  Team->>kouko: asks for last week's copy",
        # current versus wanted on two axes
        "quadrantChart\n  x-axis Rare --> Frequent\n  y-axis Cheap --> Costly\n  Manual backup: [0.8, 0.7]",
        # a styled plain flowchart
        "flowchart LR\n  A[kouko] --> B[loses tasks]\n  classDef pain fill:#f96\n  class B pain",
    ],
    ids=["sequenceDiagram", "quadrantChart", "classDef"],
)
def test_productIntentProblem_mermaidKeywordDiagram_accepted(diagram: str) -> None:
    """A Mermaid diagram whose keyword is camelCase, with plain node ids, passes the intent checker."""
    problem = f"Backing up tasks is manual today.\n\n```mermaid\n{diagram}\n```\n"
    assert _intent_failures(problem) == []


# --- spec: UI flows in table or diagram form (Acceptance 2) ---

TABLE_ONLY_FLOWS = (
    "### Export command\n\n"
    "| case | what the user does | what they see |\n"
    "|---|---|---|\n"
    "| empty list | runs todo export | the line nothing to export, exit 0 |\n"
    "| file exists | runs todo export | the question overwrite todo-export? |\n"
    "| success | runs todo export | the line exported 12 tasks, exit 0 |\n"
    "| disk full | runs todo export | the line disk full, free space and rerun, exit 1 |\n"
)

MERMAID_ONLY_FLOWS = (
    "### Export command\n\n"
    "```mermaid\n"
    "stateDiagram-v2\n"
    "  [*] --> Asking : todo export with an existing file\n"
    "  Asking --> Written : answers yes\n"
    "  Asking --> Cancelled : answers no\n"
    "  Written --> [*]\n"
    "```\n"
)

ARROW_LINE_FLOWS = "todo export → the line exported 12 tasks, exit 0\n"


def _spec_with_flows(flows: str) -> str:
    return (
        "# Export my tasks — spec\n"
        "intent: export@0000000\n"
        "pre-build-review: not-required — small\n\n"
        "## Requirements\n"
        "REQ-1 — Export\n"
        "  The command shall export every task → Acceptance #1\n\n"
        "## Design decision\n- plain export. agent-decided\n\n"
        "## Alternatives considered\n- none worth keeping\n\n"
        "## Current state evidence\n- Forward: N/A — nothing exists yet\n\n"
        f"## UI flows\n{flows}\n"
    )


def _recompute(tmp_path: Path, flows: str) -> list[tuple[str, str]]:
    change_id = "probe-flow-forms"
    spec = tmp_path / "docs" / "loom" / change_id / "spec.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(_spec_with_flows(flows), encoding="utf-8")
    return check_ui_flows_recompute(
        load_manifest(), tmp_path, change_id, ["todo/cli/export.py"]
    )


def test_uiFlowsRecompute_arrowLineForm_accepted(tmp_path: Path) -> None:
    """Control: the one-line form the gate was written for passes."""
    assert _recompute(tmp_path, ARROW_LINE_FLOWS) == []


def test_uiFlowsRecompute_tableOnlyParallelCases_accepted(tmp_path: Path) -> None:
    """A UI flows section written as the parallel-cases table the guidance prescribes passes the gate."""
    assert flow_lines(TABLE_ONLY_FLOWS), "the table carries every case but the gate sees no flow line"
    assert _recompute(tmp_path, TABLE_ONLY_FLOWS) == []


def test_uiFlowsRecompute_mermaidOnlyBranching_accepted(tmp_path: Path) -> None:
    """A UI flows section written as the stateDiagram-v2 the guidance prescribes passes the gate."""
    assert flow_lines(MERMAID_ONLY_FLOWS), "the diagram carries every path but the gate sees no flow line"
    assert _recompute(tmp_path, MERMAID_ONLY_FLOWS) == []
