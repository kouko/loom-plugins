"""Ship station text: the PR title rule lives where the title is written.

The `<title>` passed to `publish` becomes the squash-merge commit, so ship
§3 affirms that its Conventional Commits type equals the branch `<type>/`
prefix -- an agent at ship never reads write-plan Step 6.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

from loom_checker.command_handlers.push import PUBLICATION_ROUTES
from loom_checker.command_handlers.push import publication_advice
from loom_checker.selection import ENTRY_TOKENS
from loom_checker.selection import confirmation_prompt_matches
from loom_checker.selection import selection_code
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
    assert "blind-run report" in flat
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
        and "closing-review station" in s
        and "step selection" in s
        and "confirms by typing" in s
    ]
    assert len(hits) == 1, (
        "ship §3 needs one sentence forbidding a refused publication command "
        "from being handed to the user, and naming both legal routes: run the "
        "closing-review station, or propose a step selection the user confirms "
        "by typing a confirmation prompt"
    )
    # Which prompt is not pinned here: the form the station may name is the
    # form `confirmation_prompt_matches` accepts, and
    # `test_ship_prose_names_a_confirmation_the_checker_accepts` runs it.


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


# The counts a `...; found <n>` attestation refusal can report, plus the
# unknown-count caller. `publication_advice` decides per count which tail it
# appends, so how many routes a refusal names is a fact about the code.
REFUSAL_COUNTS = (None, 0, 1, 2, 3)

# The dash that scopes the sentence: everything before it speaks about any
# refusal, everything after it about the one state it names.
SCOPING_DASH = re.compile(r"\s+[—-]\s+")


def _no_handover_sentence() -> str:
    flat = " ".join(_section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once").split())
    hits = [s for s in re.split(r"(?<=[.!?])\s+", flat) if NO_HANDOVER in s]
    assert len(hits) == 1, "ship §3 states the no-handover rule in one sentence"
    return hits[0]


# ship-prose-promises-only-what-every-refusal-names (A3 positive)
def test_ship_prose_promises_only_what_every_refusal_names() -> None:
    """What the station may promise is read from the checker, not remembered.

    Two facts come out of `publication_advice`: every count gets a non-empty
    tail, so "take what the refusal names" holds for all of them; and only one
    count gets `PUBLICATION_ROUTES`, so naming routes in a clause that speaks
    about any refusal promises a state the checker does not always produce.
    The clause before the scoping dash is therefore held to the first fact and
    the routes belong after it, where the sentence names the state they apply
    to.

    Chosen over `assert "the two legal routes it names" not in sentence`: the
    literal passes the moment the same false promise is reworded, and says
    nothing if `publication_advice` later changes which counts carry routes --
    this reads both from the module. Its limit is the dash: a sentence that
    hides an unconditional promise after one is not caught, and only the
    refusal string itself is enforceable.
    """
    advice = {count: publication_advice(count) for count in REFUSAL_COUNTS}
    assert all(tail.strip() for tail in advice.values()), (
        "every refusal names something the agent can act on"
    )
    assert [count for count, tail in advice.items() if tail is not PUBLICATION_ROUTES], (
        "premise: some refusal names no route -- were every refusal to carry "
        "PUBLICATION_ROUTES again, the station could promise routes outright"
    )
    general = SCOPING_DASH.split(_no_handover_sentence(), maxsplit=1)[0]
    for promise in ("route", "closing-review", "step selection"):
        assert promise not in general.lower(), (
            f"ship §3 promises {promise!r} for any refusal, but the checker "
            "names the routes for one attestation count only; scope the "
            "promise to that state, after the dash"
        )


# The module that emits the publication refusals ship §3 speaks about, read as
# source rather than imported: what the test needs is which reasons reach
# `report()` as a bare literal, and that is a fact about the call sites.
PUBLISH_HANDLER = (
    Path(__file__).resolve().parents[1]
    / "scripts" / "loom_checker" / "command_handlers" / "publish.py"
)


def _bare_attestation_refusals() -> list[str]:
    """Every `push.attestation` reason `publish` emits as a plain string.

    `_publish_block(reason, err)` is `report([("push.attestation", reason)])`,
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
    `push.attestation` refusals whose whole text is a string constant, with
    none of `publication_advice`'s tails in it -- `literal origin is not a
    supported GitHub repository URL` is the one the blind runner hit. An
    agent that met one of those and read an unconditional "take the remedy
    that refusal names" had nothing to take and nothing it was allowed to do,
    which is the state this change exists to eliminate.

    Were every refusal later given a remedy, the premise assertion fails here
    rather than leaving the station quietly over-scoped in the other
    direction.
    """
    tails = {publication_advice(count) for count in REFUSAL_COUNTS}
    bare = _bare_attestation_refusals()
    assert bare, (
        "premise: `publish` emits no bare-literal attestation refusal, so "
        "every refusal may name a remedy and ship 3 could promise one outright"
    )
    remediless = [
        reason for reason in bare
        if not any(tail in reason for tail in tails)
    ]
    assert remediless, (
        "premise: every bare refusal carries a publication_advice tail after all"
    )
    general = SCOPING_DASH.split(_no_handover_sentence(), maxsplit=1)[0]
    assert re.search(r"where a refusal names a remedy, take it", general), (
        "ship 3 scopes the remedy clause to the refusals that carry one; "
        f"{len(remediless)} of publish's own refusals name none"
    )
    assert re.search(r"where it names none, report the refusal and stop", general), (
        "ship 3 says what the agent does where the refusal names no remedy, "
        "because the same sentence forbids handing the command over"
    )


# The confirmation prompt the station names, in backticks with `<code>` where
# the proposal's code goes -- the one part of the sentence the user retypes.
CONFIRMATION_FORM = re.compile(r"`([^`]*<code>[^`]*)`")


# ship-prose-names-a-confirmation-the-checker-accepts (A3 positive)
def test_ship_prose_names_a_confirmation_the_checker_accepts() -> None:
    """The prompt the station tells the user to type is run through the
    matcher that decides whether a typed prompt binds anything.

    `confirmation_prompt_matches` binds a selection only when the prompt's
    first token is one of `ENTRY_TOKENS` and the code is a standalone token
    after it, so a station that asks for the bare code sends the user to a
    prompt that binds nothing and leaves the reviewer floor where it was.
    Asserting the literal `/loom-code:expert-mode <code>` would pin one of the
    four entry tokens and would keep passing if the matcher later stopped
    accepting it; executing the form catches both, and any reword that is
    wrong in a new way fails the same assertion.
    """
    sentence = _no_handover_sentence()
    forms = CONFIRMATION_FORM.findall(sentence)
    assert len(forms) == 1, (
        "ship §3 names exactly one confirmation prompt, in backticks, with "
        "`<code>` standing for the code the proposal printed"
    )
    code = selection_code("2026-09-18-example-change", [], ["reviewers"])
    assert confirmation_prompt_matches(forms[0].replace("<code>", code), code), (
        f"the prompt ship §3 names, {forms[0]!r}, binds nothing: "
        "confirmation_prompt_matches wants an entry token first, then the code"
    )
    # The placeholder is the code's seat, not decoration: naming the prompt
    # without it, or the code without the prompt, binds nothing either.
    assert not confirmation_prompt_matches(forms[0].replace("<code>", "").strip(), code)
    assert not confirmation_prompt_matches(code, code)


# Every backticked form in the sentence whose first word is an entry-point
# token: the confirmation spellings the station offers the user.
BACKTICKED = re.compile(r"`([^`]+)`")


# ship-prose-names-every-confirmation-spelling-the-checker-accepts (A3 positive)
def test_ship_prose_names_every_confirmation_spelling_the_checker_accepts() -> None:
    """`expert-mode` always gives the Codex spelling beside the Claude Code
    one, because a reader on either host retypes the form in front of them.

    Which spellings count as entry points is read from `selection.ENTRY_TOKENS`
    and each one the station names is run through the matcher, so a station
    that named a fifth spelling the matcher does not accept fails here, and so
    does one that drops to a single host again.
    """
    sentence = _no_handover_sentence()
    named = [
        form for form in BACKTICKED.findall(sentence)
        if form.split()[0] in ENTRY_TOKENS
    ]
    assert len(named) >= 2, (
        "ship 3 names the Claude Code and Codex spellings of the confirmation, "
        f"as `expert-mode` does; it names {named}"
    )
    code = selection_code("2026-09-18-example-change", [], ["reviewers"])
    for form in named:
        prompt = form if "<code>" in form else f"{form} <code>"
        assert confirmation_prompt_matches(prompt.replace("<code>", code), code), (
            f"the spelling ship 3 names, {form!r}, binds nothing"
        )


# ship-prose-states-the-hook-body-check-limit (A3 positive)
def test_ship_prose_states_the_limit_of_the_hook_body_check() -> None:
    """The hook reads the body file when the command is proposed; `gh` reads it
    again when the command runs. Nothing holds the bytes still in between, and
    no `PreToolUse` hook can: it judges a command it does not execute.

    `test_probe_body_can_change_between_the_check_and_the_request` runs that
    swap. The station says it out loud so an agent does not read the check as a
    promise about the pull request's contents. Advisory prose, no gate marker --
    the enforceable carrier stays the checker's own refusal."""
    section = " ".join(_section(SHIP.read_text(encoding="utf-8"), "## 3. Publish once").split())
    hits = [
        s for s in re.split(r"(?<=[.!?])\s+", section)
        if "judges the body it can read when it looks" in s
        and "not the body the pull request receives" in s
        and "swapped" in s
    ]
    assert len(hits) == 1, (
        "ship §3 needs one sentence stating that the hook judges the body it "
        "can read when it looks, not the body the pull request receives, and "
        "that a file swapped between the two reads is outside what any such "
        "check can promise"
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
