"""The routing table sends each artifact type to the recipe that attacks it.

Acceptance 4, 5 and 7 of
`docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

The cases this module makes, the six of the plan plus the one the plan's
wording turned out to need:

- add-kind-one-file-one-row (A4 positive): giving a kind a recipe it lacks
  today is one new file beside the protocol plus one row of the routing
  table, and nothing else in the folder changes;
- existing-recipe-file-untouched (A4 negative): that same addition leaves
  every recipe file that already existed byte-identical. Counting what the
  addition touches is not the whole of A4, so the addition is also performed
  for real, in a copy of the whole repository and once per artifact type the
  table leaves unrouted, with the checks run on the result and the kind then
  taken away again -- a kind added exactly as the routing table describes has
  no test module of its own, and its removal must come out as clean as the
  removal of one that has;
- reworded-recipe-not-blamed (none of the plan's six; the one the measurement
  of them called for): the addition and the removal are each held to
  the difference between the copy's failures before and after the edit, never
  to the copy being green. The claim is that giving a kind a recipe introduces
  no new failure, and a copy carries whatever the working tree carries: one
  reworded sentence in one recipe is that recipe's own test file's business,
  and demanding a green copy would make it fail the addition once per unrouted
  kind. Proven by rewording a recipe in a copy on purpose and performing the
  addition there anyway. Which recipe is reworded is selected rather than
  assumed: the premise is that the reword can still plant a failure, which is
  only true of a recipe whose own test module is green in the tree the copy
  came from, so a recipe already edited on this branch is passed over and a
  tree where every recipe's module is red says so instead of measuring;
- protocol-plus-kind-is-complete (A7 positive): the adversary contract names
  the protocol, the protocol's row names the recipe, the recipe points back
  at the protocol, and that pair needs no third file;
- unrouted-kind-detected (A7 negative): every artifact type of the
  repository's own vocabulary has a row, a type with no recipe says so in
  its own row rather than being absent, and a row naming a file that is not
  there is caught;
- deleting-a-kind-leaves-no-reference (A5 positive): removing a kind is
  deleting its recipe file and its own test file, if it has one, and putting
  its routing row back to `none`; afterwards no file in the repository names
  either deleted file and the removal breaks no check that was passing before
  it. Made once per recipe the routing table names, so the kinds it is proven
  on are the kinds that exist;
- stale-reference-detected (A5 negative): a removal that leaves the recipe's
  own test file behind, one that leaves the routing row pointing at the
  deleted file, and one that leaves the deleted name in a live file are each
  caught, and the scan that catches them fails loudly rather than reporting
  nothing when it can see nothing.

The addition in the first two cases is performed on a copy of the reference
folder in a temporary directory, so the assertion is made on the result of
a real edit rather than on a sentence promising the edit would be small.

The removal cases go wider: they copy every tracked file of the repository
into a temporary directory, remove a kind there, scan every copied file for
the deleted names, and run the adversary test files inside that copy.
Nothing is asserted about wording; every assertion is made on the result of
an edit that was really performed.

The positive removes a kind routed today, where it stands, once per recipe
file the routing table names: what is asserted afterwards is that nothing
outside the change records still names it and that the remaining checks run.
The negatives need a removal they can do wrong without deleting a kind the
repository still uses, so each first gives a kind the routing table lists as
having no recipe one -- a kind whose names belong to no other file -- and
then removes it with one step left undone. Each copy of the repository costs
seconds, so a case is made here only where it catches something no other
case does.

Two debt lists run alongside, and both may only shrink:
`_BOUNDED_REMOVAL_DEBT` the files that still hand-list a routed recipe by
name, and `_UNBOUNDED_REMOVAL_DEBT_KINDS` the kinds whose removal a module
elsewhere still breaks. An entry that stopped violating fails as loudly as
a file that started.
"""
from __future__ import annotations

import importlib
import os
import re
import shutil
import subprocess
import warnings
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
PROTOCOL = REFERENCES / "adversarial.md"
CONTRACT = ROOT / "loom-code/agents/adversary.md"
MANIFEST = ROOT / "loom-code/contract/manifest.yaml"

# The path form the adversary contract already uses, unchanged by this
# change: a backtick-quoted path from the repository root.
CONTRACT_PROTOCOL_PATH = "`loom-code/skills/closing-review/references/adversarial.md`"
ROUTING_HEADING = "## Which recipe to read"
# What a row says when the kind has no recipe today.
NO_RECIPE = "none"
# The verb the contract carries before it names the routing table.
CONTRACT_ROUTE_VERB = "read"
CONTRACT_ROUTE_LITERAL = "the recipe file its routing table names for every artifact type"

# Where a kind's own test file lives, by the convention Acceptance 6 fixes:
# one test file per recipe, named after the kind the recipe attacks.
SCRIPTS = "loom-code/scripts"
RECIPE_STEM = "adversarial-"
RECIPE_TEST_STEM = "test_adversary_recipe_"

# The test files that read the protocol and the recipes. The removal cases
# run these inside the copy; a recipe test that the removal deleted is gone
# from the glob, and one the addition wrote is picked up by it.
SUITE_GLOB = "test_adversary_*.py"
SUITE_EXTRA = (
    "test_build_mechanical_checks.py",
    "test_review_convergence_contract.py",
    # The module criteria map names the check that enforces each criterion. A
    # removal that left it naming a module that is no longer there would pass
    # a scan for the deleted names and still be broken, so the copy runs it.
    "test_module_criteria_text.py",
)

# Files that still hand-list a recipe file routed today, so removing that
# kind would leave their reference dangling. The three that were here when
# this check went in now read the routing table instead, and the list is
# empty. It stays: an entry is a debt, never a permission, so the list may
# only shrink and `test_no_new_file_hand_lists_a_routed_recipe` fails on an
# entry that stopped violating as loudly as on a file that started.
_BOUNDED_REMOVAL_DEBT: tuple[str, ...] = ()
# The one tree the debt scan passes over by path: the change records, which
# state where a rule lived at a commit already made and cannot stop being
# true. The other two exclusions the debt scan makes are named where it makes
# them -- the reference folder, whose routing row the removal rewrites, and
# the kind's own test file, which the removal deletes with the recipe.
_DEBT_SCAN_SKIP = ("docs/loom/",)

# The cases below that each copy the repository and run pytest inside the
# copy. The copy's own run must not start that again, so these are deselected
# there by name; a name that no longer exists makes pytest exit non-zero.
NESTED_TESTS = (
    "test_adding_a_kind_that_has_no_recipe_today_introduces_no_failure",
    "test_a_reworded_recipe_is_not_blamed_on_the_addition",
    "test_removing_a_kind_routed_today_leaves_no_reference",
    "test_recorded_unbounded_removal_is_still_unbounded",
    "test_removal_that_leaves_the_kinds_own_test_file_behind_is_detected",
    "test_removal_that_leaves_the_routing_row_behind_is_detected",
    "test_removal_that_leaves_the_name_in_a_live_file_is_detected",
)

_ROW = re.compile(r"^\|(?P<cells>.+)\|$")
_LINK = re.compile(r"\[.*?\]\((?P<target>[^)]+)\)")
_TYPE = re.compile(r"^\s*-\s*\{glob:.*type:\s*(?P<type>[A-Za-z-]+)\s*\}\s*$")


def _cell(text: str) -> str:
    """A cell's value: the link target when it is a link, else its bare words."""
    link = _LINK.search(text)
    return (link.group("target") if link else text).strip().strip("`").strip()


