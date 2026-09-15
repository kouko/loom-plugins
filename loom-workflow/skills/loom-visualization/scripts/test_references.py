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
    else:
        if "metaphor" not in steps[-1].lower():
            errors.append("last rewrite step is not a metaphor check")
        first = steps[0].lower()
        if not all(w in first for w in ("conclusion", "announcement", "heading", "background")):
            errors.append("first rewrite step is not conclusion-first")
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


NEGATION = re.compile(r"\b(?:never|not|no|avoid|don't)\b", re.I)


def _sentence_with(body, phrase):
    flat = " ".join(body.split())
    return next((s for s in re.split(r"(?<=[.!?])\s+", flat) if phrase in s), "")


def polarity_errors(text):
    """Rule 3, rule 5 and yes-or-no sentences that are missing or say the opposite; empty = valid."""
    errors = []
    rules = rule_titles(text)
    ban = _sentence_with(rules.get(3, ""), "metaphors or analogies")
    if not ban.startswith("Do not use metaphors or analogies, and do not reach for"):
        errors.append("rule 3 does not ban metaphors and analogies")
    rule5 = rules.get(5, "")
    yes_no = _sentence_with(rule5, "yes-or-no confirmation")
    if "is asked directly" not in yes_no \
            or NEGATION.search(yes_no.replace("yes-or-no", "").replace("no invented alternatives", "")):
        errors.append("yes-or-no confirmation is not asked directly")
    option = _sentence_with(rule5, "you recommend")
    if "lists at least two workable alternatives and marks the one you recommend" not in option \
            or NEGATION.search(option):
        errors.append("option question does not list alternatives and mark a recommendation")
    return errors


def test_affirmative_option_and_yes_no_rules_accepted():
    """A6/A7 positive: the committed rule 3, rule 5 and yes-or-no sentences pass the polarity check."""
    assert polarity_errors(_text()) == []


def test_negated_option_rule_rejected():
    """A7 negative negated-option-rule-rejected: a flipped rule 5 sentence is caught."""
    text = _text()
    for pattern, new in ((r"marks\s+the\s+one\s+you\s+recommend", "never marks the one you recommend"),
                         (r"is\s+asked\s+directly", "is not asked directly")):
        broken, n = re.subn(pattern, new, text, count=1)
        assert n == 1, pattern
        assert polarity_errors(broken) != [], new


def test_metaphor_ban_removed_rejected():
    """A6 negative metaphor-ban-removed-rejected: rule 3 turned into permission is caught."""
    flat = _text()
    old = "Do not use metaphors or analogies, and do not reach for"
    assert old in " ".join(flat.split())
    broken = re.sub(r"Do\s+not\s+use\s+metaphors\s+or\s+analogies,\s+and\s+do\s+not\s+reach\s+for",
                    "Use metaphors or analogies, and reach for", flat, count=1)
    assert "rule 3 does not ban metaphors and analogies" in polarity_errors(broken)


def test_guide_has_seven_rules_and_rewrite_steps():
    text = _text()
    assert guide_errors(text) == []
    assert "rule 3 does not ban metaphors and analogies" not in polarity_errors(text)
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


DECISION_HEADERS = SITUATIONS["Decision consequences"]
LETTERED_OPTION = re.compile(r"\((?:[A-C])(?:,[^)]*)?\)")


def all_header_rows(body):
    """Return the cells of every markdown table header in body."""
    return [tuple(c.strip() for c in m.group(1).split("|"))
            for m in re.finditer(r"^\|(.+)\|\s*$\n^\|[\s:|-]+\|\s*$", body, flags=re.MULTILINE)]


def rule5_example_errors(text):
    """Errors when rule 5's how-question example is not a question plus a consequences table."""
    errors = []
    rule5 = rule_titles(text).get(5, "")
    if DECISION_HEADERS not in all_header_rows(rule5):
        errors.append("rule 5 example has no Decision consequences table")
    elif not re.search(r"^\| [^|\n]*\(recommended\) \|", rule5, flags=re.MULTILINE):
        errors.append("rule 5 example table marks no recommended option")
    if any(len(LETTERED_OPTION.findall(line)) >= 2 for line in rule5.splitlines()):
        errors.append("rule 5 example sets out options as prose")
    return errors


def test_rule_five_example_is_a_table():
    """A7 positive rule-five-example-is-a-table."""
    assert rule5_example_errors(_text()) == []


