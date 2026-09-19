"""The four properties a modular split is judged by, in the repository's conventions.

Acceptance 9 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

Two things are pinned here. `AGENTS.md` states each of the four properties --
change, add, remove, locate -- once, in the pin discipline the rest of these
tests use: an affirmative verb before the pinned literal, a negation in the
same sentence rejected, the helper self-tested both ways. And `loom-code/
ROADMAP.md` states that the rest of loom is brought to this shape one skill
per change, naming the worked example.

The negative case is a property with no check behind it. A property is only
worth stating if something in this repository recomputes it, so every
property the conventions state is mapped here to the executable checks that
enforce it, and a property stated with no entry -- or an entry naming a check
that is not there -- turns this file red.

The map names no adversary recipe's own test module. Those modules exist only
while the routing table routes their kind, so the checks they carry are
expanded from that table instead of written here: retiring a kind takes its
entry out of the map with it, and every property keeps a check that no kind's
existence depends on.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences
from test_adversary_routing import RECIPE_TEST_STEM, recipe_test_module, routed_recipes


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "loom-code/scripts"
CONVENTIONS = ROOT / "AGENTS.md"
ROADMAP = ROOT / "loom-code/ROADMAP.md"

CRITERIA_HEADING = "### Module Criteria"


def _section(text: str, heading: str) -> str:
    """The prose under `heading`, flattened, up to the next heading of any level."""
    after = text.split(heading, 1)[1] if heading in text else ""
    body = re.split(r"^#{1,6} ", after, maxsplit=1, flags=re.M)[0]
    return " ".join(body.split())


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _affirms(text: str, verb: str, literal: str) -> bool:
    """`text` carries `verb` before `literal`, with no negation in it."""
    v, lit = text.find(verb), text.find(literal)
    return 0 <= v < lit and not has_negation(text)


def _stated_once(text: str, verb: str, literal: str) -> bool:
    """Exactly one sentence carries `verb` before `literal` and no negation."""
    return sum(1 for s in split_sentences(text) if _affirms(s, verb, literal)) == 1


def _units(path: Path) -> list[str]:
    """The file's bullets and paragraphs, each flattened.

    The roadmap's bullets carry no closing period, so sentence splitting
    would sweep several of them into one span and a negation in a
    neighbouring bullet would reject a pin that is not about it.
    """
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n|\n(?=- )", text)
    return [" ".join(b.split()) for b in blocks if b.strip()]


def _named_properties(section: str) -> list[str]:
    """The property names the section states, in the order it states them."""
    return re.findall(r"- \*\*([a-z]+)\*\* —", section)


# --- What each property says, and what recomputes it ------------------------
#
# name: (verb, literal, affirmative example, rejected examples)
PROPERTY_PINS = {
    "change": (
        "Editing one capability touches",
        "that capability's file and its own test",
        "- **change** — Editing one capability touches that capability's file and its own "
        "test, and nothing else.",
        ("- **change** — Editing one capability touches that capability's file and its own "
         "test, but not only those.",
         "- **change** — Editing one capability touches whatever the edit reaches."),
    ),
    "add": (
        "Adding a capability is",
        "a new file plus one routing entry",
        "- **add** — Adding a capability is a new file plus one routing entry, and every "
        "existing capability file stays untouched.",
        ("- **add** — Adding a capability is a new file plus one routing entry, and no "
         "existing capability file stays untouched.",
         "- **add** — Adding a capability is an edit to the shared file."),
    ),
    "remove": (
        "Removing a capability deletes",
        "its file and its routing entry",
        "- **remove** — Removing a capability deletes its file and its routing entry, and "
        "leaves nothing behind that still names it.",
        ("- **remove** — Removing a capability deletes its file and its routing entry, but "
         "not what still names it.",
         "- **remove** — Removing a capability deletes the passages that belong to it."),
    ),
    "locate": (
        "A rule that belongs to one capability lives in",
        "that capability's file",
        "- **locate** — A rule that belongs to one capability lives in that capability's "
        "file, while the shared part carries only what every capability shares and a "
        "sibling file carries only its own.",
        ("- **locate** — A rule that belongs to one capability lives in that capability's "
         "file, not in the shared part.",
         "- **locate** — A rule that belongs to one capability lives wherever it was "
         "written."),
    ),
}

# name: the checks in this repository that recompute the property.
# path -> the test functions in it that do the recomputing.
#
# No recipe's own test module is named here. A recipe exists only while the
# routing table routes its kind, so a name written here would be left
# dangling by that kind's retirement and would take a stated property's only
# check with it. What every routed recipe's own test module must carry is
# `RECIPE_ENFORCED_BY` below, which the routing table expands; every property
# keeps at least one check here, which no kind's existence depends on.
ENFORCED_BY = {
    "change": {
        "test_adversary_routing.py": ("test_no_new_file_hand_lists_a_routed_recipe",),
    },
    "add": {
        "test_adversary_routing.py": (
            "test_adding_a_kind_is_one_file_and_one_row",
            "test_adding_a_kind_leaves_every_existing_recipe_file_untouched",
        ),
    },
    "remove": {
        "test_adversary_routing.py": (
            "test_removing_a_kind_restores_the_tree_and_leaves_no_reference",
            "test_removal_that_leaves_the_name_in_a_live_file_is_detected",
        ),
    },
    "locate": {
        "test_adversary_layout.py": (
            "test_each_kind_section_lives_in_its_own_file",
            "test_no_kind_rule_appears_outside_its_own_file",
        ),
        "test_adversary_protocol.py": ("test_procedure_sentence_in_both_files_rejected",),
    },
}

# name: the test functions every routed recipe's own test module carries for
# the property. Expanded against the routing table, so the check that keeps a
# rule in one file is required of each recipe that exists and of no recipe
# that does not.
RECIPE_ENFORCED_BY = {
    "change": ("test_procedure_sentence_in_both_files_rejected",),
}


def enforced_by(prop: str) -> dict[str, tuple[str, ...]]:
    """Every check that recomputes `prop`: those named above, plus the
    per-recipe check in each routed recipe's own test module."""
    checks = dict(ENFORCED_BY[prop])
    functions = RECIPE_ENFORCED_BY.get(prop, ())
    if functions:
        for recipe in routed_recipes():
            module = recipe_test_module(recipe)
            assert module not in checks, module
            checks[module] = functions
    return checks

