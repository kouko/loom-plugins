"""Decision guidance asks for user-owned outcomes and consent, not technical risk."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2] / "loom-code" / "skills"
DOOR = ROOT / "write-plan" / "references" / "one-way-door.md"
CONFIRM = ROOT / "write-plan" / "references" / "confirm-intent.md"
PLAN = ROOT / "write-plan" / "SKILL.md"
LENSES = ROOT / "closing-review" / "references" / "lenses.md"


def text(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).lower()


def assert_rule(path: Path, pattern: str) -> None:
    assert re.search(pattern, text(path)), path


def test_technical_choice_with_evidence_proceeds() -> None:
    assert_rule(DOOR, r"(?:existing decisions|project evidence).*?(?:tests|measure).*?technical.*?(?:decide|choose)")
    assert_rule(PLAN, r"decide the technical choice.*?record.*?reason")


def test_three_tradeoffs_alone_do_not_ask() -> None:
    door = text(DOOR)
    assert re.search(r"three or more trade-offs.*?(?:alone|by itself).*?(?:not|never).*?ask", door)
    assert not re.search(r"three or more trade-offs.*?also put to the user", door)


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
