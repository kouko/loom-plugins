"""One shape every attack recipe keeps, checked for all of them at once.

Acceptance 10 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

The two cases this module makes, in the words of the plan:

- every-recipe-keeps-the-shape (A10 positive): every recipe the routing
  table names keeps all five parts of the shape at once;
- recipe-missing-part-of-shape-rejected (A10 negative): a recipe edited or
  added with one part of the shape missing is rejected, and the rejection
  names the part that broke -- one case per part, each performed on a copy
  of the reference folder.

The five parts, from Acceptance 10:

- `back-pointer`: the recipe points back at the shared protocol, and every
  file it points at is there;
- `routed`: the routing table names the recipe, and every file the table
  names is there -- so a recipe file nobody routes to, and a row with no
  file, are both caught;
- `one-kind`: the recipe carries exactly one `## ` section, and no two
  recipes carry the same one, so one file never covers two kinds;
- `protocol-rule-in-recipe`: no rule the shared protocol states is stated
  again in a recipe;
- `kind-rule-in-protocol`: the protocol holds no rule belonging to a single
  kind -- neither by a kind's rules leaving the kind's own file, nor by the
  protocol addressing one routed artifact type by name, in the routing
  table's backticks or in plain prose.

What this module deliberately does not do is pin how any recipe words
anything. Each recipe's own test file pins its sentences (Acceptance 6);
a shape check that pinned prose would couple the recipes back together,
which is what this change exists to undo. Every assertion here is about a
part being present and correctly owned, and the set of recipes is read from
the routing table, never hand-listed, so a kind added or retired later is
covered without editing this file.

Three bounds worth stating, because a reader should know what this check does
not see. Duplication is a symmetric observable: a sentence living in both
the protocol and a recipe is reported as `protocol-rule-in-recipe`
whichever file it was copied from, because nothing in the tree says which
copy came first. A rule that leaves its recipe is seen when the kind's
section stops stating any rule, not when one sentence of several is moved
out; the granularity of ownership the tree itself defines is the section.

And a rule for one kind is seen in the protocol only where it names that
kind as a type: the routed name in backticks, heading a generic noun phrase
(`for a code artifact`, `of any spec`, `is a skill`), or standing as a bare
complement (`when the artifact is code`). Three ways of naming a kind go
through. A definite reference does -- `the code artifact gets two runs` --
because the protocol legitimately writes `needs the code changed to fail`
and a check that rejected the definite article could not be satisfied. A
hyphenated compound does -- `a spec-shaped probe gets two runs` -- for the
same reason, that a compound names a shape more often than the type. And a
rule that never writes the routed name at all goes through however it is
phrased, whether by synonym or by description (`anything under
loom-code/scripts/`); no check on the prose can close that one, and the
recipe-side parts of the shape are what stand behind it.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import NamedTuple

from prose_pin import split_sentences
# The routing table reader, imported rather than copied: the table is the one
# place a kind is given a recipe or has it taken away, so a second reader here
# would be a second thing to keep right. It takes the protocol's text, which
# is what lets the negative cases run it against a copy of the folder.
from test_adversary_routing import NO_RECIPE, RECIPE_STEM, _routing_rows


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
PROTOCOL_NAME = "adversarial.md"
ROUTING_HEADING = "## Which recipe to read"

# The five parts of the shape. A violation carries the part it broke, so a
# failure says which one rather than only that something is wrong.
BACK_POINTER = "back-pointer"
ROUTED = "routed"
ONE_KIND = "one-kind"
PROTOCOL_RULE_IN_RECIPE = "protocol-rule-in-recipe"
KIND_RULE_IN_PROTOCOL = "kind-rule-in-protocol"

# Below this length a sentence is too generic to be evidence of duplication:
# a shared "Three is the floor." would be a coincidence, not a copied rule.
MIN_RULE = 40

# The determiners that make a noun phrase generic: "a code artifact" is a rule
# about every artifact of that type, where "the code artifact" is one artifact
# the sentence around it already picked out. That difference is what keeps the
# protocol's own "needs the code changed to fail" readable prose rather than a
# violation, and it is grammar, not wording: no phrase any recipe or the
# protocol uses is pinned here.
_GENERIC = "a|an|any|every|each"
_COPULA = "is|are|was|were"

_LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)#][^)]*)\)")
_HEADING = re.compile(r"^#{1,6} .*$", re.M)
_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.M)


class Violation(NamedTuple):
    part: str
    file: str
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _prose(text: str) -> str:
    """The rule prose of a document: heading lines and table rows dropped.

    A heading is structure and `test_adversary_layout.py` owns it; a table
    row is a lookup, not a sentence. Left in, both would be swept into the
    sentence after them.
    """
    return _flat(_TABLE_ROW.sub("", _HEADING.sub("", text)))


def _rules(text: str) -> list[str]:
    """The sentences of `text` long enough to be a rule of their own."""
    return [s for s in split_sentences(_prose(text)) if len(s) >= MIN_RULE]


def _addressed_as_a_type(kind: str) -> re.Pattern[str]:
    """Where a sentence names `kind` as the artifact type a rule applies to.

    Three positions, all of them structural: the type name in backticks, the
    way the routing table writes it; the type name heading a generic noun
    phrase (`for a code artifact`, `of any spec`, `is a skill`); and the type
    name as a bare complement (`when the artifact is code`). A hyphen after
    the name is excluded, because `a spec-shaped probe` names a shape and not
    the type.
    """
    name = re.escape(kind)
    return re.compile(
        rf"`{name}`"
        rf"|\b(?:{_GENERIC})\s+{name}\b(?!-)"
        rf"|\b(?:{_COPULA})\s+{name}\b(?!-)",
        re.IGNORECASE,
    )


def _addressing_sentence(text: str, kind: str) -> str | None:
    """The first sentence of `text` that addresses `kind` as a type, if any."""
    pattern = _addressed_as_a_type(kind)
    for sentence in split_sentences(text):
        if pattern.search(sentence):
            return sentence
    return None


def _sections(text: str) -> dict[str, str]:
    """Map each `## ` heading to its body, heading line excluded."""
    sections: dict[str, list[str]] = {}
    heading: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            sections[heading] = []
        elif heading is not None:
            sections[heading].append(line)
    return {h: "\n".join(body) for h, body in sections.items()}


def _without_routing(text: str) -> str:
    """The protocol without its routing section, which is structure.

    The rows name the recipe files and the artifact types, so leaving the
    section in would make the protocol look as though it addressed each kind
    by name.
    """
    if ROUTING_HEADING not in text:
        return text
    head, rest = text.split(ROUTING_HEADING, 1)
    tail = rest.split("\n## ", 1)
    return head + ("\n## " + tail[1] if len(tail) > 1 else "")


def routing(folder: Path) -> dict[str, str]:
    """The routing table of the protocol in `folder`, type -> recipe file."""
    return _routing_rows(_read(folder / PROTOCOL_NAME))


def routed_kinds(folder: Path) -> dict[str, tuple[str, ...]]:
    """Recipe file -> the artifact types routed to it. Two types may share a
    recipe, which is why this is a tuple and not one name."""
    grouped: dict[str, list[str]] = {}
    for kind, target in sorted(routing(folder).items()):
        if target != NO_RECIPE:
            grouped.setdefault(target, []).append(kind)
    return {recipe: tuple(kinds) for recipe, kinds in sorted(grouped.items())}


def recipe_files(folder: Path) -> list[Path]:
    """Every recipe file present in `folder`, routed or not.

    Present rather than routed, so that a recipe file the table does not
    name is a file this check sees and reports, instead of one it cannot
    look at.
    """
    return sorted(p for p in folder.glob(f"{RECIPE_STEM}*.md") if p.is_file())


def protocol_rules(folder: Path) -> list[str]:
    """The rules the shared protocol owns: its prose bar the routing table."""
    return _rules(_without_routing(_read(folder / PROTOCOL_NAME)))


def shape_violations(folder: Path) -> list[Violation]:
    """Every part of the shape that a recipe in `folder` fails to keep.

    One pass over all recipes at once, so a recipe added or edited short of
    any part is reported here rather than in whichever file happens to read
    it. An empty list is the shape kept.
    """
    protocol = folder / PROTOCOL_NAME
    found: list[Violation] = []
    if not protocol.is_file():
        return [Violation(BACK_POINTER, PROTOCOL_NAME, "the shared protocol is not there")]

    present = {p.name: p for p in recipe_files(folder)}
    routed = routed_kinds(folder)
    for name in sorted(set(routed) - set(present)):
        found.append(Violation(ROUTED, PROTOCOL_NAME, f"a row names {name}, which is not there"))
    for name in sorted(set(present) - set(routed)):
        found.append(Violation(ROUTED, name, "no row of the routing table names this recipe"))

    owned = protocol_rules(folder)
    protocol_text = _prose(_without_routing(_read(protocol)))
    headings: dict[str, str] = {}
    for name, path in sorted(present.items()):
        text = _read(path)

        targets = {m.group("target").strip() for m in _LINK.finditer(text)}
        if PROTOCOL_NAME not in targets:
            found.append(
                Violation(BACK_POINTER, name, "it points at no shared protocol")
            )
        for target in sorted(targets):
            if not (folder / target).is_file():
                found.append(
                    Violation(BACK_POINTER, name, f"it points at {target}, which is not there")
                )

        sections = _sections(text)
        if len(sections) != 1:
            found.append(
                Violation(ONE_KIND, name, f"it carries {len(sections)} sections: {sorted(sections)}")
            )
        for heading in sections:
            if heading in headings:
                found.append(
                    Violation(ONE_KIND, name, f"it shares the section {heading!r} with {headings[heading]}")
                )
            else:
                headings[heading] = name

        flat = _prose(text)
        for rule in owned:
            if rule in flat:
                found.append(
                    Violation(PROTOCOL_RULE_IN_RECIPE, name, f"it states again: {rule}")
                )

        if name in routed:
            for heading, body in sections.items():
                if not _rules(body):
                    found.append(
                        Violation(
                            KIND_RULE_IN_PROTOCOL,
                            name,
                            f"the section {heading!r} states no rule of its own",
                        )
                    )

    for kind in sorted({k for kinds in routed.values() for k in kinds}):
        sentence = _addressing_sentence(protocol_text, kind)
        if sentence is not None:
            found.append(
                Violation(
                    KIND_RULE_IN_PROTOCOL,
                    PROTOCOL_NAME,
                    f"it addresses the routed artifact type {kind} outside the "
                    f"routing table: {sentence}",
                )
            )
    return found


# --- helper self-tests -----------------------------------------------------

# A synthetic folder, so that no fixture here writes the name of a recipe the
# routing table routes: such a name would be a hand-listed reference that the
# removal of that kind would leave dangling.
_ONE = f"{RECIPE_STEM}synthetic-one.md"
_TWO = f"{RECIPE_STEM}synthetic-two.md"

_PROTOCOL = (
    "# Adversarial\n\nA shared rule long enough to be counted as one rule here.\n\n"
    f"{ROUTING_HEADING}\n\n| Artifact type | Recipe file |\n|---|---|\n"
    f"| `one` | [`{_ONE}`]({_ONE}) |\n| `two` | [`{_TWO}`]({_TWO}) |\n"
    "| `three` | none |\n\n"
    "## Recording\n\nRecord every attempt that failed to break anything at all.\n"
)


def _synthetic(folder: Path, *, protocol: str = _PROTOCOL) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / PROTOCOL_NAME).write_text(protocol, encoding="utf-8")
    for name, heading in ((_ONE, "One"), (_TWO, "Two")):
        (folder / name).write_text(
            f"# Adversarial — {heading}\n\n"
            f"Read it together with the shared protocol in [`{PROTOCOL_NAME}`]({PROTOCOL_NAME}).\n\n"
            f"## {heading}\n\nAttack the {heading.lower()} artifact until something of it fails.\n",
            encoding="utf-8",
        )
    return folder


def test_prose_helper_drops_headings_and_table_rows_synthetic() -> None:
    text = "# Title\n\nA rule.\n\n| Class | The question |\n|---|---|\n| Empty | does it? |\n"
    assert _prose(text) == "A rule."
    assert _rules("Too short.") == []
    assert _rules("A sentence with enough words in it to count as a rule of its own.") == [
        "A sentence with enough words in it to count as a rule of its own."
    ]


def test_section_helper_synthetic() -> None:
    assert _sections("# T\n\nlead\n\n## A\n\nfirst\n\n## B\n\nsecond\n") == {
        "A": "\nfirst\n",
        "B": "\nsecond",
    }
    assert _sections("# T\n\nno sections here\n") == {}


def test_routing_section_is_cut_out_synthetic() -> None:
    cut = _without_routing(_PROTOCOL)
    assert "## Recording" in cut and ROUTING_HEADING not in cut
    assert _ONE not in cut
    assert _without_routing("# T\n\n## Recording\n\nbody\n").count("## Recording") == 1


def test_synthetic_folder_keeps_the_shape(tmp_path: Path) -> None:
    folder = _synthetic(tmp_path / "synthetic")
    assert shape_violations(folder) == []
    assert sorted(p.name for p in recipe_files(folder)) == sorted([_ONE, _TWO])
    assert routed_kinds(folder) == {_ONE: ("one",), _TWO: ("two",)}


def test_synthetic_folder_rejects_each_broken_part(tmp_path: Path) -> None:
    """Each part is broken once on the synthetic folder too, so the checker is
    exercised on recipes that are nobody's real file."""
    base = _synthetic(tmp_path / "synthetic")

    dangling = _synthetic(tmp_path / "dangling")
    (dangling / _ONE).write_text(
        _read(dangling / _ONE).replace(f"({PROTOCOL_NAME})", "(adversarial-gone.md)"),
        encoding="utf-8",
    )
    assert {v.part for v in shape_violations(dangling)} == {BACK_POINTER}

    unrouted = _synthetic(tmp_path / "unrouted")
    (unrouted / PROTOCOL_NAME).write_text(
        _read(unrouted / PROTOCOL_NAME).replace(f"[`{_TWO}`]({_TWO})", NO_RECIPE),
        encoding="utf-8",
    )
    assert {v.part for v in shape_violations(unrouted)} == {ROUTED}

    two_kinds = _synthetic(tmp_path / "two-kinds")
    (two_kinds / _ONE).write_text(
        _read(two_kinds / _ONE) + "\n## Two\n\nAttack the two artifact until something fails.\n",
        encoding="utf-8",
    )
    assert {v.part for v in shape_violations(two_kinds)} == {ONE_KIND}

    copied = _synthetic(tmp_path / "copied")
    (copied / _ONE).write_text(
        _read(copied / _ONE) + f"\n{protocol_rules(base)[0]}\n", encoding="utf-8"
    )
    assert {v.part for v in shape_violations(copied)} == {PROTOCOL_RULE_IN_RECIPE}

    addressed = _synthetic(
        tmp_path / "addressed",
        protocol=_PROTOCOL.replace(
            "## Recording\n", "## Recording\n\nFor a `one` artifact, record the attempt twice.\n"
        ),
    )
    assert {v.part for v in shape_violations(addressed)} == {KIND_RULE_IN_PROTOCOL}


