"""The routing table sends each artifact type to the recipe that attacks it.

Acceptance 4, 5 and 7 of
`docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

The six cases this module makes, in the words of the plan:

- add-kind-one-file-one-row (A4 positive): giving a kind a recipe it lacks
  today is one new file beside the protocol plus one row of the routing
  table, and nothing else in the folder changes;
- existing-recipe-file-untouched (A4 negative): that same addition leaves
  every recipe file that already existed byte-identical;
- protocol-plus-kind-is-complete (A7 positive): the adversary contract names
  the protocol, the protocol's row names the recipe, the recipe points back
  at the protocol, and that pair needs no third file;
- unrouted-kind-detected (A7 negative): every artifact type of the
  repository's own vocabulary has a row, a type with no recipe says so in
  its own row rather than being absent, and a row naming a file that is not
  there is caught;
- deleting-a-kind-leaves-no-reference (A5 positive): removing a kind is
  deleting its recipe file and its own test file and putting its routing row
  back to `none`; afterwards no file in the repository names either deleted
  file, the tree is byte-for-byte what it was before the kind existed, and
  the adversary test files still pass;
- stale-reference-detected (A5 negative): a removal that leaves the recipe's
  own test file behind, one that leaves the routing row pointing at the
  deleted file, and one that leaves the deleted name in a live file are each
  caught, and the scan that catches them fails loudly rather than reporting
  nothing when it can see nothing.

The addition in the first two cases is performed on a copy of the reference
folder in a temporary directory, so the assertion is made on the result of
a real edit rather than on a sentence promising the edit would be small.

The removal cases go wider: they copy every tracked file of the repository
into a temporary directory, add a kind there, remove it again, scan every
copied file for the deleted names, and run the adversary test files inside
that copy. Nothing is asserted about wording; every assertion is made on the
result of an edit that was really performed.

The kind removed is one the routing table lists as having no recipe today,
so the round trip ends where it started and the deleted names belong to no
other file in the repository. Removing one of the three kinds routed today
is not yet this bounded: `_BOUNDED_REMOVAL_DEBT` records the files that
still hand-list a routed recipe by name, and the debt list may only shrink.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

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
SUITE_EXTRA = ("test_build_mechanical_checks.py", "test_review_convergence_contract.py")

# Files that still hand-list a recipe file routed today, so removing one of
# today's three kinds would leave their reference dangling. Every entry is a
# debt recorded when this check went in, not a permission: the list may only
# shrink, and `test_no_new_file_hand_lists_a_routed_recipe` fails on an entry
# that stopped violating as loudly as on a file that started.
_BOUNDED_REMOVAL_DEBT = (
    f"{SCRIPTS}/test_adversary_layout.py",
    f"{SCRIPTS}/test_adversary_recipe_code.py",
    f"{SCRIPTS}/test_build_mechanical_checks.py",
)
# The one tree the debt scan passes over by path: the change records, which
# state where a rule lived at a commit already made and cannot stop being
# true. The other two exclusions the debt scan makes are named where it makes
# them -- the reference folder, whose routing row the removal rewrites, and
# the kind's own test file, which the removal deletes with the recipe.
_DEBT_SCAN_SKIP = ("docs/loom/",)

# The removal cases below each copy the repository and run pytest inside the
# copy. The copy's own run must not start that again, so these are deselected
# there by name; a name that no longer exists makes pytest exit non-zero.
REMOVAL_TESTS = (
    "test_removing_a_kind_restores_the_tree_and_leaves_no_reference",
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
    """The test file Acceptance 6 gives that kind's recipe."""
    return f"{SCRIPTS}/{RECIPE_TEST_STEM}{kind.replace('-', '_')}.py"


def _recipe_file(kind: str) -> str:
    return f"{RECIPE_STEM}{kind}.md"


def _removable_kind() -> str:
    """A kind the routing table says has no recipe, chosen deterministically.

    The round trip adds a recipe for it and removes it again, so the tree it
    must return to is the tree as it stands, and the names it deletes belong
    to no other file in the repository.
    """
    rows = _routing_rows(PROTOCOL.read_text(encoding="utf-8"))
    unrouted = sorted(k for k, target in rows.items() if target == NO_RECIPE)
    assert unrouted, "every kind is routed; this check has no kind to add and remove"
    return unrouted[0]