ROADMAP_PIN = (
    "The rest of loom is brought to this shape",
    "one skill per change",
)
ROADMAP_REJECTED = (
    "- The rest of loom is brought to this shape, but not one skill per change.",
    "- The rest of loom is brought to this shape when someone gets to it.",
)


# --- helper self-tests -------------------------------------------------------

def test_section_helper_synthetic() -> None:
    text = "# Top\n\n### Module Criteria\n\n- **change** — One file.\n\n### Next\n\n- other\n"
    assert _section(text, CRITERIA_HEADING) == "- **change** — One file."
    assert "other" not in _section(text, CRITERIA_HEADING)
    assert _section(text, "### Missing") == ""


def test_named_properties_helper_synthetic() -> None:
    assert _named_properties("- **change** — a. - **locate** — b.") == ["change", "locate"]
    assert _named_properties("- change — a.") == []


def test_stated_once_helper_synthetic() -> None:
    sentence = "Editing one capability touches that capability's file and its own test."
    assert _stated_once(f"Read this. {sentence}", "Editing one capability touches",
                        "that capability's file and its own test")
    assert not _stated_once(f"{sentence} {sentence}", "Editing one capability touches",
                            "that capability's file and its own test")
    assert not _stated_once("Nothing here.", "Editing one capability touches",
                            "that capability's file and its own test")


@pytest.mark.parametrize("prop", sorted(PROPERTY_PINS))
def test_property_pin_helpers_synthetic(prop: str) -> None:
    verb, literal, affirmative, rejected = PROPERTY_PINS[prop]
    assert _stated_once(affirmative, verb, literal), prop
    assert any(has_negation(r) for r in rejected), prop
    for example in rejected:
        assert not _stated_once(example, verb, literal), example


# --- A9 positive: the four properties are stated once, in the conventions ---

