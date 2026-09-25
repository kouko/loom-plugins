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

A map can also be wrong while every name in it resolves, which is the harder
negative: a property pointed at a check written for a different property is
as unenforced as a property pointed at nothing. So each entry is read back
against the section header the named check sits under in its own module,
which carries the Acceptance number that check was written for.

The map names no adversary recipe's own test module, and requires none. Such
a module exists only while the routing table routes its kind, so a name
written here would be left dangling by that kind's retirement; and requiring
one of a routed recipe would make giving a kind a recipe two files rather
than the one file and one row the routing table, `AGENTS.md`'s `add`
criterion and Acceptance 4 all describe. Every property is therefore mapped
to checks that no kind's existence depends on.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences
from test_adversary_routing import RECIPE_TEST_STEM


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "loom-code/tests"
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
        "test, where it has one, and nothing else.",
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
        "its file, its routing entry and its own test where it has one",
        "- **remove** — Removing a capability deletes its file, its routing entry and its "
        "own test where it has one, and leaves nothing behind that still names it.",
        ("- **remove** — Removing a capability deletes its file, its routing entry and its "
         "own test where it has one, but not what still names it.",
         "- **remove** — Removing a capability deletes its file and its routing entry, and "
         "leaves nothing behind that still names it.",
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
# No recipe's own test module is named here, and none is required of a routed
# recipe. A recipe exists only while the routing table routes its kind, so a
# name written here would be left dangling by that kind's retirement and would
# take a stated property's only check with it; and a per-recipe module
# required of every routed kind would make giving a kind a recipe two files
# instead of one file and one row. Every check named here is one no kind's
# existence depends on.
ENFORCED_BY = {
    "change": {
        "test_adversary_routing.py": ("test_a_reworded_recipe_is_not_blamed_on_the_addition",),
    },
    "add": {
        "test_adversary_routing.py": (
            "test_adding_a_kind_is_one_file_and_one_row",
            "test_adding_a_kind_leaves_every_existing_recipe_file_untouched",
        ),
    },
    "remove": {
        "test_adversary_routing.py": (
            "test_removing_a_kind_routed_today_leaves_no_reference",
            "test_removal_that_leaves_the_name_in_a_live_file_is_detected",
            "test_no_new_file_hand_lists_a_routed_recipe",
        ),
    },
    "locate": {
        "test_adversary_layout.py": (
            "test_each_kind_section_lives_in_its_own_file",
            "test_no_kind_rule_appears_outside_its_own_file",
        ),
    },
}

# The trade `add` and `change` make together, which used to be recorded only
# in two test modules' docstrings: `add` is one file plus one routing entry,
# so a capability may exist with no test module of its own, and `change` has
# to be read that way too. A reader of the conventions opens neither module,
# so the conventions state it themselves.
OPTIONAL_TEST_PIN = ("A capability's own test module is", "optional")
OPTIONAL_TEST_AFFIRMATIVE = (
    "- A capability's own test module is optional: `add` stays one file plus one routing "
    "entry, and `change` reads as its own test where it has one."
)
OPTIONAL_TEST_REJECTED = (
    "- A capability's own test module is never optional: `add` stays one file plus one "
    "routing entry, and `change` reads as its own test where it has one.",
    "- A capability's own test module is written by whoever gave it a routing entry.",
)

# Which Acceptance line of the intent each criterion is the repository's
# wording of. The checks are grouped in their own modules under section
# headers that name that line, so a criterion registered to a check written
# for a different one is caught by reading the check's own section rather
# than by trusting this map.
CRITERION_ACCEPTANCE = {"change": 3, "add": 4, "remove": 5, "locate": 2}

_SECTION_HEADER = re.compile(r"^# --- (?P<label>.*?)\s*-*$", re.M)
_ACCEPTANCE_LABEL = re.compile(r"^A(?P<n>\d+)\b")


def _acceptance_of(text: str, function: str) -> int | None:
    """The Acceptance number of the section `function` is defined under.

    The nearest section header above the definition, and only that one: a
    header carrying no Acceptance number -- the helper self-test blocks --
    answers `None` rather than letting the numbered section above it stand
    in for a section that does not claim a number.
    """
    definition = re.search(rf"^def {re.escape(function)}\(", text, re.M)
    assert definition is not None, function
    at = definition.start()
    labels = [m.group("label") for m in _SECTION_HEADER.finditer(text) if m.start() < at]
    if not labels:
        return None
    match = _ACCEPTANCE_LABEL.match(labels[-1])
    return int(match.group("n")) if match else None


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


def test_optional_test_module_pin_helpers_synthetic() -> None:
    verb, literal = OPTIONAL_TEST_PIN
    assert _stated_once(OPTIONAL_TEST_AFFIRMATIVE, verb, literal)
    assert any(has_negation(r) for r in OPTIONAL_TEST_REJECTED)
    for example in OPTIONAL_TEST_REJECTED:
        assert not _stated_once(example, verb, literal), example


def test_conventions_say_a_capabilitys_own_test_module_is_optional() -> None:
    """What `add` costs `change`, said where a reader of the criteria sees it."""
    verb, literal = OPTIONAL_TEST_PIN
    section = _section(CONVENTIONS.read_text(encoding="utf-8"), CRITERIA_HEADING)
    assert _stated_once(section, verb, literal), section


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
    checks = ENFORCED_BY[prop]
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

    A recipe's own test module goes away with its kind, so a property whose
    only entry were such a module would be left stated with nothing
    recomputing it the day that kind retired. Nothing here requires a routed
    recipe to have such a module either: that requirement would make giving a
    kind a recipe two files rather than one file and one row.
    """
    assert ENFORCED_BY[prop], prop
    named = [f for f in ENFORCED_BY[prop] if f.startswith(RECIPE_TEST_STEM)]
    assert named == [], (prop, named)


def test_acceptance_reader_synthetic() -> None:
    """The reader takes the nearest header, and refuses to guess past one."""
    text = (
        "# --- A4: adding ------\n\n"
        "def test_added() -> None:\n    pass\n\n\n"
        "# --- helper self-tests ------\n\n"
        "def test_helper() -> None:\n    pass\n\n\n"
        "# --- A5 boundary: removing ------\n\n"
        "def test_removed() -> None:\n    pass\n"
    )
    assert _acceptance_of(text, "test_added") == 4
    assert _acceptance_of(text, "test_helper") is None
    assert _acceptance_of(text, "test_removed") == 5
    assert _acceptance_of("def test_alone() -> None:\n    pass\n", "test_alone") is None


def test_every_criterion_has_an_acceptance_line() -> None:
    assert set(CRITERION_ACCEPTANCE) == set(ENFORCED_BY)
    assert len(set(CRITERION_ACCEPTANCE.values())) == len(CRITERION_ACCEPTANCE)


@pytest.mark.parametrize("prop", sorted(ENFORCED_BY))
def test_each_check_sits_under_the_criterion_it_enforces(prop: str) -> None:
    """A criterion's checks are the ones written for its own Acceptance line.

    The negative Acceptance 9 is really watching for: not a criterion with no
    entry at all, but a criterion whose entry names a check that recomputes
    something else. Read from the check's own module, so the map cannot say
    one thing while the check does another.
    """
    expected = CRITERION_ACCEPTANCE[prop]
    for filename, functions in ENFORCED_BY[prop].items():
        text = (SCRIPTS / filename).read_text(encoding="utf-8")
        for function in functions:
            assert _acceptance_of(text, function) == expected, (
                prop, filename, function, _acceptance_of(text, function), expected
            )


def test_enforcement_lookup_catches_a_check_that_is_not_there() -> None:
    """The same lookup, run against a property whose check does not exist."""
    missing = SCRIPTS / "test_adversary_recipe_no_such_kind.py"
    assert not missing.exists()
    text = (SCRIPTS / "test_adversary_routing.py").read_text(encoding="utf-8")
    assert "def test_a_rule_nothing_recomputes(" not in text