def _add_kind_to_copy(root: Path, kind: str) -> tuple[str, str]:
    """Give `kind` a recipe in the copy: the file, its own test file, its row."""
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
        'RECIPE = Path(__file__).resolve().parents[2] / (\n'
        f'    "loom-code/skills/closing-review/references/{recipe}"\n'
        ")\n\n\n"
        "def test_recipe_states_its_own_rule() -> None:\n"
        f'    assert "Attack the {kind} artifact" in RECIPE.read_text(encoding="utf-8")\n'
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
    from the run and one the addition wrote is in it. The removal cases
    themselves are deselected by name: they would copy the copy. pytest exits
    non-zero on a name that no longer matches a test, so a renamed case is
    caught rather than quietly stopping to run.
    """
    scripts = root / SCRIPTS
    targets = sorted(str(p.relative_to(root)) for p in scripts.glob(SUITE_GLOB))
    targets += [f"{SCRIPTS}/{name}" for name in SUITE_EXTRA]
    for target in targets:
        assert (root / target).is_file(), target
    deselect: list[str] = []
    for name in REMOVAL_TESTS:
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
        ["python3", "-m", "pytest", "-q", "-p", "no:cacheprovider", *targets, *deselect],
        cwd=root, capture_output=True, text=True, env=env,
    )


def _passed(run: subprocess.CompletedProcess[str]) -> int:
    """How many tests the run reported passing, or none if it did not say.

    A run that says nothing about passing is not treated as a run of zero
    tests; the caller asserts on this number and gets the output in the
    failure.
    """
    match = re.search(r"(\d+) passed", run.stdout + run.stderr)
    return int(match.group(1)) if match else 0


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


def test_passed_helper_synthetic() -> None:
    ok = subprocess.CompletedProcess([], 0, "12 passed in 0.5s", "")
    assert _passed(ok) == 12
    assert _passed(subprocess.CompletedProcess([], 1, "2 failed, 3 passed", "")) == 3
    assert _passed(subprocess.CompletedProcess([], 2, "Interrupted: 2 errors", "")) == 0


# --- A5 positive: the removal leaves nothing behind ------------------------

def test_removing_a_kind_restores_the_tree_and_leaves_no_reference(tmp_path: Path) -> None:
    """deleting-a-kind-leaves-no-reference.

    The kind is added and removed again in a copy of the whole repository, so
    what the removal must restore is known byte for byte.
    """
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    before = {rel: (root / rel).read_bytes() for rel in copied}

    kind = _removable_kind()
    recipe, own_test = _add_kind_to_copy(root, kind)
    added = _run_adversary_tests(root)
    assert added.returncode == 0, added.stdout + added.stderr
    assert _passed(added) > 0, added.stdout + added.stderr

    _remove_kind_from_copy(root, kind)

    names = (recipe, Path(own_test).name)
    assert _references_to(root, names, expected=len(copied)) == []
    assert _files_in(root) == sorted(copied)
    after = {rel: (root / rel).read_bytes() for rel in copied}
    assert [rel for rel in copied if before[rel] != after[rel]] == []

    removed = _run_adversary_tests(root)
    assert removed.returncode == 0, removed.stdout + removed.stderr
    assert _passed(removed) > 0, removed.stdout + removed.stderr


# --- A5 negative: a removal done wrong is caught ---------------------------

def test_removal_that_leaves_the_kinds_own_test_file_behind_is_detected(tmp_path: Path) -> None:
    """stale-reference-detected: the recipe is gone, its test still names it."""
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    kind = _removable_kind()
    recipe, own_test = _add_kind_to_copy(root, kind)
    _remove_kind_from_copy(root, kind, drop_own_test=False)

    names = (recipe, Path(own_test).name)
    assert _references_to(root, names, expected=len(copied)) == [own_test]
    run = _run_adversary_tests(root)
    assert run.returncode != 0, run.stdout + run.stderr


def test_removal_that_leaves_the_routing_row_behind_is_detected(tmp_path: Path) -> None:
    """stale-reference-detected: both files are gone, the row still names one."""
    root = tmp_path / "repo"
    copied = _copy_repository(root)
    kind = _removable_kind()
    recipe, own_test = _add_kind_to_copy(root, kind)
    _remove_kind_from_copy(root, kind, restore_row=False)

    names = (recipe, Path(own_test).name)
    protocol = f"{REFERENCES.relative_to(ROOT)}/adversarial.md"
    assert _references_to(root, names, expected=len(copied)) == [protocol]
    run = _run_adversary_tests(root)
    assert run.returncode != 0, run.stdout + run.stderr


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


# --- A5 boundary: today's routed recipes are still hand-listed elsewhere ----

def test_no_new_file_hand_lists_a_routed_recipe() -> None:
    """Removing a kind routed today is not yet this bounded.

    A file that writes a routed recipe's name would be left dangling by that
    kind's removal. The reference folder holds the routing table itself, a
    recipe's own test file is deleted with the recipe, and `docs/loom/`
    records where a rule lived at a commit already made. Everything else is
    debt: the list may only shrink, so an entry that stopped hand-listing
    fails here as loudly as a file that started.
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
