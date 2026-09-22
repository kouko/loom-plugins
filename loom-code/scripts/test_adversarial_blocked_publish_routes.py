"""Adversarial probes for `2026-09-18-blocked-publish-names-the-legal-routes`.

The change appends one shared sentence (`push.PUBLICATION_ROUTES`) to the two
refusals that fire when a branch carries no single attestation -- the push /
publish gate and `land`'s earlier acceptor-derivation refusal -- and adds an
advisory rule to the ship station's prose. Two halves are attacked here:

* the gate must not have moved: same exit code, same rule id, the same number
  of `BLOCK ` lines, and the original reason still the literal prefix; and
* the routes the new sentence names must be routes that actually work.

Probes named `probe_...` that pass are attacks the change repelled. Probes
carrying `pytest.mark.xfail(strict=True)` are confirmed defects: the body
asserts what the refusal text promises, it does not hold today, and the strict
marker turns the probe red the moment the promise becomes true so the marker is
removed with the defect. No product code, existing test or record is touched by
this module.

The module carries no marker now -- every finding it recorded (F1 through F13)
was closed, and each probe stayed as the regression for its own finding. Two
were re-aimed rather than converted, because the fix answered the finding in a
way the probe had not demanded; each says so in its own docstring rather than
here. A marker must fail at its own assertion and not in fixture setup: the F6
probe once died in `git switch` and recorded that instead, so a new marker is
read under `--runxfail` before it is trusted.

Probes that neither pass on a promise nor carry a marker say "recorded, not
scored" in their first line. They are measurements of a boundary the change
chose and the reader should be able to see -- what a forged ref still costs,
what half of a finding a fix did not reach -- and they assert the behaviour
they describe, so a boundary that moves is caught rather than silently
outgrowing its own docstring.

Twice now a probe went wrong by modelling git's state one level less precisely
than the checker reads it, both times in the landed-branch fixture, and the
second time the first repair was the cause. `test_probe_landed_fixture_builds
_the_refs_a_real_clone_builds` is the answer to that class: it clones a local
repository offline and requires the fixture's refs to match, so what a landed
branch looks like is read off git rather than off whichever product function
last happened to open one.
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

import test_ship_station_text as ship_text
from loom_checker.command_handlers import push as push_handler
from loom_checker.command_handlers.publish import MISSING_ATTESTATION
from loom_checker.command_handlers.push import EXTRA_ATTESTED_CHANGES
from loom_checker.command_handlers.push import NOTHING_TO_PUBLISH
from loom_checker.command_handlers.push import PUBLICATION_ROUTES
from loom_checker.intent_state import remote_default_snapshot
from loom_checker.rule_checks.publish import render_selection_disclosure
from loom_checker.rule_checks.push import canonical_pr_create_trailing
from loom_checker.rule_checks.push import github_repo_from_origin
from loom_checker.rule_checks.push import pr_create_body
from loom_checker.rule_checks.push import render_quote_all

SCRIPTS = Path(__file__).resolve().parent
CHECKER = SCRIPTS / "loom_checker.py"
SESSION = "adversarial-blocked-publish-routes"

# The reasons origin/main emitted for these inputs. The change may append to
# them; it may not replace, reword or re-rule them.
PUSH_REASON = "branch must carry exactly one generated attestation; found "
# `land` no longer counts attestations: on these fixtures (branch `feature`, no
# intent in the delta) it refuses because the change is unidentified, whatever
# the attestation count. The text is identify_change's, restated here.
LAND_UNIDENTIFIED = (
    "cannot identify the change: branch 'feature' names no committed intent and "
    "the branch delta carries 0 intent files; rename the branch to "
    "<type>/<change-id> or commit the intent docs/loom/intent/<change-id>.md"
)


def _tail(count: int) -> str:
    """The advice the refusal carries for this attestation count. The two routes
    belong to the zero case alone; above one neither of them reduces the count,
    so that state is told what does.

    Deliberately not `push.publication_advice`: a probe that asks the product
    which tail it should have emitted proves only that the product agrees with
    itself. The rule is restated here, and `test_probe_only_a_zero_count_is_ever
    _offered_the_routes` checks the emitted bytes against the count directly."""
    return PUBLICATION_ROUTES if count == 0 else EXTRA_ATTESTED_CHANGES


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["CLAUDE_CODE_SESSION_ID"] = SESSION
    env["CLAUDE_CODE_SESSION_ATTENDED"] = "1"
    return env


def _checker(repo: Path, argv: list[str], stdin: str = "") -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECKER), *argv], cwd=str(repo),
                          capture_output=True, text=True, env=_env(), input=stdin)


def _repo(root: Path, name: str, change_ids: tuple[str, ...] = ()) -> Path:
    """A branch whose delta carries one attestation file per change id."""
    repo = root / name
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "switch", "-q", "-c", "feature")
    _git(repo, "remote", "add", "origin", "git@github.com:example/project.git")
    for change_id in change_ids:
        target = repo / "docs" / "loom" / change_id / "attestation.json"
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps({"change_id": change_id}), encoding="utf-8")
    if change_ids:
        _git(repo, "add", ".")
        _git(repo, "commit", "-q", "-m", "attest")
    return repo


def _blocks(stderr: str) -> list[tuple[str, str]]:
    out = []
    for line in stderr.splitlines():
        assert line.startswith("BLOCK "), f"stderr line is not a BLOCK line: {line!r}"
        rule, _sep, reason = line.removeprefix("BLOCK ").partition(": ")
        out.append((rule, reason))
    return out


def _hook(command: str, cwd: Path) -> str:
    return json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash",
                       "tool_input": {"command": command}, "cwd": str(cwd)})


# --------------------------------------------------------------------------
# Half one: the gate must not have moved.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("count", [0, 2, 3])
def test_probe_push_refusal_keeps_rule_exit_and_reason_prefix(tmp_path, count) -> None:
    """Attack: make the appended text change which rule fires, the exit code,
    or the wording the caller already parses."""
    ids = tuple(f"2026-09-18-change-{index}" for index in range(count))
    result = _checker(_repo(tmp_path, f"push{count}", ids), ["push"])
    assert result.returncode == 1
    assert _blocks(result.stderr) == [
        ("push.attestation", f"{PUSH_REASON}{count}{_tail(count)}")
    ]


@pytest.mark.parametrize("count", [0, 2])
def test_probe_land_refusal_keeps_rule_exit_and_reason_prefix(tmp_path, count) -> None:
    """Attack: the same, through `land`'s own earlier refusal site. `land` no
    longer refuses on the attestation count; what remains is its unidentified-
    change refusal, under the same rule id and exit code."""
    ids = tuple(f"2026-09-18-change-{index}" for index in range(count))
    result = _checker(_repo(tmp_path, f"land{count}", ids),
                      ["land", "--accepted-by", "kouko"])
    assert result.returncode == 1
    assert _blocks(result.stderr) == [("land.merge", LAND_UNIDENTIFIED)]


@pytest.mark.parametrize("count", [0, 1, 2, 3, 4])
def test_probe_only_a_zero_count_is_ever_offered_the_routes(tmp_path, count) -> None:
    """Attack: reach a state that is offered the two routes while the branch
    already attests something, which is where neither route reduces the count.

    Read off the emitted bytes, with no call into the product's own chooser."""
    ids = tuple(f"2026-09-18-change-{index}" for index in range(count))
    stderr = _checker(_repo(tmp_path, f"only{count}", ids), ["push"]).stderr
    (rule, reason), = _blocks(stderr)
    assert rule == "push.attestation", stderr
    offered = "two legal routes" in reason
    assert offered == (count == 0), stderr
    if count == 1:
        # one attestation passes the count and is refused on its contents, so
        # the refusal must be a different one rather than merely not this one.
        assert PUSH_REASON not in reason
        assert reason == "attestation has an unknown or incomplete schema", stderr
    else:
        assert reason.startswith(f"{PUSH_REASON}{count}"), stderr


def test_probe_routes_text_is_one_line_with_no_control_characters() -> None:
    """Attack: break `report()`'s one-`BLOCK`-line-per-failure contract by
    smuggling a newline, a carriage return or an escape into either tail."""
    for tail in (PUBLICATION_ROUTES, EXTRA_ATTESTED_CHANGES):
        assert not re.search(r"[\r\n\x00-\x08\x0b-\x1f\x7f]", tail)
        assert not tail.startswith("\n")
        assert tail.startswith("; ")


def test_probe_hook_mode_keeps_exit_two_and_only_block_lines(tmp_path) -> None:
    """Attack: make the longer reason survive the hook path as something other
    than a single refusal line, or as a non-blocking exit."""
    repo = _repo(tmp_path, "hook")
    result = _checker(repo, ["push", "--hook"],
                      _hook("git push origin HEAD:refs/heads/feature", repo))
    assert result.returncode == 2
    blocks = _blocks(result.stderr)
    assert [rule for rule, _ in blocks] == ["push.attestation", "push.attestation"]
    assert blocks[0][1] == f"{PUSH_REASON}0{PUBLICATION_ROUTES}"


def test_probe_refspec_refusal_still_emits_two_separate_block_lines(tmp_path) -> None:
    """Attack: let the appended sentence swallow the refspec refusal that is
    printed straight after it."""
    repo = _repo(tmp_path, "refspec")
    result = _checker(repo, ["push", "--hook"], _hook("git push origin feature", repo))
    assert result.returncode == 2
    blocks = _blocks(result.stderr)
    assert [rule for rule, _reason in blocks] == ["push.attestation", "push.attestation"]
    assert blocks[0][1] == f"{PUSH_REASON}0{PUBLICATION_ROUTES}"
    assert not blocks[1][1].endswith(PUBLICATION_ROUTES)


def test_probe_hostile_change_id_cannot_reach_the_reason(tmp_path) -> None:
    """Attack: name a change directory so that the refusal interpolates a
    forged second `BLOCK` line or an allow into the longer reason."""
    hostile = (
        # git quotes the embedded newline, so this one never even matches the
        # attestation glob; the other two do, and make the count a refusal.
        "2026-09-18-a\nBLOCK push.attestation: publication approved",
        "2026-09-18-b; echo pwned",
        "2026-09-18-c` ; BLOCK push.attestation: publication approved",
    )
    result = _checker(_repo(tmp_path, "hostile", hostile), ["push"])
    assert result.returncode == 1
    (rule, reason), = _blocks(result.stderr)
    assert rule == "push.attestation"
    assert re.fullmatch(
        rf"{re.escape(PUSH_REASON)}\d+"
        rf"(?:{re.escape(PUBLICATION_ROUTES)}|{re.escape(EXTRA_ATTESTED_CHANGES)})",
        reason,
    ), reason
    assert "pwned" not in result.stderr and "publication approved" not in result.stderr


def test_probe_other_derivation_failures_do_not_gain_the_routes(tmp_path) -> None:
    """Attack: widen `land`'s `startswith(MISSING_ATTESTATION)` guard so a
    refusal that is not about a missing attestation also claims the routes."""
    repo = _repo(tmp_path, "uncommitted", ("2026-09-18-only",))
    _git(repo, "reset", "-q", "--soft", "HEAD~1")
    _git(repo, "reset", "-q")
    result = _checker(repo, ["land", "--accepted-by", "kouko"])
    assert result.returncode == 1
    (rule, reason), = _blocks(result.stderr)
    assert rule == "land.merge"
    assert not reason.startswith(MISSING_ATTESTATION)
    assert PUBLICATION_ROUTES not in reason


def test_probe_land_names_no_attestation_route(tmp_path) -> None:
    """Attack: let `land` keep offering the attestation routes after it stopped
    refusing a missing attestation. Its only refusal here is the unidentified
    change, which names the fix and no route."""
    land = _checker(_repo(tmp_path, "l"), ["land", "--accepted-by", "kouko"]).stderr
    assert _blocks(land) == [("land.merge", LAND_UNIDENTIFIED)]
    assert PUBLICATION_ROUTES not in land


