"""The shared attack protocol's own rules: `adversarial.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

What stays here is structural: the protocol and adversary.md share no rule
fragment (one home), the adversary's return block carries the three counts,
and the case-count scan (no floor anywhere, the ceiling stated once). The
protocol's sentences themselves are not pinned; review reads them.
"""
from __future__ import annotations

import re
from pathlib import Path

from loom_checker.probes import MAX_PROBE_PROGRAMS
from prose_pin import flat_prose as _flat


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
PROTOCOL = REFERENCES / "adversarial.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


# The raw protocol, for the case-count scan; the flattened protocol and
# contract, for the one-home scan.
PROTOCOL_TEXT = PROTOCOL.read_text(encoding="utf-8")
ADVERSARIAL_REF = _flat(PROTOCOL)
ADVERSARY_PROSE = _flat(ADVERSARY)


# Two protocol sentences other modules use: `UPDATE_NO_WEAKENING` is a
# one-home fragment below, and `test_build_mechanical_checks.py` exempts
# `NO_DISCARD_UNDO` from its discard-literal scan.
UPDATE_NO_WEAKENING = "An update never deletes, skips or xfails a case to make it pass."
NO_DISCARD_UNDO = (
    "Discard commands (`git checkout --`, `git restore`, `git reset --hard`, `git clean`, "
    "`git worktree remove --force`) are never used to undo a mutation, because host guards "
    "refuse them and they can destroy uncommitted work."
)


# --- One home for the protocol's rules: adversary.md repeats none of them ---

# Each fragment names one rule the protocol owns; it lives in this file and
# nowhere in adversary.md.
PROCEDURE_FRAGMENTS = (
    "already covers the target", "counts as reuse",
    "marks each probe", "counts as `modified`", "nothing in the product", "that program unchanged",
    "mutation evidence", "an over-broad update would wrongly accept",
    "the original behaviour the stale program rejected", "hold only committed content",
    "a throwaway copy of the working tree", "still exercises its own assertion", "removes that copy",
    "Discard commands", UPDATE_NO_WEAKENING,
    "an anecdote", "must be re-runnable", "needs the code changed to fail",
)


def _procedure_fragments_in_both(agent: str, ref: str) -> list[str]:
    return [f for f in PROCEDURE_FRAGMENTS if f in agent and f in ref]


def test_procedure_fragments_helper_synthetic() -> None:
    ref = "Before writing any probe, the adversary checks what already covers the target."
    assert _procedure_fragments_in_both("Read the reference first.", ref) == []
    duplicated = "Before you write any probe, check what already covers the target."
    assert _procedure_fragments_in_both(duplicated, ref) == ["already covers the target"]


def test_procedure_sentence_in_both_files_rejected() -> None:
    assert _procedure_fragments_in_both(ADVERSARY_PROSE, ADVERSARIAL_REF) == []


# --- The adversary's return block carries the three counts ------------------

def test_agent_return_block_carries_the_three_counts() -> None:
    """The counts are a field of what the adversary returns, not loose prose."""
    block = ADVERSARY.read_text(encoding="utf-8").split("```yaml", 1)[1].split("```", 1)[0]
    assert "attack_points:" in block, block
    for key in ("found", "earned_a_program", "committed"):
        assert key in block, (key, block)


# --- The case count is a ceiling, stated here and nowhere else --------------
#
# Acceptance 8 and 9 of
# `docs/loom/intent/2026-09-23-adversarial-probes-earn-their-place.md`, as the
# intent reads after the floor was dropped. Two rules, and the scan below
# answers both:
#
# 1. No runtime file states a minimum number of cases at all. The floor is
#    what made the adversary produce volume: it set a number with no relevance
#    test. What it guarded against is answered by the `concern:` line every
#    program carries and by the reviewers who read the findings. So a floor is
#    a defect wherever it is written, the allowed restatements included.
# 2. How many cases a change may commit -- the ceiling -- is a rule of this
#    protocol and of no other runtime file. Four documents may restate it in
#    their own words: the agent contract's frontmatter, which is trigger text
#    a dispatcher reads, and the two translated READMEs, the English README
#    and the conventions file, which are indexes. Each is held to agreeing
#    with the source, so a ceiling that is not five contradicts it.
#
# The scan reads a bound and its number together ("at least three", "≥3",
# "3 つ以上", "至多五個") rather than a pinned sentence, because a restatement
# is free to reword everything except the number it states.