def test_prose_option_example_rejected():
    """A7 negative prose-option-example-rejected: the options-in-one-sentence example is caught."""
    prose = ('| "Should I refactor the parser?" | "How should the parser change? (A, recommended) '
             "Fix only the failing case: one file changes today. (B) Rewrite the parser: every "
             'input format gets retested. (C) Leave it for now." |')
    text = _text()
    rule5 = rule_titles(text)[5]
    broken = text.replace(rule5, rule5 + "\n| Hard to read | Plain |\n|---|---|\n" + prose + "\n")
    assert "rule 5 example sets out options as prose" in rule5_example_errors(broken)
    no_table = re.sub(r"\| Option \| What you gain \| What you give up \| Best if \|",
                      "| Choice | Gain | Cost | When |", rule5)
    assert "rule 5 example has no Decision consequences table" in \
        rule5_example_errors(text.replace(rule5, no_table))


# Spec REQ-7: the guide's rule 5 names the same scope as the card's inline rule.
DECISION_SCOPE = "asking or answering how to do something"


def test_rule_five_scope_matches_card():
    """A7 positive: rule 5 covers the agent asking and the user asking, in the card's words."""
    option = _sentence_with(rule_titles(_text())[5], "you recommend")
    assert DECISION_SCOPE in option, option
    card = (SKILL_DIR / "assets" / "trigger-card.md").read_text(encoding="utf-8")
    assert DECISION_SCOPE in " ".join(card.split())


def table_rule_one_errors(text):
    """Errors when table rule 1 lacks the key-value summary exception."""
    rules = numbered(sections(text).get("Table-writing rules and common mistakes", ""))
    first = rules[0] if rules else ""
    if not ("three or more attributes" in first and "key-value" in first
            and "label plus one value" in first):
        return ["table rule 1 has no key-value exception"]
    return []


def test_rule_one_key_value_exception_stated():
    """A8 positive rule-one-key-value-exception-stated."""
    assert table_rule_one_errors(_text()) == []


def test_rule_one_without_exception_fails():
    """A8 negative: rule 1 reduced to the three-attribute rule alone is caught."""
    text = _text()
    first = numbered(sections(text)["Table-writing rules and common mistakes"])[0]
    broken = text.replace(first, "Use a table only when each item has three or more attributes; "
                                 "otherwise use a list (Google, Microsoft).")
    assert table_rule_one_errors(broken) != []


OSU_URL = "https://news.osu.edu/half-of-business-decisions-fail-because-of-managements-blunders-new-study-finds/"


def nutt_citation_errors(text):
    """Errors when the 52%/32% figures are attributed to the Ohio State News article."""
    flat = " ".join(text.split())
    errors = []
    for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(\[])", flat):
        if ("52%" in s or "32%" in s) and OSU_URL in s:
            errors.append(f"figures attributed to OSU: {s[:80]}")
    return errors


def test_unsupported_nutt_figures_absent():
    """A8 negative unsupported-nutt-figures-absent: no 52%/32% sentence cites the OSU article."""
    assert nutt_citation_errors(_text()) == []
    old = ('Nutt\'s study found "whether or not" decisions failed 52% of the time, against 32% '
           f"with two or more alternatives ([Ohio State News]({OSU_URL})).")
    assert nutt_citation_errors(old) != []


def test_yes_no_confirmation_asked_directly():
    rule5 = " ".join(rule_titles(_text())[5].split())
    sentence = next(s for s in re.split(r"(?<=[.!?])\s+", rule5) if "yes-or-no" in s)
    assert "asked directly" in sentence and "no invented alternatives" in sentence
    for action in ("publish", "delete", "confirm"):
        assert action in sentence, action


KEEP_FACTS_PHRASES = (
    "keep every fact",
    "lead news",
    "a review stays a review",
    "an agent is not a person",
    "never refer to something the original did not say",
)


def test_rewrite_opens_with_conclusion_and_keeps_facts():
    text = _text()
    steps = [" ".join(s.split()) for s in numbered(sections(text)["Rewrite steps"])]
    assert "first rewrite step is not conclusion-first" not in guide_errors(text)
    facts = next((s for s in steps if "never what happened" in s), "")
    missing = [p for p in KEEP_FACTS_PHRASES if p not in facts]
    assert facts and not missing, missing
    rule2 = " ".join(rule_titles(text)[2].split())
    assert "never what happened" in rule2


def test_announcing_or_heading_opener_flagged():
    text = _text()
    steps = numbered(sections(text)["Rewrite steps"])
    announcing = text.replace(steps[0], "Say that you are explaining it again, then give a heading.")
    assert "first rewrite step is not conclusion-first" in guide_errors(announcing)
    no_heading_clause = text.replace(steps[0], steps[0].replace("heading", "title"))
    assert "first rewrite step is not conclusion-first" in guide_errors(no_heading_clause)


