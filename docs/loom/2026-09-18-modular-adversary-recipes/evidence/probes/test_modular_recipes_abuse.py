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
  the protocol plus one row -- is performed and the adversary checks are run
  on the result;
* locate (A10): a rule for one artifact kind is planted in the shared
  protocol in the plainest wording a writer would reach for, and the checks
  are run on the result;
* change (A3): one recipe's wording is edited, and what turns red is
  counted per module;
* boundary: a recipe file emptied of everything the shape requires.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


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
    NO_RECIPE,
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


def _unrouted_kind() -> str:
    """A kind the routing table says has no recipe today."""
    rows = _routing_rows((REFERENCES / PROTOCOL_NAME).read_text(encoding="utf-8"))
    unrouted = sorted(kind for kind, target in rows.items() if target == NO_RECIPE)
    assert unrouted, "every artifact type is routed; this probe has no kind to add"
    return unrouted[0]


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
    """Self-test: the kinds come from the routing table, and the two sets are
    disjoint, so no case invents a name of its own."""
    rows = _routing_rows((REFERENCES / PROTOCOL_NAME).read_text(encoding="utf-8"))
    assert rows[_unrouted_kind()] == NO_RECIPE
    assert rows[_routed_kind()] != NO_RECIPE


# --- add (A4): one new file plus one row, as the routing table describes -----

def test_adding_a_kind_file_and_row_only_keeps_the_checks_green(tmp_path) -> None:
    """A reader follows the routing table exactly: one new recipe file beside
    the protocol, one row pointed at it, nothing else touched.

    `adversarial.md` states that giving a type a recipe is one new file beside
    it plus its own row, Acceptance 4 states that the addition is one file and
    one routing entry that a reader can do once without guessing, and
    `AGENTS.md` states the same as the `add` criterion a modular split is
    judged by. This case performs exactly that addition in a copy of the
    repository and runs the adversary checks on the result.
    """
    kind = _unrouted_kind()
    root = tmp_path / "repo"
    _copy_repository(root)
    recipe = f"adversarial-{kind}.md"
    _add_kind(
        _references_in(root),
        kind,
        recipe,
        RECIPE_BODY.format(kind=kind, heading=kind.capitalize(), protocol=PROTOCOL_NAME),
    )

    run = _run_adversary_tests(root)
    assert run.returncode == 0, (
        "FINDING add-takes-a-second-file (A4, AGENTS `add`): the addition the "
        "routing table and the conventions describe -- one new recipe file plus "
        "one routing row -- leaves the checks red. A reader who follows the "
        f"routing table must also guess that {kind} needs its own test module "
        "carrying a named function, which no document says. Red modules: "
        f"{sorted(_failed_modules(run.stdout))}\n{run.stdout[-1500:]}"
    )


# --- locate (A10): a one-kind rule planted in the shared protocol ------------

def test_protocol_rule_for_one_kind_in_plain_prose_is_rejected(tmp_path) -> None:
    """The shared protocol grows a rule that belongs to a single kind.

    Acceptance 10 requires that the shared protocol hold no rule of its own
    for one kind, and the `locate` criterion says a rule belonging to one
    capability lives in that capability's file. The rule planted here names
    its kind the way a writer naturally would, in plain prose rather than in
    the backticks the routing table uses for an artifact type.
    """
    kind = _routed_kind()
    sentence = f"For a {kind} artifact, run every attempt a second time before recording it."

    folder = _copy_references(tmp_path)
    protocol = folder / PROTOCOL_NAME
    protocol.write_text(protocol.read_text(encoding="utf-8") + f"\n{sentence}\n", encoding="utf-8")
    violations = shape_violations(folder)

    root = tmp_path / "repo"
    _copy_repository(root)
    in_repo = _references_in(root) / PROTOCOL_NAME
    in_repo.write_text(in_repo.read_text(encoding="utf-8") + f"\n{sentence}\n", encoding="utf-8")
    run = _run_adversary_tests(root)

    assert violations or run.returncode != 0, (
        "FINDING plain-prose-kind-rule-accepted (A10, AGENTS `locate`): the "
        f"shared protocol states a rule for the {kind} kind alone and every "
        "check passes. The part of the shape that keeps a kind's rules out of "
        "the protocol only sees the kind named in backticks, so the wording a "
        f"writer reaches for first goes through: {sentence!r}"
    )


# --- change (A3): editing one recipe reddens that recipe's module alone ------

def test_editing_one_recipe_reddens_only_its_own_module(tmp_path) -> None:
    """One recipe's wording is changed; what goes red is counted per module.

    Acceptance 3 says the other recipe files and their tests are untouched and
    still pass. The edit is a plain rewording of the kind's rule, which that
    recipe's own test module pins.
    """
    recipe_name = sorted(routed_recipes())[0]
    own_module = f"test_adversary_recipe_{recipe_name[len('adversarial-'):-len('.md')].replace('-', '_')}.py"

    root = tmp_path / "repo"
    _copy_repository(root)
    recipe = _references_in(root) / recipe_name
    text = recipe.read_text(encoding="utf-8")
    heading, body = text.split("\n## ", 1)
    title, rest = body.split("\n", 1)
    recipe.write_text(
        f"{heading}\n## {title}\n\nGo at the artifact until some promise of it stops holding.\n",
        encoding="utf-8",
    )

    run = _run_adversary_tests(root)
    assert run.returncode != 0, (
        f"FINDING unpinned-recipe: {recipe_name} was reworded from end to end and "
        "nothing went red; its rules are pinned nowhere."
    )
    stray = _failed_modules(run.stdout) - {own_module}
    assert not stray, (
        "FINDING edit-not-confined (A3, AGENTS `change`): editing "
        f"{recipe_name} turned modules other than its own red: {sorted(stray)}"
        f"\n{run.stdout[-1500:]}"
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
