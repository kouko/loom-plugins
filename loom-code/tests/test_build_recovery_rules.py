"""One-home probes for the Build absence-recovery rule (change 2026-09-19-loom-flow-recovery-loop).

A1 negative: RL-02 — the recovery passage carries no second copy of the
             artifact-to-station mapping; it cites the contract manifest. The
             scan covers the whole `build.absence-recovery` gate block, not
             one paragraph found by a substring match, and reads inside code
             spans once known citations are neutralized — a second copy
             placed in the next paragraph, or hidden in backticks, is still a
             second copy.
A1 negative: RL-12 — §1–§2 carry no second copy of the §3 absence rule, and
             the rule's gate block occurs exactly once.

The rule's wording is review-only; the passage is located by its gate
marker, never by a sentence of its prose.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from prose_pin import split_sentences  # noqa: E402

SKILL = "loom-code/skills/build/SKILL.md"

GATE_MARKER = "<!-- gate: build.absence-recovery -->"
GATE_END = "<!-- /gate -->"

# Headings that bound the early sections a no-task run reads before it exits.
SCOPE_HEADING = "## 1. Establish scope"
VERIFY_HEADING = "## 3. Verify integration"

# Artifact nouns a restatement of the mapping would have to name. A second copy
# phrased purely in artifact nouns — "the acceptance test report is produced
# downstream" — names no station and so slips past a station-name check.
ARTIFACT_NOUNS = re.compile(
    r"(?<![\w-])(?:intents?|specs?|plans?|diffs?|attestations?"
    r"|acceptance[- ]test reports?|adversarial programs?)(?![\w-])",
    re.IGNORECASE,
)

# Words that turn an artifact noun into a claim about who produces or owns it.
PRODUCER_PHRASES = re.compile(
    r"(?<![\w-])(?:produce[ds]?|produces|producing|producer"
    r"|owns|owned|owner|owes|upstream|downstream"
    r"|comes from|belongs to|responsible for)(?![\w-])",
    re.IGNORECASE,
)

# A station reference, not any occurrence of a station name as a substring
# ("relationship", "maintains" and "ships" are ordinary English words in this
# prose, not references to closing-review, Maintain or Ship). Excludes
# "build" — this file's own station naming itself is not a restatement of
# the artifact-to-station mapping. Kept identical in wording and structure to
# closing-review's STATION_REFERENCE
# (loom-code/tests/test_closing_review_recovery_rules.py) so the two
# do not drift apart (docs/loom/memory/absence-pin-fix-recurred-in-files-authored-after-the-fix.md):
# if this pattern ever needs to change, change both copies together.
STATION_REFERENCE = re.compile(
    r"(?<![\w-])(?:capture-intent|write-spec|write-plan|closing-review)(?![\w-])"
    r"|(?<![\w-])(?:Ship|Maintain)(?![\w-])"
)

# Code-span content that cites the manifest rather than restating who
# produces what. Only these exact citations are neutralized before a
# restatement scan; anything else inside backticks is still read as prose,
# because a mapping hidden in backticks is still a second copy of it.
LEGITIMATE_CITATIONS = [
    "loom-code/contract/manifest.yaml",
    "stations[].produces",
    "actions[].owner",
    "charter.signoff",
]


def _read():
    with open(SKILL, "r", encoding="utf-8") as f:
        return f.read()


def _normalize(text):
    """Collapse whitespace so these probes test wording, not line wrapping."""
    return " ".join(text.split())


def _early_sections():
    """Return §1 and §2 — everything a no-task run reads before it would exit."""
    content = _read()
    start = content.index(SCOPE_HEADING)
    end = content.index(VERIFY_HEADING)
    return _normalize(content[start:end])


def _recovery_passage():
    """The `build.absence-recovery` gate block: the rule and the paragraphs
    that continue it. A second copy of the mapping one paragraph over
    (ADV-01) is still inside this block."""
    content = _read()
    start = content.index(GATE_MARKER)
    end = content.index(GATE_END, start)
    return _normalize(content[start + len(GATE_MARKER):end])


def _despan_for_scan(text):
    """Neutralize the known manifest citations, then unwrap any remaining
    code span into plain prose. A citation like `stations[].produces` is not
    a restatement; a mapping hidden in backticks (ADV-09) is, and blanket
    code-span stripping would hide it from the scan below."""
    for citation in LEGITIMATE_CITATIONS:
        text = text.replace(f"`{citation}`", " ")
    return re.sub(r"`([^`]*)`", r" \1 ", text)


def _mapping_restatements(text):
    """Sentences that pair an artifact noun with a claim about its producer —
    either a producer phrase ("produced by") or another station's name."""
    prose = _despan_for_scan(text)
    offenders = []
    for sentence in split_sentences(prose):
        has_artifact = ARTIFACT_NOUNS.search(sentence)
        has_claim = PRODUCER_PHRASES.search(sentence) or STATION_REFERENCE.search(sentence)
        if has_artifact and has_claim:
            offenders.append(sentence.strip())
    return offenders


def test_RL_02_no_second_copy_of_the_artifact_station_mapping():
    """No paragraph in the recovery passage restates the mapping, whether by
    naming a station, by artifact nouns alone, or hidden in a code span."""
    passage = _recovery_passage()

    for citation in ("loom-code/contract/manifest.yaml", "stations[].produces", "actions[].owner"):
        if citation not in passage:
            print(f"RL-02 FAIL: recovery passage does not cite {citation}")
            sys.exit(1)

    # Scan the whole gate block: ADV-01 placed a second copy in the very next
    # paragraph, and ADV-09 placed one inside backticks.
    offenders = _mapping_restatements(passage)
    if offenders:
        print(f"RL-02 FAIL: the recovery passage states who produces an artifact: {offenders}")
        sys.exit(1)
    print("RL-02 PASS: the producing station is read from the manifest, not restated, anywhere in the recovery passage")


def test_RL_12_the_pointer_is_not_a_second_copy_of_the_rule():
    """The early pointer points; it does not restate §3's absence rule, and §3
    states that rule exactly once, nor does it name another station."""
    content = _read()
    early = _early_sections()

    if content.count(GATE_MARKER) != 1:
        print(f"RL-12 FAIL: the absence rule gate marker appears "
              f"{content.count(GATE_MARKER)} times in {SKILL}, expected 1")
        sys.exit(1)

    # Operative content of §3's rule: if any of it is repeated early, the two
    # statements can drift apart when §3 is edited.
    operative = [
        "distinct antecedent",
        "re-run, never re-dispatched",
        "runs this section from step 1",
        "loom-code/contract/manifest.yaml",
        "stations[].produces",
        "actions[].owner",
    ]
    duplicated = [phrase for phrase in operative if phrase in early]
    if duplicated:
        print(f"RL-12 FAIL: §1–§2 restate §3's absence rule: {duplicated}")
        sys.exit(1)

    # A pointer that names another station would also be a second copy of the
    # artifact-to-station mapping, which RL-02 and closing-review's RL-04
    # forbid. Word-boundary matched, not substring: "ships" and "maintains"
    # are ordinary English words here, not station references.
    restated = sorted(set(STATION_REFERENCE.findall(_despan_for_scan(early))))
    if restated:
        print(f"RL-12 FAIL: §1–§2 name other stations: {restated}")
        sys.exit(1)
    print("RL-12 PASS: the early pointer points at §3 without restating it")


if __name__ == "__main__":
    test_RL_02_no_second_copy_of_the_artifact_station_mapping()
    test_RL_12_the_pointer_is_not_a_second_copy_of_the_rule()
    print("All probes passed.")
