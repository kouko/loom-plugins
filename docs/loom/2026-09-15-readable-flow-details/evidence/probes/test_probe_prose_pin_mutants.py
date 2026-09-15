"""Adversary probes: hand-written mutation testing of the change's own
contract tests.

The engineering baseline says a test that pins a sentence of prose rejects
any negation token in that same sentence. The W1-01..W1-03 tests pin with
bare substring or `re.search` checks. Each mutant below copies the real
station text into a temporary directory, flips the polarity of ONE pinned
sentence the way a careless compression would, points the implementer's test
module at the copy, and runs the tests that pin that sentence. A mutant that
every targeted test still passes is a surviving mutant: those tests assert
presence of words, not the rule.

The station files themselves are never modified.

Run from the repo root:
    python3 -m pytest docs/loom/2026-09-15-readable-flow-details/evidence/probes/test_probe_prose_pin_mutants.py -q -p no:cacheprovider
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
import types
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

CAPTURE_TESTS = ROOT / "loom-design/scripts/spec/test_capture_intent_contract.py"
WRITE_SPEC_TESTS = ROOT / "loom-design/scripts/spec/test_write_spec_contract.py"
WRITE_PLAN_TESTS = ROOT / "loom-code/scripts/test_write_plan_shape_text.py"

CAPTURE_SKILL = ROOT / "loom-design/skills/capture-intent/SKILL.md"
WRITE_SPEC_DIR = ROOT / "loom-design/skills/write-spec"
WRITE_PLAN_SKILL = ROOT / "loom-code/skills/write-plan/SKILL.md"


def _load(path: Path, name: str) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _mutate(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"mutation anchor must occur exactly once: {old!r}"
    return text.replace(old, new, 1)


def _killed(module: types.ModuleType, tests: list[str]) -> list[str]:
    """Names of the targeted tests that fail on the mutated text."""
    failing = []
    for name in tests:
        try:
            getattr(module, name)()
        except AssertionError:
            failing.append(name)
    return failing


def _capture_module(tmp_path: Path, old: str, new: str) -> types.ModuleType:
    module = _load(CAPTURE_TESTS, f"probe_capture_{tmp_path.name}")
    copy = tmp_path / "capture-intent" / "SKILL.md"
    copy.parent.mkdir(parents=True)
    copy.write_text(_mutate(CAPTURE_SKILL.read_text(encoding="utf-8"), old, new), encoding="utf-8")
    module.SKILL = copy
    return module


def _write_spec_module(tmp_path: Path, old: str, new: str) -> types.ModuleType:
    module = _load(WRITE_SPEC_TESTS, f"probe_write_spec_{tmp_path.name}")
    copy_dir = tmp_path / "write-spec"
    shutil.copytree(WRITE_SPEC_DIR, copy_dir)
    skill = copy_dir / "SKILL.md"
    skill.write_text(_mutate(skill.read_text(encoding="utf-8"), old, new), encoding="utf-8")
    module.SKILL = skill
    return module


def _write_plan_module(tmp_path: Path, old: str, new: str) -> types.ModuleType:
    module = _load(WRITE_PLAN_TESTS, f"probe_write_plan_{tmp_path.name}")
    copy = tmp_path / "write-plan" / "SKILL.md"
    copy.parent.mkdir(parents=True)
    copy.write_text(_mutate(WRITE_PLAN_SKILL.read_text(encoding="utf-8"), old, new), encoding="utf-8")
    module.WRITE_PLAN = copy
    return module


# --- harness self-tests (synthetic) ---


def test_mutationHarness_syntheticPinnedLiteralDeleted_killed(tmp_path: Path) -> None:
    """A synthetic test pinning a literal fails once the literal is removed."""
    source = tmp_path / "doc.md"
    source.write_text("The station writes a spec.", encoding="utf-8")
    module = types.ModuleType("synthetic")
    module.PATH = source

    def test_pin() -> None:
        assert "writes a spec" in module.PATH.read_text(encoding="utf-8")

    module.test_pin = test_pin
    source.write_text(_mutate(source.read_text(encoding="utf-8"), "writes a spec", "writes a plan"), encoding="utf-8")
    assert _killed(module, ["test_pin"]) == ["test_pin"]


def test_mutationHarness_syntheticAmbiguousAnchor_refused() -> None:
    """The mutator refuses an anchor that occurs more than once."""
    with pytest.raises(AssertionError):
        _mutate("a spec. a spec.", "a spec", "no spec")


def test_writePlanReadbackControl_negatedLeadVerb_killed(tmp_path: Path) -> None:
    """Control: a negation inside the pinned regex span is caught by the implementer's test."""
    module = _write_plan_module(
        tmp_path,
        "branches, lead with a table or a text (ASCII) diagram",
        "branches, never lead with a table or a text (ASCII) diagram",
    )
    assert _killed(module, ["test_write_plan_readback_leads_with_table_or_text_diagram"])


# --- mutants that flip one pinned sentence's polarity ---


def test_writePlanForcingSentence_negationPrefix_killed(tmp_path: Path) -> None:
    """write-plan's 'non-empty list forces that spec' sentence, negated, fails its tests."""
    module = _write_plan_module(
        tmp_path,
        "A non-empty carried-details list — from",
        "Never assume that a non-empty carried-details list — from",
    )
    assert _killed(
        module,
        ["test_carried_details_force_minimal_spec", "test_no_details_keeps_evidence_only_plan"],
    ), "surviving mutant: the forcing sentence can be negated and every targeted test passes"


def test_captureIntentHandOffForcing_negationPrefix_killed(tmp_path: Path) -> None:
    """capture-intent's 'write-plan must still write a spec' sentence, negated, fails its tests."""
    module = _capture_module(
        tmp_path,
        "When the list is non-empty and",
        "It is not the case that, when the list is non-empty and",
    )
    assert _killed(
        module,
        ["test_hand_off_lists_agreed_details_and_requires_spec", "test_no_details_no_forced_spec"],
    ), "surviving mutant: the hand-off forcing sentence can be negated and every targeted test passes"


def test_captureIntentCarriedTable_negatedShowVerb_killed(tmp_path: Path) -> None:
    """capture-intent's 'Show them as a table' instruction, negated, fails its test."""
    module = _capture_module(
        tmp_path,
        "Show them as a table, one row per detail",
        "Never show them as a table, one row per detail",
    )
    assert _killed(module, ["test_engineering_restatement_shows_carried_details_table"]), (
        "surviving mutant: 'Never show them as a table' passes the A5 positive test"
    )


def test_writeSpecCarriedRecording_negatedRecordVerb_killed(tmp_path: Path) -> None:
    """write-spec's 'record each item in the spec' instruction, negated, fails its test."""
    module = _write_spec_module(
        tmp_path,
        "hand-off and record each item in the spec",
        "hand-off and do not record each item in the spec",
    )
    assert _killed(module, ["test_spec_records_each_carried_detail"]), (
        "surviving mutant: 'do not record each item in the spec' passes the A1 positive test"
    )


def test_writeSpecReadbackLead_negatedLeadVerb_killed(tmp_path: Path) -> None:
    """write-spec's decision point ② 'lead with a table' instruction, negated, fails its test."""
    module = _write_spec_module(
        tmp_path,
        "When a flow has parallel cases or branches, lead with a table or a text",
        "When a flow has parallel cases or branches, do not lead with a table or a text",
    )
    assert _killed(module, ["test_readback_leads_with_table_or_text_diagram"]), (
        "surviving mutant: 'do not lead with a table' passes the A3 positive test"
    )