def test_probe_routes_are_not_appended_twice(tmp_path) -> None:
    """Attack: `land` appends, then delegates to the push handler, which
    appends again. Neither appends now: the refusal carries no route at all."""
    result = _checker(_repo(tmp_path, "twice"), ["land", "--accepted-by", "kouko"])
    (rule, reason), = _blocks(result.stderr)
    assert rule == "land.merge", result.stderr
    assert reason == LAND_UNIDENTIFIED, result.stderr
    assert reason.count("two legal routes") == 0


# --------------------------------------------------------------------------
# Half two: the routes the refusal names must work.
# --------------------------------------------------------------------------


NAMED_PROPOSE = re.search(r"`(loom_checker\.py selection propose[^`]*)`", PUBLICATION_ROUTES)


def _propose_argv(change_id: str) -> list[str]:
    """The proposal command exactly as the refusal writes it."""
    assert NAMED_PROPOSE, "the refusal no longer names a proposal command"
    tokens = NAMED_PROPOSE.group(1).split()
    assert tokens[0] == "loom_checker.py"
    return [change_id if token == "<change-id>" else token for token in tokens[1:]]


NAMED_CONFIRMATION = re.search(r"confirms by typing `([^`]+)`", PUBLICATION_ROUTES)


def _named_prompt(code: str) -> str:
    """The confirmation exactly as the refusal writes it, with the code filled
    in. The refusal tells the user what to type, so a probe that follows it
    literally must type this and nothing else."""
    assert NAMED_CONFIRMATION, "the refusal no longer names a confirmation form"
    return NAMED_CONFIRMATION.group(1).replace("<code>", code)


def _bind(repo: Path, change_id: str, extra: list[str], *, prompt=_named_prompt) -> dict:
    """Propose with the refusal's own command, let the user type a
    confirmation, and return what `selection show` reports."""
    proposal = _checker(repo, [*_propose_argv(change_id), *extra])
    assert proposal.returncode == 0, proposal.stderr
    code = proposal.stdout.split("code:")[1].strip().split()[0]
    payload = json.dumps({"hook_event_name": "UserPromptSubmit",
                          "prompt": prompt(code),
                          "prompt_id": f"p-{code}", "session_id": SESSION})
    _checker(repo, ["selection", "capture", "--hook"], payload)
    shown = _checker(repo, ["selection", "show", change_id])
    assert shown.returncode == 0, shown.stderr
    return json.loads(shown.stdout)


CHANGE = "2026-09-18-blocked-publish-names-the-legal-routes"


def _propose_argv_without_skip(change_id: str) -> list[str]:
    """The refusal's own proposal command with `--skip <steps>` taken out --
    the command it printed before F1 was fixed."""
    argv = _propose_argv(change_id)
    index = argv.index("--skip")
    del argv[index:index + 2]
    return argv


def _confirm_then_finalize(repo: Path, change_id: str, argv: list[str],
                           tmp_path: Path, name: str):
    """Propose with `argv`, have the user confirm, and run finalize-review with
    an empty verdict list -- the input that only passes when the floor is zero.

    The adversarial artifact is supplied because without it `finalize.adversarial`
    fires first and the run never reaches the reviewer floor at all, which is how
    this probe and its control previously passed each other by."""
    proposal = _checker(repo, argv)
    assert proposal.returncode == 0, proposal.stderr
    code = proposal.stdout.split("code:")[1].strip().split()[0]
    _checker(repo, ["selection", "capture", "--hook"], json.dumps({
        "hook_event_name": "UserPromptSubmit",
        "prompt": f"/loom-code:expert-mode {code}",
        "prompt_id": f"p-{name}", "session_id": SESSION}))
    shown = _checker(repo, ["selection", "show", change_id])
    assert shown.returncode == 0, shown.stderr
    review = tmp_path / f"{name}-review.json"
    review.write_text(json.dumps({
        "verdicts": [], "findings": [],
        "adversarial": [{"command": "python3 probe_ok.py", "artifact": "probe_ok.py"}],
    }), encoding="utf-8")
    return json.loads(shown.stdout), _checker(
        repo, ["finalize-review", change_id, "--input", str(review)])


def test_probe_named_proposal_drops_the_reviewer_floor(tmp_path) -> None:
    """Attack: follow the refusal literally and see whether the second route
    reaches the state the refusal says it reaches -- a finalize-review that
    accepts no verdicts at all and still writes the attestation."""
    change_id = "2026-09-18-floor-drops"
    repo = _publishable_fixture(tmp_path, "floordrop", change_id)
    shown, finalized = _confirm_then_finalize(
        repo, change_id, _propose_argv(change_id), tmp_path, "drop")
    assert shown["skip"] == ["reviewers"]
    assert finalized.returncode == 0, finalized.stderr
    assert (repo / "docs" / "loom" / change_id / "attestation.json").is_file()


def test_probe_named_proposal_without_the_skip_does_not_drop_the_floor(tmp_path) -> None:
    """The genuine negative. The same route with `--skip reviewers` removed --
    the command the refusal printed before F1 was fixed -- binds a selection that
    skips nothing, and finalize-review refuses at the floor.

    This is what the old "control" was meant to be. It was not: `_propose_argv`
    reads the command out of `PUBLICATION_ROUTES`, which has carried
    `--skip reviewers` since `bf3cfc81`, so the control's extra flag was a
    duplicate and the two fixtures were identical."""
    change_id = "2026-09-18-floor-holds"
    repo = _publishable_fixture(tmp_path, "floorhold", change_id)
    argv = _propose_argv_without_skip(change_id)
    assert "--skip" not in argv
    shown, finalized = _confirm_then_finalize(repo, change_id, argv, tmp_path, "hold")
    assert shown["skip"] == []
    assert finalized.returncode == 1
    (rule, reason), = _blocks(finalized.stderr)
    assert rule == "finalize.verdicts", finalized.stderr
    assert reason == "review input has no verdicts", finalized.stderr


def test_probe_typing_the_named_confirmation_confirms_the_selection(tmp_path) -> None:
    """Attack: do exactly what the refusal tells the user to do -- type the
    confirmation in the form the refusal spells out, and nothing else."""
    repo = _repo(tmp_path, "named-confirmation")
    assert _bind(repo, CHANGE, ["--skip", "reviewers"])["bound"] is True


def test_probe_bare_code_still_binds_nothing(tmp_path) -> None:
    """F2's other half: the form the refusal used to name binds nothing, so the
    refusal may not go back to naming it. No rule moved to make F2 pass."""
    repo = _repo(tmp_path, "bare-code")
    bound = _bind(repo, CHANGE, ["--skip", "reviewers"], prompt=lambda code: code)
    assert bound["bound"] is False


def test_probe_entry_token_form_is_what_actually_confirms(tmp_path) -> None:
    """Control for F2: the same code behind `/loom-code:expert-mode` binds,
    written out here rather than read from the refusal, so the two cannot drift
    into agreeing with each other about a form the checker rejects."""
    repo = _repo(tmp_path, "entry-token")
    bound = _bind(repo, CHANGE, ["--skip", "reviewers"],
                  prompt=lambda code: f"/loom-code:expert-mode {code}")
    assert bound["bound"] is True


def test_probe_two_attestation_branch_is_named_a_remedy_that_works(tmp_path) -> None:
    """Attack: on the branch shape that carries two attestations, take the
    closing-review route and see whether the publication becomes possible.

    It does not, so the refusal must not name it here; and whatever it names
    instead has to be something this branch can actually reach."""
    ids = ("2026-09-18-change-0", "2026-09-18-change-1")
    repo = _repo(tmp_path, "two", ids)
    blocked = _checker(repo, ["push"])
    assert blocked.returncode == 1
    assert PUBLICATION_ROUTES not in blocked.stderr
    assert EXTRA_ATTESTED_CHANGES in blocked.stderr

    # "run the closing-review station, which generates the attestation": what it
    # generates is one attestation file for one change id, written in place.
    target = repo / "docs" / "loom" / ids[0] / "attestation.json"
    target.write_text(json.dumps({"change_id": ids[0], "regenerated": True}),
                      encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "closing-review")

    # The count is untouched, so the same refusal stands: naming that route here
    # would have sent the agent round a loop that cannot terminate.
    assert f"{PUSH_REASON}2" in _checker(repo, ["push"]).stderr

    # What the refusal names instead: end the delta at one attested change.
    _git(repo, "rm", "-q", "-r", f"docs/loom/{ids[1]}")
    _git(repo, "commit", "-q", "-m", "publish one change per branch")
    after = _checker(repo, ["push"])
    assert PUSH_REASON not in after.stderr
    assert EXTRA_ATTESTED_CHANGES not in after.stderr
    # The count is no longer what blocks: the refusal has moved on to the
    # placeholder attestation's own contents, which is progress, not a loop.
    assert "attestation has an unknown or incomplete schema" in after.stderr


# --------------------------------------------------------------------------
# Half three: the ship prose must not become a gate.
# --------------------------------------------------------------------------


def _document_with_the_rule_inside_a_gate() -> str:
    """A ship station whose §3 carries the advisory sentence and whose later
    section repeats the same rule inside a gate-marked region."""
    return (
        "# Ship\n\n"
        "## 3. Publish once\n\n"
        "Do not run a separate attestation preflight, construct Git push or "
        "PR-create commands, or " + ship_text.NO_HANDOVER + "; on a refusal take "
        "one of the two legal routes it names -- run the closing-review station, "
        "which generates the attestation, or propose a step selection the user "
        "confirms by typing the code.\n\n"
        "## 4. Refuse\n\n"
        "<!-- gate: ship.no-handover -->\n"
        "Refuse the publication unless the agent did not "
        + ship_text.NO_HANDOVER + ".\n"
        "<!-- /gate -->\n"
    )


def test_probe_no_gate_assertion_sees_a_gate_marked_second_copy() -> None:
    """Attack: satisfy the ship station's no-gate assertion while the rule is in
    fact inside a gate-marked region.

    Re-aimed. The probe committed with F4 replicated the assertion's locator
    (`text.find`) inline, so it went on failing no matter what the station test
    did -- it was attacking a copy of the defect, not the mechanism. It now
    calls the shipped locator, so it attacks whatever the station test uses
    today and fails the moment that goes back to inspecting one offset."""
    text = _document_with_the_rule_inside_a_gate()
    assert ship_text._gate_regions(text), "the document must contain a gate region"
    assert ship_text._gate_marked_occurrences(text, ship_text.NO_HANDOVER), (
        "a gate-marked copy of the no-handover rule escaped the locator the "
        "ship station's no-gate assertion uses"
    )


def test_probe_first_copy_alone_would_still_have_missed_it() -> None:
    """Control: the document is the one that defeated the old locator -- two
    occurrences, the first outside every region -- so the probe above passes on
    the mechanism's strength, not because the document got easier."""
    text = _document_with_the_rule_inside_a_gate()
    regions = ship_text._gate_regions(text)
    occurrences = ship_text._occurrences(text, ship_text.NO_HANDOVER)
    assert len(occurrences) == 2
    assert not any(start <= occurrences[0] < end for start, end in regions)
    assert ship_text._gate_marked_occurrences(text, ship_text.NO_HANDOVER) == [
        occurrences[1]
    ]


def test_probe_ship_station_carries_no_gate_marker_at_all() -> None:
    """Attack: the negative assertion is vacuous today -- record that, so a
    later edit that introduces any gate marker into the ship station has to
    confront the weakness F4 describes."""
    assert "<!-- gate:" not in ship_text.SHIP.read_text(encoding="utf-8")