# --- A10 positive: every recipe keeps the shape -----------------------------

def test_every_recipe_keeps_the_shape() -> None:
    """every-recipe-keeps-the-shape."""
    recipes = recipe_files(REFERENCES)
    assert recipes, "the reference folder holds no recipe file"
    assert sorted(p.name for p in recipes) == sorted(routed_kinds(REFERENCES)), (
        "the recipes present and the recipes routed are not the same set"
    )
    violations = shape_violations(REFERENCES)
    assert violations == [], violations


# --- A10 negative: a recipe missing part of the shape is rejected -----------

def _copy(tmp_path: Path) -> Path:
    folder = tmp_path / "references"
    shutil.copytree(REFERENCES, folder)
    assert shape_violations(folder) == [], "the copy does not start clean"
    return folder


def _parts(folder: Path) -> set[str]:
    violations = shape_violations(folder)
    assert violations, "the broken shape was accepted"
    return {v.part for v in violations}


def _first_recipe(folder: Path) -> Path:
    """The recipe the break is made in: the first in file-name order, so the
    case names no recipe of its own and a retired kind cannot strand it."""
    recipes = recipe_files(folder)
    assert recipes, folder
    return recipes[0]


def test_dangling_back_pointer_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: the pointer back at the shared
    protocol no longer resolves."""
    folder = _copy(tmp_path)
    recipe = _first_recipe(folder)
    recipe.write_text(
        _read(recipe).replace(f"({PROTOCOL_NAME})", "(adversarial-gone.md)"), encoding="utf-8"
    )
    assert _parts(folder) == {BACK_POINTER}


def test_recipe_the_table_does_not_name_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: a recipe file added beside the
    protocol without the routing row that names it."""
    folder = _copy(tmp_path)
    (folder / f"{RECIPE_STEM}orphan.md").write_text(
        "# Adversarial — orphan\n\n"
        f"Read it together with the shared protocol in [`{PROTOCOL_NAME}`]({PROTOCOL_NAME}).\n\n"
        "## Orphan\n\nAttack the orphan artifact until something about it fails.\n",
        encoding="utf-8",
    )
    assert _parts(folder) == {ROUTED}


