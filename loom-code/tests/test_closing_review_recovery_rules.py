"""One-home probe for the closing-review absence-recovery rules (change 2026-09-19-loom-flow-recovery-loop).

A3 negative: RL-04 — the recovery passage carries no second copy of the
             artifact-to-station mapping. The scan covers the whole
             `review.absence-recovery` gate block (the lookup paragraph
             through the decision and failure paragraphs), not one paragraph
             found by a substring match, and reads inside code spans once
             known citations are neutralized — a second copy placed in the
             next paragraph, or hidden in backticks, is still a second copy.

The rules' wording is review-only; the passage is located by its gate
marker, never by a sentence of its prose.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from prose_pin import split_sentences  # noqa: E402

SKILL = Path(__file__).resolve().parents[2] / "loom-code" / "skills" / "closing-review" / "SKILL.md"

GATE_MARKER = "<!-- gate: review.absence-recovery -->"
GATE_END = "<!-- /gate -->"

# A station reference, not any occurrence of a station name as a substring.
# `build` and `ship` are ordinary English words here ("the build", "rebuild",
# "we ship"); this prose names those stations capitalized, so only the
# capitalized word is a reference to them.
STATION_REFERENCE = re.compile(
    r"(?<![\w-])(?:capture-intent|write-spec|write-plan|closing-review)(?![\w-])"
    r"|(?<![\w-])(?:Build|Ship|Maintain)(?![\w-])"
)

# Artifact nouns a restatement of the mapping would have to name. A second copy
# phrased purely in artifact nouns — "the acceptance test report is produced
# downstream" — names no station and so slips past the check above.
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


def _recovery_passage():
    """The `review.absence-recovery` gate block: the lookup paragraph through
    the decision and failure paragraphs. A second copy of the mapping one
    paragraph over (ADV-01) is still inside this block."""
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


def test_RL_04_no_second_copy_of_the_artifact_station_mapping():
    """No paragraph in the recovery passage restates the mapping, whether by
    naming a station, by artifact nouns alone, or hidden in a code span."""
    if _read().count(GATE_MARKER) != 1:
        print(f"RL-04 FAIL: expected exactly one {GATE_MARKER!r} in {SKILL}")
        sys.exit(1)

    # Scan the whole gate block: ADV-01 placed a second copy in the very next
    # paragraph, and ADV-09 placed one inside backticks.
    offenders = _mapping_restatements(_recovery_passage())
    if offenders:
        print(f"RL-04 FAIL: the recovery passage states who produces an artifact: {offenders}")
        sys.exit(1)
    print("RL-04 PASS: the recovery passage carries no second copy of the mapping")


if __name__ == "__main__":
    test_RL_04_no_second_copy_of_the_artifact_station_mapping()
    print("All probes passed.")