# The number itself has one source: the checker recomputes the ceiling from
# `MAX_PROBE_PROGRAMS`, so the prose is held to that constant rather than to a
# second copy of it written here.
CAP = MAX_PROBE_PROGRAMS
FLOOR_BOUND, CAP_BOUND = "floor", "cap"

SKILLS = ROOT / "loom-code/skills"
AGENTS = ROOT / "loom-code/agents"
# Restatements the intent allows, each read whole except the agent contract,
# whose body is runtime prose like any other and whose frontmatter is the
# trigger text.
RESTATEMENTS = (
    ROOT / "loom-code/README.md",
    ROOT / "loom-code/README.ja.md",
    ROOT / "loom-code/README.zh-TW.md",
    ROOT / "AGENTS.md",
)

_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}
_NUM = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|[一二三四五六七八九十])"
_BOUND_BEFORE = {
    "at least": FLOOR_BOUND, "no fewer than": FLOOR_BOUND,
    "not fewer than": FLOOR_BOUND, "a minimum of": FLOOR_BOUND,
    "至少": FLOOR_BOUND, "≥": FLOOR_BOUND,
    "at most": CAP_BOUND, "no more than": CAP_BOUND, "not more than": CAP_BOUND,
    "a maximum of": CAP_BOUND, "up to": CAP_BOUND,
    "至多": CAP_BOUND, "最多": CAP_BOUND, "≤": CAP_BOUND,
}
_BOUND_AFTER = {"以上": FLOOR_BOUND, "以下": CAP_BOUND}
# English states a bound after the number too, and puts it after the noun as
# often as before it ("three or more cases", "three probe programs minimum").
_BOUND_AFTER_EN = {
    "or more": FLOOR_BOUND, "or greater": FLOOR_BOUND, "minimum": FLOOR_BOUND,
    "or fewer": CAP_BOUND, "or less": CAP_BOUND, "maximum": CAP_BOUND,
}
_COUNT_RE = re.compile(
    rf"(?P<pre>{'|'.join(_BOUND_BEFORE)})\s*\**\s*(?P<n1>{_NUM})"
    rf"|(?P<n2>{_NUM})\s*(?:つ|個|件|の)?\s*(?P<post>{'|'.join(_BOUND_AFTER)})"
    rf"|\b(?P<n3>{_NUM})\b(?:\s+[A-Za-z][\w-]*){{0,3}}"
    rf"\s+(?P<post_en>{'|'.join(_BOUND_AFTER_EN)})\b",
    re.IGNORECASE,
)
# What the number has to be counting for the match to be this rule and not
# another one: an adversarial case, probe or program. The noun has to be the
# number's own head, not merely nearby -- "at least one mutation per kind of
# change" sits in a paragraph about probe programs and counts mutations, and
# "at least two reviewers read the probe programs" counts readers. English and
# Chinese put the head after the number, Japanese before it.
_CASE_NOUN = re.compile(r"\bcases?\b|\bprobes?\b|\bprograms?\b|ケース|案例", re.IGNORECASE)
_CJK = re.compile(r"[぀-ヿ㐀-鿿]")
_LEADING_MARKUP = " \t*_`\"'()[]:,"
# Inside a noun phrase, a comma or a bracket separates two modifiers of the
# same head ("three executable, abuse and boundary cases"); only a word ends
# the phrase, and `_PHRASE_END` says which ones.
_INNER_MARKUP = " \t*_`\"'()[],"
# A word that closes the number's own noun phrase: a determiner, a preposition
# or an auxiliary starts something the number is no longer counting. "at least
# two reviewers read the probe programs" stops at "the", so the programs after
# it are not what the two counts.
_PHRASE_END = {
    "a", "an", "the", "this", "that", "these", "those", "its", "their", "his",
    "her", "our", "your", "every", "each", "all", "any", "both", "some", "no",
    "per", "of", "in", "on", "for", "from", "against", "with", "by", "to",
    "at", "into", "than", "over", "under", "before", "after", "as", "if",
    "when", "where", "which", "who", "whose", "whom", "it", "they", "them",
    "is", "are", "was", "were", "be", "been", "has", "have", "had", "must",
    "should", "may", "can", "will", "shall", "does", "do", "did",
}
_BACK, _FORWARD, _HEAD_WORDS = 12, 60, 6