def _routing_rows(text: str) -> dict[str, str]:
    """Map artifact type to recipe file name for the table under the routing
    heading. A header or separator row carries no type and is skipped, so the
    table may be reformatted; a row that disappears cannot hide."""
    if ROUTING_HEADING not in text:
        return {}
    section = text.split(ROUTING_HEADING, 1)[1].split("\n## ", 1)[0]
    rows: dict[str, str] = {}
    for line in section.splitlines():
        match = _ROW.match(line.strip())
        if match is None:
            continue
        cells = [c for c in match.group("cells").split("|")]
        if len(cells) != 2:
            continue
        kind, target = _cell(cells[0]), _cell(cells[1])
        if not kind or not target or set(kind) <= set("-: "):
            continue
        if kind.lower().startswith("artifact type"):
            continue
        rows[kind] = target
    return rows


def routed_recipes() -> dict[str, tuple[str, ...]]:
    """Map each recipe file the routing table names to the artifact types
    routed to it, in file-name order.

    Two types may share one recipe, so removing that recipe puts more than
    one row back to `none`. This is the reader every module that needs to
    know which recipe files exist goes through: the routing table is the one
    place a kind is added or taken away, so a hand-written list of recipe
    paths elsewhere would be a second place to maintain and a dangling
    reference after a removal.
    """
    rows = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    grouped: dict[str, list[str]] = {}
    for kind, target in sorted(rows.items()):
        if target != NO_RECIPE:
            grouped.setdefault(target, []).append(kind)
    return {recipe: tuple(kinds) for recipe, kinds in sorted(grouped.items())}


def routed_recipe_files() -> list[Path]:
    """Every recipe file the routing table names, as paths in the tree.

    A row whose file is not there is left out rather than raised on: that
    dangling row is `test_every_artifact_type_is_routed_or_says_it_has_no_recipe`'s
    to report, and raising here would turn one named failure into a
    collection error in every module that reads a recipe.
    """
    return [REFERENCES / name for name in routed_recipes() if (REFERENCES / name).is_file()]


def recipe_kind(recipe: str) -> str:
    """The kind a recipe file is named after: `<stem><kind>.md` -> `<kind>`.

    Spelled with placeholders rather than with a recipe routed today, so
    that this reader is not itself a reference that a removal would leave
    dangling.
    """
    assert recipe.startswith(RECIPE_STEM) and recipe.endswith(".md"), recipe
    return recipe[len(RECIPE_STEM):-len(".md")]


def recipe_test_module(recipe: str) -> str:
    """The file name of the test module that owns `recipe`'s rules.

    Acceptance 6's convention, spelled in one place: one test file per recipe,
    named after the kind the recipe attacks. A module that needs another
    recipe's test module goes through here rather than writing the name, so
    what it reaches for is what the routing table routes today and the kind's
    removal takes the name away with the recipe.
    """
    return f"{RECIPE_TEST_STEM}{recipe_kind(recipe).replace('-', '_')}.py"


def recipe_pins() -> dict[str, tuple]:
    """Every `RECIPE_PINS` entry the routed recipes' own test modules define.

    A cross-document scan that must not flag a recipe's own pinned sentence
    reads the pin from here. Importing one recipe's test module by name would
    make that scan a reference the kind's removal leaves dangling; going
    through the routing table, the scan loses exactly the pins whose recipe
    went away and keeps the rest.

    A recipe whose module defines no pin table contributes nothing. A pin name
    two modules define is refused, because the caller looks a pin up by name
    alone and would otherwise silently get one of the two.
    """
    merged: dict[str, tuple] = {}
    for recipe in routed_recipes():
        module_name = recipe_test_module(recipe)
        if not (ROOT / SCRIPTS / module_name).is_file():
            continue
        module = importlib.import_module(module_name[:-len(".py")])
        for name, pin in getattr(module, "RECIPE_PINS", {}).items():
            assert name not in merged, (name, module_name)
            merged[name] = pin
    return merged


def _artifact_types() -> set[str]:
    """Every type name of the repository's own artifact-type vocabulary."""
    block = MANIFEST.read_text(encoding="utf-8").split("\nartifact_types:", 1)[1]
    types = {m.group("type") for line in block.splitlines() if (m := _TYPE.match(line))}
    return types


def _snapshot(folder: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(folder.iterdir()) if p.is_file()}


def _add_kind(folder: Path, kind: str, recipe: str, body: str) -> None:
    """Give `kind` a recipe: write the file, and point its row at it."""
    (folder / recipe).write_text(body, encoding="utf-8")
    protocol = folder / "adversarial.md"
    text = protocol.read_text(encoding="utf-8")
    rows = [line for line in text.splitlines() if _ROW.match(line.strip())]
    old = next(line for line in rows if _cell(line.strip().strip("|").split("|")[0]) == kind)
    new = f"| `{kind}` | [`{recipe}`]({recipe}) |"
    protocol.write_text(text.replace(old, new), encoding="utf-8")


def _affirms(text: str, verb: str, literal: str) -> bool:
    """Some sentence carries `verb` before `literal` and no negation.

    The verb is matched case-insensitively so that it may open a sentence;
    the literal is matched as written."""
    for sentence in split_sentences(text):
        v, lit = sentence.lower().find(verb.lower()), sentence.find(literal)
        if 0 <= v < lit and not has_negation(sentence):
            return True
    return False


# --- helper self-tests -----------------------------------------------------

# The synthetic fixtures name no recipe file that the routing table routes
# and none that a removal case deletes: a literal here would be a reference
# to a real file, and `test_no_new_file_hand_lists_a_routed_recipe` counts
# this module like any other.
_SYNTHETIC_RECIPE = "adversarial-synthetic-one.md"
_SYNTHETIC_OTHER = "adversarial-synthetic-two.md"

_SYNTHETIC = (
    "# Title\n\n## Which recipe to read\n\n"
    "| Artifact type | Recipe file |\n|---|---|\n"
    f"| `code` | [`{_SYNTHETIC_RECIPE}`]({_SYNTHETIC_RECIPE}) |\n"
    "| `plan` | none |\n\n"
    f"## Recording\n\n| `docs` | [`{_SYNTHETIC_OTHER}`]({_SYNTHETIC_OTHER}) |\n"
)


def test_routing_row_helper_synthetic() -> None:
    assert _routing_rows(_SYNTHETIC) == {"code": _SYNTHETIC_RECIPE, "plan": NO_RECIPE}
    assert _routing_rows("# Title\n\n## Recording\n\n| `code` | x.md |\n") == {}


def test_routed_recipe_reader_synthetic() -> None:
    """The reader groups the rows by file, so a recipe two rows share is one
    entry carrying both types, and every file it names is there."""
    grouped = routed_recipes()
    assert grouped, "the routing table names no recipe file"
    rows = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    for recipe, kinds in grouped.items():
        assert kinds, recipe
        for kind in kinds:
            assert rows[kind] == recipe, (kind, recipe)
    assert sorted(grouped) == sorted(p.name for p in routed_recipe_files())
    # A synthetic name, for the reason the fixtures above give: a kind whose
    # name carries a hyphen is the case that a naive split would get wrong.
    assert recipe_kind(_SYNTHETIC_RECIPE) == "synthetic-one"


def test_recipe_test_module_and_pin_reader_synthetic() -> None:
    """A recipe's test module is named from the recipe, and the pin reader
    reaches the module of every routed recipe that has one."""
    assert recipe_test_module(_SYNTHETIC_RECIPE) == f"{RECIPE_TEST_STEM}synthetic_one.py"
    pins = recipe_pins()
    # Every pin the reader returns comes from a routed recipe's own module,
    # and every pin such a module defines is in what it returns. Not asserted:
    # that there is any pin at all -- a repository whose recipes pin nothing
    # is a repository with nothing for the scans to exempt, which is the state
    # a removal case reaches when the last recipe carrying a pin table goes.
    # Nor that a routed recipe has a module at all: requiring one would make
    # giving a kind a recipe two files rather than the one file and one row
    # the routing table describes, so a recipe without one contributes
    # nothing here, exactly as `recipe_pins` reads it.
    from_modules: dict[str, tuple] = {}
    for recipe in routed_recipes():
        path = ROOT / SCRIPTS / recipe_test_module(recipe)
        if not path.is_file():
            continue
        module = importlib.import_module(recipe_test_module(recipe)[:-len(".py")])
        from_modules.update(getattr(module, "RECIPE_PINS", {}))
    assert pins == from_modules
    for name, pin in pins.items():
        assert len(pin) == 6, (name, pin)


