"""Adversarial probes for `2026-09-18-modular-adversary-recipes`.

The change splits the adversary's attack recipes into one file per artifact
kind beside a shared protocol, and claims four properties for the result --
change, add, remove, locate -- in `AGENTS.md` and in Acceptance 3, 4, 5 and
10 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`. These
probes try to make those claims fail.

Every case is performed on a copy of the repository or of the reference
folder and asserts on the result of an edit that was really made; nothing
here writes inside the repository, and no case asserts on wording.

Probes that hold pass. Probes that land a finding fail on purpose and name
the finding in their assertion message, the convention the probes of
`2026-09-15-adversary-probe-maintenance` established.

Cases:

* add (A4): the addition the routing table describes -- one new file beside
  the protocol plus one row -- is performed once per artifact type the table
  leaves unrouted, and every check that reads these documents is run on the
  result, with nothing deselected;
* population (A4): the types the addition is proven on are every unrouted
  type the manifest holds, computed here rather than borrowed;
* locate (A10): a rule for one artifact kind is planted in the shared
  protocol in the plainest wording a writer would reach for, and the checks
  are run on the result;
* change (A3): one recipe's wording is edited, and what turns red is
  counted per module;
* boundary: a recipe file emptied of everything the shape requires.

Two things this file refuses to do, because doing either would let it
declare the add claim green by looking away from what breaks it.

It deselects nothing. The repository's own addition case runs its inner
suite through `_run_adversary_tests`, which deselects the cases that copy
the repository -- and those were exactly the cases that demanded a second
file when this probe first ran, so that case could not see the defect it
was about. The reason they have to be deselected there is that their copy
is built from `git ls-files`, which cannot see a file the addition has just
written and nobody has staged: run without the deselection, they fail on a
tree whose routing row names a recipe their copy never received. So the
copy this file makes is a git repository of its own, sharing the real
repository's object store, with everything staged -- and then the nested
cases see the added recipe, the inner run deselects nothing, and a failure
of any of them is a failure this probe reports. `_git_visible_copy` carries
the detail.

And it compares, rather than demanding green. A copy of this repository is
not guaranteed to be green for reasons that have nothing to do with the
addition -- one reworded sentence in one recipe reddens that recipe's own
module, and an addition case that demands a whole green suite inside its
copy then reddens once per kind for a reason that is not about any kind.
So the claim is tested as a difference: the same copy is run before and
after the addition, and what must be empty is the set of cases the addition
newly reddened.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "loom-code").is_dir() and (candidate / "loom-design").is_dir():
            return candidate
    raise RuntimeError(f"could not locate repo root above {start}")


REPO = _find_repo_root(Path(__file__).parent)
sys.path.insert(0, str(REPO / "loom-code/scripts"))

# The repository's own readers, imported rather than copied: the routing
# table is the one place a kind is given a recipe, and the shape check is the
# one place the five parts of the shape are computed. A second copy of either
# here would be a second thing to keep right, and would stop testing the
# programs this change actually ships.
from test_adversary_routing import (  # noqa: E402
    NESTED_TESTS,
    NO_RECIPE,
    SCRIPTS,
    SUITE_EXTRA,
    SUITE_GLOB,
    _add_kind,
    _copy_repository,
    _routing_rows,
    _run_adversary_tests,
    routed_recipes,
)
from test_adversary_recipe_shape import (  # noqa: E402
    PROTOCOL_NAME,
    REFERENCES,
    recipe_files,
    shape_violations,
)

RECIPE_BODY = (
    "# Adversarial — {kind}\n\n"
    "The attack recipe for a {kind}. Read it together with the shared\n"
    "protocol in [`{protocol}`]({protocol}).\n\n"
    "## {heading}\n\n"
    "Attack the {kind} artifact until something it promises stops being true.\n"
)


def _references_in(root: Path) -> Path:
    return root / str(REFERENCES.relative_to(REPO))


MANIFEST = REPO / "loom-code/contract/manifest.yaml"
_TYPE_IN_MANIFEST = re.compile(r"type:\s*(?P<type>[A-Za-z-]+)\s*\}")


def _manifest_types() -> set[str]:
    """Every artifact type the manifest names, parsed here.

    The one reader this file does not borrow. Which kinds the addition is
    proven on decides what the add claim means: a case that adds the
    alphabetically first unrouted kind proves the claim for that kind and no
    other, and the kinds whose names are common English words are exactly the
    ones that used to break. So the population is computed from the manifest
    here, and a separate case compares it with the population the
    repository's own addition case uses.
    """
    block = MANIFEST.read_text(encoding="utf-8").split("\nartifact_types:", 1)[1]
    stop = re.search(r"^[a-z_]+:", block, re.M)
    block = block[: stop.start()] if stop else block
    types = {m.group("type") for m in _TYPE_IN_MANIFEST.finditer(block)}
    assert len(types) > 3, types
    return types


def _unrouted_kinds() -> list[str]:
    """Every artifact type of the manifest that has no recipe today.

    The population the add case is parametrized over: every type a reader
    could be asked to give a recipe to, not the first one in sorted order.
    """
    rows = _routing_rows((REFERENCES / PROTOCOL_NAME).read_text(encoding="utf-8"))
    unrouted = sorted(t for t in _manifest_types() if rows.get(t, NO_RECIPE) == NO_RECIPE)
    assert unrouted, "every artifact type is routed; this probe has no kind to add"
    return unrouted


def _routed_kind() -> str:
    """A kind the routing table sends to a recipe today."""
    kinds = sorted(k for kinds in routed_recipes().values() for k in kinds)
    assert kinds, "the routing table routes no kind"
    return kinds[0]


def _failed_modules(output: str) -> set[str]:
    """The modules pytest reported a failure in, from its FAILED lines."""
    return {
        Path(m.group(1)).name
        for m in re.finditer(r"^FAILED (\S+?)::", output, re.M)
    }


def _failed_cases(output: str) -> set[str]:
    """Every failing case pytest named, as `module::name[id]`.

    The module is kept, because the same case name lives in the protocol's
    module and in every recipe's module at once.
    """
    return {
        f"{Path(m.group('path')).name}::{m.group('name')}"
        for m in re.finditer(r"^FAILED (?P<path>\S+?)::(?P<name>\S+)", output, re.M)
    }


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    run = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    assert run.returncode == 0, (args, run.stdout, run.stderr)
    return run


def _git_visible_copy(root: Path) -> list[str]:
    """A copy of the repository that git can see, added files included.

    The checks that copy the repository build their copy from `git ls-files`,
    and the migration assertions read two commits out of git history. A plain
    directory copy satisfies neither: a recipe file the addition has just
    written is not in anyone's index, so those checks receive a tree whose
    routing row names a recipe that never arrived, and they fail for that and
    not for anything the addition did. Deselecting them is how the
    repository's own addition case lives with it, and deselecting them is
    what let this probe once call the claim green while they were the cases
    that broke.

    So the copy is made a repository of its own: `git init`, its object store
    pointed at the real one through `objects/info/alternates` so that a
    `git show <split commit>:<path>` still resolves, and everything staged.
    Then `git ls-files` inside the copy lists the added recipe, the nested
    checks copy a consistent tree, and the inner run needs no deselection.
    """
    copied = _copy_repository(root)
    objects = _git(REPO, "rev-parse", "--git-path", "objects").stdout.strip()
    _git(root, "init", "-q")
    info = root / ".git/objects/info"
    info.mkdir(parents=True, exist_ok=True)
    (info / "alternates").write_text(f"{(REPO / objects).resolve()}\n", encoding="utf-8")
    _git(root, "add", "-A")
    return copied


def _inner_targets(root: Path) -> list[str]:
    """The test files the inner run covers: the same set the repository's own
    runner uses, taken from its glob and its extras so that a module added or
    retired later is covered without editing this file."""
    scripts = root / SCRIPTS
    targets = sorted(str(p.relative_to(root)) for p in scripts.glob(SUITE_GLOB))
    targets += [f"{SCRIPTS}/{name}" for name in SUITE_EXTRA]
    for target in targets:
        assert (root / target).is_file(), target
    return targets


def _run_every_check(root: Path) -> subprocess.CompletedProcess[str]:
    """Run every check that reads these documents inside `root`, deselecting
    nothing.

    Termination is not this run's problem to solve: a nested case makes its
    own copy and runs it through the repository's runner, which deselects the
    nesting cases one level down, so the depth is two and bounded there.
    """
    return subprocess.run(
        ["python3", "-m", "pytest", "-q", "-p", "no:cacheprovider", *_inner_targets(root)],
        cwd=root, capture_output=True, text=True,
        env={**_env(), "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _env() -> dict[str, str]:
    import os

    env = dict(os.environ)
    env.pop("GIT_DIR", None)  # the copy is its own repository now
    return env


def _copy_references(tmp_path: Path) -> Path:
    folder = tmp_path / "references"
    shutil.copytree(REFERENCES, folder)
    assert shape_violations(folder) == [], "the copy does not start clean"
    return folder


# --- helper self-tests -------------------------------------------------------

def test_failed_module_parser_synthetic() -> None:
    """Self-test: a FAILED line yields its module; a passing run yields none."""
    out = (
        "FAILED loom-code/scripts/test_adversary_recipe_spec.py::test_recipe_states_its_rule\n"
        "FAILED loom-code/scripts/test_adversary_protocol.py::test_x[an-id]\n"
    )
    assert _failed_modules(out) == {
        "test_adversary_recipe_spec.py",
        "test_adversary_protocol.py",
    }
    assert _failed_modules("24 passed in 6.4s\n") == set()


def test_kind_helpers_synthetic() -> None:
    """Self-test: the population comes from the manifest and the table, the
    routed kind from the table, and the two are disjoint."""
    rows = _routing_rows((REFERENCES / PROTOCOL_NAME).read_text(encoding="utf-8"))
    for kind in _unrouted_kinds():
        assert rows.get(kind, NO_RECIPE) == NO_RECIPE, kind
    assert rows[_routed_kind()] != NO_RECIPE
    assert _routed_kind() not in _unrouted_kinds()


def test_failed_case_parser_synthetic() -> None:
    """Self-test: a failing case is identified with its module, so the same
    case name in two modules is two cases, and a green run names none."""
    out = (
        "FAILED loom-code/scripts/test_adversary_recipe_spec.py::test_x[an-id]\n"
        "FAILED loom-code/scripts/test_adversary_protocol.py::test_x[an-id]\n"
    )
    assert _failed_cases(out) == {
        "test_adversary_recipe_spec.py::test_x[an-id]",
        "test_adversary_protocol.py::test_x[an-id]",
    }
    assert _failed_cases("33 passed, 1 skipped in 40.9s\n") == set()


# --- add (A4): one new file plus one row, as the routing table describes -----

@pytest.fixture(scope="module")
def baseline(tmp_path_factory) -> tuple[set[str], str]:
    """Which cases are red in a git-visible copy with nothing added.

    The comparison the add cases are made against, taken once: a copy of the
    repository as it stands, run with nothing deselected. A case red here is
    red for a reason that is not the addition's, and the add cases below say
    so instead of blaming the kind they were given.
    """
    root = tmp_path_factory.mktemp("baseline") / "repo"
    _git_visible_copy(root)
    run = _run_every_check(root)
    return _failed_cases(run.stdout), run.stdout


def test_baseline_run_reaches_the_nested_cases(baseline, tmp_path) -> None:
    """The comparison run really runs the cases that copy the repository.

    If it did not -- if they were deselected, or collected under other names
    -- a failure of exactly those cases could not show up as a difference,
    which is the hole this probe exists to close. So the same targets are
    collected, and every case the repository's own runner deselects must be
    among the cases collected here.
    """
    _failures, output = baseline
    assert "deselected" not in output, output[-2000:]

    root = tmp_path / "collect"
    _git_visible_copy(root)
    collect = subprocess.run(
        ["python3", "-m", "pytest", "-q", "--collect-only", "-p", "no:cacheprovider",
         *_inner_targets(root)],
        cwd=root, capture_output=True, text=True,
        env={**_env(), "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert collect.returncode == 0, collect.stdout + collect.stderr
    assert NESTED_TESTS, "the repository names no nesting case"
    missing = [name for name in NESTED_TESTS if f"::{name}" not in collect.stdout]
    assert not missing, (
        "the cases the repository's own runner deselects are not in this "
        f"probe's run either, so nothing here could see them fail: {missing}"
    )


@pytest.mark.parametrize("kind", _unrouted_kinds())
def test_adding_any_unrouted_kind_reddens_nothing_new(kind: str, baseline, tmp_path) -> None:
    """A reader follows the routing table exactly, for every kind it offers.

    `adversarial.md` states that giving a type a recipe is one new file beside
    it plus its own row, Acceptance 4 states that the addition is one file and
    one routing entry a reader can do once without guessing, and `AGENTS.md`
    states the same as the `add` criterion. The addition is performed here for
    every artifact type the manifest leaves unrouted -- not for the first in
    sorted order, whose name collides with nothing -- and every check that
    reads these documents is run on the result with nothing deselected.

    What must be empty is the set of cases the addition newly reddened. A
    whole-suite-green demand would fail here for any unrelated recipe edit
    that reddens that recipe's own module, which is a fact about the edit and
    not about adding a kind.
    """
    known_red, _ = baseline
    root = tmp_path / "repo"
    _git_visible_copy(root)
    recipe = f"adversarial-{kind}.md"
    _add_kind(
        _references_in(root),
        kind,
        recipe,
        RECIPE_BODY.format(kind=kind, heading=kind.capitalize(), protocol=PROTOCOL_NAME),
    )
    _git(root, "add", "-A")

    run = _run_every_check(root)
    new_red = _failed_cases(run.stdout) - known_red
    assert not new_red, (
        f"FINDING add-is-not-one-file-and-one-row (A4, AGENTS `add`, kind {kind!r}): "
        "the addition the routing table and the conventions describe -- one new "
        "recipe file plus one routing row -- reddened cases that were green "
        f"before it: {sorted(new_red)}. A reader who follows the routing table "
        f"must guess whatever else {kind} needs, which no document states."
        f"\n{run.stdout[-2000:]}"
    )


def test_the_addition_is_proven_on_every_kind_the_manifest_offers() -> None:
    """The population, compared with the one the repository's own case uses.

    A kind missing from that population is a kind whose addition nothing in
    the repository ever performs, which is how an addition case comes to pass
    for the one name that collides with nothing.
    """
    from test_adversary_routing import unrouted_types

    theirs, mine = set(unrouted_types()), set(_unrouted_kinds())
    assert mine - theirs == set(), (
        "FINDING narrow-add-population (A4): the repository's addition case is "
        f"parametrized over {sorted(theirs)}, which leaves {sorted(mine - theirs)} "
        "unproven though the manifest offers them and the routing table leaves "
        "them unrouted."
    )


# --- locate (A10): a one-kind rule planted in the shared protocol ------------

WORDINGS = (
    "For a {kind} artifact, run every attempt a second time before recording it.",
    "When the changed path is a {kind}, feed its gate script one character of difference.",
    "A {kind} change gets its abuse cases run twice before any of them is recorded.",
)


def _routed_kinds() -> list[str]:
    return sorted(k for kinds in routed_recipes().values() for k in kinds)


def test_protocol_rule_for_one_kind_in_plain_prose_is_rejected(tmp_path) -> None:
    """The shared protocol grows a rule that belongs to a single kind.

    Acceptance 10 requires that the shared protocol hold no rule of its own
    for one kind, and the `locate` criterion says a rule belonging to one
    capability lives in that capability's file. The rules planted here name
    their kind the way a writer would reach for first -- in plain prose, not
    in the backticks the routing table uses for an artifact type -- and every
    routed kind gets all three wordings, so the verdict cannot turn on which
    kind or which phrasing the case happened to pick.
    """
    accepted = []
    for kind in _routed_kinds():
        for wording in WORDINGS:
            sentence = wording.format(kind=kind)
            folder = _copy_references(tmp_path / f"{kind}-{WORDINGS.index(wording)}")
            protocol = folder / PROTOCOL_NAME
            protocol.write_text(
                protocol.read_text(encoding="utf-8") + f"\n{sentence}\n", encoding="utf-8"
            )
            if not shape_violations(folder):
                accepted.append(sentence)
    assert not accepted, (
        "FINDING plain-prose-kind-rule-accepted (A10, AGENTS `locate`): the "
        "shared protocol states a rule for one kind alone and the shape check "
        f"reports nothing: {accepted}"
    )


def test_protocol_rule_for_one_kind_reddens_the_real_checks(baseline, tmp_path) -> None:
    """The same plant, carried through every check with nothing deselected.

    The case above reads the shape check directly; this one asks whether the
    repository as a whole rejects the plant, so that a shape check reporting
    a violation nobody runs would still be caught.
    """
    known_red, _ = baseline
    kind = _routed_kinds()[0]
    sentence = WORDINGS[0].format(kind=kind)

    root = tmp_path / "repo"
    _git_visible_copy(root)
    protocol = _references_in(root) / PROTOCOL_NAME
    protocol.write_text(
        protocol.read_text(encoding="utf-8") + f"\n{sentence}\n", encoding="utf-8"
    )
    _git(root, "add", "-A")

    run = _run_every_check(root)
    assert _failed_cases(run.stdout) - known_red, (
        "FINDING plain-prose-kind-rule-unchecked (A10): the shared protocol "
        f"states {sentence!r}, a rule for the {kind} kind alone, and no check "
        f"that reads these documents goes red on it.\n{run.stdout[-2000:]}"
    )


# --- change (A3): editing one recipe reddens that recipe's module alone ------

def _own_module(recipe_name: str) -> str:
    kind = recipe_name[len("adversarial-"):-len(".md")]
    return f"test_adversary_recipe_{kind.replace('-', '_')}.py"


_HEADING_LINE = re.compile(r"^#{1,6} .*$", re.M)
_TABLE_LINE = re.compile(r"^\s*\|.*$", re.M)


def _reword_one_sentence(recipe: Path) -> str:
    """Change the wording of one of the recipe's sentences, and nothing else.

    The edit Acceptance 3 is about: one recipe's prose reads differently, and
    the file is otherwise the file it was. Heading lines and table rows are
    dropped before the sentence is chosen, because a "sentence" that swallows
    a `## ` heading or a table row is not a rewording at all -- rewriting it
    deletes the section or the table, and then every check that reads the
    folder's structure goes red for a reason that has nothing to do with
    wording. That mistake is the reason this helper says so here: it was made
    once, and it made this case accuse the repository of something the case
    itself had done.

    The rewording exchanges the sentence's second and third words, so every
    word it had is still in it, the leading token stays leading -- a list
    bullet is one -- and the closing period stays closing. That is enough to
    stop a pin that quotes the sentence or opens a literal inside it.
    """
    text = recipe.read_text(encoding="utf-8")
    prose = _TABLE_LINE.sub("", _HEADING_LINE.sub("", text))
    flat = " ".join(prose.split())
    sentences = [s.strip() for s in re.split(r"(?<=\.)\s", flat) if s.strip().endswith(".")]
    assert sentences, recipe
    sentence = max(sentences, key=len)
    words = sentence.split(" ")
    assert len(words) > 3, sentence
    pattern = re.compile(r"\s+".join(re.escape(w) for w in words))
    assert len(pattern.findall(text)) == 1, sentence
    reworded = " ".join([words[0], words[2], words[1], *words[3:]])
    recipe.write_text(pattern.sub(lambda _m: reworded, text), encoding="utf-8")
    return sentence


def test_reword_helper_changes_wording_only_synthetic(tmp_path) -> None:
    """Self-test: the heading and the table survive, one sentence reads
    differently, and every word of it is still there."""
    path = tmp_path / "recipe.md"
    original = (
        "# Adversarial — thing\n\nRead the protocol.\n\n## Thing\n\n"
        "The longest sentence of this file is the one that gets\nreworded here.\n\n"
        "| Class | The question |\n|---|---|\n| Empty | does it behave, or explode? |\n"
    )
    path.write_text(original, encoding="utf-8")
    sentence = _reword_one_sentence(path)
    after = path.read_text(encoding="utf-8")
    assert sentence == "The longest sentence of this file is the one that gets reworded here."
    assert "## Thing" in after and "| Class | The question |" in after
    # The leading word and the closing period stay where they were; two
    # interior words change places, so no pin quoting the sentence survives.
    assert "The longest sentence of" not in after
    assert "The sentence longest of" in after
    assert after.rstrip().endswith("|")
    assert sorted(" ".join(after.split()).split(" ")) == sorted(" ".join(original.split()).split(" "))


@pytest.mark.parametrize("recipe_name", sorted(routed_recipes()))
def test_rewording_one_recipe_reddens_only_its_own_module(
    recipe_name: str, baseline, tmp_path
) -> None:
    """One recipe's wording is changed; what goes red is counted per module.

    Acceptance 3 says the other recipe files and their tests are untouched
    and still pass. The edit is a rewording of one sentence, made once per
    recipe rather than in whichever one sorts first, and the run deselects
    nothing, so a case elsewhere that this edit reddens is reported here
    rather than passed over.
    """
    known_red, _ = baseline
    root = tmp_path / "repo"
    _git_visible_copy(root)
    sentence = _reword_one_sentence(_references_in(root) / recipe_name)
    _git(root, "add", "-A")

    run = _run_every_check(root)
    new_red = _failed_cases(run.stdout) - known_red
    assert new_red, (
        f"FINDING unpinned-recipe: rewording {sentence!r} in {recipe_name} "
        "reddened nothing; that sentence is pinned nowhere."
    )
    own = _own_module(recipe_name)
    stray = {case for case in new_red if not case.startswith(f"{own}::")}
    assert not stray, (
        "FINDING edit-not-confined (A3, AGENTS `change`): rewording one "
        f"sentence of {recipe_name} newly reddened cases outside its own "
        f"module {own}: {sorted(stray)}\n{run.stdout[-2000:]}"
    )


def test_a_recipe_whose_pins_already_fail_still_confines_the_next_edit(
    baseline, tmp_path
) -> None:
    """The harder state: a recipe already rewritten past its own pins.

    A branch mid-implementation looks like this -- a recipe edited, its own
    test file not yet caught up -- and Build runs the checks in exactly that
    state. So this case replaces one recipe's section body outright, which
    reddens that recipe's own module, and then asks the same question
    Acceptance 3 asks: is anything outside that module newly red?
    """
    known_red, _ = baseline
    recipe_name = sorted(routed_recipes())[0]
    root = tmp_path / "repo"
    _git_visible_copy(root)
    recipe = _references_in(root) / recipe_name
    heading, body = recipe.read_text(encoding="utf-8").split("\n## ", 1)
    title = body.split("\n", 1)[0]
    recipe.write_text(
        f"{heading}\n## {title}\n\nGo at the artifact until some promise of it stops holding.\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")

    run = _run_every_check(root)
    new_red = _failed_cases(run.stdout) - known_red
    own = _own_module(recipe_name)
    stray = {case for case in new_red if not case.startswith(f"{own}::")}
    assert not stray, (
        "FINDING contamination-guard-premise (A3, AGENTS `change`): with "
        f"{recipe_name} rewritten past its own pins -- the state a branch is "
        "in between editing a recipe and updating its test file -- these "
        f"cases outside {own} go red: {sorted(stray)}. They subtract the "
        "failures an untouched copy carries, but their own premise is that a "
        "fresh edit inside the copy still reddens something; a tree whose "
        "pins already fail leaves that premise with nothing to plant."
        f"\n{run.stdout[-2000:]}"
    )


# --- boundary: a recipe file with nothing in it ------------------------------

def test_recipe_emptied_of_everything_is_rejected(tmp_path) -> None:
    """The empty-and-absent boundary: a recipe file left with no content at all.

    A routed row still names it, so the folder must not be accepted as a
    folder whose recipes keep the shape.
    """
    folder = _copy_references(tmp_path)
    target = recipe_files(folder)[0]
    target.write_text("", encoding="utf-8")
    parts = {v.part for v in shape_violations(folder)}
    assert parts, (
        f"FINDING empty-recipe-accepted: {target.name} holds nothing at all and "
        "the shape check reports no violation."
    )
