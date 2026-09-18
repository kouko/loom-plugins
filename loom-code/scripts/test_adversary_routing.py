"""The routing table sends each artifact type to the recipe that attacks it.

Acceptance 4 and 7 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

The four cases this module makes, in the words of the plan:

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
  there is caught.

The addition in the first two cases is performed on a copy of the reference
folder in a temporary directory, so the assertion is made on the result of
a real edit rather than on a sentence promising the edit would be small.
"""
from __future__ import annotations

import re
import shutil
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

_SYNTHETIC = (
    "# Title\n\n## Which recipe to read\n\n"
    "| Artifact type | Recipe file |\n|---|---|\n"
    "| `code` | [`adversarial-code.md`](adversarial-code.md) |\n"
    "| `plan` | none |\n\n"
    "## Recording\n\n| `docs` | [`adversarial-docs.md`](adversarial-docs.md) |\n"
)


def test_routing_row_helper_synthetic() -> None:
    assert _routing_rows(_SYNTHETIC) == {"code": "adversarial-code.md", "plan": NO_RECIPE}
    assert _routing_rows("# Title\n\n## Recording\n\n| `code` | x.md |\n") == {}


def test_cell_helper_synthetic() -> None:
    assert _cell(" [`adversarial-spec.md`](adversarial-spec.md) ") == "adversarial-spec.md"
    assert _cell(" `spec` ") == "spec"
    assert _cell(" none ") == NO_RECIPE


def test_artifact_type_helper_synthetic() -> None:
    assert _TYPE.match('  - {glob: "docs/loom/*/plan.md",        type: plan}').group("type") == "plan"
    assert _TYPE.match("  - {name: package-tests, grammar: none}") is None


def test_add_kind_helper_synthetic(tmp_path: Path) -> None:
    (tmp_path / "adversarial.md").write_text(_SYNTHETIC, encoding="utf-8")
    _add_kind(tmp_path, "plan", "adversarial-plan.md", "# Adversarial — plan\n")
    rows = _routing_rows((tmp_path / "adversarial.md").read_text(encoding="utf-8"))
    assert rows["plan"] == "adversarial-plan.md"
    assert rows["code"] == "adversarial-code.md"


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