def test_cell_helper_synthetic() -> None:
    assert _cell(f" [`{_SYNTHETIC_OTHER}`]({_SYNTHETIC_OTHER}) ") == _SYNTHETIC_OTHER
    assert _cell(" `spec` ") == "spec"
    assert _cell(" none ") == NO_RECIPE


def test_artifact_type_helper_synthetic() -> None:
    assert _TYPE.match('  - {glob: "docs/loom/*/plan.md",        type: plan}').group("type") == "plan"
    assert _TYPE.match("  - {name: package-tests, grammar: none}") is None


def test_add_kind_helper_synthetic(tmp_path: Path) -> None:
    (tmp_path / "adversarial.md").write_text(_SYNTHETIC, encoding="utf-8")
    _add_kind(tmp_path, "plan", _SYNTHETIC_OTHER, "# Adversarial — plan\n")
    rows = _routing_rows((tmp_path / "adversarial.md").read_text(encoding="utf-8"))
    assert rows["plan"] == _SYNTHETIC_OTHER
    assert rows["code"] == _SYNTHETIC_RECIPE


def test_affirms_helper_synthetic() -> None:
    affirmative = f"Read {CONTRACT_ROUTE_LITERAL} the change touched."
    assert _affirms(affirmative, CONTRACT_ROUTE_VERB, CONTRACT_ROUTE_LITERAL)
    negated = f"Never read {CONTRACT_ROUTE_LITERAL} the change touched."
    assert not _affirms(negated, CONTRACT_ROUTE_VERB, CONTRACT_ROUTE_LITERAL)
    assert not _affirms("Read the protocol.", CONTRACT_ROUTE_VERB, CONTRACT_ROUTE_LITERAL)


# --- A4: one new file and one new row, and no existing recipe touched -------

def test_adding_a_kind_is_one_file_and_one_row(tmp_path: Path) -> None:
    """add-kind-one-file-one-row."""
    folder = tmp_path / "references"
    shutil.copytree(REFERENCES, folder)
    before = _snapshot(folder)
    kind = next(k for k, target in _routing_rows(PROTOCOL.read_text(encoding="utf-8")).items()
                if target == NO_RECIPE)
    recipe = f"adversarial-{kind}.md"
    _add_kind(folder, kind, recipe, f"# Adversarial — {kind}\n\nSee [`adversarial.md`](adversarial.md).\n")
    after = _snapshot(folder)

    assert set(after) - set(before) == {recipe}, set(after) - set(before)
    assert set(before) - set(after) == set()
    changed = [name for name in before if before[name] != after[name]]
    assert changed == ["adversarial.md"], changed
    old_lines = before["adversarial.md"].decode().splitlines()
    new_lines = after["adversarial.md"].decode().splitlines()
    assert len(old_lines) == len(new_lines)
    differing = [i for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
    assert len(differing) == 1, [old_lines[i] for i in differing]
    assert _routing_rows(after["adversarial.md"].decode())[kind] == recipe


def test_adding_a_kind_leaves_every_existing_recipe_file_untouched(tmp_path: Path) -> None:
    """existing-recipe-file-untouched."""
    folder = tmp_path / "references"
    shutil.copytree(REFERENCES, folder)
    before = _snapshot(folder)
    routed = {t for t in _routing_rows(PROTOCOL.read_text(encoding="utf-8")).values() if t != NO_RECIPE}
    assert routed, "the routing table names no recipe file"
    kind = next(k for k, target in _routing_rows(PROTOCOL.read_text(encoding="utf-8")).items()
                if target == NO_RECIPE)
    _add_kind(folder, kind, f"adversarial-{kind}.md", f"# Adversarial — {kind}\n")
    after = _snapshot(folder)
    for recipe in routed:
        assert after[recipe] == before[recipe], recipe


# --- A7: contract, protocol and recipe are one followable chain -------------

def test_contract_routes_through_the_protocol_to_each_recipe() -> None:
    """protocol-plus-kind-is-complete, first half: the contract is followable."""
    contract = " ".join(CONTRACT.read_text(encoding="utf-8").split())
    assert CONTRACT_PROTOCOL_PATH in contract, contract
    assert PROTOCOL.is_file(), PROTOCOL
    assert _affirms(contract, CONTRACT_ROUTE_VERB, CONTRACT_ROUTE_LITERAL), contract


def test_protocol_plus_the_matching_recipe_is_the_whole_procedure() -> None:
    """protocol-plus-kind-is-complete, second half: the pair needs no third file."""
    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    rows = _routing_rows(protocol_text)
    recipes = {target for target in rows.values() if target != NO_RECIPE}
    assert recipes, "the routing table names no recipe file"
    for recipe in sorted(recipes):
        path = REFERENCES / recipe
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert "[`adversarial.md`](adversarial.md)" in text, recipe
        siblings = {m.group("target") for m in _LINK.finditer(text)}
        assert siblings <= {"adversarial.md", recipe}, (recipe, siblings)


def test_every_artifact_type_is_routed_or_says_it_has_no_recipe() -> None:
    """unrouted-kind-detected."""
    rows = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    types = _artifact_types()
    assert types, MANIFEST
    assert types <= set(rows), types - set(rows)
    assert set(rows) <= types, set(rows) - types
    for kind, target in sorted(rows.items()):
        if target == NO_RECIPE:
            continue
        assert (REFERENCES / target).is_file(), (kind, target)


def test_unrouted_kind_detection_synthetic() -> None:
    """A missing row and a row naming a file that is not there are both caught."""
    types = _artifact_types()
    complete = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    assert types <= set(complete)
    dropped = dict(complete)
    dropped.pop(sorted(types)[0])
    assert not types <= set(dropped)
    dangling = _routing_rows(
        f"{ROUTING_HEADING}\n\n| `code` | [`adversarial-ghost.md`](adversarial-ghost.md) |\n"
    )
    assert not (REFERENCES / dangling["code"]).is_file()


# --- A5: removing a kind, performed for real on a copy of the repository ----
#
# Every helper below works on a copy. None of them writes inside the
# repository, and none of them asserts on the wording of a document.

# Directories a copy grows while pytest runs in it. They are not repository
# content, so the byte-for-byte comparison and the reference scan pass over
# them; nothing else is ever passed over.
_GENERATED = {"__pycache__", ".pytest_cache"}


def _tracked_files() -> list[str]:
    """Every file git tracks, as repository-relative paths."""
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    names = [n for n in result.stdout.split("\0") if n]
    assert names, "git lists no tracked file"
    return names


def _copy_repository(dest: Path) -> list[str]:
    """Copy every tracked file into `dest`, from the working tree.

    The working tree rather than a commit, so a check under development is
    copied as it currently reads. Returns the paths copied, which is what the
    byte-for-byte comparison and the scan are later held to.
    """
    copied: list[str] = []
    for rel in _tracked_files():
        source = ROOT / rel
        if not source.is_file():  # a submodule or a deleted-but-staged path
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(rel)
    assert len(copied) > 500, f"the copy holds only {len(copied)} files"
    return copied


def _files_in(root: Path) -> list[str]:
    """Every file under `root` bar the directories pytest generates."""
    found: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.relative_to(root).parts)
        if parts & _GENERATED:
            continue
        found.append(str(path.relative_to(root)))
    return sorted(found)


