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
"""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import test_ship_station_text as ship_text
from loom_checker.command_handlers import push as push_handler
from loom_checker.command_handlers.publish import MISSING_ATTESTATION
from loom_checker.command_handlers.push import EXTRA_ATTESTED_CHANGES
from loom_checker.command_handlers.push import PUBLICATION_ROUTES
from loom_checker.rule_checks.publish import render_selection_disclosure
from loom_checker.rule_checks.push import github_repo_from_origin
from loom_checker.rule_checks.push import pr_create_body
from loom_checker.rule_checks.push import render_quote_all

SCRIPTS = Path(__file__).resolve().parent
CHECKER = SCRIPTS / "loom_checker.py"
SESSION = "adversarial-blocked-publish-routes"

# The reasons origin/main emitted for these inputs. The change may append to
# them; it may not replace, reword or re-rule them.
PUSH_REASON = "branch must carry exactly one generated attestation; found "
LAND_REASON = "branch must carry exactly one attested change; found "


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
    """Attack: the same, through `land`'s own earlier refusal site."""
    ids = tuple(f"2026-09-18-change-{index}" for index in range(count))
    result = _checker(_repo(tmp_path, f"land{count}", ids),
                      ["land", "--accepted-by", "kouko"])
    assert result.returncode == 1
    assert _blocks(result.stderr) == [
        ("land.merge", f"{LAND_REASON}{count}{_tail(count)}")
    ]


@pytest.mark.parametrize("count", [0, 1, 2, 3, 4])
def test_probe_only_a_zero_count_is_ever_offered_the_routes(tmp_path, count) -> None:
    """Attack: reach a state that is offered the two routes while the branch
    already attests something, which is where neither route reduces the count.

    Read off the emitted bytes, with no call into the product's own chooser."""
    ids = tuple(f"2026-09-18-change-{index}" for index in range(count))
    stderr = _checker(_repo(tmp_path, f"only{count}", ids), ["push"]).stderr
    offered = "two legal routes" in stderr
    assert offered == (count == 0), stderr
    if count == 1:  # one attestation passes the count and is refused later
        assert PUSH_REASON not in stderr


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
    assert len(blocks) == 2
    assert blocks[0][1].endswith(PUBLICATION_ROUTES)
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


def test_probe_push_and_land_name_byte_identical_routes(tmp_path) -> None:
    """Attack: let the two sites drift into naming two different ways out."""
    push = _checker(_repo(tmp_path, "p"), ["push"]).stderr
    land = _checker(_repo(tmp_path, "l"), ["land", "--accepted-by", "kouko"]).stderr
    assert push.split(PUSH_REASON + "0", 1)[1] == land.split(LAND_REASON + "0", 1)[1]


def test_probe_routes_are_not_appended_twice(tmp_path) -> None:
    """Attack: `land` appends, then delegates to the push handler, which
    appends again."""
    result = _checker(_repo(tmp_path, "twice"), ["land", "--accepted-by", "kouko"])
    assert result.stderr.count("two legal routes") == 1


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


def test_probe_named_proposal_drops_the_reviewer_floor(tmp_path) -> None:
    """Attack: follow the refusal literally and see whether the second route
    reaches the state the refusal says it reaches."""
    repo = _repo(tmp_path, "route2")
    assert _bind(repo, CHANGE, [])["skip"] == ["reviewers"]

    review = tmp_path / "review-input.json"
    review.write_text(json.dumps({"verdicts": [], "findings": [], "adversarial": []}),
                      encoding="utf-8")
    result = _checker(repo, ["finalize-review", CHANGE, "--input", str(review)])
    assert "review input has no verdicts" not in result.stderr


def test_probe_named_proposal_with_an_explicit_skip_does_drop_the_floor(tmp_path) -> None:
    """Control for F1: the same command plus `--skip reviewers` -- the words the
    refusal leaves out -- is what actually drops the floor."""
    repo = _repo(tmp_path, "route2ok")
    assert _bind(repo, CHANGE, ["--skip", "reviewers"])["skip"] == ["reviewers"]

    review = tmp_path / "review-ok.json"
    review.write_text(json.dumps({"verdicts": [], "findings": [], "adversarial": []}),
                      encoding="utf-8")
    result = _checker(repo, ["finalize-review", CHANGE, "--input", str(review)])
    assert "review input has no verdicts" not in result.stderr


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
    accepted = _checker(repo, ["publish", "--title", "feat(x): verbatim route",
                               "--body-file", str(body), "--confirm-authorized"])
    assert "push.contextual-body" not in accepted.stderr, accepted.stderr


def _already_landed_branch(tmp_path: Path, change_id: str, review: Path) -> Path:
    """A branch whose base already carries the attestation finalize-review
    generates for it -- so the branch delta holds none, and regenerating it
    changes no byte."""
    repo = _repo(tmp_path, "landed")
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

    _git(repo, "switch", "-q", "main")
    _git(repo, "merge", "-q", "--ff-only", "prep")
    _git(repo, "switch", "-q", "-c", "feature")
    return repo