def test_each_missed_alternative_included_or_ruled_out():
    rule5 = " ".join(rule_titles(_text())[5].split())
    sentence = next((s for s in re.split(r"(?<=[.!?;])\s+", rule5) if "ruled out" in s), "")
    assert "For each of the three" in sentence and "one short clause" in sentence
    assert not sentence.startswith("If only two"), sentence


def test_reply_keeps_user_script():
    scope = " ".join(sections(_text())["Scope"].split())
    assert ("Reply in the user's language and script: Traditional Chinese stays "
            "Traditional, Simplified stays Simplified.") in scope


def test_eight_conversation_situations_present():
    text = _text()
    assert table_errors(text) == []
    body = sections(text)["Conversation situation tables"]
    assert "templates/01-option-comparison.md" in body


def test_missing_table_rules_section_fails():
    text = _text()
    broken = text.replace("## Table-writing rules and common mistakes", "## Other notes")
    assert "missing section: Table-writing rules and common mistakes" in table_errors(broken)


IN_CELL_ITEMS = {
    "bar with number": ("████░░░░", "same cell"),
    "sparkline": ("▁▂▃▄▅▆▇█", "Tufte", "8 levels"),
    "shape over hue": ("shape", "Status symbols"),
    "colour legend": ("legend", "WCAG 1.4.1"),
    "blank cell": ("rule 6",),
    "heatmap not possible": ("heatmap", "not possible"),
    "badge": ("shields.io", "cache"),
    "progress/meter": ("<progress>", "<meter>", "WHATWG"),
    "svg": ("<svg>", "GitHub"),
}
TIME_PHRASES = ("column axis", "cell value", "confidence", "B22", "templates/10-timeline.md")


def in_cell_errors(text):
    """Return errors in the in-cell visuals and time subsections; empty = valid."""
    errors = []
    subs = sections(sections(text).get("Table-writing rules and common mistakes", ""), level=3)
    in_cell = " ".join(subs.get("In-cell visuals", "").split())
    if not in_cell:
        errors.append("missing subsection: In-cell visuals")
    else:
        for item, phrases in IN_CELL_ITEMS.items():
            if not all(p in in_cell for p in phrases):
                errors.append(f"in-cell visuals misses {item}")
    time = " ".join(subs.get("Time in tables", "").split())
    if not time:
        errors.append("missing subsection: Time in tables")
    else:
        errors += [f"time in tables misses {p}" for p in TIME_PHRASES if p not in time]
    return errors


def test_in_cell_visuals_and_time_axis_guidance_present():
    """A8 positive in-cell-visuals-and-time-axis-guidance-present."""
    assert in_cell_errors(_text()) == []


def test_removed_in_cell_section_fails():
    """A8 negative removed-in-cell-section-fails: a renamed in-cell heading is caught."""
    text = _text()
    broken = text.replace("### In-cell visuals", "### Other notes")
    assert "missing subsection: In-cell visuals" in in_cell_errors(broken)


# Earlier table research: (subsection, phrases in that subsection, source URL in Sources).
TABLE_CRITERIA = {
    "Datawrapper two-direction comparison": (
        "Table or chart", ("two directions", "Datawrapper"),
        "https://www.datawrapper.de/blog/guide-what-to-consider-when-creating-tables"),
    "W3C WAI table as text alternative": (
        "Table or chart", ("text alternative", "flowchart", "org chart", "W3C WAI"),
        "https://www.w3.org/WAI/tutorials/images/complex/"),
    "Google no table inside numbered steps": (
        "When not to use a table", ("numbered steps", "Google"),
        "https://developers.google.com/style/tables"),
}


def table_criteria_errors(text):
    """Return missing or duplicated earlier table criteria; empty = valid."""
    errors = []
    subs = sections(sections(text).get("Table-writing rules and common mistakes", ""), level=3)
    sources = sections(text).get("Sources", "")
    flat_all = " ".join(text.split())
    for name, (sub, phrases, url) in TABLE_CRITERIA.items():
        body = " ".join(subs.get(sub, "").split())
        bullet = next((b for b in re.split(r"(?:^| )- ", body) if all(p in b for p in phrases)), None)
        if bullet is None:
            errors.append(f"missing criterion: {name}")
        elif flat_all.count(phrases[0]) != 1:
            errors.append(f"duplicated criterion: {name}")
        if url not in sources:
            errors.append(f"missing source URL: {name}")
    return errors


def test_three_earlier_criteria_present():
    """A8 positive three-earlier-criteria-present."""
    assert table_criteria_errors(_text()) == []