def _references_to(root: Path, names: tuple[str, ...], *, expected: int) -> list[str]:
    """Which files under `root` write any of `names`.

    `expected` is how many files the caller knows are there. The scan reads
    every one of them and fails if it read fewer, so a scan that walked the
    wrong directory, or that a read error emptied, cannot report "no
    reference" and be believed.
    """
    assert names, "the scan was given no name to look for"
    read = 0
    hits: list[str] = []
    for rel in _files_in(root):
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            text = (root / rel).read_bytes().decode("utf-8", "replace")
        read += 1
        if any(name in text for name in names):
            hits.append(rel)
    assert read >= expected, f"the scan read {read} files where {expected} were copied"
    return sorted(hits)


def _own_test_file(kind: str) -> str:
    """The test file Acceptance 6 gives that kind's recipe, as a path."""
    return f"{SCRIPTS}/{recipe_test_module(_recipe_file(kind))}"


def _recipe_file(kind: str) -> str:
    return f"{RECIPE_STEM}{kind}.md"


def _deleted_names(recipe: str, own_test: str | None) -> tuple[str, ...]:
    """The names a removal took away, for the scan to look for.

    One name when the recipe had no test module of its own, two when it did.
    The scan's `expected` count is derived from the length rather than written
    as a literal, so a removal of one file is not held to the file count of a
    removal of two.
    """
    return (recipe,) if own_test is None else (recipe, Path(own_test).name)


def unrouted_types() -> list[str]:
    """Every artifact type of the repository's vocabulary with no recipe today.

    Read from the manifest and from the table together, so that a type the
    manifest grows is covered by whatever is parametrized over this the day it
    is added, without anyone editing a list. Every module that performs the
    addition goes through here, so the kinds it is proven on are the kinds
    that can be added.
    """
    rows = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    return sorted(t for t in _artifact_types() if rows.get(t, NO_RECIPE) == NO_RECIPE)


# The recipe a kind gets when the addition is performed: the one file the
# routing table asks for and nothing else. One template, read by every module
# that performs the addition, so the file the checks are proven on is the same
# file everywhere. Written from the kind's name rather than taken from a recipe
# routed today, so it is not a reference a removal would leave dangling.
ADDED_RECIPE = (
    "# Adversarial — {kind}\n\n"
    "Read it together with the shared protocol in [`adversarial.md`](adversarial.md).\n\n"
    "## {heading}\n\n"
    "Attack the {kind} artifact until something it promises stops being true.\n"
)


def added_recipe(kind: str) -> str:
    """`ADDED_RECIPE` filled in for `kind`."""
    return ADDED_RECIPE.format(kind=kind, heading=kind.capitalize())


def _kinds_named_in(texts: list[str], candidates: dict[str, tuple[str, str]]) -> set[str]:
    """Which `candidates` (kind -> (recipe name, own-test name)) are already
    written somewhere in `texts`.

    Pure and filesystem-free, so the collision rule `_removable_kind` applies
    is provable on its own: a kind is tainted the moment either name it would
    delete already appears in a text that is not going anywhere, such as a
    migration note recording where a past removal's rule now lives.
    """
    tainted: set[str] = set()
    for text in texts:
        for kind, (recipe, own_test) in candidates.items():
            if kind not in tainted and (recipe in text or own_test in text):
                tainted.add(kind)
    return tainted


def _removable_kind() -> str:
    """A kind the routing table says has no recipe, and whose recipe and own
    test file names are not already written anywhere else in the repository,
    chosen deterministically.

    The negative cases give it a recipe and then remove it wrongly, so the
    names they delete must belong to no other file in the repository -- else
    the reference they find would be one they did not plant. An unrouted kind
    whose recipe name a permanent record already writes -- true of a kind once
    its own removal reaches the routing table, such as a migration note that
    keeps naming the file that removal deleted -- would break that promise if
    it were chosen, so it is passed over rather than picked.
    """
    rows = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    unrouted = sorted(k for k, target in rows.items() if target == NO_RECIPE)
    assert unrouted, "every kind is routed; this check has no kind to add and remove"
    candidates = {k: (_recipe_file(k), Path(_own_test_file(k)).name) for k in unrouted}
    texts: list[str] = []
    for rel in _tracked_files():
        path = ROOT / rel
        if not path.is_file():
            continue
        try:
            texts.append(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError):
            texts.append(path.read_bytes().decode("utf-8", "replace"))
    tainted = _kinds_named_in(texts, candidates)
    available = [k for k in unrouted if k not in tainted]
    assert available, "every unrouted kind's name is already written elsewhere"
    return available[0]


def _add_kind_to_copy(root: Path, kind: str) -> tuple[str, str]:
    """Give `kind` a recipe in the copy: the file, its own test file, its row.

    Nothing requires a routed recipe to have a test module of its own --
    giving a kind a recipe is one file and one row. One is written here
    anyway, because the removal these cases do wrong is the removal of a kind
    that has one: it is the second file a removal must not leave behind.
    """
    recipe, own_test = _recipe_file(kind), _own_test_file(kind)
    body = (
        f"# Adversarial — {kind}\n\n"
        f"Read [`adversarial.md`](adversarial.md) first; this file holds what is\n"
        f"specific to a {kind} artifact.\n\n"
        f"## {kind.capitalize()}\n\n"
        f"Attack the {kind} artifact until it fails.\n"
    )
    _add_kind(root / "loom-code/skills/closing-review/references", kind, recipe, body)
    test_body = (
        f'"""The {kind} recipe\'s own rules."""\n'
        "from pathlib import Path\n\n\n"
        "ROOT = Path(__file__).resolve().parents[2]\n"
        f'RECIPE = ROOT / "loom-code/skills/closing-review/references/{recipe}"\n'
        'ADVERSARY = ROOT / "loom-code/agents/adversary.md"\n'
        f'RULE = "Attack the {kind} artifact"\n\n\n'
        "def test_recipe_states_its_own_rule() -> None:\n"
        '    assert RULE in RECIPE.read_text(encoding="utf-8")\n\n\n'
        "def test_procedure_sentence_in_both_files_rejected() -> None:\n"
        '    assert RULE not in ADVERSARY.read_text(encoding="utf-8")\n'
    )
    (root / own_test).write_text(test_body, encoding="utf-8")
    return recipe, own_test


def _remove_kind_from_copy(
    root: Path, kind: str, *, drop_recipe=True, drop_own_test=True, restore_row=True
) -> None:
    """Remove `kind`: delete its recipe, delete its own test, row back to none.

    Each step can be left undone, which is how the negative cases build a
    removal that was done wrong.
    """
    if drop_recipe:
        (root / "loom-code/skills/closing-review/references" / _recipe_file(kind)).unlink()
    if drop_own_test:
        (root / _own_test_file(kind)).unlink()
    if restore_row:
        protocol = root / "loom-code/skills/closing-review/references/adversarial.md"
        text = protocol.read_text(encoding="utf-8")
        recipe = _recipe_file(kind)
        row = f"| `{kind}` | [`{recipe}`]({recipe}) |"
        assert row in text, row
        protocol.write_text(text.replace(row, f"| `{kind}` | {NO_RECIPE} |"), encoding="utf-8")