def test_probe_gate_open_marker_grammar_is_narrow() -> None:
    """Attack: hide the rule behind a gate comment the counter cannot parse.

    Repelled, not by the counter but by the grammar above it: AGENTS.md
    declares `<!-- gate: <id> -->` as the marker, so a comment outside that
    grammar is not a gate anywhere in this repository either, and a reader
    following the declared grammar reaches the same answer the counter does."""
    for marker in ("<!-- gate: ship.no-handover (advisory) -->",
                   "<!-- gate:ship no-handover -->"):
        text = f"{marker}\n{ship_text.NO_HANDOVER}\n<!-- /gate -->\n"
        assert not ship_text._gate_regions(text)


# --------------------------------------------------------------------------
# Half four: the seam from the attestation finalize-review emits to the
# attestation a publication command reads, crossed with a real skip.
# --------------------------------------------------------------------------


SEAM_CHANGE = "2026-09-18-seam-probe"

PR_HEADINGS = ("Context", "Intended outcome", "Scope", "Decisions", "Implementation",
               "Behaviour change", "Verification", "Risks and rollback", "Follow-ups")


def _pr_body(verification_opening: tuple[str, ...] = ()) -> str:
    """A body that clears the structural floor, with a chosen Verification
    opening so a disclosure line is present or absent on purpose."""
    blocks = []
    for heading in PR_HEADINGS:
        lines = list(verification_opening) if heading == "Verification" else []
        lines.append("This section carries enough substantive prose to pass.")
        blocks.append(f"## {heading}\n\n" + "\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def _attested_branch_with_a_skip(tmp_path: Path) -> tuple[Path, dict]:
    """Run the real closing-review finalization on a branch whose user-typed
    selection skips the reviewers, and return the repo and the attestation."""
    repo = _repo(tmp_path, "seam")
    (repo / "docs" / "loom").mkdir(parents=True)
    (repo / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text(
        "# Kickoff Defaults\n\n"
        "- package-tests: python3 probe_ok.py — fixture (2026-09-18)\n",
        encoding="utf-8")
    (repo / "probe_ok.py").write_text("print('ok')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "fixture")

    assert _bind(repo, SEAM_CHANGE, ["--skip", "reviewers"])["skip"] == ["reviewers"]

    review = tmp_path / "seam-review.json"
    review.write_text(json.dumps({
        "verdicts": [], "findings": [],
        "adversarial": [{"command": "python3 probe_ok.py", "artifact": "probe_ok.py"}],
    }), encoding="utf-8")
    finalized = _checker(repo, ["finalize-review", SEAM_CHANGE, "--input", str(review)])
    assert finalized.returncode == 0, finalized.stderr
    attestation = json.loads(
        (repo / "docs" / "loom" / SEAM_CHANGE / "attestation.json").read_text(encoding="utf-8"))
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "attest")
    return repo, attestation


def _commit_intent(repo: Path, change_id: str) -> None:
    """`publish` refuses a change it cannot identify; on branch `feature` the
    one intent in the delta is what identifies it."""
    intent = repo / "docs" / "loom" / "intent" / f"{change_id}.md"
    intent.parent.mkdir(parents=True, exist_ok=True)
    intent.write_text("# Change\nstatus: confirmed 2026-09-18\n\n"
                      "## Proposed outcome\nThe probe's change.\n", encoding="utf-8")
    _git(repo, "add", str(intent))
    _git(repo, "commit", "-q", "-m", "intent")


def test_probe_finalize_and_push_agree_across_the_seam(tmp_path) -> None:
    """Attack: each half of the seam is proven separately against a
    hand-written payload, so cross it for real -- emit the attestation with
    finalize-review and hand that very file to the publication gate."""
    repo, attestation = _attested_branch_with_a_skip(tmp_path)
    assert attestation["selection"]["skip"] == ["reviewers"]
    assert [c["skip"] for c in attestation["selection"]["confirmations"]] == [["reviewers"]]
    assert _checker(repo, ["push"]).returncode == 0


def test_probe_publish_refuses_a_body_that_hides_the_skip(tmp_path) -> None:
    """Attack: publish a real skipped-reviewer change with a body that says
    nothing about the skip. Repelled by `push.contextual-body`."""
    repo, _attestation = _attested_branch_with_a_skip(tmp_path)
    _commit_intent(repo, SEAM_CHANGE)
    body = tmp_path / "body-no-disclosure.md"
    body.write_text(_pr_body(), encoding="utf-8")
    result = _checker(repo, ["publish", "--title", "feat(x): seam probe",
                             "--body-file", str(body), "--confirm-authorized"])
    assert result.returncode == 1
    # This refusal's reason spans lines (it quotes the disclosure it wants), so
    # it is read as a whole rather than through the one-line `_blocks` reader.
    assert result.stderr.startswith("BLOCK push.contextual-body: ")
    assert "Skipped steps: reviewers" in result.stderr


def _canonical_metadata_command(repo: Path, body: Path) -> str:
    """The one trusted PR-opening Bash form the hook admits."""
    gh_repo = github_repo_from_origin(repo)
    assert gh_repo, "the fixture origin must resolve to a GitHub identity"
    return render_quote_all([
        "command", str(Path(shutil.which("env")).resolve()),
        f"LOOM_REPO_ROOT={repo.resolve()}", f"GH_REPO={gh_repo}",
        str(Path(shutil.which("gh")).resolve()), "pr", "create",
        "--head", "feature", "--title", "feat(x): seam probe",
        "--body-file", str(body),
    ])


def _run_hook(repo: Path, command: str, monkeypatch, *,
              payload_cwd: Path | None = None) -> tuple[int, str]:
    """The publication hook on one Bash command, with the live remote-head
    lookup -- the external seam -- answered with the state that holds right
    after a successful push.

    `payload_cwd` is the directory the Bash tool would run the command in. The
    hook chdirs to the repository root regardless, so the two differ whenever
    the agent is working from a subdirectory."""
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": command},
               "cwd": str(payload_cwd or repo)}
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SESSION)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ATTENDED", "1")
    monkeypatch.setattr(push_handler, "read_hook_payload", lambda *a, **k: payload)
    monkeypatch.setattr(push_handler, "check_pr_create_remote_head", lambda *a, **k: None)
    monkeypatch.chdir(repo)
    out, err = io.StringIO(), io.StringIO()
    return push_handler.cmd_push(["--hook"], out, err), err.getvalue()


def test_probe_hook_refuses_a_pr_body_that_hides_the_skip(tmp_path, monkeypatch) -> None:
    """Attack: same repository, same undisclosed body, the other route.

    F5's marker is gone: `f8a5559a` made the hook ask publish's own
    `selection_disclosure_failure`, and this now refuses. The probe stays as the
    regression that would catch the route being opened again."""
    repo, _attestation = _attested_branch_with_a_skip(tmp_path)
    body = tmp_path / "hook-body-no-disclosure.md"
    body.write_text(_pr_body(), encoding="utf-8")
    code, err = _run_hook(repo, _canonical_metadata_command(repo, body), monkeypatch)
    assert code == 2, "the hook let an undisclosed skip through: " + (err or "no refusal")
    assert "push.contextual-body" in err, err


def test_probe_hook_route_really_reaches_the_pull_request(tmp_path, monkeypatch) -> None:
    """Control: the same command with a correctly disclosing body is admitted,
    so the refusal above is the disclosure rule firing and not the route being
    closed to every body."""
    repo, attestation = _attested_branch_with_a_skip(tmp_path)
    disclosure = tuple(render_selection_disclosure(attestation))
    assert disclosure, "the fixture must produce a disclosure line"
    body = tmp_path / "hook-body-disclosed.md"
    body.write_text(_pr_body(disclosure), encoding="utf-8")
    code, err = _run_hook(repo, _canonical_metadata_command(repo, body), monkeypatch)
    assert code == 0, err
    assert err == "", err


# --------------------------------------------------------------------------
# Half five: the rewritten refusal, attacked as if the old one never existed.
# Nothing below reads an imported constant to decide what to do; it reads the
# bytes the agent reads, out of the refusal the checker just printed.
# --------------------------------------------------------------------------


def _refusal(repo: Path) -> str:
    """The publication refusal this branch actually produces."""
    result = _checker(repo, ["push"])
    assert result.returncode == 1, result.stderr
    return result.stderr


def _quoted_propose(refusal: str, change_id: str) -> list[str]:
    """The proposal command the refusal prints, as argv."""
    match = re.search(r"`(loom_checker\.py selection propose[^`]*)`", refusal)
    assert match, f"the refusal names no proposal command: {refusal}"
    tokens = match.group(1).split()
    assert tokens[0] == "loom_checker.py"
    return [change_id if token == "<change-id>" else token for token in tokens[1:]]


def _quoted_confirmation(refusal: str, code: str) -> str:
    """The confirmation the refusal tells the user to type, with the code in."""
    match = re.search(r"confirms by typing `([^`]+)`", refusal)
    assert match, f"the refusal names no confirmation form: {refusal}"
    return match.group(1).replace("<code>", code)