def test_routing_row_naming_a_file_that_is_not_there_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: the other half of the same part,
    a row the folder has no file for."""
    folder = _copy(tmp_path)
    recipe = _first_recipe(folder)
    recipe.unlink()
    assert _parts(folder) == {ROUTED}


def test_recipe_covering_two_kinds_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: one file, two kinds."""
    folder = _copy(tmp_path)
    recipe = _first_recipe(folder)
    recipe.write_text(
        _read(recipe) + "\n## Ledger\n\nKeep a ledger of every attempt this second kind makes.\n",
        encoding="utf-8",
    )
    assert _parts(folder) == {ONE_KIND}


def test_protocol_rule_copied_into_a_recipe_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: a rule the shared protocol owns,
    stated again in a recipe."""
    folder = _copy(tmp_path)
    recipe = _first_recipe(folder)
    borrowed = protocol_rules(folder)[0]
    assert borrowed not in _prose(_read(recipe)), borrowed
    recipe.write_text(_read(recipe) + f"\n{borrowed}\n", encoding="utf-8")
    assert _parts(folder) == {PROTOCOL_RULE_IN_RECIPE}


def test_kind_rule_moved_into_the_protocol_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: the kind's rules leave the kind's
    file for the shared protocol, which is where they may not be."""
    folder = _copy(tmp_path)
    recipe = _first_recipe(folder)
    text = _read(recipe)
    before, section = text.split("\n## ", 1)
    heading, body = section.split("\n", 1)
    recipe.write_text(f"{before}\n## {heading}\n", encoding="utf-8")
    protocol = folder / PROTOCOL_NAME
    protocol.write_text(_read(protocol) + body, encoding="utf-8")
    assert _parts(folder) == {KIND_RULE_IN_PROTOCOL}


