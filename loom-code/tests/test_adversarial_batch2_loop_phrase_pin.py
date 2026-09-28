"""Adversary probe: a batch-2 file still asserts a prose phrase is present.

A test that loops over a tuple of multi-word phrases and asserts each one is
`in` the prose is a phrase pin in loop form: rewording the prose turns it red.
The batch-2 census cannot see this form, and the override rows for these files
say "no sentence asserted present".

concern: a residual positive phrase pin survives in one of the 26 batch-2 files, hidden from the census by its loop form.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BATCH_2 = [
    "loom-code/tests/test_acceptance_test_report_shape.py",
    "loom-code/tests/test_adversary_protocol.py",
    "loom-code/tests/test_adversary_routing.py",
    "loom-code/tests/test_build_mechanical_checks.py",
    "loom-code/tests/test_build_recovery_rules.py",
    "loom-code/tests/test_closing_review_recovery_rules.py",
    "loom-code/tests/test_codex_hook_trust_contract.py",
    "loom-code/tests/test_dispatch_profile_contract.py",
    "loom-code/tests/test_expert_mode_skill.py",
    "loom-code/tests/test_fix_scope_text.py",
    "loom-code/tests/test_lenses_deletion_first.py",
    "loom-code/tests/test_plan_simplicity_text.py",
    "loom-code/tests/test_review_convergence_contract.py",
    "loom-code/tests/test_reviewer_mechanical_evidence.py",
    "loom-code/tests/test_ship_station_text.py",
    "loom-code/tests/test_simplified_station_text.py",
    "loom-code/tests/test_sync_before_review_text.py",
    "loom-code/tests/test_test_budget_text.py",
    "loom-code/tests/test_write_plan_shape_text.py",
    "loom-code/tests/test_write_plan_station_text.py",
    "loom-design/tests/spec/test_capture_intent_contract.py",
    "loom-design/tests/spec/test_write_spec_contract.py",
    "loom-workflow/tests/goal-create/test_skill_md.py",
    "loom-workflow/tests/scripts/test_critique_compaction.py",
    "loom-workflow/tests/scripts/test_distill_sessions_compaction.py",
]


def _phrase(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value.split()) >= 3


def loop_phrase_pins(src: str) -> list[int]:
    """Lines of `for x in (<phrase literals>): assert x in <text>` with a positive `in`."""
    hits = []
    for loop in ast.walk(ast.parse(src)):
        if not (isinstance(loop, ast.For) and isinstance(loop.target, ast.Name)):
            continue
        if not (isinstance(loop.iter, (ast.Tuple, ast.List)) and any(_phrase(e) for e in loop.iter.elts)):
            continue
        for node in ast.walk(loop):
            test = getattr(node, "test", None) if isinstance(node, ast.Assert) else None
            if (isinstance(test, ast.Compare) and isinstance(test.left, ast.Name)
                    and test.left.id == loop.target.id and isinstance(test.ops[0], ast.In)):
                hits.append(node.lineno)
    return hits


def test_loop_phrase_pins_synthetic_affirmative_and_negated() -> None:
    """The scan flags a positive loop pin and ignores the negated (absence) form."""
    positive = 'def t():\n    for p in ("steps six govern", "x"):\n        assert p in TEXT\n'
    negated = 'def t():\n    for p in ("steps six govern", "x"):\n        assert p not in TEXT\n'
    assert loop_phrase_pins(positive) == [3]
    assert loop_phrase_pins(negated) == []


def test_batch2_files_after_prune_carry_no_loop_phrase_pin() -> None:
    """None of the pruned batch-2 files asserts a multi-word phrase present in a loop."""
    found = {rel: loop_phrase_pins((REPO / rel).read_text(encoding="utf-8")) for rel in BATCH_2}
    assert {rel: lines for rel, lines in found.items() if lines} == {}
