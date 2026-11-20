# concern: Sandbox recovery must retain evidence, operation consent, one retry, and denial boundaries.
"""Ship station text: headings, absences and gate-marker placement.

The wording of ship's rules is read by closing review; what stays here is
structure (section headings, gate regions), absences, and the publish
refusal premise recomputed from `publish.py`.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from prose_pin import affirms, has_negation, split_sentences

SHIP = Path(__file__).resolve().parents[1] / "skills" / "ship" / "SKILL.md"


def test_ship_bounds_execution_context_network_recovery() -> None:
    text = " ".join(SHIP.read_text(encoding="utf-8").split())
    start = text.index("### Execution-context connectivity recovery")
    recovery = text[start:text.index("Repository protection is opt-in", start)]
    for verb, literal, extras in (
        ("Apply", "`github-rules`", ("`open-pr` (including CI checks), `land`, and `delivery`",)),
        ("identifies", "known sandbox network restrictions", (
            "policy permits recovery", "authorization applicable to that operation",
            "retry the same authorized Loom command once",
            "host's permitted execution or approval mechanism")),
        ("ends", "recovery", ("Explicit platform denial", "unavailable permission mechanism", "failed retry")),
        ("Preserve", "original and retry outputs", ("stop automatic retries",)),
        ("Inspect", "partial PR-opening state", ("canonical Loom route",)),
    ):
        assert affirms(recovery, verb, literal, *extras), literal
        sample = f"{verb} {literal} {' '.join(extras)}."
        assert affirms(sample, verb, literal, *extras)
        assert not affirms(f"Do not {sample}", verb, literal, *extras)
    # Check the prohibited inference and actions in their own clauses;
    # surrounding prose and conjunctions may change without changing the rule.
    sentences = split_sentences(recovery)
    assert any(
        "connection" in s and re.search(r"\bproves neither\b.*\bDNS\b.*\bnor\b.*\bcredentials\b", s)
        for s in sentences
    )
    assert any(
        "Authentication" in s and "repository-permission" in s
        and re.search(r"\brequire\b.*\bremedy\b.*\bnot\b.*\bexecution-permission retry\b", s)
        for s in sentences
    )
    assert any(
        re.match(r"Never substitute\b", s) and "raw Git push" in s
        and "GitHub CLI" in s and "PR-opening/merge" in s
        and "alter credentials" in s and "bypass a denial" in s
        for s in sentences
    )
    assert "apply the recovery guidance above before stopping" in text
    assert "Other observation errors stop immediately." not in text


def _land_sentences() -> list[str]:
    text = SHIP.read_text(encoding="utf-8")
    section = re.search(r"^## 5\. Land after acceptance$(.*?)^## ", text, re.M | re.S)
    assert section, "ship §5 heading"
    return split_sentences(" ".join(section.group(1).split()))


# ship-reports-trunk-not-updated-and-asks (A3 positive)
def test_ship_reports_trunk_not_updated_to_the_maintainer() -> None:
    assert any(
        "`trunk not updated`" in s and "report" in s and "maintainer" in s
        and not has_negation(s.replace("`trunk not updated`", ""))
        for s in _land_sentences()
    ), "§5 must tell the agent to report land's `trunk not updated` line"


# acceptance-is-not-permission-to-discard (A3 negative)
def test_merge_acceptance_is_not_permission_to_discard_trunk() -> None:
    rule = [s for s in _land_sentences() if "discard" in s and "trunk" in s]
    assert rule, "§5 must carry the never-discard-trunk-commits rule"
    for s in rule:
        assert has_negation(s), f"affirmative discard instruction: {s}"
    # The prohibition must be the clause's own, not a negation elsewhere in
    # the sentence ("without", "is not that permission").
    assert any(re.search(r"\bNever discard local trunk commits\b", s) for s in rule), rule
    assert any(
        "reset" in s and "branch -f" in s and "explicit yes" in s
        and "③" in s and "not that permission" in s
        for s in rule
    ), "the rule names reset/branch -f and denies that acceptance at ③ is permission"
    assert any(
        "uncommitted" in s and "stash" in s and "restore" in s and "explicit yes" in s
        for s in rule
    ), "the rule also covers uncommitted changes in the trunk checkout"


# ship-text-calls-open-pr (A5 positive) / no-station-text-runs-publish-subcommand (A5 negative)
def test_ship_text_calls_open_pr_not_publish() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert "--repair open-pr --intent" in text
    assert "--repair open-pr --confirm-authorized" in text
    assert "--repair publish" not in text
    assert not re.search(r"^## \d\. Publish", text, re.M)


# ship-text-separates-authorization-from-acceptance
def test_ship_text_separates_authorization_from_acceptance() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert not re.search(r"^## 1\. Confirm acceptance$", text, re.M)
    assert re.search(r"^## 1\. Confirm PR-opening authorization$", text, re.M)


# ship-text-has-no-direct-gh-pr-merge (A1 negative)
def test_ship_text_has_no_direct_gh_pr_merge() -> None:
    flat = " ".join(SHIP.read_text(encoding="utf-8").split())
    assert not re.search(r"gh pr merge\s+[<0-9-]", flat), "no gh pr merge command form"
    for sentence in re.split(r"(?<=[.!?])\s+", flat):
        if "gh pr merge" in sentence:
            assert has_negation(sentence), f"affirmative merge instruction: {sentence}"
            clause = next(c for c in re.split(r"[:;,]", sentence) if "gh pr merge" in c)
            assert has_negation(clause), f"`gh pr merge` clause is affirmative: {sentence}"


# ship-text-adds-keep-worktree-when-maintainer-asks (A5 positive)
def test_ship_text_adds_keep_worktree_when_maintainer_asks() -> None:
    flat = " ".join(SHIP.read_text(encoding="utf-8").split())
    land = flat[flat.index("## 5. Land after acceptance"):]
    land = land[:land.index("## 6.")] if "## 6." in land else land
    assert affirms(land, "add", "`--keep-worktree`", "maintainer asks to keep the worktree")
    assert "Never type `gh pr merge` yourself" in land
    assert affirms(land, "kept", "`land --cleanup <branch>`")
    research = flat[flat.index("After verified merge into main"):]
    research = research[:research.index("`loom-code:engineering-research`")]
    assert "successful cleanup" not in research, "research follow-up waits on cleanup"


KEEP_FLAG = "`--keep-worktree`"
KEEP_VERB = re.compile(r"\b(keep|keeps|leave|leaves|stay|stays|preserve|preserves)\b.*\bworktree\b",
                       re.IGNORECASE)


def _keeps_after_block(sentences: list[str]) -> bool:
    """Some sentence names a BLOCK and the flag, and affirms keeping the worktree."""
    for s in sentences:
        if "BLOCK" not in s or KEEP_FLAG not in s:
            continue
        # The flag's own spelling contains "keep" and "worktree"; it is not the verb.
        if KEEP_VERB.search(s.replace(KEEP_FLAG, " ")) and not has_negation(s):
            return True
    return False


# ship-keep-block-recovery-keeps-worktree (A5 positive)
def test_ship_keep_block_recovery_keeps_worktree() -> None:
    land = _land_sentences()
    assert any("If land prints `Merged PR` and then a BLOCK" in s for s in land)
    assert _keeps_after_block(land), (
        "ship §5 routes a post-merge BLOCK to `land --cleanup <branch>` with no "
        "`--keep-worktree` exception; the kept worktree would be removed")


# negated-keep-sentence-rejected (A5 negative)
def test_keep_block_matcher_negated_sentence_rejected() -> None:
    assert not _keeps_after_block(split_sentences(
        "When land with `--keep-worktree` prints a BLOCK, do not keep the worktree."))
    assert not _keeps_after_block(split_sentences(
        "When land with `--keep-worktree` prints a BLOCK, run `land --cleanup <branch>`."))


GATE_OPEN_RE = re.compile(r"<!--\s*gate:\s*[A-Za-z0-9._-]+\s*-->")
GATE_CLOSE = "<!-- /gate -->"
NO_HANDOVER = "hand a refused PR-opening command to the user to run"


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


def test_delivery_runtime_mechanisms_are_registered() -> None:
    import sys
    sys.path.insert(0, str(SHIP.parents[2] / "scripts"))
    import check_mechanisms as cm
    repo = SHIP.parents[3]
    computed = cm.recompute_all(repo)
    registered = {m["id"] for m in cm.load_mechanisms(repo)}
    expected = {"Stop::loom-python", "Stop::loom-python@codex",
                "delivery.observed", "action:delivery", "action:native-git-protection"}
    assert expected <= set().union(*computed.values())
    assert expected <= registered
