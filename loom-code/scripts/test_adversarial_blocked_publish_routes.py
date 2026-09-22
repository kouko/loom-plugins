"""Adversarial probes for `2026-09-18-blocked-publish-names-the-legal-routes`.

The `push` refusal, its route tails and the hook's PR-body reader were removed
by `2026-09-22-publication-floor-moves-to-github` (plan W1-03); the probes
that attacked them went with them. What remains probes `land`, `publish`, the
ship prose and the remote-default resolver.

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

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

import test_ship_station_text as ship_text
from loom_checker.command_handlers.publish import MISSING_ATTESTATION
from loom_checker.intent_state import remote_default_snapshot

SCRIPTS = Path(__file__).resolve().parent
CHECKER = SCRIPTS / "loom_checker.py"
SESSION = "adversarial-blocked-publish-routes"

# `land` no longer counts attestations: on these fixtures (branch `feature`, no
# intent in the delta) it refuses because the change is unidentified, whatever
# the attestation count. The text is identify_change's, restated here.
LAND_UNIDENTIFIED = (
    "cannot identify the change: branch 'feature' names no committed intent and "
    "the branch delta carries 0 intent files; rename the branch to "
    "<type>/<change-id> or commit the intent docs/loom/intent/<change-id>.md"
)


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


# --------------------------------------------------------------------------
# Half one: the gate must not have moved.
# --------------------------------------------------------------------------


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


def test_probe_routes_are_not_appended_twice(tmp_path) -> None:
    """Attack: `land` appends, then delegates to the push handler, which
    appends again. Neither appends now: the refusal carries no route at all."""
    result = _checker(_repo(tmp_path, "twice"), ["land", "--accepted-by", "kouko"])
    (rule, reason), = _blocks(result.stderr)
    assert rule == "land.merge", result.stderr
    assert reason == LAND_UNIDENTIFIED, result.stderr
    assert reason.count("two legal routes") == 0


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


# --------------------------------------------------------------------------
# Half five: the rewritten refusal, attacked as if the old one never existed.
# Nothing below reads an imported constant to decide what to do; it reads the
# bytes the agent reads, out of the refusal the checker just printed.
# --------------------------------------------------------------------------


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
# Half ten: the resolver itself. `0072b5f8` put `remote_default_snapshot` where
# a literal pair of names used to be, so the third fact now rests on whatever
# `refs/remotes/origin/HEAD` happens to say. A ref is a file; files go wrong in
# ways a hardcoded string cannot. Both directions are attacked -- a broken ref
# that makes a landed branch look unpublished, and a ref that makes an
# unpublished branch look landed.
# --------------------------------------------------------------------------


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