@pytest.mark.xfail(
    strict=True,
    reason="FINDING F6: the count-zero tail names the closing-review route "
           "unconditionally, but a branch whose base already carries the "
           "attestation finalize-review regenerates gets `found 0` and stays "
           "there -- running the named station rewrites byte-identical content, "
           "so the count never moves. This is the non-terminating loop the "
           "count-above-one branch was split off to avoid, left in place on the "
           "branch that kept the routes",
)
def test_probe_closing_review_route_terminates_at_count_zero(tmp_path) -> None:
    """Attack: take the first named route on every branch shape that is offered
    it, not only the one it was written for."""
    change_id = "2026-09-18-already-landed"
    review = tmp_path / "landed-review.json"
    repo = _already_landed_branch(tmp_path, change_id, review)

    refusal = _refusal(repo)
    assert f"{PUSH_REASON}0" in refusal and "two legal routes" in refusal, refusal

    # "run the closing-review station, which generates the attestation" -- the
    # real station, not a stand-in for it.
    regenerated = _checker(repo, ["finalize-review", change_id, "--input", str(review)])
    assert regenerated.returncode == 0, regenerated.stderr
    assert _git(repo, "status", "--porcelain") == "", (
        "the fixture is only interesting while the regenerated attestation is "
        "byte-identical to the one already in the base")

    assert f"{PUSH_REASON}0" not in _checker(repo, ["push"]).stderr


def test_probe_land_always_reports_a_countable_attestation_count(tmp_path) -> None:
    """Attack: reach `land`'s unknown-count fallback, which hands a branch the
    extra-attestations remedy without knowing the count is above one.

    Repelled: the reason `land` parses is built as `f'…found {len(candidates)}'`,
    so the tail after the prefix is always digits and the fallback is dead. It is
    still the wrong default for an unknown state, and only unreachability is
    keeping that from mattering."""
    for count in (0, 2, 3):
        ids = tuple(f"2026-09-18-change-{index}" for index in range(count))
        result = _checker(_repo(tmp_path, f"count{count}", ids),
                          ["land", "--accepted-by", "kouko"])
        (_rule, reason), = _blocks(result.stderr)
        found = reason.removeprefix(MISSING_ATTESTATION).split(";", 1)[0]
        assert found.isdigit() and int(found) == count, reason


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


@pytest.mark.xfail(
    strict=True,
    reason="FINDING F7b: the ship station still says the user confirms `by "
           "typing the code`, the exact phrasing the checker was corrected away "
           "from, and `test_ship_prose_forbids_handing_the_command_over` "
           "requires that substring -- so the station cannot be corrected "
           "without editing the test that pins it",
)
def test_probe_ship_prose_names_a_confirmation_the_checker_accepts() -> None:
    """Attack: make the station and the refusal disagree about what the user
    types, so that following the station binds nothing.

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
    assert _run_hook(repo, hidden_last, monkeypatch)[0] == 2
    assert _run_hook(repo, honest_last, monkeypatch)[0] == 0


def test_probe_joined_body_file_form_is_read(tmp_path, monkeypatch) -> None:
    """Attack: spell the option `--body-file=<path>` so the parse misses it and
    falls back to an empty body the disclosure rule has nothing to say about."""
    repo, disclosure = _skipped_branch(tmp_path)
    _honest, hidden = _bodies(tmp_path, disclosure)
    assert _run_hook(repo, _command(repo, f"--body-file={hidden}"), monkeypatch)[0] == 2


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


@pytest.mark.xfail(
    strict=True,
    reason="FINDING F8: `check_pr_create_remote_head` requires an absolute path "
           "for `--body-file` and `--body-file=` but not for the `-F` spelling, "
           "which `pr_create_body` reads. The hook resolves the relative path "
           "against the repository root it chdirs to; the shell resolves it "
           "against its own working directory. F5 survives verbatim under `-F`",
)
def test_probe_short_body_file_option_cannot_diverge_from_the_shell(tmp_path, monkeypatch) -> None:
    """Attack: make the gate and the request read two different files under one
    path, by spelling the option the absoluteness rule does not cover."""
    repo, disclosure = _skipped_branch(tmp_path)
    (repo / "rel.md").write_text(_pr_body(disclosure), encoding="utf-8")  # the gate's copy
    sub = repo / "sub"
    sub.mkdir()
    (sub / "rel.md").write_text(_pr_body(), encoding="utf-8")             # the shell's copy

    command = _command(repo, "-F", "rel.md")
    code, _err = _run_hook(repo, command, monkeypatch, payload_cwd=sub)
    assert code == 2, (
        "the hook admitted a command whose body it resolved against the "
        "repository root while the shell will resolve it against " + str(sub)
    )


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


@pytest.mark.xfail(
    strict=True,
    reason="FINDING F9: the hook route now enforces the disclosure half of "
           "`push.contextual-body` and still not the structural half. Both "
           "routes refuse under the same rule id, so the rule looks enforced "
           "everywhere while the nine-heading floor and the "
           "chain-of-thought ban hold on the publish route alone",
)
def test_probe_hook_enforces_the_whole_contextual_body_rule(tmp_path, monkeypatch) -> None:
    """Attack: a branch with nothing to disclose, and a body that fails every
    other part of the rule the hook's own refusal is named after."""
    repo = _attested_branch_without_a_skip(tmp_path)
    body = tmp_path / "naked.md"
    body.write_text(NAKED_BODY, encoding="utf-8")
    code, _err = _run_hook(repo, _command(repo, "--body-file", str(body)), monkeypatch)
    assert code == 2


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
    assert "nine top-level contextual headings" in result.stderr


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="needs FIFOs")
@pytest.mark.xfail(
    strict=True,
    reason="FINDING F10: `pr_create_body` opens the named path with no "
           "regular-file guard and no timeout, so a FIFO body file blocks the "
           "PreToolUse hook indefinitely -- `/dev/zero` is the unbounded-read "
           "variant. `publish` refuses the same path outright, because "
           "`_publish_args` requires `--body-file` to be a readable regular file",
)
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