def _run_adversary_tests(root: Path) -> subprocess.CompletedProcess[str]:
    """Run the adversary test files inside the copy.

    The file list is a glob, so a recipe test the removal deleted is absent
    from the run and one the addition wrote is in it. The cases that copy the
    repository are deselected by name: they would copy the copy. pytest exits
    non-zero on a name that no longer matches a test, so a renamed case is
    caught rather than quietly stopping to run.
    """
    scripts = root / SCRIPTS
    targets = sorted(str(p.relative_to(root)) for p in scripts.glob(SUITE_GLOB))
    targets += [f"{SCRIPTS}/{name}" for name in SUITE_EXTRA]
    for target in targets:
        assert (root / target).is_file(), target
    deselect: list[str] = []
    for name in NESTED_TESTS:
        assert name in globals(), name
        deselect += ["--deselect", f"{SCRIPTS}/test_adversary_routing.py::{name}"]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # The copy has no `.git`; the layout module reads the migration out of
    # git history, so it is pointed at this repository's object store.
    gitdir = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"], cwd=ROOT, capture_output=True, text=True
    )
    assert gitdir.returncode == 0, gitdir.stderr
    env["GIT_DIR"] = gitdir.stdout.strip()
    return subprocess.run(
        # `-rfE` so the run always names what failed: the comparison below is
        # made on those names, and a pytest whose summary characters were
        # configured away would otherwise leave it comparing empty sets.
        ["python3", "-m", "pytest", "-q", "-rfE", "-p", "no:cacheprovider", *targets, *deselect],
        cwd=root, capture_output=True, text=True, env=env,
    )


_FAILED = re.compile(r"^(?:FAILED|ERROR) (?P<node>\S+)", re.M)


def failures(run: subprocess.CompletedProcess[str]) -> frozenset[str]:
    """Which tests the run reported failing, by name.

    This is what the cases that copy the repository assert on, rather than the
    exit status: a copy inherits every failure the working tree already has, so
    an exit status is a statement about the whole suite while the difference
    between two of these sets is a statement about the edit made between them.

    A run that exited non-zero without naming a single failing test -- a
    collection error, an internal error, a crash -- is raised on rather than
    read as an empty set, so a comparison that has nothing to compare cannot
    come out clean.
    """
    named = frozenset(m.group("node") for m in _FAILED.finditer(run.stdout + run.stderr))
    if run.returncode != 0 and not named:
        raise AssertionError(
            "the run exited non-zero without naming a failing test, so its "
            f"failures cannot be compared:\n{run.stdout}{run.stderr}"
        )
    return named


def _passed(run: subprocess.CompletedProcess[str]) -> int:
    """How many tests the run reported passing, or none if it did not say.

    A run that says nothing about passing is not treated as a run of zero
    tests; the caller asserts on this number and gets the output in the
    failure.
    """
    match = re.search(r"(\d+) passed", run.stdout + run.stderr)
    return int(match.group(1)) if match else 0


@pytest.fixture(scope="session")
def inherited_failures(tmp_path_factory: pytest.TempPathFactory) -> frozenset[str]:
    """What is already failing in an untouched copy of the repository.

    The cases below edit a copy and ask what the edit broke. A copy carries
    whatever the working tree carries, so the answer is the difference against
    this set and not the copy's exit status: one reworded sentence in one
    recipe reddens that recipe's own test file inside every copy, and holding
    a copy to green would make that one edit fail every case here.

    Measured once for the whole session -- one copy and one run, whatever the
    number of cases -- and warned about when it is not empty, so a copy that
    was already failing is stated rather than passed over in silence.
    """
    root = tmp_path_factory.mktemp("inherited") / "repo"
    _copy_repository(root)
    run = _run_adversary_tests(root)
    named = failures(run)
    assert _passed(run) > 0, run.stdout + run.stderr
    if named:
        warnings.warn(
            "this copy of the repository was already failing before any kind "
            "was added or removed; these failures are not the subject of the "
            "cases in this module and are subtracted from them: "
            + ", ".join(sorted(named)),
            stacklevel=1,
        )
    return named


def caused_by_the_edit(
    run: subprocess.CompletedProcess[str], inherited: frozenset[str]
) -> frozenset[str]:
    """Which failures of `run` the edit made in the copy is answerable for.

    Every failure the untouched copy already had is subtracted. A test that
    only exists once the edit was made -- a case parametrized over the routing
    table gains a parameter when a kind gains a recipe -- is not in the
    inherited set, so a failure of it counts here, which is right: the edit
    brought it into being.
    """
    return failures(run) - inherited


def _longest_sentence(text: str) -> str:
    """The longest sentence of `text` with its heading lines dropped.

    Used to reword a recipe without writing any recipe's name or any of its
    sentences here: both would be a reference that the kind's removal leaves
    dangling.
    """
    stripped = re.sub(r"^#{1,6} .*$", "", text, flags=re.M)
    sentences = [s.strip() for s in split_sentences(" ".join(stripped.split()))]
    assert sentences, text
    return max(sentences, key=len)


def _reword(sentence: str) -> str:
    """The same sentence with its first two words exchanged.

    Every word the sentence had is still in it, so the edit is a wording
    change and nothing else -- no file added, deleted or emptied, no rule
    taken out of the folder -- and it is enough to stop any pin that quotes
    the sentence or opens a literal at its first word. Deliberately
    mechanical: an invented synonym would be a sentence of a recipe written
    into this file, which the removal of that kind would leave dangling.
    """
    words = sentence.split(" ")
    assert len(words) > 2, sentence
    return " ".join([words[1], words[0], *words[2:]])


def _failing_modules(named: frozenset[str]) -> set[str]:
    """The test file names a set of failure node ids belongs to."""
    return {node.split("::")[0].rsplit("/", 1)[-1] for node in named}


def _reword_candidates(inherited: frozenset[str]) -> list[str]:
    """The routed recipes whose reword can still plant a failure, in order.

    A recipe qualifies when it has a test module of its own -- nothing else
    goes red for a wording change -- and that module is not already among
    `inherited`'s failures. The ordinary state of a working branch is the
    reason: between editing a recipe and updating its test file, that
    recipe's module is red before anything here touches a copy, so rewording
    that recipe plants nothing new and proves nothing, while rewording any
    other one still does. Sorted, so which recipe is picked is fixed by the
    routing table and not by the order a dict happens to carry.
    """
    failing = _failing_modules(inherited)
    return [
        recipe
        for recipe in sorted(routed_recipes())
        if (module := recipe_test_module(recipe)) not in failing
        and (ROOT / SCRIPTS / module).is_file()
    ]


def _first_planting(attempts: dict[str, frozenset[str]]) -> tuple[str, frozenset[str]]:
    """The first reword of `attempts` that really did redden something.

    Raised on when no attempt did: a round of rewords that planted nothing
    leaves the contamination measurement unexercised, which is a failure and
    never a quiet pass. Pure, so the sabotaged measurement -- one that reports
    every reword as harmless -- is provable without copying the repository.
    """
    for recipe, planted in attempts.items():
        if planted:
            return recipe, planted
    raise AssertionError(
        "no reword of a recipe whose own test module was green planted a "
        "failure, so the contamination measurement was not exercised: "
        + ", ".join(sorted(attempts))
    )


def _reword_a_recipe_in(root: Path, recipe: str) -> str:
    """Reword one sentence of `recipe` in the copy, and say which sentence.

    The recipe is the caller's, chosen through `_reword_candidates`, so
    nothing here depends on which kinds exist. The sentence is matched across
    the line breaks it is wrapped over, so only its wording changes -- no file
    is added, deleted, renamed or emptied.
    """
    path = root / str(REFERENCES.relative_to(ROOT)) / recipe
    text = path.read_text(encoding="utf-8")
    sentence = _longest_sentence(text)
    pattern = re.compile(r"\s+".join(re.escape(w) for w in sentence.split(" ")))
    assert len(pattern.findall(text)) == 1, sentence
    reworded = _reword(sentence)
    # A function as the replacement, so nothing in the sentence is read as a
    # backreference.
    path.write_text(pattern.sub(lambda _m: reworded, text), encoding="utf-8")
    return sentence


# --- helper self-tests -----------------------------------------------------