def _publishable_fixture(tmp_path: Path, name: str, change_id: str) -> Path:
    """A branch with functional content and a runnable package command, and no
    attestation -- the state the count-zero refusal is written for."""
    repo = _repo(tmp_path, name)
    (repo / "docs" / "loom").mkdir(parents=True)
    (repo / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text(
        "# Kickoff Defaults\n\n"
        "- package-tests: python3 probe_ok.py — fixture (2026-09-18)\n",
        encoding="utf-8")
    (repo / "probe_ok.py").write_text("print('ok')\n", encoding="utf-8")
    (repo / "feature.py").write_text("VALUE = 1\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "feature")
    return repo


def test_probe_following_the_refusal_verbatim_reaches_a_publishable_state(tmp_path) -> None:
    """Attack: the whole second route, end to end, driven only by the refusal's
    own bytes. If any word of it is wrong the branch never becomes publishable.

    This is the probe the route half was missing: F1 and F2 each checked one
    link, and a chain can have two sound links and still not carry."""
    change_id = "2026-09-18-verbatim-route"
    repo = _publishable_fixture(tmp_path, "verbatim", change_id)

    refusal = _refusal(repo)
    assert "two legal routes" in refusal, refusal

    proposal = _checker(repo, _quoted_propose(refusal, change_id))
    assert proposal.returncode == 0, proposal.stderr
    code = proposal.stdout.split("code:")[1].strip().split()[0]

    payload = json.dumps({"hook_event_name": "UserPromptSubmit",
                          "prompt": _quoted_confirmation(refusal, code),
                          "prompt_id": "p-verbatim", "session_id": SESSION})
    _checker(repo, ["selection", "capture", "--hook"], payload)

    review = tmp_path / "verbatim-review.json"
    review.write_text(json.dumps({
        "verdicts": [], "findings": [],
        "adversarial": [{"command": "python3 probe_ok.py", "artifact": "probe_ok.py"}],
    }), encoding="utf-8")
    finalized = _checker(repo, ["finalize-review", change_id, "--input", str(review)])
    assert finalized.returncode == 0, (
        "the refusal promised finalize-review would drop the reviewer floor to "
        "zero and still emit an attestation: " + finalized.stderr)
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "attest")

    published = _checker(repo, ["push"])
    assert published.returncode == 0, published.stderr

    # …and the skip the route created is disclosable, which is the condition
    # `publish` puts on the same branch a moment later.
    attestation = json.loads(
        (repo / "docs" / "loom" / change_id / "attestation.json").read_text(encoding="utf-8"))
    assert attestation["selection"]["skip"] == ["reviewers"]
    body = tmp_path / "verbatim-body.md"
    body.write_text(_pr_body(tuple(render_selection_disclosure(attestation))),
                    encoding="utf-8")
    _commit_intent(repo, change_id)
    accepted = _checker(repo, ["publish", "--title", "feat(x): verbatim route",
                               "--body-file", str(body), "--confirm-authorized"])
    assert "push.contextual-body" not in accepted.stderr, accepted.stderr
    assert "BLOCK publish:" not in accepted.stderr, accepted.stderr


def _already_landed_branch(tmp_path: Path, change_id: str, review: Path, *,
                           trunk: str = "main", published: bool = True,
                           local_trunk: str = "main", name: str | None = None,
                           arrange=None) -> Path:
    """A branch whose base already carries the attestation finalize-review
    generates for it -- so the branch delta holds none, and regenerating it
    changes no byte.

    `landed` is the state this fixture means, and landed means the base is on
    the remote, not merely in a local branch. Two rounds went wrong at exactly
    this line by modelling that one level less precisely than the checker reads
    it -- `22dd7f92` made the remote matter and this fixture had no
    remote-tracking ref; `0072b5f8` made the checker read the remote's own
    default-branch ref and this fixture had no such ref either -- so the refs
    are no longer guessed from what the current reader happens to open. A real
    `git clone` of a repository whose default branch is `<trunk>` was run
    offline and its refs read back: it writes exactly two, a normal
    `refs/remotes/origin/<trunk>` and a symbolic `refs/remotes/origin/HEAD`
    selecting it, on top of the `remote.origin.fetch` refspec `_repo`'s `git
    remote add` already wrote. Both are written here. A landed branch is now
    the clone, not the half of the clone some reader needed.

    `published=False` keeps no remote-tracking ref at all, and that is a real
    repository rather than a lazier one -- `git init` plus `git remote add`
    with nothing ever fetched. It is also the only shape that reaches the state
    its probe wants, which is why it is not "repaired" into a clone too: give
    it a clone's stale `refs/remotes/origin/main` and `branch_base` prefers
    that ref over the local trunk, the branch delta stops being empty, the
    branch carries its own attestation and `push` exits 0 with no refusal to
    read at all (measured).

    `trunk`, `local_trunk`, `published`, `name` and `arrange` exist so the
    probes below can build the states the resolver has to answer about;
    `arrange(repo, landed_sha, initial_sha)` replaces the ref writing entirely.
    """
    repo = _repo(tmp_path, name or f"landed-{trunk}-{local_trunk}-{int(published)}")
    initial = _git(repo, "rev-parse", "main")
    if local_trunk != "main":
        # A clone of a repository whose default branch is not `main` has no
        # local `main` either, and `helpers.TRUNK_CANDIDATES` is a literal list.
        _git(repo, "branch", "-m", "main", local_trunk)
    _git(repo, "switch", "-q", "-c", "prep")
    (repo / "docs" / "loom").mkdir(parents=True)
    (repo / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text(
        "# Kickoff Defaults\n\n"
        "- package-tests: python3 probe_ok.py — fixture (2026-09-18)\n",
        encoding="utf-8")
    (repo / "probe_ok.py").write_text("print('ok')\n", encoding="utf-8")
    (repo / "feature.py").write_text("VALUE = 1\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "feature")

    review.write_text(json.dumps({
        "verdicts": [{"reviewer": "a", "verdict": "PASS"},
                     {"reviewer": "b", "verdict": "PASS"}],
        "findings": [],
        "adversarial": [{"command": "python3 probe_ok.py", "artifact": "probe_ok.py"}],
    }), encoding="utf-8")
    finalized = _checker(repo, ["finalize-review", change_id, "--input", str(review)])
    assert finalized.returncode == 0, finalized.stderr
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "attest")

    _git(repo, "switch", "-q", local_trunk)
    _git(repo, "merge", "-q", "--ff-only", "prep")
    # `_repo` already created `feature`, so this moves it onto the base rather
    # than creating it. `switch -c` here died with exit 128 during fixture setup,
    # which the strict marker then recorded as the expected failure -- the probe
    # asserted nothing and could never have retired itself.
    if arrange is not None:
        arrange(repo, _git(repo, "rev-parse", local_trunk), initial)
    elif published:
        # What makes it landed rather than finished: the base is reachable from
        # the branch the remote itself names as its default, which is the only
        # witness this checker has that the work is somewhere other than this
        # working copy. Both refs, because a clone writes both and the checker
        # reads both -- the tracking ref for the commit, `HEAD` for the name.
        _git(repo, "update-ref", f"refs/remotes/origin/{trunk}", local_trunk)
        _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD",
             f"refs/remotes/origin/{trunk}")
    _git(repo, "switch", "-q", "feature")
    _git(repo, "reset", "-q", "--hard", local_trunk)
    assert _git(repo, "rev-parse", "HEAD") == _git(repo, "rev-parse", local_trunk)
    return repo


def test_probe_landed_fixture_builds_the_refs_a_real_clone_builds(tmp_path) -> None:
    """The fixture check the last two rounds did not have. Clone a local
    repository offline -- no network, no GitHub -- read back every ref the clone
    holds, and require the landed fixture to hold the same set.

    This is the assertion that would have caught both regressions before the
    checker did: a fixture that models a landed branch has to build what a real
    clone builds, and the only way to know what that is, is to make one."""
    source = tmp_path / "source"
    source.mkdir()
    _git(source, "init", "-q", "-b", "trunk")
    _git(source, "config", "user.email", "t@example.com")
    _git(source, "config", "user.name", "T")
    (source / "file.txt").write_text("content\n", encoding="utf-8")
    _git(source, "add", ".")
    _git(source, "commit", "-q", "-m", "initial")
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", str(source), str(clone)], check=True,
                   capture_output=True, text=True)

    def remote_shape(repo: Path) -> set[str]:
        listing = _git(repo, "for-each-ref", "--format=%(refname) %(symref)",
                       "refs/remotes/")
        return {line.replace("trunk", "<trunk>").replace("main", "<trunk>")
                for line in listing.splitlines()}

    review = tmp_path / "shape-review.json"
    landed = _already_landed_branch(tmp_path, "2026-09-18-clone-shape", review)
    assert remote_shape(landed) == remote_shape(clone), (
        "the landed fixture does not carry the refs a real clone carries")
    assert _git(clone, "symbolic-ref", "refs/remotes/origin/HEAD")
    assert _git(landed, "config", "--get", "remote.origin.fetch") == \
        _git(clone, "config", "--get", "remote.origin.fetch")


def test_probe_closing_review_route_terminates_at_count_zero(tmp_path) -> None:
    """Attack: take the first named route on every branch shape that is offered
    it, not only the one it was written for.

    F6's marker is gone, and the fix is not the one the probe demanded. The
    probe asserted that this branch becomes publishable; it never will, and it
    should not -- there is genuinely nothing here to publish. `41cbcf1b`
    answered the finding at the naming instead: `nothing_left_to_publish`
    recomputes the state and `publication_advice` withholds both routes from it.
    So the assertion moved from "the route works here" to "the route is not
    named here", and the loop below stays as the reason it must not be."""
    change_id = "2026-09-18-already-landed"
    review = tmp_path / "landed-review.json"
    repo = _already_landed_branch(tmp_path, change_id, review)

    (rule, reason), = _blocks(_refusal(repo))
    assert rule == "push.attestation", reason
    assert reason == f"{PUSH_REASON}0{NOTHING_TO_PUBLISH}", reason
    assert "two legal routes" not in reason, reason

    # Why neither route may be named here: run the real closing-review station,
    # not a stand-in for it, and watch the count fail to move.
    regenerated = _checker(repo, ["finalize-review", change_id, "--input", str(review)])
    assert regenerated.returncode == 0, regenerated.stderr
    assert _git(repo, "status", "--porcelain") == "", (
        "the fixture is only interesting while the regenerated attestation is "
        "byte-identical to the one already in the base")
    (_rule, again), = _blocks(_checker(repo, ["push"]).stderr)
    assert again == reason, "the station ran and changed nothing, as expected"


def test_probe_land_always_reports_a_countable_attestation_count(tmp_path) -> None:
    """Attack: reach `land`'s unknown-count fallback, which hands a branch the
    extra-attestations remedy without knowing the count is above one.

    Repelled differently now: `land` no longer counts attestations at all, so
    no count reaches its reason. Whatever the count, the refusal on these
    fixtures is the unidentified change, never the attestation-count reason."""
    for count in (0, 2, 3):
        ids = tuple(f"2026-09-18-change-{index}" for index in range(count))
        result = _checker(_repo(tmp_path, f"count{count}", ids),
                          ["land", "--accepted-by", "kouko"])
        (rule, reason), = _blocks(result.stderr)
        assert rule == "land.merge", result.stderr
        assert not reason.startswith(MISSING_ATTESTATION), reason
        assert reason == LAND_UNIDENTIFIED, reason


SHIP_RULE_SENTENCE = re.search(
    r"[^.]*" + re.escape(ship_text.NO_HANDOVER) + r"[^.]*\.",
    " ".join(ship_text.SHIP.read_text(encoding="utf-8").split()),
)


def test_probe_ship_prose_does_not_promise_routes_the_refusal_may_not_name() -> None:
    """Attack: reach a state where the station's instruction cannot be carried
    out. The checker learnt that a count above one has no route; the prose had
    to learn it too.

    F7a's marker is gone: `eabbe2c0` scoped the routes to the branch that
    attests nothing. The probe stays as the regression, and reads the property
    rather than the old literal -- an unconditional promise reworded would
    otherwise walk straight past it. The split is computed here rather than
    imported from the station's own test, so the two cannot drift into agreeing
    about a sentence the checker contradicts."""
    assert SHIP_RULE_SENTENCE, "the no-handover sentence is missing from the station"
    sentence = SHIP_RULE_SENTENCE.group(0)
    unconditional = re.split(r"\s+[—-]\s+", sentence, maxsplit=1)[0].lower()
    for promise in ("route", "closing-review", "step selection"):
        assert promise not in unconditional, (
            f"ship §3 promises {promise!r} for any refusal, while the checker "
            f"names routes for one attestation count only: {sentence}"
        )


def test_probe_ship_prose_names_a_confirmation_the_checker_accepts() -> None:
    """Attack: make the station and the refusal disagree about what the user
    types, so that following the station binds nothing.

    F7b's marker is gone: `cfaa2057` put the binding form in the station, and
    the assertion that had pinned the false phrasing moved with it.

    Why this is not cosmetic is already executable above: an agent relaying the
    station's wording asks for the bare code, and
    `test_probe_bare_code_still_binds_nothing` shows the bare code binds nothing.
    """
    assert SHIP_RULE_SENTENCE, "the no-handover sentence is missing from the station"
    sentence = SHIP_RULE_SENTENCE.group(0)
    assert "typing the code" not in sentence
    assert "/loom-code:expert-mode" in sentence


# --------------------------------------------------------------------------
# Half six: the body the hook now reads. The gate's guarantee is only as good
# as its agreement with the bytes `gh` will actually send, so every probe here
# asks whether the two can be made to differ.
# --------------------------------------------------------------------------


def _skipped_branch(tmp_path: Path) -> tuple[Path, tuple[str, ...]]:
    repo, attestation = _attested_branch_with_a_skip(tmp_path)
    disclosure = tuple(render_selection_disclosure(attestation))
    assert disclosure, "the fixture must produce a disclosure line"
    return repo, disclosure


def _bodies(tmp_path: Path, disclosure: tuple[str, ...]) -> tuple[Path, Path]:
    honest, hidden = tmp_path / "honest.md", tmp_path / "hidden.md"
    honest.write_text(_pr_body(disclosure), encoding="utf-8")
    hidden.write_text(_pr_body(), encoding="utf-8")
    return honest, hidden