def test_removed_criterion_fails():
    """A8 negative removed-criterion-fails: dropping one criterion's bullet is caught."""
    text = _text()
    broken = re.sub(r"^- [^\n]*numbered steps[^\n]*\n", "", text, count=1, flags=re.MULTILINE)
    assert "missing criterion: Google no table inside numbered steps" in table_criteria_errors(broken)


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
    if "progress" not in routes.get("references/plain-language.md", "").lower():
        errors.append("plain-language row does not name progress")
    prose = " ".join(skill_text.split())
    if "a conversation-situation reply never opens a domain file" not in prose:
        errors.append("no sentence routing conversation replies to the general set only")
    if "Read only the one file whose row matches" not in prose:
        errors.append("no sentence limiting domain files to named document types")
    return errors


# Document type each held (non-pointer) entry is routed by; every one must appear in its row.
HELD_TYPES = {
    "tables-software": {
        1: ("ADR",), 2: ("RFC",), 3: ("technology selection",), 6: ("test plan",),
        8: ("feature-flag rollout",), 9: ("incident postmortem",), 10: ("incident postmortem",),
        11: ("risk register",), 12: ("RACI",), 15: ("migration guide",), 16: ("API parameters",),
        17: ("release notes",), 18: ("runbook",), 19: ("incident report",),
        21: ("decision table",), 22: ("state-transition table",), 23: ("truth table",),
        24: ("traceability",), 25: ("morphological box",), 26: ("risk matrix",),
        27: ("RAID log",), 28: ("threat model (STRIDE)",), 29: ("feature table",),
        30: ("confusion matrix",), 31: ("correlation matrix",),
    },
    "tables-design": {
        1: ("heuristic evaluation",), 2: ("usability test report",), 4: ("content audit",),
        5: ("design critique",), 6: ("design tokens",), 7: ("component states",),
        8: ("accessibility audit",), 9: ("journey map",), 10: ("personas or JTBD",),
        11: ("design decision log",),
    },
    "tables-business": {
        1: ("weighted",), 2: ("Pugh",), 3: ("RICE",), 4: ("ICE",), 5: ("MoSCoW",),
        6: ("SWOT", "TOWS"), 7: ("competitive analysis",), 8: ("Five Forces",),
        9: ("stakeholder analysis",), 11: ("scenario planning",), 12: ("business case",),
        14: ("OKR",), 15: ("assumption log",), 18: ("pricing tiers",), 19: ("WSJF",),
        20: ("decisional balance sheet",), 21: ("Kano",), 22: ("roadmap",), 23: ("2×2",),
    },
}


def _has_term(term, text):
    return re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, re.I) is not None


def held_type_routing_errors(skill_text, texts):
    """Errors when a held entry's document type is missing from its routing row, or RACI
    is routed anywhere but software; empty = valid."""
    rows = re.findall(r"^\| (.+?) \| `(references/[\w.-]+)` \|$", skill_text, flags=re.MULTILINE)
    routes = {path: need for need, path in rows}
    errors = []
    for stem, types in HELD_TYPES.items():
        need = routes.get(f"references/{stem}.md", "")
        held = {int(m.group(2)) for m in ENTRY.finditer(texts[stem])
                if not POINTER.search(entries(texts[stem])[m.group(3).strip()])}
        errors += [f"{stem}: entry {n} has no routed document type" for n in sorted(held - set(types))]
        for n, terms in types.items():
            errors += [f"{stem} row misses {t}" for t in terms if not _has_term(t, need)]
    for stem in ("tables-design", "tables-business"):
        load = re.search(r"^Load this when: (.+)$", texts[stem], flags=re.MULTILINE)
        if _has_term("RACI", routes.get(f"references/{stem}.md", "")) \
                or (load and _has_term("RACI", load.group(1))):
            errors.append(f"RACI routed to {stem}")
    return errors


def test_routing_rows_name_all_held_document_types():
    """A9 positive routing-rows-name-all-held-document-types."""
    assert held_type_routing_errors(SKILL.read_text(encoding="utf-8"), _domain_texts()) == []


def test_raci_routed_to_software_only():
    """A9 negative raci-routed-to-software-only: RACI in the business load line is caught."""
    texts = _domain_texts()
    texts["tables-business"] = re.sub(r"^(Load this when: .+?)\.$", r"\1, RACI.",
                                      texts["tables-business"], count=1, flags=re.MULTILINE)
    assert "RACI routed to tables-business" in \
        held_type_routing_errors(SKILL.read_text(encoding="utf-8"), texts)


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
