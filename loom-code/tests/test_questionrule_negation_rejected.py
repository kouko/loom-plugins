# concern: A prose contract test can accept a negated technical-decision rule.
"""Exercise the question-rule test against affirmative and negated guidance."""

import importlib.util
from pathlib import Path

import pytest


ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "loom-code/tests/test_one_way_door_question_rule.py").is_file()
)
TEST = ROOT / "loom-code/tests/test_one_way_door_question_rule.py"


def test_questionrule_negation_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The existing rule test should reject a same-sentence negation."""
    spec = importlib.util.spec_from_file_location("question_rule_under_test", TEST)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    door = tmp_path / "one-way-door.md"
    monkeypatch.setattr(module, "DOOR", door)

    door.write_text("Check existing decisions, project evidence, tests; for this technical choice, decide based on evidence.", encoding="utf-8")
    module.test_technical_choice_with_evidence_proceeds()

    door.write_text("Check existing decisions, project evidence, tests; for this technical choice, do not decide based on evidence.", encoding="utf-8")
    with pytest.raises(AssertionError):
        module.test_technical_choice_with_evidence_proceeds()