def _head_is_a_case(text: str) -> bool:
    """True when the noun the number counts, at the start of `text`, is a case.

    English puts modifiers between the number and its head noun -- "three
    executable abuse and boundary cases" -- so the first word does not decide;
    the words are read in order until one of them is a case noun, or until the
    noun phrase ends. It ends at punctuation, at a determiner, preposition or
    auxiliary (`_PHRASE_END`), or after `_HEAD_WORDS` words, which is what
    keeps "two reviewers read the probe programs" a count of readers and "one
    mutation per kind of change" a count of mutations. Chinese and Japanese
    put a classifier and any modifiers between the number and its head with no
    word boundary to split on ("三個可執行的邊界案例"), so a CJK run is read as
    a whole instead.
    """
    rest = text.lstrip(_LEADING_MARKUP)
    if not rest:
        return False
    if _CJK.match(rest):
        return bool(_CASE_NOUN.search(rest[:_FORWARD]))
    for _ in range(_HEAD_WORDS):
        word = re.match(r"[A-Za-z][\w-]*", rest)
        if not word:
            return False
        if _CASE_NOUN.fullmatch(word.group()):
            return True
        if word.group().lower() in _PHRASE_END:
            return False
        rest = rest[word.end():].lstrip(_INNER_MARKUP)
    return False


def _number(token: str) -> int:
    return int(token) if token.isdigit() else _NUMBERS[token.lower()]


def _units(text: str) -> list[str]:
    """The text in the units a rule is stated in: paragraphs, and each table
    row on its own, so that no window below reaches out of one row into the
    next."""
    units: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        lines = paragraph.splitlines()
        units += [ln for ln in lines if ln.lstrip().startswith("|")]
        units.append(" ".join(ln for ln in lines if not ln.lstrip().startswith("|")))
    return [" ".join(unit.split()) for unit in units if unit.strip()]


def case_counts(text: str) -> set[tuple[str, int]]:
    """Every (bound, number) pair the text states about cases, `floor` or `cap`."""
    found: set[tuple[str, int]] = set()
    for unit in _units(text):
        for match in _COUNT_RE.finditer(unit):
            if match.group("pre"):
                if not _head_is_a_case(unit[match.end():]):
                    continue
                found.add((_BOUND_BEFORE[match.group("pre").lower()], _number(match.group("n1"))))
            elif match.group("post"):
                behind = unit[max(0, match.start() - _BACK):match.start()]
                if not (_CASE_NOUN.search(behind) or _head_is_a_case(unit[match.end():])):
                    continue
                found.add((_BOUND_AFTER[match.group("post")], _number(match.group("n2"))))
            else:
                # The head sits either between the number and the bound word
                # ("three probe programs minimum") or after it ("three or
                # more cases").
                if not (
                    _head_is_a_case(unit[match.end("n3"):])
                    or _head_is_a_case(unit[match.end():])
                ):
                    continue
                found.add((
                    _BOUND_AFTER_EN[match.group("post_en").lower()],
                    _number(match.group("n3")),
                ))
    return found


