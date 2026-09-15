"""Tests for the plain-language reference.

Acceptance 6 (seven rules and five rewrite steps ending in a metaphor check),
acceptance 7 (decision questions: alternatives, recommendation, direct
yes-or-no confirmations) and acceptance 8 (eight conversation-situation
tables plus table-writing rules).
"""

import re
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SKILL_DIR = SCRIPTS.parent
PLAIN = SKILL_DIR / "references" / "plain-language.md"

SITUATIONS = {
    "Decision consequences": ("Option", "What you gain", "What you give up", "Best if"),
    "Before and after": ("Item", "Before", "After", "Impact on you"),
    "Progress report": ("Item", "Status", "Blocked on", "Next step"),
    "Acceptance checklist": ("Criterion", "Met?", "Note"),
    "Confirmed, unconfirmed, to decide": ("Item", "Status", "Basis or next step"),
    "Findings and recommendations": ("Problem", "Severity", "Recommendation"),
    "Risks": ("Risk", "Likelihood", "Impact", "Mitigation"),
    "Support matrix": ("Feature", "Environment A", "Environment B", "Environment C"),
}
DECISION_PHRASES = (
    "yes-or-no",
    "asked directly",
    "no invented alternatives",
    "at least two",
    "recommend",
    "do nothing or later",
    "smaller",
    "combining two",
    "why there is no third",
)
METAPHOR_WORDS = ('"like"', '"imagine"', '"think of it as"', "analog")


def sections(text, level=2):
    """Map each heading title at `level` to its body text."""
    marks = "#" * level
    parts = re.split(rf"^{marks} (.+)$", text, flags=re.MULTILINE)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def numbered(body):
    """Return the text of each top-level numbered list item."""
    return re.findall(r"^\d+\. (.+)$", body, flags=re.MULTILINE)


def rule_titles(text):
    """Map rule number to its H3 body under the seven-rules section."""
    body = sections(text).get("The seven rules", "")
    return {int(m.group(1)): m.group(2)
            for m in re.finditer(r"^### (\d+)\. .+$\n(.*?)(?=^### |\Z)", body,
                                 flags=re.MULTILINE | re.DOTALL)}


def header_row(body):
    """Return the cells of the first markdown table header in body, or None."""
    m = re.search(r"^\|(.+)\|\s*$\n^\|[\s:|-]+\|\s*$", body, flags=re.MULTILINE)
    return tuple(c.strip() for c in m.group(1).split("|")) if m else None


def guide_errors(text):
    """Return structural errors in the rules and rewrite steps; empty = valid."""
    errors = []
    rules = rule_titles(text)
    if sorted(rules) != list(range(1, 8)):
        errors.append(f"rules numbered {sorted(rules)}, expected 1-7")
    steps = numbered(sections(text).get("Rewrite steps", ""))
    if len(steps) != 5:
        errors.append(f"{len(steps)} rewrite steps, expected 5")
    elif "metaphor" not in steps[-1].lower():
        errors.append("last rewrite step is not a metaphor check")
    return errors


def table_errors(text):
    """Return errors in the situation tables and table rules; empty = valid."""
    errors = []
    found = sections(sections(text).get("Conversation situation tables", ""), level=3)
    titles = {re.sub(r"^\d+\. ", "", t): body for t, body in found.items()}
    for name, headers in SITUATIONS.items():
        if name not in titles:
            errors.append(f"missing situation: {name}")
        elif header_row(titles[name]) != headers:
            errors.append(f"{name}: header {header_row(titles[name])}")
    rules = sections(text).get("Table-writing rules and common mistakes")
    if rules is None:
        errors.append("missing section: Table-writing rules and common mistakes")
    elif len(numbered(rules)) < 10:
        errors.append(f"{len(numbered(rules))} table rules, expected 10")
    return errors


def _text():
    return PLAIN.read_text(encoding="utf-8")


def test_guide_has_seven_rules_and_rewrite_steps():
    text = _text()
    assert guide_errors(text) == []
    assert "Scope" in sections(text)
    assert "Internal terms" in sections(text)
    rule3 = rule_titles(text)[3]
    for word in METAPHOR_WORDS:
        assert word in rule3, word


def test_guide_without_metaphor_check_fails():
    text = _text()
    steps = numbered(sections(text)["Rewrite steps"])
    broken = text.replace(steps[-1], "Send it.")
    assert "last rewrite step is not a metaphor check" in guide_errors(broken)


def test_option_rule_two_alternatives_and_recommendation():
    rule5 = " ".join(rule_titles(_text())[5].split())
    missing = [p for p in DECISION_PHRASES if p not in rule5]
    assert not missing, missing
    assert "Nutt" in rule5 and "Chernev" in rule5


def test_yes_no_confirmation_asked_directly():
    rule5 = " ".join(rule_titles(_text())[5].split())
    sentence = next(s for s in re.split(r"(?<=[.!?])\s+", rule5) if "yes-or-no" in s)
    assert "asked directly" in sentence and "no invented alternatives" in sentence
    for action in ("publish", "delete", "confirm"):
        assert action in sentence, action


def test_eight_conversation_situations_present():
    text = _text()
    assert table_errors(text) == []
    body = sections(text)["Conversation situation tables"]
    assert "templates/01-option-comparison.md" in body


def test_missing_table_rules_section_fails():
    text = _text()
    broken = text.replace("## Table-writing rules and common mistakes", "## Other notes")
    assert "missing section: Table-writing rules and common mistakes" in table_errors(broken)


def test_reference_cites_no_repository_records():
    assert "docs/loom" not in _text()
