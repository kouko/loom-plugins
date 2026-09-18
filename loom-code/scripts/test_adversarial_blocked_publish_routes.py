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
    so that state is told what does."""
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


def test_probe_routes_text_is_one_line_with_no_control_characters() -> None:
    """Attack: break `report()`'s one-`BLOCK`-line-per-failure contract by
    smuggling a newline, a carriage return or an escape into the reason."""
    assert not re.search(r"[\r\n\x00-\x08\x0b-\x1f\x7f]", PUBLICATION_ROUTES)
    assert not PUBLICATION_ROUTES.startswith("\n")


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


def test_probe_closing_review_route_unblocks_a_two_attestation_branch(tmp_path) -> None:
    """Attack: take the first named route on the branch shape that produces the
    same refusal, and see whether the publication becomes possible.

    It does not, so the refusal must not name it here; and what it names instead
    has to be a state this branch can actually reach."""
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
    assert PUSH_REASON not in _checker(repo, ["push"]).stderr


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


@pytest.mark.xfail(
    strict=True,
    reason="FINDING F4: the no-gate assertion locates the rule with "
           "`text.find`, so it only ever inspects the FIRST occurrence; a "
           "second, gate-marked copy of the same rule is invisible to it",
)
def test_probe_no_gate_assertion_sees_a_gate_marked_second_copy() -> None:
    """Attack: satisfy `test_ship_prose_rule_is_not_marked_as_a_gate` while the
    rule is in fact inside a gate-marked region."""
    text = _document_with_the_rule_inside_a_gate()
    regions = ship_text._gate_regions(text)
    assert regions, "the synthetic document must contain a gate region"

    index = text.find(ship_text.NO_HANDOVER)
    assert any(start <= index < end for start, end in regions)


def test_probe_gate_marked_copy_is_really_there_and_really_missed() -> None:
    """Control for F4: the rule does sit inside a detected gate region, and the
    existing assertion's own locator still points outside every region."""
    text = _document_with_the_rule_inside_a_gate()
    regions = ship_text._gate_regions(text)
    occurrences = [match.start() for match in
                   re.finditer(re.escape(ship_text.NO_HANDOVER), text)]
    assert len(occurrences) == 2
    assert not any(start <= occurrences[0] < end for start, end in regions)
    assert any(start <= occurrences[1] < end for start, end in regions)


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


def _run_hook(repo: Path, command: str, monkeypatch) -> tuple[int, str]:
    """The publication hook on one Bash command, with the live remote-head
    lookup -- the external seam -- answered with the state that holds right
    after a successful push."""
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": command}, "cwd": str(repo)}
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SESSION)
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ATTENDED", "1")
    monkeypatch.setattr(push_handler, "read_hook_payload", lambda *a, **k: payload)
    monkeypatch.setattr(push_handler, "check_pr_create_remote_head", lambda *a, **k: None)
    monkeypatch.chdir(repo)
    out, err = io.StringIO(), io.StringIO()
    return push_handler.cmd_push(["--hook"], out, err), err.getvalue()


@pytest.mark.xfail(
    strict=True,
    reason="FINDING F5: the publication hook validates the attestation and the "
           "remote head for the trusted metadata-only PR-opening command, but "
           "never the PR body, so the skip disclosure `publish` enforces is not "
           "enforced on that route and a user-typed skip reaches a pull request "
           "undisclosed",
)
def test_probe_hook_refuses_a_pr_body_that_hides_the_skip(tmp_path, monkeypatch) -> None:
    """Attack: same repository, same undisclosed body, the other route."""
    repo, _attestation = _attested_branch_with_a_skip(tmp_path)
    body = tmp_path / "hook-body-no-disclosure.md"
    body.write_text(_pr_body(), encoding="utf-8")
    code, err = _run_hook(repo, _canonical_metadata_command(repo, body), monkeypatch)
    assert code == 2, "the hook let an undisclosed skip through: " + (err or "no refusal")


def test_probe_hook_route_really_reaches_the_pull_request(tmp_path, monkeypatch) -> None:
    """Control for F5: the same command with a correctly disclosing body is
    admitted too, which shows the hook is not reading the body at all rather
    than reading it and happening to accept."""
    repo, attestation = _attested_branch_with_a_skip(tmp_path)
    disclosure = tuple(render_selection_disclosure(attestation))
    assert disclosure, "the fixture must produce a disclosure line"
    body = tmp_path / "hook-body-disclosed.md"
    body.write_text(_pr_body(disclosure), encoding="utf-8")
    code, err = _run_hook(repo, _canonical_metadata_command(repo, body), monkeypatch)
    assert code == 0, err
