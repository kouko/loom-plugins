"""Decision guidance asks for user-owned outcomes and consent, not technical risk."""

import re
import sys
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences


ROOT = Path(__file__).resolve().parents[2] / "loom-code" / "skills"
DOOR = ROOT / "write-plan" / "references" / "one-way-door.md"
CONFIRM = ROOT / "write-plan" / "references" / "confirm-intent.md"
PLAN = ROOT / "write-plan" / "SKILL.md"
LENSES = ROOT / "closing-review" / "references" / "lenses.md"


def text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).lower()


def assert_rule(path: Path, pattern: str) -> None:
    assert re.search(pattern, text(path)), path


def assert_affirmative_rule(path: Path, pattern: str) -> None:
    assert any(
        re.search(pattern, sentence) and not has_negation(sentence)
        for sentence in split_sentences(text(path), ends=".")
    ), path


def test_technical_choice_with_evidence_proceeds() -> None:
    assert_affirmative_rule(
        DOOR,
        r"(?:existing decisions|project evidence).*?(?:tests|measure).*?"
        r"(?:decide the technical choice|technical choice.*?decide)",
    )
    assert_affirmative_rule(PLAN, r"decide the technical choice.*?record.*?reason")


def test_three_tradeoffs_alone_do_not_ask() -> None:
    sentences = split_sentences(text(DOOR), ends=".")
    assert any(
        re.search(
            r"three or more trade-offs.*?(?:alone|by itself).*?"
            r"(?:do not|does not|never) require a user question",
            sentence,
        )
        for sentence in sentences
    )
    assert not any(
        re.search(r"three or more trade-offs.*?also put to the user", sentence)
        for sentence in sentences
    )


def test_three_tradeoffs_reversed_rule_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mutated = tmp_path / "one-way-door.md"
    original = DOOR.read_text(encoding="utf-8")
    assert "Three or more trade-offs\nalone do not require a user question." in original
    mutated.write_text(
        original.replace(
            "Three or more trade-offs\nalone do not require a user question.",
            "Three or more trade-offs\nalone require a user question.",
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "DOOR", mutated)
    with pytest.raises(AssertionError):
        test_three_tradeoffs_alone_do_not_ask()


def test_unresolved_user_outcome_is_asked() -> None:
    assert_rule(DOOR, r"(?:materially|substantially).*?outcome.*?unresolved.*?ask")
    assert_rule(CONFIRM, r"(?:unresolved|unknown).*?outcome.*?ask")


def test_pinned_choice_is_not_asked_again() -> None:
    assert_rule(DOOR, r"(?:pins|pinned|already decided).*?(?:do not|never).*?ask")
    assert_rule(CONFIRM, r"(?:pinned|already decided).*?(?:do not|never).*?ask")


def test_major_choice_discloses_user_consequences() -> None:
    assert_rule(DOOR, r"(?:major|material).*?choice.*?(?:disclose|show).*?consequence")
    assert_rule(LENSES, r"(?:material|major).*?choice.*?(?:disclose|show).*?consequence")


def test_data_egress_requires_consent() -> None:
    assert_rule(DOOR, r"(?:sending|send).*?existing data.*?(?:off|out).*?machine.*?(?:consent|authori[sz]ation)")
    assert_rule(LENSES, r"existing data.*?leaving.*?machine.*?(?:explicit consent|authori[sz]ation)")