def test_reference_scan_reads_what_it_is_given_synthetic(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "a/one.md").write_text("names ghost.md here\n", encoding="utf-8")
    (tmp_path / "a/two.md").write_text("names nothing\n", encoding="utf-8")
    (tmp_path / "a/__pycache__").mkdir()
    (tmp_path / "a/__pycache__/three.pyc").write_bytes(b"ghost.md")
    assert _references_to(tmp_path, ("ghost.md",), expected=2) == ["a/one.md"]
    assert _references_to(tmp_path, ("absent.md",), expected=2) == []


def test_reference_scan_fails_loudly_when_it_can_see_nothing(tmp_path: Path) -> None:
    """A scan over a tree that is not there reports a failure, not a clean bill."""
    empty = tmp_path / "empty"
    empty.mkdir()
    assert _files_in(empty) == []
    try:
        _references_to(empty, ("ghost.md",), expected=1)
    except AssertionError as exc:
        assert "read 0 files" in str(exc), exc
    else:
        raise AssertionError("the scan reported no reference over a tree it never read")
    try:
        _references_to(tmp_path, (), expected=0)
    except AssertionError as exc:
        assert "no name" in str(exc), exc
    else:
        raise AssertionError("the scan accepted an empty list of names")


def test_removable_kind_and_name_helpers_synthetic() -> None:
    kind = _removable_kind()
    assert _routing_rows(PROTOCOL.read_text(encoding="utf-8"))[kind] == NO_RECIPE
    assert _recipe_file(kind) == f"{RECIPE_STEM}{kind}.md"
    assert _own_test_file("skill-gate") == f"{SCRIPTS}/{RECIPE_TEST_STEM}skill_gate.py"
    assert not (ROOT / _own_test_file(kind)).exists(), kind
    assert not (REFERENCES / _recipe_file(kind)).exists(), kind


def test_kinds_named_in_helper_synthetic() -> None:
    """The pure name-collision check `_removable_kind` relies on: a kind is
    tainted when a text anywhere carries its recipe or its own test file's
    name, such as a migration note that still names the file a past removal
    deleted."""
    candidates = {
        "alpha": ("adversarial-alpha.md", "test_adversary_recipe_alpha.py"),
        "beta": ("adversarial-beta.md", "test_adversary_recipe_beta.py"),
    }
    texts = ["A migration note names `adversarial-alpha.md` as the file a removal deleted."]
    assert _kinds_named_in(texts, candidates) == {"alpha"}
    assert _kinds_named_in([], candidates) == set()
    assert _kinds_named_in(["nothing relevant here"], candidates) == set()