@pytest.mark.parametrize("prop", sorted(PROPERTY_PINS))
def test_conventions_state_the_property_once(prop: str) -> None:
    verb, literal, _affirmative, _rejected = PROPERTY_PINS[prop]
    section = _section(CONVENTIONS.read_text(encoding="utf-8"), CRITERIA_HEADING)
    assert _stated_once(section, verb, literal), (prop, verb, literal)


def test_conventions_name_the_four_properties_and_no_others() -> None:
    section = _section(CONVENTIONS.read_text(encoding="utf-8"), CRITERIA_HEADING)
    assert _named_properties(section) == ["change", "add", "remove", "locate"]


def test_roadmap_pin_helpers_synthetic(tmp_path: Path) -> None:
    verb, literal = ROADMAP_PIN
    path = tmp_path / "ROADMAP.md"
    path.write_text(
        "# roadmap\n\n- Something that does not rise\n- The rest of loom is brought to this "
        "shape one skill per change, with the split as the worked example.\n",
        encoding="utf-8",
    )
    assert [u for u in _units(path) if _affirms(u, verb, literal)] == [
        "- The rest of loom is brought to this shape one skill per change, with the split as "
        "the worked example."
    ]
    for example in ROADMAP_REJECTED:
        assert not _affirms(example, verb, literal), example
    assert any(has_negation(r) for r in ROADMAP_REJECTED)


def test_roadmap_records_one_skill_per_change_with_the_worked_example() -> None:
    verb, literal = ROADMAP_PIN
    matches = [u for u in _units(ROADMAP) if _affirms(u, verb, literal)]
    assert len(matches) == 1, _flat(ROADMAP)
    assert "worked example" in matches[0], matches[0]
    assert "loom-code/skills/closing-review/references/" in matches[0], matches[0]


# --- A9 negative: a property stated with no check behind it ------------------

def test_every_property_the_conventions_state_has_an_entry() -> None:
    section = _section(CONVENTIONS.read_text(encoding="utf-8"), CRITERIA_HEADING)
    stated = set(_named_properties(section))
    assert stated, section
    assert stated - set(ENFORCED_BY) == set(), stated - set(ENFORCED_BY)
    assert set(ENFORCED_BY) - stated == set(), set(ENFORCED_BY) - stated


@pytest.mark.parametrize("prop", sorted(ENFORCED_BY))
def test_each_property_is_enforced_by_a_check_that_exists(prop: str) -> None:
    checks = enforced_by(prop)
    assert checks, prop
    for filename, functions in checks.items():
        path = SCRIPTS / filename
        assert path.exists(), (prop, filename)
        text = path.read_text(encoding="utf-8")
        for function in functions:
            assert f"def {function}(" in text, (prop, filename, function)


@pytest.mark.parametrize("prop", sorted(ENFORCED_BY))
def test_no_property_depends_on_one_kind_existing(prop: str) -> None:
    """A property keeps a check that no recipe's existence carries.

    The per-recipe checks go away with their kind, so a property whose only
    entry were one of those would be left stated with nothing recomputing it
    the day that kind retired.
    """
    assert ENFORCED_BY[prop], prop
    named = [f for f in ENFORCED_BY[prop] if f.startswith(RECIPE_TEST_STEM)]
    assert named == [], (prop, named)


def test_per_recipe_checks_cover_every_routed_recipe() -> None:
    """Each routed recipe's own test module is required to carry the check,
    and no module that is not one of them is added by the expansion."""
    recipes = routed_recipes()
    assert recipes, "the routing table names no recipe file"
    for prop, functions in RECIPE_ENFORCED_BY.items():
        expanded = enforced_by(prop)
        for recipe in recipes:
            assert expanded.get(recipe_test_module(recipe)) == functions, (prop, recipe)
        assert set(expanded) - set(ENFORCED_BY[prop]) == {
            recipe_test_module(r) for r in recipes
        }, prop


def test_enforcement_lookup_catches_a_check_that_is_not_there() -> None:
    """The same lookup, run against a property whose check does not exist."""
    missing = SCRIPTS / "test_adversary_recipe_no_such_kind.py"
    assert not missing.exists()
    text = (SCRIPTS / "test_adversary_routing.py").read_text(encoding="utf-8")
    assert "def test_a_rule_nothing_recomputes(" not in text