def _command(repo: Path, *trailing: str) -> str:
    return render_quote_all([
        "command", str(Path(shutil.which("env")).resolve()),
        f"LOOM_REPO_ROOT={repo.resolve()}",
        f"GH_REPO={github_repo_from_origin(repo)}",
        str(Path(shutil.which("gh")).resolve()), "pr", "create",
        "--head", "feature", "--title", "feat(x): seam probe", *trailing,
    ])


def test_probe_repeated_body_file_is_read_last_wins(tmp_path, monkeypatch) -> None:
    """Attack: repeat the option so the gate judges one body and the request
    carries another.

    Repelled. `gh pr create --help` declares `-b, --body string` and
    `-F, --body-file file`: both scalar pflag flags, whose `Set` overwrites, so
    a repeated flag keeps the last value. Had either been declared
    `stringArray`, last-wins would be the wrong reading. I did not execute `gh`
    to confirm it: this repository's own hook refuses the command, and the
    invocations that would reach body handling risk a network call the pass
    forbids. The claim rests on gh's declared flag types, and this probe pins
    only the half that is mine -- that the gate reads the last one."""
    repo, disclosure = _skipped_branch(tmp_path)
    honest, hidden = _bodies(tmp_path, disclosure)
    hidden_last = _command(repo, "--body-file", str(honest), "--body-file", str(hidden))
    honest_last = _command(repo, "--body-file", str(hidden), "--body-file", str(honest))
    hidden_code, hidden_err = _run_hook(repo, hidden_last, monkeypatch)
    assert hidden_code == 2
    assert hidden_err.startswith("BLOCK push.contextual-body: "), hidden_err
    assert "Skipped steps: reviewers" in hidden_err, hidden_err
    honest_code, honest_err = _run_hook(repo, honest_last, monkeypatch)
    assert honest_code == 0 and honest_err == "", honest_err


def test_probe_joined_body_file_form_is_refused_at_admission(tmp_path, monkeypatch) -> None:
    """Attack: spell the option `--body-file=<path>` so the parse misses it and
    falls back to an empty body the disclosure rule has nothing to say about.

    Repelled, and not where the old name said. The joined spelling is not in
    `CANONICAL_PR_CREATE_OPTIONS`, so the command is refused at admission and no
    body is read on this route at all. The probe asserted only `== 2` and so
    passed on a refusal it was not aimed at. Both halves are pinned now: the rule
    the hook really prints, and the reader still understanding the spelling --
    which is the tripwire if it is ever allowlisted."""
    repo, disclosure = _skipped_branch(tmp_path)
    _honest, hidden = _bodies(tmp_path, disclosure)
    command = _command(repo, f"--body-file={hidden}")
    code, err = _run_hook(repo, command, monkeypatch)
    assert code == 2
    assert "BLOCK push.attestation: PR creation must use the canonical" in err, err
    assert "push.contextual-body" not in err, err
    assert pr_create_body(command) == hidden.read_text(encoding="utf-8")


def test_probe_unreadable_body_is_refused_while_a_skip_stands(tmp_path, monkeypatch) -> None:
    """Attack: the fix calls an unreadable body "discloses nothing". Name a file
    that does not exist and see whether nothing is read as honest.

    Repelled where it matters: an empty body carries no disclosure line, and a
    branch with a recorded skip requires one, so the empty reading refuses."""
    repo, _disclosure = _skipped_branch(tmp_path)
    missing = _command(repo, "--body-file", str(tmp_path / "absent.md"))
    code, err = _run_hook(repo, missing, monkeypatch)
    assert code == 2 and "push.contextual-body" in err, err


def test_probe_disclosure_check_is_not_reached_before_the_attestation(tmp_path, monkeypatch) -> None:
    """Attack the ordering: reach the body check on a branch whose attestation
    does not validate, so a body verdict stands in for an attestation verdict.

    Repelled: the body is judged only after `_cmd_push` returns 0, so a broken
    attestation refuses under its own rule id and the body is never consulted."""
    repo = _repo(tmp_path, "unattested")
    body = tmp_path / "ordering.md"
    body.write_text(_pr_body(), encoding="utf-8")
    code, err = _run_hook(repo, _command(repo, "--body-file", str(body)), monkeypatch)
    assert code == 2
    assert "push.attestation" in err and "push.contextual-body" not in err, err


def test_probe_short_body_file_option_cannot_diverge_from_the_shell(tmp_path, monkeypatch) -> None:
    """Attack: make the gate and the request read two different files under one
    path, by spelling the option the absoluteness rule does not cover.

    F8's marker is gone. `775eba95` closed it on the admission side: `-F` is not
    in `CANONICAL_PR_CREATE_OPTIONS`, so the command is no longer canonical and
    is refused before any body is read. The probe stays pointed at the outcome,
    not the mechanism, so it still fails if `-F` is ever allowlisted."""
    repo, disclosure = _skipped_branch(tmp_path)
    (repo / "rel.md").write_text(_pr_body(disclosure), encoding="utf-8")  # the gate's copy
    sub = repo / "sub"
    sub.mkdir()
    (sub / "rel.md").write_text(_pr_body(), encoding="utf-8")             # the shell's copy

    command = _command(repo, "-F", "rel.md")
    code, err = _run_hook(repo, command, monkeypatch, payload_cwd=sub)
    assert code == 2, (
        "the hook admitted a command whose body it resolved against the "
        "repository root while the shell will resolve it against " + str(sub)
    )
    assert "BLOCK push.attestation: PR creation must use the canonical" in err, err


def test_probe_short_body_file_option_really_reads_two_different_files(tmp_path, monkeypatch) -> None:
    """Control for F8: the same relative path, read from the two directories,
    yields a disclosing body and a hiding one."""
    repo, disclosure = _skipped_branch(tmp_path)
    (repo / "rel.md").write_text(_pr_body(disclosure), encoding="utf-8")
    sub = repo / "sub"
    sub.mkdir()
    (sub / "rel.md").write_text(_pr_body(), encoding="utf-8")
    command = _command(repo, "-F", "rel.md")

    monkeypatch.chdir(repo)
    assert "Skipped steps" in pr_create_body(command)
    monkeypatch.chdir(sub)
    assert "Skipped steps" not in pr_create_body(command)


def _attested_branch_without_a_skip(tmp_path: Path) -> Path:
    """The same fixture with real reviewer verdicts instead of a skip, so the
    attestation records no selection and there is nothing to disclose."""
    repo = _repo(tmp_path, "noskip")
    (repo / "docs" / "loom").mkdir(parents=True)
    (repo / "docs" / "loom" / "KICKOFF-DEFAULTS.md").write_text(
        "# Kickoff Defaults\n\n"
        "- package-tests: python3 probe_ok.py — fixture (2026-09-18)\n",
        encoding="utf-8")
    (repo / "probe_ok.py").write_text("print('ok')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "fixture")
    review = tmp_path / "noskip-review.json"
    review.write_text(json.dumps({
        "verdicts": [{"reviewer": "a", "verdict": "PASS"},
                     {"reviewer": "b", "verdict": "PASS"}],
        "findings": [],
        "adversarial": [{"command": "python3 probe_ok.py", "artifact": "probe_ok.py"}],
    }), encoding="utf-8")
    finalized = _checker(repo, ["finalize-review", SEAM_CHANGE, "--input", str(review)])
    assert finalized.returncode == 0, finalized.stderr
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "attest")
    return repo


NAKED_BODY = ("no headings at all, and this body claims to expose private "
              "chain-of-thought.\n")


def test_probe_hook_enforces_the_whole_contextual_body_rule(tmp_path, monkeypatch) -> None:
    """Attack: a branch with nothing to disclose, and a body that fails every
    other part of the rule the hook's own refusal is named after."""
    repo = _attested_branch_without_a_skip(tmp_path)
    body = tmp_path / "naked.md"
    body.write_text(NAKED_BODY, encoding="utf-8")
    code, err = _run_hook(repo, _command(repo, "--body-file", str(body)), monkeypatch)
    assert code == 2
    assert err.startswith("BLOCK push.contextual-body: "), err
    assert 'heading "Context" is missing' in err, err