def test_protocol_addressing_one_routed_kind_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: the protocol keeps every recipe's
    rules where they are and grows a rule of its own for one routed kind."""
    folder = _copy(tmp_path)
    protocol = folder / PROTOCOL_NAME
    kind = sorted({k for kinds in routed_kinds(folder).values() for k in kinds})[0]
    protocol.write_text(
        _read(protocol) + f"\nFor a `{kind}` artifact, run every attempt a second time.\n",
        encoding="utf-8",
    )
    assert _parts(folder) == {KIND_RULE_IN_PROTOCOL}


# The same rule, written the way a writer writes prose rather than the way the
# routing table writes a type. The first three are the wordings the adversary
# of this change planted in the protocol and watched go through; the last two
# are this module's own, one naming the kind mid-sentence and one naming it
# with no article at all.
_PLAIN_KIND_RULES = (
    "For a {kind} artifact, run every attempt a second time before recording it.",
    "When the changed path is a {kind}, run every attempt a second time.",
    "A {kind} change gets every attempt run a second time before it is recorded.",
    "The second run is asked of any {kind} artifact before its attempt is recorded.",
    "When the changed artifact is {kind}, run every attempt a second time.",
)

# Sentences that name a routed type and state no rule about it: the type is
# mentioned as the thing at hand, not as the class a rule applies to. The
# protocol must stay writable in this register, so each of these is accepted.
_PLAIN_MENTIONS = (
    "Nothing the adversary writes replaces reading the {kind} the change touched.",
    "The reviewer who read the {kind} is never the reviewer who wrote it.",
    "A reader of the {kind} reads this shared protocol before any recipe of it.",
)


def _routed_kind(folder: Path) -> str:
    """One routed artifact type, read from the table rather than named here."""
    kinds = sorted({k for kinds in routed_kinds(folder).values() for k in kinds})
    assert kinds, folder
    return kinds[0]


def test_kind_rule_in_plain_prose_in_the_protocol_is_rejected(tmp_path: Path) -> None:
    """recipe-missing-part-of-shape-rejected: the same rule for one routed kind,
    written in ordinary prose instead of the routing table's backticks."""
    kind = _routed_kind(REFERENCES)
    for index, wording in enumerate(_PLAIN_KIND_RULES):
        folder = _copy(tmp_path / f"plain-{index}")
        protocol = folder / PROTOCOL_NAME
        sentence = wording.format(kind=kind)
        protocol.write_text(_read(protocol) + f"\n{sentence}\n", encoding="utf-8")
        assert _parts(folder) == {KIND_RULE_IN_PROTOCOL}, sentence


def test_protocol_naming_a_kind_without_ruling_on_it_is_accepted(tmp_path: Path) -> None:
    """The other side of the same part: naming a routed type is not by itself a
    rule about it, and a check that rejected these could not be satisfied."""
    kind = _routed_kind(REFERENCES)
    for index, wording in enumerate(_PLAIN_MENTIONS):
        folder = _copy(tmp_path / f"mention-{index}")
        protocol = folder / PROTOCOL_NAME
        sentence = wording.format(kind=kind)
        protocol.write_text(_read(protocol) + f"\n{sentence}\n", encoding="utf-8")
        assert shape_violations(folder) == [], sentence
