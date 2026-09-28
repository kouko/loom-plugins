"""Ship station text: headings, absences and gate-marker placement.

The wording of ship's rules is read by closing review; what stays here is
structure (section headings, gate regions), absences, and the publish
refusal premise recomputed from `publish.py`.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from prose_pin import has_negation

SHIP = Path(__file__).resolve().parents[1] / "skills" / "ship" / "SKILL.md"


# ship-text-separates-authorization-from-acceptance
def test_ship_text_separates_authorization_from_acceptance() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert not re.search(r"^## 1\. Confirm acceptance$", text, re.M)
    assert re.search(r"^## 1\. Confirm publication authorization$", text, re.M)


# ship-text-has-no-direct-gh-pr-merge (A1 negative)
def test_ship_text_has_no_direct_gh_pr_merge() -> None:
    flat = " ".join(SHIP.read_text(encoding="utf-8").split())
    assert not re.search(r"gh pr merge\s+[<0-9-]", flat), "no gh pr merge command form"
    for sentence in re.split(r"(?<=[.!?])\s+", flat):
        if "gh pr merge" in sentence:
            assert has_negation(sentence), f"affirmative merge instruction: {sentence}"


# ship-text-keeps-no-worktree-instruction (A11 negative)
def test_ship_text_keeps_no_worktree_instruction() -> None:
    text = SHIP.read_text(encoding="utf-8").lower()
    assert "keep the worktree" not in " ".join(text.split())


GATE_OPEN_RE = re.compile(r"<!--\s*gate:\s*[A-Za-z0-9._-]+\s*-->")
GATE_CLOSE = "<!-- /gate -->"
NO_HANDOVER = "hand a refused publication command to the user to run"


def _gate_regions(text: str) -> list[tuple[int, int]]:
    """Offsets of every `<!-- gate: id -->` ... `<!-- /gate -->` span."""
    regions = []
    for match in GATE_OPEN_RE.finditer(text):
        close = text.find(GATE_CLOSE, match.end())
        end = len(text) if close == -1 else close + len(GATE_CLOSE)
        regions.append((match.start(), end))
    return regions


def _occurrences(text: str, rule: str) -> list[int]:
    """Offsets of every occurrence of `rule`, not just the first."""
    return [match.start() for match in re.finditer(re.escape(rule), text)]


def _gate_marked_occurrences(text: str, rule: str) -> list[int]:
    """Offsets of the occurrences of `rule` that sit inside a gate region.

    A document can carry the rule twice -- advisory in one section, gate-marked
    in another -- so a single offset is not evidence about the document.
    """
    regions = _gate_regions(text)
    return [index for index in _occurrences(text, rule)
            if any(start <= index < end for start, end in regions)]


# ship-prose-rule-is-not-marked-as-a-gate (A3 negative)
def test_ship_prose_rule_is_not_marked_as_a_gate() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert _gate_marked_occurrences(text, NO_HANDOVER) == [], (
        "PRINCIPLES.md forbids prose-only gates: every copy of the no-handover "
        "rule is advisory prose, and the enforceable carrier is the checker's "
        "missing-attestation refusal string"
    )


# The module that emits the publication refusals ship §3 speaks about, read as
# source rather than imported: what the test needs is which reasons reach
# `report()` as a bare literal, and that is a fact about the call sites.
PUBLISH_HANDLER = (
    Path(__file__).resolve().parents[1]
    / "scripts" / "loom_checker" / "command_handlers" / "publish.py"
)


def _bare_attestation_refusals() -> list[str]:
    """Every `publish.preconditions` reason `publish` emits as a plain string.

    `_publish_block(reason, err)` is `report([("publish.preconditions", reason)])`,
    so a call whose first argument is a string constant is a refusal whose
    whole text is that constant: nothing appends a remedy to it. A call that
    passes a name (`origin_error`) is not counted -- what that name holds is
    not decidable here.
    """
    tree = ast.parse(PUBLISH_HANDLER.read_text(encoding="utf-8"))
    return [
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_publish_block"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    ]


# ship-prose-covers-the-refusals-that-name-no-remedy (A3 positive)
def test_ship_prose_covers_the_refusals_that_name_no_remedy() -> None:
    """The station may only promise a remedy where the checker names one.

    The premise is recomputed, not remembered: `publish` emits
    `publish.preconditions` refusals whose whole text is a string constant, with
    no remedy appended -- `literal origin is not a
    supported GitHub repository URL` is the one the acceptance tester hit. An
    agent that met one of those and read an unconditional "take the remedy
    that refusal names" had nothing to take and nothing it was allowed to do,
    which is the state this change exists to eliminate.

    Were every refusal later given a remedy, the premise assertion fails here
    rather than leaving the station quietly over-scoped in the other
    direction.
    """
    bare = _bare_attestation_refusals()
    assert bare, (
        "premise: `publish` emits no bare-literal attestation refusal, so "
        "every refusal may name a remedy and ship 3 could promise one outright"
    )


TWO_COPY_DOC = (
    "## 3. Publish once\n\nDo not " + NO_HANDOVER + ".\n\n"
    "## 4. Refuse\n\n"
    "<!-- gate: ship.no-handover -->\n"
    "Refuse the publication unless the agent did not " + NO_HANDOVER + ".\n"
    "<!-- /gate -->\n"
)


def test_gate_marked_locator_sees_a_second_gate_marked_copy() -> None:
    """The ship station carries no gate marker today, so the assertion above
    holds under any locator -- including one that inspects a single offset.
    Exercise the locator on the document that separates them: the advisory
    sentence in one section, the same rule gate-marked in a later one."""
    assert len(_occurrences(TWO_COPY_DOC, NO_HANDOVER)) == 2
    assert _gate_marked_occurrences(TWO_COPY_DOC, NO_HANDOVER) == [
        _occurrences(TWO_COPY_DOC, NO_HANDOVER)[1]
    ]


# ship-setup-consent-in-consequence-form (round-1 review)
def test_ship_asks_setup_consent_in_consequence_form() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert _gate_marked_occurrences(text, "consequence form") == [], (
        "a new prose gate would raise the net mechanism count; the consent rule is guidance"
    )
