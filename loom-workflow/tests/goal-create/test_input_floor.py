"""
Structural test for input-floor.md reference.

Tests verify:
- The slot-to-field mapping uses the actual field names goal-shape.md
  defines (Outcome, Verification), read from that file rather than
  hardcoded twice

WHY: The slot-to-field mapping is a live seam onto goal-shape.md: if that
file renames a field, this file's mapping text must be checked against the
renamed field, not a frozen copy of the old name.

The helpers stay in this module rather than test_goal_shape.py, whose own
`_read_reference()` reads goal-shape.md, not input-floor.md.
"""

import re
from pathlib import Path

REFERENCES_DIR = Path(__file__).resolve().parents[2] / "skills" / "goal-create" / "references"
REFERENCE_PATH = REFERENCES_DIR / "input-floor.md"
SHAPE_REFERENCE_PATH = REFERENCES_DIR / "goal-shape.md"


def _read_reference() -> str:
    """Read the reference file; fail with a descriptive message if missing."""
    assert REFERENCE_PATH.exists(), (
        f"Reference file not found: {REFERENCE_PATH}\n"
        "This is expected at RED stage. Create the reference to make this test pass."
    )
    return REFERENCE_PATH.read_text(encoding="utf-8")


def _bullet_list_items(content: str) -> list:
    """Split a top-level markdown `- ` bullet list into per-item strings.

    §5's three provenance-tag bullets carry no blank line between them, so
    paragraph-level splitting merges all three into ONE block — the same
    shape that motivated `_numbered_list_items()` for §4. That merge let a
    mutant that inverted ONE bullet (e.g. `proposed`) keep passing, because
    the OTHER two bullets' unmutated text ("quoted directly", "not ...
    confirmed", "names the anchor") were still present somewhere in the
    same merged paragraph and satisfied a bare containment/co-occurrence
    check meant for the mutated bullet. Splitting at each `- ` line start,
    the way `_numbered_list_items` splits at each `N. ` line start, binds
    each bullet's polarity to its own clause only.

    Each chunk is also cut at the next markdown heading, for the same
    reason `_numbered_list_items` does: without it, the LAST bullet in the
    list has no following `- ` boundary to stop it and silently absorbs
    every section after the list.
    """
    chunks = re.split(r"\n(?=-\s)", content)
    items = []
    for chunk in chunks:
        if not re.match(r"^-\s", chunk.strip()):
            continue
        chunk = re.split(r"\n#", chunk)[0]
        items.append(re.sub(r"\s+", " ", chunk).strip())
    return items


def _field_names_from_shape_reference() -> list:
    """Extract the field names goal-shape.md actually defines, in order.

    Headers look like: '## 1 — `Outcome`'. Pulling the names out of the
    file (instead of hardcoding "Outcome" / "Verification" as literals in
    this test) means a rename upstream fails this probe rather than
    drifting silently, per the cross-seam requirement.
    """
    assert SHAPE_REFERENCE_PATH.exists(), (
        f"Upstream reference not found: {SHAPE_REFERENCE_PATH}"
    )
    shape_content = SHAPE_REFERENCE_PATH.read_text(encoding="utf-8")
    names = re.findall(r"^## \d+ — `([\w-]+)`", shape_content, re.MULTILINE)
    assert len(names) >= 3, (
        f"Expected at least 3 field headers in {SHAPE_REFERENCE_PATH}, found {names}"
    )
    return names


def test_slot_mapping_uses_the_shape_reference_field_names() -> None:
    """Cross-seam probe: the mapping must cite goal-shape.md's real names.

    This does not hardcode "Outcome" / "Verification" as the expectation —
    it pulls the field names goal-shape.md actually defines and asserts
    this file's slot-to-field mapping paragraph uses those exact names. If
    goal-shape.md is renamed upstream, this probe fails here instead of the
    mapping silently pointing at a field that no longer exists.
    """
    field_names = _field_names_from_shape_reference()

    outcome_name = next((n for n in field_names if n.lower() == "outcome"), None)
    verification_name = next(
        (n for n in field_names if n.lower() == "verification"), None
    )
    assert outcome_name and verification_name, (
        f"goal-shape.md must define both an 'Outcome' and a 'Verification' "
        f"field; found {field_names}"
    )

    content = _read_reference()

    # §2 packs its two mapping bullets back-to-back with no blank line
    # between them, so `_paragraphs_normalized()` (blank-line splitting)
    # merges both into ONE block. Scanning that merged block for "current
    # state ... verification_name" and, separately, "wanted difference ...
    # outcome_name" only proves the four tokens co-occur somewhere in the
    # merged text — it does not prove which slot maps to which field. A
    # mutant that swaps the mapping (current state -> Outcome, wanted
    # difference -> Verification) leaves all four tokens present in the
    # same merged block and still passes. Isolating each bullet first, the
    # way `_bullet_list_items()` isolates §5's tags, binds each slot name
    # to the field name inside ITS OWN bullet only.
    section2_match = re.search(
        r"## 2 — Slot-to-field mapping\n\n(.*?)(?=\n## )", content, re.DOTALL
    )
    assert section2_match, "Expected the §2 'Slot-to-field mapping' section."
    section2_items = _bullet_list_items(section2_match.group(1))

    # Match on the bullet's OWN bolded slot name (its subject), not on
    # whether the phrase merely appears anywhere in the bullet's prose —
    # the "current state" bullet's own explanatory clause happens to
    # mention "the wanted difference" too, which would otherwise pick the
    # wrong bullet for the "wanted difference" match below.
    current_state_item = next(
        (
            item
            for item in section2_items
            if re.match(r"-\s*\*\*current state\*\*", item.lower())
        ),
        None,
    )
    assert current_state_item, (
        "Expected a §2 bullet mapping the 'current state' slot to a field."
    )
    assert verification_name.lower() in current_state_item.lower(), (
        f"Expected the 'current state' bullet itself to name the "
        f"'{verification_name}' field (as named in goal-shape.md), not "
        f"merely have that name appear elsewhere in §2."
    )

    wanted_difference_item = next(
        (
            item
            for item in section2_items
            if re.match(r"-\s*\*\*wanted difference\*\*", item.lower())
        ),
        None,
    )
    assert wanted_difference_item, (
        "Expected a §2 bullet mapping the 'wanted difference' slot to a field."
    )
    assert outcome_name.lower() in wanted_difference_item.lower(), (
        f"Expected the 'wanted difference' bullet itself to name the "
        f"'{outcome_name}' field (as named in goal-shape.md), not merely "
        f"have that name appear elsewhere in §2."
    )
