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
            for m in re.finditer(r"^### (\d+)\. [^\n]+\n(.*?)(?=^### |\Z)", body,
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


# --- Domain table collections (acceptance 8) and routing (acceptance 9) ---

REFS = SKILL_DIR / "references"
SKILL = SKILL_DIR / "SKILL.md"
DOMAINS = {
    # file stem: (entry prefix, minimum entries = research count + added patterns)
    "tables-software": ("S", 20 + 11),
    "tables-design": ("D", 12),
    "tables-business": ("B", 18 + 5),
}
ENTRY = re.compile(r"^### ([SDB])(\d+)\. (.+)$", re.MULTILINE)
POINTER = re.compile(r"^Pointer: (.+)$", re.MULTILINE)
# Domain entries that are one of the eight general conversation situations.
GENERAL_POINTERS = {
    ("tables-software", "PR before and after summary"): "Before and after",
    ("tables-software", "Compatibility table"): "Support matrix",
    ("tables-software", "Weekly status report"): "Progress report",
    ("tables-software", "Known and unknown issues"): "Confirmed, unconfirmed, to decide",
    ("tables-software", "Migration plan, team-level before and after"): "Before and after",
    ("tables-design", "Microcopy before and after"): "Before and after",
    ("tables-business", "RAG status report"): "Progress report",
    ("tables-business", "Trade-off consequence table"): "Decision consequences",
    ("tables-business", "Go/No-Go decision checklist"): "Acceptance checklist",
}
LOAD_TYPES = {
    "tables-software": ("incident postmortem", "test plan", "runbook", "RACI"),
    "tables-design": ("heuristic evaluation", "design tokens", "journey map"),
    "tables-business": ("SWOT", "RICE", "go/no-go", "roadmap"),
}
CONVERSATION_WORDS = ("progress", "before and after", "checklist", "findings")


def entries(text):
    """Map each entry title to its body, up to the next H2 or H3 heading."""
    found = {}
    for m in ENTRY.finditer(text):
        rest = text[m.end():]
        stop = re.search(r"^##", rest, flags=re.MULTILINE)
        found[m.group(3).strip()] = rest[: stop.start()] if stop else rest
    return found


def domain_errors(texts):
    """Return errors across the three domain files; empty = valid."""
    errors = []
    for stem, (prefix, minimum) in DOMAINS.items():
        text = texts[stem]
        if not re.search(r"^Load this when: .+$", text, flags=re.MULTILINE):
            errors.append(f"{stem}: no 'Load this when' line")
        for doc_type in LOAD_TYPES[stem]:
            load = re.search(r"^Load this when: (.+)$", text, flags=re.MULTILINE)
            if load and doc_type not in load.group(1):
                errors.append(f"{stem}: load line misses {doc_type}")
        heads = ENTRY.findall(text)
        if any(p != prefix for p, _, _ in heads):
            errors.append(f"{stem}: entry prefix is not {prefix}")
        if [int(n) for _, n, _ in heads] != list(range(1, len(heads) + 1)):
            errors.append(f"{stem}: entries not numbered 1..{len(heads)}")
        if len(heads) < minimum:
            errors.append(f"{stem}: {len(heads)} entries, expected >= {minimum}")
        for title, body in entries(text).items():
            if "https://" not in body and not POINTER.search(body):
                errors.append(f"{stem}: {title} has no source URL or pointer")
            if POINTER.search(body) and header_row(body):
                errors.append(f"{stem}: pointer entry {title} repeats a table")
        if "docs/loom" in text:
            errors.append(f"{stem}: cites docs/loom")
    for (stem, title), situation in GENERAL_POINTERS.items():
        body = entries(texts[stem]).get(title)
        pointer = POINTER.search(body or "")
        if body is None:
            errors.append(f"{stem}: missing entry {title}")
        elif not pointer or "references/plain-language.md" not in pointer.group(1) \
                or situation not in pointer.group(1):
            errors.append(f"{stem}: {title} does not point to general {situation}")
    return errors


def risk_register_placement(texts):
    """Return (files with a full risk register entry, files with a pointer)."""
    full, pointer = [], []
    for stem in ("tables-software", "tables-business"):
        body = entries(texts[stem]).get("Risk register")
        if body is not None:
            (pointer if POINTER.search(body) else full).append(stem)
    return full, pointer


def routing_errors(skill_text):
    """Return errors in SKILL.md's Need | Read routing; empty = valid."""
    errors = []
    rows = re.findall(r"^\| (.+?) \| `(references/[\w.-]+)` \|$", skill_text, flags=re.MULTILINE)
    routes = {path: need for need, path in rows}
    for stem in ("plain-language", *DOMAINS):
        if f"references/{stem}.md" not in routes:
            errors.append(f"routing table misses references/{stem}.md")
    for stem, doc_types in LOAD_TYPES.items():
        need = routes.get(f"references/{stem}.md", "")
        for doc_type in doc_types:
            if doc_type.lower() not in need.lower():
                errors.append(f"{stem} row misses {doc_type}")
        for word in CONVERSATION_WORDS:
            if word in need.lower():
                errors.append(f"{stem} row names conversation situation: {word}")
    prose = " ".join(skill_text.split())
    if not re.search(r"conversation-situation reply \([^)]*progress[^)]*\) reads only "
                     r"`references/plain-language.md`", prose):
        errors.append("no sentence routing conversation replies to the general set only")
    if "read only when the user asks for one of its named document types" not in prose:
        errors.append("no sentence limiting domain files to named document types")
    return errors


def _domain_texts():
    return {stem: (REFS / f"{stem}.md").read_text(encoding="utf-8") for stem in DOMAINS}


def test_all_research_usages_present_per_domain():
    assert domain_errors(_domain_texts()) == []


def test_duplicated_usage_points_to_general_set():
    texts = _domain_texts()
    body = entries(texts["tables-software"])["Weekly status report"]
    table = "\n| Item | Status |\n|---|---|\n| A | Done |\n"
    texts["tables-software"] = texts["tables-software"].replace(body, body + table)
    assert "tables-software: pointer entry Weekly status report repeats a table" \
        in domain_errors(texts)


def test_risk_register_full_once_and_pointer_once():
    full, pointer = risk_register_placement(_domain_texts())
    assert len(full) == 1 and len(pointer) == 1 and set(full) != set(pointer)


def test_routing_names_document_types_per_collection():
    assert routing_errors(SKILL.read_text(encoding="utf-8")) == []


def test_conversation_reply_routes_to_general_only():
    text = SKILL.read_text(encoding="utf-8")
    broken = text.replace("| `references/tables-software.md` |",
                          "progress report | `references/tables-software.md` |")
    assert "tables-software row names conversation situation: progress" in routing_errors(broken)
    removed = re.sub(r"conversation-situation reply", "reply", text)
    assert "no sentence routing conversation replies to the general set only" \
        in routing_errors(removed)
