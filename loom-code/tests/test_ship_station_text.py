"""Ship station text: the PR title rule lives where the title is written.

The `<title>` passed to `publish` becomes the squash-merge commit, so ship
§3 affirms that its Conventional Commits type equals the branch `<type>/`
prefix -- an agent at ship never reads write-plan Step 6.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from prose_pin import has_negation

SHIP = Path(__file__).resolve().parents[1] / "skills" / "ship" / "SKILL.md"


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"section {heading!r} missing"
    return match.group(0)


def test_ship_publish_title_type_equals_branch_type() -> None:
    section = _section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once")
    flat = " ".join(section.split())
    sentences = re.split(r"(?<=[.!?])\s+", flat)
    hits = [
        s for s in sentences
        if "`<title>`" in s and "Conventional Commits subject" in s
        and "type" in s and "`<type>/`" in s and "branch" in s
        and "squash-merge commit" in s and not has_negation(s)
    ]
    assert len(hits) == 1, (
        "ship §3 needs one affirmative sentence: the `<title>` is a Conventional "
        "Commits subject whose type equals the branch `<type>/` prefix, because "
        "it becomes the squash-merge commit"
    )


LAND_COMMAND = (
    "cd '<absolute worktree root>' && python3 <loom-code>/scripts/loom_checker.py "
    "land --accepted-by <name>"
)


# ship-text-runs-land-after-acceptance (A1 positive)
def test_ship_text_runs_land_after_acceptance() -> None:
    text = SHIP.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert LAND_COMMAND in text
    assert "decision point ③" in flat
    assert "acceptance test report" in flat
    assert "`next:`" in flat and "starts with the `cd`" in flat
    assert "`land --cleanup <branch>`" in flat
    assert "`land --sweep`" in flat
    assert "`--sweep --confirm <token>`" in flat
    confirm = [
        s for s in re.split(r"(?<=[.!?])\s+", flat)
        if "`--sweep --confirm <token>`" in s and "answers yes" in s
    ]
    assert len(confirm) == 1, "the sweep token is passed only after the maintainer answers yes"
    handoff = " ".join(_section(text, "## Handoff").split())
    assert "land" in handoff and "output" in handoff


# ship-text-separates-authorization-from-acceptance
def test_ship_text_separates_authorization_from_acceptance() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert not re.search(r"^## 1\. Confirm acceptance$", text, re.M)
    assert re.search(r"^## 1\. Confirm publication authorization$", text, re.M)
    land = " ".join(_section(text, "## 5. Land after acceptance").split())
    assert (
        "Publication authorization, including `publication: automatic`, is not "
        "acceptance; always present the result and ask at decision point ③ "
        "before running land."
    ) in land


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


# ship-prose-forbids-handing-the-command-over (A3 positive)
def test_ship_prose_forbids_handing_the_command_over() -> None:
    section = _section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once")
    flat = " ".join(section.split())
    hits = [
        s for s in re.split(r"(?<=[.!?])\s+", flat)
        if NO_HANDOVER in s
        and "report the refusal and stop" in s
    ]
    assert len(hits) == 1, (
        "ship §3 needs one sentence forbidding a refused publication command "
        "from being handed to the user, and saying what the agent does instead"
    )


# ship-prose-rule-is-not-marked-as-a-gate (A3 negative)
def test_ship_prose_rule_is_not_marked_as_a_gate() -> None:
    text = SHIP.read_text(encoding="utf-8")
    assert _occurrences(text, NO_HANDOVER), (
        "the no-handover rule is missing from the ship station"
    )
    assert _gate_marked_occurrences(text, NO_HANDOVER) == [], (
        "PRINCIPLES.md forbids prose-only gates: every copy of the no-handover "
        "rule is advisory prose, and the enforceable carrier is the checker's "
        "missing-attestation refusal string"
    )


# The dash that scopes the sentence: everything before it speaks about any
# refusal, everything after it about the one state it names.
SCOPING_DASH = re.compile(r"\s+[—-]\s+")


def _no_handover_sentence() -> str:
    flat = " ".join(_section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once").split())
    hits = [s for s in re.split(r"(?<=[.!?])\s+", flat) if NO_HANDOVER in s]
    assert len(hits) == 1, "ship §3 states the no-handover rule in one sentence"
    return hits[0]


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
    # The hook's route tails (`publication_advice`) are gone with its
    # refusals (plan W1-03), so every bare refusal names no remedy.
    remediless = bare
    general = SCOPING_DASH.split(_no_handover_sentence(), maxsplit=1)[0]
    assert re.search(r"where a refusal names a remedy, take it", general), (
        "ship 3 scopes the remedy clause to the refusals that carry one; "
        f"{len(remediless)} of publish's own refusals name none"
    )
    assert re.search(r"where it names none, report the refusal and stop", general), (
        "ship 3 says what the agent does where the refusal names no remedy, "
        "because the same sentence forbids handing the command over"
    )


GITHUB_RULES = "`python3 <loom-code>/scripts/loom_checker.py github-rules`"
AGREES = "only after the user explicitly agrees in conversation"


def _sentences() -> list[str]:
    return re.split(r"(?<=[.!?])\s+", " ".join(SHIP.read_text(encoding="utf-8").split()))


# ship-runs-github-rules-before-publish (A7 positive)
def test_ship_runs_github_rules_before_publish() -> None:
    sentences = _sentences()
    runs = [
        s for s in sentences
        if "Before publishing, run " + GITHUB_RULES in s
        and "relay its lines to the user" in s and not has_negation(s)
    ]
    assert len(runs) == 1, "ship runs the github-rules probe before publishing"
    flat = " ".join(sentences)
    assert flat.index(runs[0]) < flat.index("loom_checker.py publish --intent")
    assert [s for s in sentences if "missing rule" in s and "--print-setup" in s
            and "show the user" in s], "a missing rule shows the setup command"
    assert [s for s in sentences if "could not be confirmed" in s
            and "continue publishing" in s], "unconfirmed rules do not stop Ship"


# ship-never-runs-setup-unasked (A7 negative)
def test_ship_never_runs_setup_unasked() -> None:
    sentences = _sentences()
    assert "Never run the setup command unasked." in sentences
    for s in sentences:
        if ("--print-setup" in s or "setup command" in s) and re.search(r"\brun\b", s):
            assert AGREES in s or has_negation(s), f"setup run without consent: {s}"
    assert sum(AGREES in s for s in sentences) == 1


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


# ship-template-lands-as-its-own-change (round-1 review)
def test_ship_template_missing_waits_for_consent_and_its_own_change() -> None:
    flat = " ".join(_sentences())
    assert (
        "When it reports `template not on <trunk>`, relay the printed step to the user; "
        "add the template only after the user explicitly agrees, as its own change and "
        "never inside the current change's PR, then run `github-rules` again for the rules."
    ) in flat
    assert "lands the template on the trunk first" not in flat


# ship-setup-consent-in-consequence-form (round-1 review)
def test_ship_asks_setup_consent_in_consequence_form() -> None:
    sentences = _sentences()
    hits = [s for s in sentences if "missing rule" in s and "--print-setup" in s]
    assert len(hits) == 1
    assert (
        "ask the user in consequence form — from then on <trunk> accepts changes only "
        "through a PR whose body check passes, for you too — then show the user the setup "
        "command"
    ) in hits[0]
    text = SHIP.read_text(encoding="utf-8")
    assert _gate_marked_occurrences(text, "consequence form") == [], (
        "a new prose gate would raise the net mechanism count; the consent rule is guidance"
    )


# ship-names-every-publish-refusal (round-1 review)
def test_ship_names_every_publish_refusal() -> None:
    flat = " ".join(_section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once").split())
    assert (
        "Before pushing, beyond authorization and repository safety, it refuses only a "
        "malformed body (naming the heading), a `Skipped steps:` mismatch against a bound "
        "selection, and an unidentified change."
    ) in flat


# ship-lands-from-the-change-worktree (round-1 review)
def test_ship_lands_from_the_change_branch_worktree_and_reports_status() -> None:
    text = SHIP.read_text(encoding="utf-8")
    land = " ".join(_section(text, "## 5. Land after acceptance").split())
    assert "take the root of the change branch's worktree" in land
    assert "whose branch carries the attestation" not in land
    handoff = " ".join(_section(text, "## Handoff").split())
    assert handoff.startswith(
        "## Handoff Report the attestation digest when one exists, else the verification "
        "status publish printed,"
    ), handoff