def test_probe_publish_refuses_the_same_naked_body(tmp_path) -> None:
    """Control for F9: `publish` refuses that body under `push.contextual-body`,
    which is the rule id the hook route also prints -- for less."""
    repo = _attested_branch_without_a_skip(tmp_path)
    body = tmp_path / "naked-publish.md"
    body.write_text(NAKED_BODY, encoding="utf-8")
    result = _checker(repo, ["publish", "--title", "feat(x): naked",
                             "--body-file", str(body), "--confirm-authorized"])
    assert result.returncode == 1
    assert result.stderr.startswith("BLOCK push.contextual-body: ")
    assert 'heading "Context" is missing' in result.stderr


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="needs FIFOs")
def test_probe_body_read_cannot_block_the_hook(tmp_path) -> None:
    """Attack: hand the gate a path that is not a file it can finish reading."""
    fifo = tmp_path / "fifo.md"
    os.mkfifo(fifo)
    command = render_quote_all(["command", "env", "LOOM_REPO_ROOT=/", "GH_REPO=x",
                                "gh", "pr", "create", "--body-file", str(fifo)])
    script = (
        "import sys; sys.path.insert(0, %r)\n"
        "from loom_checker.rule_checks.push import pr_create_body\n"
        "print(repr(pr_create_body(%r)))\n" % (str(SCRIPTS), command)
    )
    try:
        done = subprocess.run([sys.executable, "-c", script], capture_output=True,
                              text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("pr_create_body blocked for more than ten seconds on a FIFO")
    assert done.returncode == 0, done.stderr
    # The value, not only the exit: a reader that returned anything at all here
    # would have had to open the FIFO to do it.
    assert done.stdout.strip() == "''", done.stdout


def test_probe_publish_refuses_a_body_that_is_not_a_regular_file(tmp_path) -> None:
    """Control for F10: the route that has a guard. `publish` exits 2 on the
    same path before reading a byte, which is the guard the hook route lacks."""
    if not hasattr(os, "mkfifo"):
        pytest.skip("needs FIFOs")
    repo = _repo(tmp_path, "fiforepo")
    fifo = tmp_path / "publish-fifo.md"
    os.mkfifo(fifo)
    result = _checker(repo, ["publish", "--title", "t",
                             "--body-file", str(fifo), "--confirm-authorized"])
    assert result.returncode == 2
    assert "--body-file is not a readable file" in result.stderr


def test_probe_body_can_change_between_the_check_and_the_request(tmp_path) -> None:
    """Attack: the gate reads the body; `gh` reads it again afterwards. Nothing
    holds the bytes still in between.

    Recorded, not scored as a defect: a `PreToolUse` hook judges a command it
    does not execute, so time-of-check is all any body rule on this route can
    have. It bounds what the F5 fix can promise -- that the body was honest when
    the hook looked, not that the pull request received it."""
    disclosing = tmp_path / "disclosing.md"
    disclosing.write_text(_pr_body(("Skipped steps: reviewers — authority: "
                                    "user-typed (AAAA, 2026-09-18)",)), encoding="utf-8")
    hiding = tmp_path / "hiding.md"
    hiding.write_text(_pr_body(), encoding="utf-8")
    pointer = tmp_path / "body.md"
    pointer.symlink_to(disclosing)
    command = render_quote_all(["command", "env", "LOOM_REPO_ROOT=/", "GH_REPO=x",
                                "gh", "pr", "create", "--body-file", str(pointer)])

    assert "Skipped steps" in pr_create_body(command)
    pointer.unlink()
    pointer.symlink_to(hiding)
    assert "Skipped steps" not in pr_create_body(command)


def test_probe_scoping_dash_hides_a_promise_placed_after_it() -> None:
    """Attack the assertion that closed F7a: it holds only the clause before the
    scoping dash to "promise no route", so an unconditional promise written
    after the dash is invisible to it.

    Recorded, not scored. The station test declares this limit in its own
    docstring, the sentence is advisory prose whose enforceable carrier is the
    refusal string, and F4's version of this shape was a defect only because it
    was undeclared. It is here so that the limit stays measured rather than
    remembered, and so a later sentence that uses it is caught by something."""
    forged = (
        "Do not " + ship_text.NO_HANDOVER + " — on a refusal take one of the "
        "two legal routes it names: run the closing-review station, or propose "
        "a step selection."
    )
    before_dash = re.split(r"\s+[—-]\s+", forged, maxsplit=1)[0].lower()
    assert "route" not in before_dash, "the forged sentence must look clean"
    assert "two legal routes it names" in forged, (
        "…while promising, after the dash, exactly what the checker does not "
        "always name"
    )


# --------------------------------------------------------------------------
# Half seven: route two is named on every host and in every session. It is not
# available in every host or every session.
# --------------------------------------------------------------------------


def _bind_in(repo: Path, change_id: str, *, propose_session: str,
             confirm_session: str, attended: str) -> dict:
    """Propose in one session, confirm in another, under a chosen attendedness."""
    def run(argv, stdin="", **overrides):
        env = _env()
        env.update(overrides)
        return subprocess.run([sys.executable, str(CHECKER), *argv], cwd=str(repo),
                              capture_output=True, text=True, env=env, input=stdin)

    proposal = run([*_propose_argv(change_id), "--skip", "reviewers"],
                   CLAUDE_CODE_SESSION_ID=propose_session,
                   CLAUDE_CODE_SESSION_ATTENDED="1")
    assert proposal.returncode == 0, proposal.stderr
    code = proposal.stdout.split("code:")[1].strip().split()[0]
    run(["selection", "capture", "--hook"], json.dumps({
        "hook_event_name": "UserPromptSubmit",
        "prompt": f"/loom-code:expert-mode {code}",
        "prompt_id": f"p-{code}", "session_id": confirm_session}),
        CLAUDE_CODE_SESSION_ID=confirm_session,
        CLAUDE_CODE_SESSION_ATTENDED=attended)
    shown = run(["selection", "show", change_id],
                CLAUDE_CODE_SESSION_ID=confirm_session,
                CLAUDE_CODE_SESSION_ATTENDED="1")
    assert shown.returncode == 0, shown.stderr
    return json.loads(shown.stdout)


UNBINDABLE = (
    # label, propose session, confirm session, attended
    ("a nested unattended session", "S1", "S1", "0"),
    ("a confirmation typed in a later session", "S1", "S2", "1"),
)


@pytest.mark.parametrize("label,propose,confirm,attended", UNBINDABLE)
def test_probe_route_two_really_is_unavailable_there(tmp_path, label, propose,
                                                     confirm, attended) -> None:
    """The mechanism behind F11, which is correct and must stay: a confirmation
    that was not typed by an attended user in the proposing session binds
    nothing. Nothing here argues for loosening it."""
    repo = _repo(tmp_path, "unbindable" + str(abs(hash(label)) % 1000))
    assert _bind_in(repo, CHANGE, propose_session=propose,
                    confirm_session=confirm, attended=attended)["bound"] is False


def test_probe_refusal_names_route_two_only_where_it_can_be_taken(tmp_path) -> None:
    """Attack: reach a state where a named route cannot be completed at all, and
    see whether the refusal still claims it outright.

    F11's marker is gone, and the fix is not the one the probe originally
    demanded. `775eba95` did not suppress route two in those sessions -- it
    qualified it, and said in the same breath that route one needs none. That is
    a defensible answer: the refusal is one line, it reads the same in every
    session, and computing the condition would put session state into a message.
    The probe is re-aimed at the property the fix claims, and
    `test_probe_route_two_condition_is_not_self_evaluable` below records what
    the qualification still costs."""
    repo = _repo(tmp_path, "unattended")
    env = _env()
    env["CLAUDE_CODE_SESSION_ATTENDED"] = "0"
    refused = subprocess.run([sys.executable, str(CHECKER), "push"], cwd=str(repo),
                             capture_output=True, text=True, env=env, input="")
    assert refused.returncode == 1
    reason = refused.stderr
    assert "needs no confirmation" in reason and "in every session" in reason, (
        "route one must be stated to be open in the sessions route two is not: "
        + reason)
    before_route_two = reason.split("propose a step selection", 1)[0]
    assert "can record a confirmation" in before_route_two, (
        "route two must carry its condition before it is named: " + reason)


def test_probe_route_two_condition_is_not_self_evaluable(tmp_path) -> None:
    """What the qualification costs, recorded so it is not lost.

    The condition the refusal now attaches to route two is not one an agent can
    evaluate before acting: nothing in the checker reports whether this session
    records confirmations. The agent learns it by proposing, asking the user to
    type the code, and reading `bound: false` afterwards -- one wasted keystroke
    per blocked publication in an unattended or cross-session run. Route one is
    unconditional, so nobody is stranded; this is a cost, not a block."""
    repo = _repo(tmp_path, "notselfeval")
    bound = _bind_in(repo, CHANGE, propose_session="S1", confirm_session="S1",
                     attended="0")
    assert bound["bound"] is False
    assert bound.get("code") is None
    # Nothing in the store distinguishes "not confirmed yet" from "this session
    # cannot confirm", which is why the agent has to ask to find out.
    assert bound["skip"] == []


def test_probe_route_one_survives_where_route_two_does_not(tmp_path) -> None:
    """The bound on F11: route one needs no confirmation, so the agent is
    slowed, not stranded. This is why F11 is not F6.

    The closing assertion used to run `finalize-review` with no `--input`, which
    exits 2 on a usage error before consulting anything -- it recorded nothing.
    The station is now actually run, in the session that could not bind, and has
    to succeed."""
    change_id = "2026-09-18-route-one-survives"
    repo = _publishable_fixture(tmp_path, "routeone", change_id)
    assert _bind_in(repo, change_id, propose_session="S1", confirm_session="S1",
                    attended="0")["bound"] is False

    review = tmp_path / "route-one-review.json"
    review.write_text(json.dumps({
        "verdicts": [{"reviewer": "a", "verdict": "PASS"},
                     {"reviewer": "b", "verdict": "PASS"}],
        "findings": [],
        "adversarial": [{"command": "python3 probe_ok.py", "artifact": "probe_ok.py"}],
    }), encoding="utf-8")
    finalized = _checker(repo, ["finalize-review", change_id, "--input", str(review)])
    assert finalized.returncode == 0, finalized.stderr
    assert (repo / "docs" / "loom" / change_id / "attestation.json").is_file()


# --------------------------------------------------------------------------
# Half eight: the trailing-option allowlist that replaced the parse. The
# question is no longer what the gate reads, but what it admits.
# --------------------------------------------------------------------------


# (trailing tokens, admitted, what is being tried)
ALLOWLIST_CASES = [
    ([], True, "no trailing options"),
    (["--head", "feature", "--title", "t", "--body-file", "/a/b.md"], True, "ship's form"),
    (["--draft"], True, "the one flag that spends no value"),
    (["--body-file", "/a.md", "--body-file", "/b.md"], True, "repeated, last wins"),
    (["--title", "--draft"], True, "a value that looks like an option"),
    (["--title"], False, "an option with no value left"),
    (["--body-file", "--title", "x"], False, "the value eats the next option, x dangles"),
    (["-F", "/a/b.md"], False, "the short spelling F8 travelled on"),
    (["--body-file=/a/b.md"], False, "the joined spelling"),
    (["-R", "o/r"], False, "repo override"),
    (["--repo", "o/r"], False, "repo override"),
    (["--hostname", "h"], False, "host override"),
    (["--repo=o/r"], False, "joined repo override"),
    (["-Ro/r"], False, "clustered repo override"),
    (["--title", "x", "-R", "o/r"], False, "override after a complete option"),
    (["--"], False, "end of options"),
    (["--", "--repo", "o/r"], False, "end of options, then an override"),
    ([""], False, "an empty token"),
    (["--draft", "false"], False, "a bool given a separate value"),
    (["--draft=true"], False, "a bool given a joined value"),
    (["--fill"], False, "a body gh composes from commits"),
    (["--fill-first"], False, "a body gh composes from one commit"),
    (["--fill-verbose"], False, "a body gh composes from commit bodies"),
    (["--editor"], False, "a body typed in an editor"),
    (["--template", "/t.md"], False, "a body seeded from a template"),
    (["--web"], False, "a body composed in a browser"),
    (["--recover", "{}"], False, "a body restored from a failed run"),
    (["--attach", "/i.png"], False, "content appended to the body"),
]


@pytest.mark.parametrize("trailing,admitted,label", ALLOWLIST_CASES)
def test_probe_allowlist_admits_only_what_it_can_judge(trailing, admitted, label) -> None:
    """Attack the allowlist walk itself: wrong value counts, values that look
    like options, end-of-options, empty tokens, repeats, and every gh input that
    determines a body the hook cannot see."""
    assert canonical_pr_create_trailing(list(trailing)) is admitted, label


REPO_OVERRIDE_SPELLINGS = (["-R", "o/r"], ["--repo", "o/r"], ["--hostname", "h"],
                           ["--repo=o/r"], ["--hostname=h"], ["-Ro/r"])


@pytest.mark.parametrize("trailing", REPO_OVERRIDE_SPELLINGS)
def test_probe_deleted_repo_override_check_is_really_subsumed(trailing) -> None:
    """The F4 lesson applied to a deletion: `775eba95` removed the explicit
    repo-override enumeration on the grounds that the allowlist subsumes it. A
    subsumption that is only claimed is exactly what F4 was. Every spelling the
    deleted check named is measured here, including the joined and clustered
    forms it handled specially."""
    assert canonical_pr_create_trailing(list(trailing)) is False


def test_probe_option_value_is_consumed_the_way_pflag_consumes_it() -> None:
    """Attack: make the walk and gh disagree about where an option's value ends.

    `--title --draft` is admitted, with `--draft` read as the title's value.
    That matches gh: `pflag.parseLongArg` takes the following argument as the
    value whenever the flag has no `NoOptDefVal`, without testing it for a
    leading dash, so gh sees the title `--draft` and no draft flag. Reasoned
    from pflag's documented behaviour and gh's declared flag types, not executed
    -- this repository's own hook refuses the command text, and the invocations
    that reach flag parsing risk a network call. Every allowlisted option is
    either separate-value or valueless, so there is no third case to disagree
    about."""
    assert canonical_pr_create_trailing(["--title", "--draft"]) is True
    assert canonical_pr_create_trailing(["--title", "--draft", "--draft"]) is True
    assert canonical_pr_create_trailing(["--draft", "--title"]) is False


def test_probe_unseen_body_flags_are_refused_before_the_body_is_read(tmp_path, monkeypatch) -> None:
    """The fix's stated mechanism for the unseen-body inputs was that they read
    as "" and "" fails the nine headings. The allowlist now refuses them first,
    under a different rule id -- so the outcome holds and the reason in the
    comment is superseded. Recorded because a future reader will otherwise trust
    the comment's route."""
    repo, _disclosure = _skipped_branch(tmp_path)
    command = _command(repo, "--fill")
    code, err = _run_hook(repo, command, monkeypatch)
    assert code == 2
    assert "push.attestation" in err and "push.contextual-body" not in err, err


def test_probe_structural_floor_runs_before_the_disclosure_clause(tmp_path, monkeypatch) -> None:
    """Attack the composition: a body that fails both halves must still produce
    one refusal, one rule id, one line -- and the half `cmd_publish` runs first
    must be the half that speaks."""
    repo, _disclosure = _skipped_branch(tmp_path)
    body = tmp_path / "fails-both.md"
    body.write_text("neither headings nor a disclosure line.\n", encoding="utf-8")
    code, err = _run_hook(repo, _command(repo, "--body-file", str(body)), monkeypatch)
    assert code == 2
    assert _blocks(err.splitlines()[0] + "\n")[0][0] == "push.contextual-body"
    assert 'heading "Context" is missing' in err
    assert "Skipped steps" not in err


def test_probe_hook_refusal_is_one_block_line_per_failure(tmp_path, monkeypatch) -> None:
    """Attack the contract the whole change rests on, from the route that was
    added last. Every other probe reads refusals through `_blocks()`; this one
    points `_blocks()` at the stderr no probe had read that way.

    F12's marker is gone: `41cbcf1b` flattens the reason at this emission only,
    leaving publish's multi-line rendering for the terminal that reads it. The
    probe stays as the regression for the contract."""
    repo, disclosure = _skipped_branch(tmp_path)
    _honest, hidden = _bodies(tmp_path, disclosure)
    code, err = _run_hook(repo, _command(repo, "--body-file", str(hidden)), monkeypatch)
    assert code == 2
    assert err.startswith("BLOCK push.contextual-body: "), err
    # `_blocks` is the reader the rest of this module judges refusals with; it
    # asserts every stderr line carries the prefix, which is the contract.
    assert [rule for rule, _reason in _blocks(err)] == ["push.contextual-body"]


BODY_PATHS_THAT_ARE_NOT_BODIES = ("fifo", "chardev", "stdin", "directory",
                                  "unreadable", "symlink-to-fifo")


@pytest.mark.parametrize("kind", BODY_PATHS_THAT_ARE_NOT_BODIES)
def test_probe_guarded_body_read_returns_promptly(tmp_path, kind) -> None:
    """Attack the F10 guard the way any check-then-read deserves: every path
    that is not a readable regular file must come back empty and come back at
    once, including one reached through a symlink."""
    if kind in {"fifo", "symlink-to-fifo"} and not hasattr(os, "mkfifo"):
        pytest.skip("needs FIFOs")
    if kind == "fifo":
        path = tmp_path / "f.fifo"
        os.mkfifo(path)
    elif kind == "symlink-to-fifo":
        target = tmp_path / "t.fifo"
        os.mkfifo(target)
        path = tmp_path / "link.md"
        path.symlink_to(target)
    elif kind == "chardev":
        path = Path("/dev/zero")
    elif kind == "stdin":
        path = Path("-")
    elif kind == "directory":
        path = tmp_path
    else:
        path = tmp_path / "u.md"
        path.write_text("x", encoding="utf-8")
        os.chmod(path, 0o000)

    command = render_quote_all(["command", "env", "LOOM_REPO_ROOT=/", "GH_REPO=x",
                                "gh", "pr", "create", "--body-file", str(path)])
    started = time.monotonic()
    assert pr_create_body(command) == ""
    assert time.monotonic() - started < 5, f"{kind} did not come back promptly"


def test_probe_body_read_has_no_size_ceiling(tmp_path) -> None:
    """Recorded, not scored. The guard admits any readable regular file, and
    there is no cap on how much of it is read into the hook's memory. Twenty
    megabytes here; nothing stops twenty gigabytes. It is agent-named and
    self-inflicted -- the agent stalls its own tool call, nothing is published,
    and `publish` reads its body file the same way -- so it is a limitation
    rather than a hole. It is measured so that it stays a known one."""
    big = tmp_path / "big.md"
    big.write_text("x" * (20 * 1024 * 1024), encoding="utf-8")
    command = render_quote_all(["command", "env", "LOOM_REPO_ROOT=/", "GH_REPO=x",
                                "gh", "pr", "create", "--body-file", str(big)])
    assert len(pr_create_body(command)) == 20 * 1024 * 1024


# --------------------------------------------------------------------------
# Half nine: the published-trunk fact. It decides whether a branch is told its
# work has landed or told to go and review it, so both directions are attacked.
# --------------------------------------------------------------------------


def _landed_refusal(tmp_path: Path, change_id: str, **kwargs) -> str:
    review = tmp_path / f"{change_id}-review.json"
    repo = _already_landed_branch(tmp_path, change_id, review, **kwargs)
    (rule, reason), = _blocks(_refusal(repo))
    assert rule == "push.attestation", reason
    return reason


def test_probe_finished_but_unpublished_branch_keeps_its_routes(tmp_path) -> None:
    """The state `22dd7f92` was written for, attacked from my side: a reviewed,
    attested branch nobody pushed, with local `main` moved onto it. It is
    byte-identical to a landed one, and it must still be offered the routes --
    telling it there is nothing to publish would abandon finished work."""
    reason = _landed_refusal(tmp_path, "2026-09-18-finished-unpublished",
                             published=False)
    assert reason == f"{PUSH_REASON}0{PUBLICATION_ROUTES}", reason
    assert "this branch adds nothing" not in reason, reason


def test_probe_landed_branch_is_recognised_on_a_trunk_not_called_main(tmp_path) -> None:
    """Attack the fact in the direction that restores the old defect: land the
    change on a remote default this checker does not know the name of.

    F13's marker is gone. `0072b5f8` deleted `PUBLISHED_TRUNK_CANDIDATES` and
    put `intent_state.remote_default_snapshot` in its place, which asks
    `refs/remotes/origin/HEAD` -- the branch the remote itself named -- rather
    than guessing from a list, and the probe passes on the assertion it always
    carried rather than on a softened one. It stays as the regression for the
    finding: a literal name reintroduced anywhere in `base_is_published` turns
    it red again for every repository that does not use that name.

    What it does not reach is one level up, where the base it asks about comes
    from. `test_probe_landed_on_a_clone_with_no_local_main` measures that."""
    reason = _landed_refusal(tmp_path, "2026-09-18-landed-on-trunk", trunk="trunk")
    assert "this branch adds nothing" in reason, reason


def test_probe_landed_on_a_clone_with_no_local_main(tmp_path) -> None:
    """Recorded, not scored, and deliberately not a marker.

    F13 was a trunk under another name, and the fix reaches half of it. The
    probe above passes because `_repo` leaves a local `main` behind for
    `helpers.TRUNK_CANDIDATES` -- the literal `origin/main, main, origin/master,
    master, @{upstream}` -- to find, and `branch_base` reads that list to
    produce the very base `base_is_published` is then asked about. A real clone
    of a `trunk`-defaulting repository has no `main` at all. Then no base
    resolves, `push` raises before any count is taken and before any tail is
    chosen, and the refusal this change rewrote is never reached.

    Not a marker, because nothing the refusal promises is broken here: the
    command fails closed, exits 2 and names every candidate it tried. Not this
    change's defect either -- `branch_base` predates it and every recomputing
    rule in the checker shares the same list. It is recorded so that the half of
    F13 the fix did not reach is visible rather than implied by a green probe,
    and so that a later attempt to make the checker trunk-agnostic knows there
    is a second literal pair to remove."""
    review = tmp_path / "no-main-review.json"
    repo = _already_landed_branch(tmp_path, "2026-09-18-landed-clone-trunk", review,
                                  trunk="trunk", local_trunk="trunk")
    assert _git(repo, "branch", "--list", "main") == ""
    assert _git(repo, "branch", "--list", "master") == ""
    # The remote default resolves perfectly well; it is the base that does not.
    assert _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD") == \
        "refs/remotes/origin/trunk"

    result = _checker(repo, ["push"])
    assert result.returncode == 2, result.stderr
    assert "no branch base resolves" in result.stderr, result.stderr
    assert "two legal routes" not in result.stderr, result.stderr
    assert "this branch adds nothing" not in result.stderr, result.stderr


def test_probe_landed_branch_on_master_is_recognised(tmp_path) -> None:
    """Control for F13. It was the other name the deleted literal pair knew, and
    it survives the pair's deletion as the control for the resolver: `master`
    goes through `refs/remotes/origin/HEAD` exactly as `trunk` does, so the
    probe above is measuring what the remote says and not the fixture."""
    reason = _landed_refusal(tmp_path, "2026-09-18-landed-on-master", trunk="master")
    assert "this branch adds nothing" in reason, reason


def test_probe_published_trunk_witness_is_agent_writable(tmp_path) -> None:
    """The other direction, recorded and not scored, and re-measured after
    `0072b5f8` changed the witness's shape.

    The witness that work was ever published is now two refs rather than one --
    `refs/remotes/origin/HEAD` and the tracking ref it selects -- and the
    question worth asking is whether writing two by hand is meaningfully harder
    than writing one. It is not, and the honest answer is narrower than that:
    in the repository shape this actually arises in, it is still one command.
    `refs/remotes/origin/HEAD` is written by `git clone`, so every cloned
    repository already carries it, and forging the landed state there is the
    single `git update-ref` it always was. Only a repository that was never
    cloned or fetched -- `git init` plus `git remote add`, which is what this
    probe's first half builds -- costs the second command, and the second
    command is `git symbolic-ref`, no harder to type than the first.

    So the new resolver did not raise the cost of forging the third fact; it
    changed which name gets forged. Still not scored as a defect: the harm is an
    agent talking itself out of publishing its own finished work, not a gate
    admitting anything, and no offline checker can tell a fetched ref from a
    written one -- a stale cache after a remote rewind reaches the same state
    with nobody acting at all. It is the honest boundary of the third fact, and
    the recompute in PRINCIPLES.md non-negotiable 3 rests on refs the agent can
    write."""
    review = tmp_path / "forged-review.json"
    repo = _already_landed_branch(tmp_path, "2026-09-18-forged-witness", review,
                                  published=False)
    (rule, before), = _blocks(_refusal(repo))
    assert rule == "push.attestation"
    assert before.endswith(PUBLICATION_ROUTES), before

    # Never cloned, so both refs are missing and both have to be written. The
    # first alone no longer moves the answer, which is the whole of what
    # `0072b5f8` added to the cost.
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")
    (_rule, halfway), = _blocks(_refusal(repo))
    assert halfway == before, (
        "the tracking ref alone was still enough: " + halfway)

    _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
    (_rule, after), = _blocks(_refusal(repo))
    assert "this branch adds nothing" in after, (
        "two hand-written refs turned a finished branch into a landed one: " + after)


def test_probe_a_cloned_repo_still_forges_the_witness_with_one_command(tmp_path) -> None:
    """The measurement the probe above depends on, made rather than asserted:
    in a clone -- the shape every repository an agent works in actually has --
    `refs/remotes/origin/HEAD` is already present, so the two-ref witness costs
    exactly one `git update-ref`, the same gesture as before `0072b5f8`.

    It is worse than a tie here, and that is the point of running it in this
    direction: the branch this starts from is not refused at all. Its
    attestation sits in its own delta and `push` exits 0, so one command turns a
    branch the checker was about to publish into a branch it says has nothing to
    publish."""
    review = tmp_path / "clone-forge-review.json"

    def clone_shaped(repo: Path, landed: str, initial: str) -> None:
        # A clone made before the work: the remote's default exists, is named,
        # and sits at the commit the branch grew from.
        _git(repo, "update-ref", "refs/remotes/origin/main", initial)
        _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")

    repo = _already_landed_branch(tmp_path, "2026-09-18-clone-forge", review,
                                  arrange=clone_shaped)
    publishable = _checker(repo, ["push"])
    assert publishable.returncode == 0, publishable.stderr

    _git(repo, "update-ref", "refs/remotes/origin/main", "main")

    (rule, after), = _blocks(_refusal(repo))
    assert rule == "push.attestation", after
    assert "this branch adds nothing" in after, (
        "one update-ref turned a publishable branch into a landed one: " + after)


# --------------------------------------------------------------------------
# Half ten: the resolver itself. `0072b5f8` put `remote_default_snapshot` where
# a literal pair of names used to be, so the third fact now rests on whatever
# `refs/remotes/origin/HEAD` happens to say. A ref is a file; files go wrong in
# ways a hardcoded string cannot. Both directions are attacked -- a broken ref
# that makes a landed branch look unpublished, and a ref that makes an
# unpublished branch look landed.
# --------------------------------------------------------------------------


def _head_file(repo: Path) -> Path:
    return repo / ".git" / "refs" / "remotes" / "origin" / "HEAD"


def _landed_but(tmp_path: Path, change_id: str, name: str, break_it) -> Path:
    """A branch whose change genuinely landed, with the default-branch ref
    damaged afterwards. Every state here is one the resolver has to answer
    about, and in every one of them the work really is on the remote."""

    def arrange(repo: Path, landed: str, initial: str) -> None:
        _git(repo, "update-ref", "refs/remotes/origin/main", landed)
        _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        break_it(repo, landed, initial)

    review = tmp_path / f"{name}-review.json"
    return _already_landed_branch(tmp_path, change_id, review, name=name,
                                  arrange=arrange)


def _prune_target(repo: Path, landed: str, initial: str) -> None:
    """`git remote prune origin` after the default branch was deleted upstream:
    the tracking ref goes, the symbolic ref is left pointing at nothing."""
    _git(repo, "update-ref", "-d", "refs/remotes/origin/main")


def _not_symbolic(repo: Path, landed: str, initial: str) -> None:
    """`refs/remotes/origin/HEAD` replaced by an ordinary ref holding a commit.

    `--no-deref` is what makes this the state it claims to be: plain
    `git update-ref` follows a symbolic ref and writes through it, so without
    the flag this rewrites `refs/remotes/origin/main` and leaves `HEAD` symbolic
    and resolving. The first version of this probe did exactly that and passed
    for the wrong reason, which is the same mistake in miniature the fixture
    above was repaired for."""
    _git(repo, "update-ref", "--no-deref", "refs/remotes/origin/HEAD", landed)


def _outside_the_prefix(repo: Path, landed: str, initial: str) -> None:
    """The symbolic ref selecting a local branch instead of a remote-tracking
    one -- the state the resolver's prefix test exists for."""
    _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/heads/main")


def _self_referential(repo: Path, landed: str, initial: str) -> None:
    _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/HEAD")


def _two_ref_loop(repo: Path, landed: str, initial: str) -> None:
    _git(repo, "symbolic-ref", "refs/remotes/origin/ring", "refs/remotes/origin/HEAD")
    _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/ring")


def _not_a_commit(repo: Path, landed: str, initial: str) -> None:
    """The tracking ref pointing at a tree. `^{commit}` is the only reason this
    is not read as a snapshot."""
    tree = _git(repo, "rev-parse", "HEAD^{tree}")
    (repo / ".git" / "refs" / "remotes" / "origin" / "main").write_text(
        tree + "\n", encoding="utf-8")


@pytest.mark.parametrize("name,break_it", [
    ("pruned-target", _prune_target),
    ("not-symbolic", _not_symbolic),
    ("outside-prefix", _outside_the_prefix),
    ("self-referential", _self_referential),
    ("two-ref-loop", _two_ref_loop),
    ("not-a-commit", _not_a_commit),
])
def test_probe_broken_default_ref_fails_towards_the_routes(tmp_path, name, break_it) -> None:
    """Attack: damage `refs/remotes/origin/HEAD` on a branch that genuinely
    landed, and see which way the resolver falls.

    Every one of these six answers the same way -- no default branch resolves,
    so the third fact is unproven and the two routes stay. That is the direction
    `base_is_published`'s docstring commits to, and it is the right one: the
    cost of falling this way is an agent re-running closing review on work that
    is already merged, and the cost of falling the other way is a finished
    change being told it is nothing and abandoned.

    It is the direction, not a free pass. Three of these six are reachable
    without anyone touching a ref by hand -- `git remote prune` after the
    default branch is deleted upstream leaves exactly the first state -- and in
    every one of them a landed branch walks back into the loop F6 named. The
    loop is bounded now only by the agent noticing the count will not move.

    Timed as well as asserted: a symbolic ref that points at itself and a pair
    that point at each other are the two shapes that make a naive resolver spin,
    and neither is allowed to take the refusal with it."""
    started = time.monotonic()
    reason = _landed_refusal_broken(tmp_path, f"2026-09-18-{name}", name, break_it)
    assert time.monotonic() - started < 120, f"{name} did not come back promptly"
    assert "two legal routes" in reason, reason
    assert "this branch adds nothing" not in reason, reason


def _landed_refusal_broken(tmp_path: Path, change_id: str, name: str, break_it) -> str:
    repo = _landed_but(tmp_path, change_id, name, break_it)
    (rule, reason), = _blocks(_refusal(repo))
    assert rule == "push.attestation", reason
    return reason


@pytest.mark.parametrize("content", [
    "ref: refs/remotes/origin/main@{1}\n",
    "ref: refs/remotes/origin/../../heads/main\n",
    "ref: refs/remotes/origin/main^{commit}\n",
    "ref: not a ref\n",
    "garbage\n",
    "",
])
def test_probe_a_hand_written_head_file_is_never_read_as_a_revision(tmp_path, content) -> None:
    """Attack: the resolver takes `symbolic-ref`'s output and hands it straight
    to `rev-parse --verify <target>^{commit}`. If a hand-written ref file can
    put a revision expression through that seam -- a reflog selector, a path
    escape, a second peel -- then the ref no longer has to name a branch the
    remote has, and the third fact can be satisfied by a string.

    Repelled, and by git rather than by the checker's own parsing: every one of
    these makes `symbolic-ref --quiet` fail, so the target never reaches
    `rev-parse` at all. The prefix test and the `^{commit}` peel are the second
    and third lines of that defence, not the first. Argv is the reason none of
    this is worse: the target is one element of a list, never a shell word."""
    def write_it(repo: Path, landed: str, initial: str) -> None:
        _head_file(repo).write_text(content, encoding="utf-8")

    started = time.monotonic()
    reason = _landed_refusal_broken(tmp_path, "2026-09-18-handwritten",
                                    f"handwritten-{abs(hash(content)) % 9973}", write_it)
    assert time.monotonic() - started < 120, "the malformed ref did not come back promptly"
    assert "two legal routes" in reason, reason


def test_probe_a_chained_symbolic_default_ref_still_resolves(tmp_path) -> None:
    """The control for the six above, and the one shape that must answer yes.

    `refs/remotes/origin/HEAD` -> `refs/remotes/origin/alias` ->
    `refs/remotes/origin/main` passes the prefix test at the first hop and is
    chased the rest of the way by `rev-parse`, not by `symbolic-ref`. Worth
    pinning: the resolver's own comment credits `symbolic-ref` with following
    chains, and if that were the load-bearing claim a chain would be the way to
    break it. It is not -- the peel resolves the chain either way -- so the
    comment is imprecise rather than wrong, and this probe is what keeps the
    imprecision from mattering."""
    def chain(repo: Path, landed: str, initial: str) -> None:
        _git(repo, "symbolic-ref", "refs/remotes/origin/alias", "refs/remotes/origin/main")
        _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/alias")

    reason = _landed_refusal_broken(tmp_path, "2026-09-18-chained", "chained", chain)
    assert "this branch adds nothing" in reason, reason


def test_probe_remote_default_moved_after_the_last_fetch(tmp_path) -> None:
    """Recorded, not scored. The remote renamed its default from `main` to
    `trunk` and the change landed on `trunk`; nobody has fetched since, so
    `refs/remotes/origin/HEAD` still selects `refs/remotes/origin/main` and that
    ref still sits at the commit the branch grew from.

    The resolver answers about the stale name, confidently and wrongly, but the
    error never reaches the tail: the stale ref is also the first entry of
    `helpers.TRUNK_CANDIDATES`, so `branch_base` measures the delta against it,
    the delta is not empty, the branch carries its own attestation and `push`
    exits 0. A landed change is offered publication again rather than told it
    has nothing to publish.

    Which is the safe half of the two possible wrongs, and is here so the
    reading is on the record: a stale default ref cannot make this refusal claim
    a change landed. It can only fail to notice that one did."""
    def moved(repo: Path, landed: str, initial: str) -> None:
        _git(repo, "update-ref", "refs/remotes/origin/trunk", landed)
        _git(repo, "update-ref", "refs/remotes/origin/main", initial)
        _git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")

    review = tmp_path / "moved-review.json"
    repo = _already_landed_branch(tmp_path, "2026-09-18-default-moved", review,
                                  name="default-moved", arrange=moved)
    result = _checker(repo, ["push"])
    assert result.returncode == 0, result.stderr


def test_probe_a_second_remote_holding_the_default_is_out_of_reach(tmp_path) -> None:
    """Recorded, not scored. `remote_default_snapshot` is always called with its
    default argument, so the third fact is a question about `origin` and about
    no other remote -- and `origin` is the only remote a repository is obliged
    to have a default-branch ref for.

    The state built here is the one that makes that bite, and it needs no forked
    workflow to reach: `origin` is up to date and contains the landed change,
    `upstream` carries the only `HEAD` ref in the repository, and `origin/HEAD`
    was never written because nothing here was cloned -- `git remote add` plus
    `git fetch` does not write it. The resolver reads `origin/HEAD`, finds
    nothing, and a landed branch keeps both routes and re-enters the loop while
    a default-branch ref is sitting in the same repository under another name.

    Not scored, because the checker is `origin`-bound one layer down and says
    so: `rule_checks/push.py` refuses any publication whose git remote is not
    the literal `origin`, so reading another remote's default would answer a
    question about a publication this gate would never make. Recorded because
    the resolver's hardcoded `origin` is now load-bearing and the reason it is
    the right name lives in a different file from the call."""
    def forked(repo: Path, landed: str, initial: str) -> None:
        _git(repo, "remote", "add", "upstream", "git@github.com:other/project.git")
        _git(repo, "update-ref", "refs/remotes/upstream/main", landed)
        _git(repo, "symbolic-ref", "refs/remotes/upstream/HEAD", "refs/remotes/upstream/main")
        _git(repo, "update-ref", "refs/remotes/origin/main", landed)

    review = tmp_path / "fork-review.json"
    repo = _already_landed_branch(tmp_path, "2026-09-18-fork-upstream", review,
                                  name="fork-upstream", arrange=forked)
    assert _git(repo, "symbolic-ref", "refs/remotes/upstream/HEAD")
    (rule, reason), = _blocks(_refusal(repo))
    assert rule == "push.attestation", reason
    assert "two legal routes" in reason, reason


@pytest.mark.parametrize("remote", [
    "", "-", "--upload-pack=touch /tmp/pwned", "origin main", "origin/../../etc",
    "ori gin", "..", "origin\n", "origin;id",
])
def test_probe_resolver_refuses_a_remote_name_that_is_not_a_literal(tmp_path, remote) -> None:
    """Attack the one argument the resolver takes. No caller in this change
    passes a non-default remote today, which is exactly why the guard is worth
    a probe now rather than after someone wires a configurable one to it.

    The guard answers before any git runs, so nothing reaches argv, and it
    answers in the same three-tuple shape as every other failure -- no
    exception, no ref, no snapshot, and a reason that says which name it was."""
    repo = _repo(tmp_path, "remote-name")
    ref, snapshot, error = remote_default_snapshot(repo, remote)
    assert ref is None and snapshot is None, (ref, snapshot)
    assert "is not a safe literal" in error, error
    assert repr(remote) in error, error