def _body(path: Path) -> str:
    """The file without a YAML frontmatter block, which is trigger text."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        return text[4:].split("\n---\n", 1)[1]
    return text


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text[4:].split("\n---\n", 1)[0] if text.startswith("---\n") else ""


def runtime_prose_files() -> list[Path]:
    """Every runtime prose file of loom-code that is not the source."""
    return sorted(
        p for p in list(SKILLS.rglob("*.md")) + list(AGENTS.glob("*.md"))
        if p != PROTOCOL
    )


def test_case_counts_reads_every_wording_synthetic() -> None:
    assert case_counts("write at least three cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("write **at least three** cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("実行可能な境界ケース 3 つ以上を書く") == {(FLOOR_BOUND, 3)}
    assert case_counts("至少三個可執行的邊界案例") == {(FLOOR_BOUND, 3)}
    assert case_counts("≥3 個可執行的邊界案例") == {(FLOOR_BOUND, 3)}
    assert case_counts("a change commits at most five probe programs") == {(CAP_BOUND, 5)}
    assert case_counts("at most four cases") == {(CAP_BOUND, 4)}
    # Plain English states the same floor without the phrase "at least".
    assert case_counts("write three or more cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("a minimum of three cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("write not fewer than three cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("three probe programs minimum") == {(FLOOR_BOUND, 3)}
    assert case_counts("a maximum of five probe programs") == {(CAP_BOUND, 5)}
    assert case_counts("five probe programs maximum") == {(CAP_BOUND, 5)}
    # Modifiers stand between the number and its head noun. This is the
    # wording this change deleted from the READMEs, and acceptance testing pasted it
    # back into `loom-code/README.md` with the whole suite still green.
    assert case_counts(
        "at least three executable abuse and boundary cases"
    ) == {(FLOOR_BOUND, 3)}
    assert case_counts("at most five executable probe programs") == {(CAP_BOUND, 5)}
    # A comma or a bracket inside the noun phrase is punctuation between two
    # modifiers, not the end of the phrase; the head is still `cases`.
    assert case_counts(
        "at least three executable, abuse and boundary cases"
    ) == {(FLOOR_BOUND, 3)}
    assert case_counts("at most five (executable) probe programs") == {(CAP_BOUND, 5)}


def test_case_counts_ignores_a_count_of_something_else_synthetic() -> None:
    """A number beside another noun is not a count of cases."""
    assert case_counts("when it reports `up to date`, continue") == set()
    assert case_counts("the episode admits at most three distinct digests") == set()
    assert case_counts(
        "mutation evidence run against the committed probe program itself: at least "
        "one mutation per kind of change the update touches"
    ) == set()
    # A table row's number belongs to its own row, not to the row above it.
    table = "| **read** | ≥2 fresh-context reviewers | verdict |\n| **attack** | cases |\n"
    assert case_counts(table) == set()
    # The number's head noun decides, not whatever noun follows within a
    # window: these count readers, and say nothing about how many cases.
    assert case_counts("at least two reviewers read the probe programs") == set()
    # A comma does not end the phrase, so the word after it still has to be
    # the head: here the phrase ends at a determiner as it always did.
    assert case_counts(
        "at least two reviewers, and the probe programs they read"
    ) == set()
    assert case_counts(
        "at least one reviewer re-runs every probe program of the change"
    ) == set()


def test_body_and_frontmatter_helpers_synthetic() -> None:
    path = ADVERSARY
    assert _frontmatter(path).startswith("name: adversary"), _frontmatter(path)[:40]
    assert "name: adversary" not in _body(path)
    assert _body(path).lstrip().startswith("# adversary subagent")


def test_protocol_states_the_ceiling_and_no_floor() -> None:
    assert case_counts(PROTOCOL_TEXT) == {(CAP_BOUND, CAP)}


def test_no_runtime_prose_states_a_minimum_case_count() -> None:
    """Rule 1: a floor is a defect wherever it is written.

    Every runtime prose file, the protocol and the four allowed restatements
    included, because a restatement may keep its own words but not reintroduce
    the number the intent removed.
    """
    read = {PROTOCOL: PROTOCOL_TEXT, ADVERSARY: ADVERSARY.read_text(encoding="utf-8")}
    read |= {path: path.read_text(encoding="utf-8") for path in RESTATEMENTS}
    read |= {path: path.read_text(encoding="utf-8") for path in runtime_prose_files()}
    floors = {
        str(path.relative_to(ROOT)): sorted(n for bound, n in case_counts(text) if bound == FLOOR_BOUND)
        for path, text in read.items()
        if any(bound == FLOOR_BOUND for bound, _ in case_counts(text))
    }
    assert floors == {}, floors


def test_no_second_statement_of_the_case_count_in_runtime_prose() -> None:
    """Rule 2: the ceiling is stated in the protocol and in no other runtime
    file. A recipe, a station or an agent body that states a number of cases
    again is a second place to keep right."""
    second = {
        str(path.relative_to(ROOT)): sorted(case_counts(_body(path)))
        for path in runtime_prose_files()
        if case_counts(_body(path))
    }
    assert second == {}, second


def test_no_restatement_contradicts_the_source() -> None:
    allowed = {(CAP_BOUND, CAP)}
    sources = {str(p.relative_to(ROOT)): p.read_text(encoding="utf-8") for p in RESTATEMENTS}
    sources["loom-code/agents/adversary.md frontmatter"] = _frontmatter(ADVERSARY)
    contradicting = {
        name: sorted(case_counts(text) - allowed)
        for name, text in sources.items()
        if case_counts(text) - allowed
    }
    assert contradicting == {}, contradicting