def test_removable_kind_skips_a_routed_kind_whose_removal_would_collide(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`code` is routed today, but its recipe and own-test names are already
    written in this repository's own migration record (the plan and the
    rule-correspondence note for this change). If `code`'s row ever goes back
    to `none`, the round trip must not pick `code` to add and remove again --
    doing so would break the promise it is built on: that the names it
    deletes belong to no other file in the repository. Proven against the
    real tree, with only `code`'s own row flipped to `none`.
    """
    tainted_kind = "code"
    recipe = _recipe_file(tainted_kind)
    real_text = PROTOCOL.read_text(encoding="utf-8")
    row = f"| `{tainted_kind}` | [`{recipe}`]({recipe}) |"
    if row not in real_text:
        # This copy already carries a removal of `code`, performed by the
        # very case this helper exists for; the collision it would prove is
        # then in the past tense, recorded rather than reproducible here.
        pytest.skip("`code` is not routed in this tree")
    synthetic_protocol = tmp_path / "adversarial.md"
    synthetic_protocol.write_text(
        real_text.replace(row, f"| `{tainted_kind}` | {NO_RECIPE} |"), encoding="utf-8"
    )
    monkeypatch.setattr("test_adversary_routing.PROTOCOL", synthetic_protocol)

    assert _removable_kind() != "code"


def test_passed_helper_synthetic() -> None:
    ok = subprocess.CompletedProcess([], 0, "12 passed in 0.5s", "")
    assert _passed(ok) == 12
    assert _passed(subprocess.CompletedProcess([], 1, "2 failed, 3 passed", "")) == 3
    assert _passed(subprocess.CompletedProcess([], 2, "Interrupted: 2 errors", "")) == 0


def test_failure_reader_synthetic() -> None:
    """The names a run gives, read off its summary; a green run names none."""
    green = subprocess.CompletedProcess([], 0, "30 passed in 1.0s", "")
    assert failures(green) == frozenset()
    red = subprocess.CompletedProcess(
        [], 1,
        "FAILED a/b.py::test_one[x]\nERROR a/c.py\n1 failed, 2 passed in 1.0s\n", "",
    )
    assert failures(red) == {"a/b.py::test_one[x]", "a/c.py"}


def test_failure_reader_fails_loudly_on_a_run_it_cannot_read() -> None:
    """A non-zero run that named nothing is raised on, not read as green.

    Otherwise a copy whose suite crashed before collecting would hand every
    case below an empty set and every comparison would come out clean.
    """
    crashed = subprocess.CompletedProcess([], 3, "INTERNALERROR> boom\n", "")
    try:
        failures(crashed)
    except AssertionError as exc:
        assert "cannot be compared" in str(exc), exc
    else:
        raise AssertionError("a crashed run was read as having no failure")


def test_edit_blame_helper_synthetic() -> None:
    """Only what the untouched copy was not already failing is blamed on the
    edit, and a test the edit brought into being is."""
    inherited = frozenset({"a/recipe_spec.py::test_rule[anchor]"})
    unchanged = subprocess.CompletedProcess(
        [], 1, "FAILED a/recipe_spec.py::test_rule[anchor]\n1 failed, 9 passed\n", "",
    )
    assert caused_by_the_edit(unchanged, inherited) == frozenset()
    worse = subprocess.CompletedProcess(
        [], 1,
        "FAILED a/recipe_spec.py::test_rule[anchor]\n"
        "FAILED a/shape.py::test_shape[adversarial-new.md]\n2 failed, 8 passed\n", "",
    )
    assert caused_by_the_edit(worse, inherited) == {"a/shape.py::test_shape[adversarial-new.md]"}


def test_reword_helpers_synthetic() -> None:
    """The reword is one sentence, wording only, and the longest sentence is
    picked from prose rather than from a heading."""
    text = "# Adversarial — thing\n\nShort one.\n\nThe longer sentence here\nwraps a line.\n"
    assert _longest_sentence(text) == "The longer sentence here wraps a line."
    assert _reword("The longer sentence here wraps a line.") == (
        "longer The sentence here wraps a line."
    )
    assert sorted(_reword("a b c").split(" ")) == ["a", "b", "c"]


def test_failing_module_reader_synthetic() -> None:
    assert _failing_modules(frozenset()) == set()
    assert _failing_modules(frozenset({
        "loom-code/scripts/test_one.py::test_rule[anchor]",
        "loom-code/scripts/test_one.py::test_other",
        "loom-code/scripts/test_two.py",
    })) == {"test_one.py", "test_two.py"}


def test_reword_candidates_pass_over_a_recipe_already_red_synthetic() -> None:
    """A reword is measured on a recipe whose own test module is green.

    The three states the guard meets: an untouched tree, where every routed
    recipe that has a module of its own is a candidate; a branch where one
    recipe was edited and its test file not yet updated, where that recipe is
    passed over and the others still serve; and a tree where every one of them
    is red, where there is nothing left to measure and the guard says so
    rather than failing for an edit that was not its subject.
    """
    green = _reword_candidates(frozenset())
    assert green, "no routed recipe has a test module of its own"
    for recipe in green:
        assert (ROOT / SCRIPTS / recipe_test_module(recipe)).is_file(), recipe

    one_red = frozenset({f"{SCRIPTS}/{recipe_test_module(green[0])}::test_rule[anchor]"})
    assert _reword_candidates(one_red) == green[1:]

    all_red = frozenset(f"{SCRIPTS}/{recipe_test_module(r)}::test_rule" for r in green)
    assert _reword_candidates(all_red) == []


def test_first_planting_fails_when_nothing_was_planted_synthetic() -> None:
    """The sabotaged measurement: every reword comes back harmless.

    A guard that answered that with a skip, or with a pass, would prove
    nothing at all -- so this is the one outcome that is raised on. The
    synthetic recipe names are the ones this module already uses for its
    fixtures, for the reason given there.
    """
    try:
        _first_planting({_SYNTHETIC_RECIPE: frozenset(), _SYNTHETIC_OTHER: frozenset()})
    except AssertionError as exc:
        assert "was not exercised" in str(exc), exc
    else:
        raise AssertionError("a round of rewords that planted nothing came out clean")

    planted = frozenset({"a/b.py::test_rule[anchor]"})
    assert _first_planting({_SYNTHETIC_RECIPE: frozenset(), _SYNTHETIC_OTHER: planted}) == (
        _SYNTHETIC_OTHER, planted
    )
    assert _first_planting({_SYNTHETIC_RECIPE: planted}) == (_SYNTHETIC_RECIPE, planted)


# --- A5 negative: a removal done wrong is caught ---------------------------
#
# The positive these are the negatives of is
# `test_removing_a_kind_routed_today_leaves_no_reference` below, which removes
# each kind that exists. What is added and removed here is an invented kind,
# because a removal done wrong has to be done on a kind the repository can
# spare.

def test_removal_that_leaves_the_kinds_own_test_file_behind_is_detected(
    tmp_path: Path, inherited_failures: frozenset[str]
) -> None:
    """stale-reference-detected: the recipe is gone, its test still names it.

    What is asserted is that the botched removal broke something the untouched
    copy was passing, not merely that the copy is red: a failure the copy
    already carried would otherwise stand in for the detection.
    """
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    kind = _removable_kind()
    recipe, own_test = _add_kind_to_copy(root, kind)
    _remove_kind_from_copy(root, kind, drop_own_test=False)

    names = (recipe, Path(own_test).name)
    assert _references_to(root, names, expected=len(copied)) == [own_test]
    run = _run_adversary_tests(root)
    assert caused_by_the_edit(run, inherited_failures), run.stdout + run.stderr


def test_removal_that_leaves_the_routing_row_behind_is_detected(
    tmp_path: Path, inherited_failures: frozenset[str]
) -> None:
    """stale-reference-detected: both files are gone, the row still names one.

    Held to the same difference as the case above, and for the same reason.
    """
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    kind = _removable_kind()
    recipe, own_test = _add_kind_to_copy(root, kind)
    _remove_kind_from_copy(root, kind, restore_row=False)

    names = (recipe, Path(own_test).name)
    protocol = f"{REFERENCES.relative_to(ROOT)}/adversarial.md"
    assert _references_to(root, names, expected=len(copied)) == [protocol]
    run = _run_adversary_tests(root)
    assert caused_by_the_edit(run, inherited_failures), run.stdout + run.stderr


def test_removal_that_leaves_the_name_in_a_live_file_is_detected(tmp_path: Path) -> None:
    """stale-reference-detected: the removal is complete, one file still writes
    the deleted name, and the scan is what notices."""
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    kind = _removable_kind()
    recipe, own_test = _add_kind_to_copy(root, kind)

    stale = "loom-code/agents/adversary.md"
    contract = root / stale
    contract.write_text(
        contract.read_text(encoding="utf-8") + f"\n<!-- left behind: {recipe} -->\n",
        encoding="utf-8",
    )
    _remove_kind_from_copy(root, kind)

    names = (recipe, Path(own_test).name)
    assert _references_to(root, names, expected=len(copied)) == [stale]


# --- A5 positive, for a kind routed today -----------------------------------

def _remove_routed_kind_from_copy(root: Path, recipe: str, kinds: tuple[str, ...]) -> str | None:
    """Remove a kind that is routed today, in the copy: delete its recipe,
    delete its own test file if it has one, and put every row that named the
    recipe back to `none`. Returns the test file it deleted, or `None`.

    Nothing requires a routed recipe to have a test module of its own: giving
    a kind a recipe is one new file plus one row, and Acceptance 4 is that
    addition and nothing else. So the removal must be the mirror of it --
    demanding a second file back would make the check the one thing that
    knows about a file no document asks a reader to write, and a kind added
    exactly as the routing table describes would fail its own removal.
    """
    references = root / str(REFERENCES.relative_to(ROOT))
    (references / recipe).unlink()
    own_test: str | None = _own_test_file(recipe_kind(recipe))
    if (root / own_test).is_file():
        (root / own_test).unlink()
    else:
        own_test = None
    protocol = references / "adversarial.md"
    text = protocol.read_text(encoding="utf-8")
    for kind in kinds:
        row = f"| `{kind}` | [`{recipe}`]({recipe}) |"
        assert row in text, row
        text = text.replace(row, f"| `{kind}` | {NO_RECIPE} |")
    protocol.write_text(text, encoding="utf-8")
    return own_test


# Recipes whose removal is not bounded yet, because a module outside the
# reference folder reaches for that kind's own test file by name rather than
# through the routing table. The one kind that was here when this check went
# in is gone: `test_build_mechanical_checks.py` now reads the recipes' pin
# tables through `recipe_pins()`, and `test_module_criteria_text.py` derives
# each recipe's own test module from the routing table, so the list is empty.
# It stays: entries are debt, not permission, and the test below proves each
# one is still unbounded, so clearing one fails here until it is struck off
# and the case above takes the recipe over. Recorded by kind rather than by
# file name, so that the list is not itself a reference the removal it
# describes would leave dangling.
_UNBOUNDED_REMOVAL_DEBT_KINDS: tuple[str, ...] = ()
_UNBOUNDED_REMOVAL_DEBT = tuple(_recipe_file(k) for k in _UNBOUNDED_REMOVAL_DEBT_KINDS)


@pytest.mark.parametrize(
    "recipe", sorted(set(routed_recipes()) - set(_UNBOUNDED_REMOVAL_DEBT))
)
def test_removing_a_kind_routed_today_leaves_no_reference(
    recipe: str, tmp_path: Path, inherited_failures: frozenset[str]
) -> None:
    """deleting-a-kind-leaves-no-reference, for the kinds that exist today.

    The kind is not one this case invented: it is removed where it stands, in
    a copy of the whole repository, once per recipe file the routing table
    names -- which covers the recipe two rows share as well as the recipes one
    row each names. Afterwards nothing outside the change records still writes
    either deleted name, and the removal breaks no check that was passing
    before it -- which is not the same as the copy being green: a copy carries
    every failure the working tree has, and one of them is another recipe's
    business, not this removal's.
    """
    kinds = routed_recipes()[recipe]
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    own_test = _remove_routed_kind_from_copy(root, recipe, kinds)

    names = _deleted_names(recipe, own_test)
    hits = _references_to(root, names, expected=len(copied) - len(names))
    # `docs/loom/` records where a rule lived at a commit already made; they
    # are the one tree a removal is not expected to rewrite.
    assert [h for h in hits if not h.startswith(_DEBT_SCAN_SKIP)] == [], hits

    run = _run_adversary_tests(root)
    broke = caused_by_the_edit(run, inherited_failures)
    assert not broke, (sorted(broke), sorted(inherited_failures), run.stdout + run.stderr)
    assert _passed(run) > 0, run.stdout + run.stderr


@pytest.mark.parametrize("kind", unrouted_types())
def test_adding_a_kind_that_has_no_recipe_today_introduces_no_failure(
    kind: str, tmp_path: Path, inherited_failures: frozenset[str]
) -> None:
    """add-kind-one-file-one-row and existing-recipe-file-untouched, performed
    for real and then undone.

    `test_adding_a_kind_is_one_file_and_one_row` counts what the addition
    touches; this one asks what the addition broke. The addition is made in a
    copy of the whole repository, for every artifact type the table leaves
    unrouted rather than for one that happens not to collide with anything,
    and the checks that read these documents are run on the result. Then the
    kind is taken away again by the removal the protocol describes, which must
    come out as clean for a kind that never had a test module of its own as
    for one that did.

    What is asserted after each run is the difference against
    `inherited_failures`, not that the copy is green. The claim is that giving
    an artifact type a recipe introduces no new failure, which is a statement
    about before and after; a copy is a copy of the working tree, so a green
    copy is a statement about the whole suite instead, and one reworded
    sentence in one recipe -- another recipe's business entirely -- would fail
    this case once per unrouted kind. An addition whose recipe file is
    missing, whose row points elsewhere, or that edits a recipe already there
    still fails: each of those turns a check red that the untouched copy was
    passing, so the difference is not empty.
    """
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    recipe = _recipe_file(kind)
    _add_kind(root / str(REFERENCES.relative_to(ROOT)), kind, recipe, added_recipe(kind))

    added = _run_adversary_tests(root)
    broke = caused_by_the_edit(added, inherited_failures)
    assert not broke, (sorted(broke), sorted(inherited_failures), added.stdout + added.stderr)
    assert _passed(added) > 0, added.stdout + added.stderr

    own_test = _remove_routed_kind_from_copy(root, recipe, (kind,))
    assert own_test is None, own_test
    names = _deleted_names(recipe, own_test)
    hits = _references_to(root, names, expected=len(copied))
    assert [h for h in hits if not h.startswith(_DEBT_SCAN_SKIP)] == [], hits

    removed = _run_adversary_tests(root)
    broke_again = caused_by_the_edit(removed, inherited_failures)
    assert not broke_again, (
        sorted(broke_again), sorted(inherited_failures), removed.stdout + removed.stderr
    )


def test_a_reworded_recipe_is_not_blamed_on_the_addition(
    tmp_path: Path, inherited_failures: frozenset[str]
) -> None:
    """The contamination this module used to have, kept out.

    One sentence of one recipe is reworded in a copy -- the edit that belongs
    to that recipe's own test file and to no other -- and the addition is then
    performed in the same copy. What is asserted is that the reword really did
    redden something, that what it reddened is the reworded recipe's own test
    file, and that the run after the addition names no failure the run before
    it did not. Held against a copy the reword has already contaminated, which
    is what an addition case reading only the exit status could not survive:
    it would fail here, and once per unrouted kind, for an edit that was not
    its subject.

    The recipe reworded is selected, not assumed. This case's premise is that
    a fresh edit can still plant a failure, and that is false of a recipe
    whose own test module the working tree is already failing -- the state a
    branch is in between editing a recipe and updating its test file. So the
    reword goes to a recipe whose module is green, trying them in routing-table
    order until one plants something; a tree where every recipe's module is
    already red is stated as the reason this case is not measuring, rather
    than passing silently or failing for an edit that was not its subject.
    """
    candidates = _reword_candidates(inherited_failures)
    if not candidates:
        pytest.skip(
            "no routed recipe has a test module of its own that is green in "
            "this tree, so no reword here can plant a failure to measure; "
            "already failing: "
            + ", ".join(sorted(_failing_modules(inherited_failures)))
        )

    # One copy per candidate, and no more: the loop stops at the first reword
    # that planted something, so the ordinary tree costs exactly one.
    attempts: dict[str, frozenset[str]] = {}
    runs: dict[str, subprocess.CompletedProcess[str]] = {}
    sentences: dict[str, str] = {}
    for candidate in candidates:
        root = tmp_path / f"repo-{recipe_kind(candidate)}"
        _copy_repository(root)
        sentences[candidate] = _reword_a_recipe_in(root, candidate)
        runs[candidate] = _run_adversary_tests(root)
        # What the reword did, and not what the working tree was already
        # failing: this case is itself one of the cases that must survive a
        # contaminated copy, so it subtracts the same inherited set the others
        # do.
        attempts[candidate] = caused_by_the_edit(runs[candidate], inherited_failures)
        if attempts[candidate]:
            break

    # The addition is performed in the copy the planting reword was made in,
    # named rather than inherited from the loop variable.
    recipe, planted = _first_planting(attempts)
    root = tmp_path / f"repo-{recipe_kind(recipe)}"
    run_before = runs[recipe]
    before = failures(run_before)
    own_test = recipe_test_module(recipe)
    assert _failing_modules(planted) == {own_test}, (sentences[recipe], sorted(planted))

    kind = unrouted_types()[0]
    added_file = _recipe_file(kind)
    _add_kind(root / str(REFERENCES.relative_to(ROOT)), kind, added_file, added_recipe(kind))

    after = _run_adversary_tests(root)
    broke = caused_by_the_edit(after, before)
    assert not broke, (sorted(broke), after.stdout + after.stderr)
    assert _passed(after) > 0, after.stdout + after.stderr


@pytest.mark.parametrize("recipe", sorted(_UNBOUNDED_REMOVAL_DEBT))
def test_recorded_unbounded_removal_is_still_unbounded(
    recipe: str, tmp_path: Path, inherited_failures: frozenset[str]
) -> None:
    """Every recorded debt is real, so the list may only shrink.

    The same removal is performed, and this time what is asserted is that it
    does not come out clean: either a live file still writes a deleted name,
    or the removal itself broke a check that was passing before it. Measured
    as the difference against `inherited_failures` for the same reason the
    case above is: a failure the copy already carried would otherwise stand in
    for the debt and keep an entry alive that is no longer real. The day the
    removal comes out clean this case fails, the entry comes off the list, and
    the case above takes the recipe over.
    """
    assert recipe in routed_recipes(), recipe
    kinds = routed_recipes()[recipe]
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    own_test = _remove_routed_kind_from_copy(root, recipe, kinds)

    names = _deleted_names(recipe, own_test)
    hits = [
        h for h in _references_to(root, names, expected=len(copied) - len(names))
        if not h.startswith(_DEBT_SCAN_SKIP)
    ]
    run = _run_adversary_tests(root)
    broke = caused_by_the_edit(run, inherited_failures)
    assert hits or broke, (hits, sorted(inherited_failures), run.stdout + run.stderr)


# --- A5 boundary: no file hand-lists a routed recipe ------------------------

def test_no_new_file_hand_lists_a_routed_recipe() -> None:
    """Nothing outside the three allowed places writes a routed recipe's name.

    A file that writes one would be left dangling by that kind's removal. The
    reference folder holds the routing table itself, a recipe's own test file
    is deleted with the recipe, and `docs/loom/` records where a rule lived at
    a commit already made. Everything else is debt: the list may only shrink,
    so an entry that stopped hand-listing fails here as loudly as a file that
    started.
    """
    rows = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    routed = {kind: target for kind, target in rows.items() if target != NO_RECIPE}
    assert routed, "the routing table names no recipe file"

    hand_listing: set[str] = set()
    tracked = _tracked_files()
    for kind, recipe in routed.items():
        own = _own_test_file(recipe[len(RECIPE_STEM):-len(".md")])
        for rel in tracked:
            if rel.startswith(f"{REFERENCES.relative_to(ROOT)}/") or rel == own:
                continue
            if any(rel.startswith(prefix) for prefix in _DEBT_SCAN_SKIP):
                continue
            path = ROOT / rel
            if not path.is_file():
                continue
            try:
                if recipe in path.read_text(encoding="utf-8"):
                    hand_listing.add(rel)
            except (UnicodeDecodeError, OSError):
                continue
    assert hand_listing == set(_BOUNDED_REMOVAL_DEBT), {
        "new": sorted(hand_listing - set(_BOUNDED_REMOVAL_DEBT)),
        "cleared": sorted(set(_BOUNDED_REMOVAL_DEBT) - hand_listing),
    }
