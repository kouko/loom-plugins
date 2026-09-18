"""Each artifact kind owns its attack recipe file beside the shared protocol.

Acceptance 1, 2 and 8 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

The three assertions this module makes, in the words of the plan:

1. every recipe file sits beside the protocol in the same skill reference
   folder, and the folder stays flat (A1 positive);
   the protocol keeps no recipe body (A1 negative);
2. a rule that belongs to one kind of artifact lives in that kind's file
   (A2 positive) and in neither the protocol nor another kind's file
   (A2 negative). The negative is a scan of the current files; the positive
   names sentences quoted from the pre-split document, so it reads the
   split's own files for the reason assertion 3 does, and the tree is read
   for the structural half of it -- the kind's section is in the kind's
   file;
3. every rule of the pre-split document is still there, section for section
   (A8 positive), and no recipe file grew one (A8 boundary).

Assertions 1 and 2 are standing structural rules, checked against the
working tree: they must hold for as long as the recipes exist.

Assertion 3 is migration evidence, and both of its sides are read out of
git history at the commits the correspondence note names -- the pre-split
document at its own commit, the split files at the split commit. It states
a fact about one past event, that the split moved every rule and invented
none, and a fact about the past does not change. Reading the current files
instead would have frozen the recipes themselves: every later edit to one
of them would have failed a check named after the migration, which
Acceptance 3 forbids. A later edit to a recipe belongs to that recipe's own
test file.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
PROTOCOL = REFERENCES / "adversarial.md"
RECIPES = {
    "code": REFERENCES / "adversarial-code.md",
    "spec": REFERENCES / "adversarial-spec.md",
    "skill-gate": REFERENCES / "adversarial-skill-gate.md",
}
CORRESPONDENCE = (
    ROOT / "docs/loom/2026-09-18-modular-adversary-recipes/evidence/rule-correspondence.md"
)

REFERENCES_PATH = "loom-code/skills/closing-review/references"
ORIGINAL_PATH = f"{REFERENCES_PATH}/adversarial.md"
_BASE_COMMIT_RE = re.compile(r"at commit `([0-9a-f]{7,40})`")
# The split commit is named with its own phrasing so that the base-commit
# pattern above cannot match it, and vice versa.
_SPLIT_COMMIT_RE = re.compile(r"at split commit `([0-9a-f]{7,40})`")

# The H2 the split moves into each recipe file, exactly as the pre-split
# document spells it.
KIND_HEADINGS = {"code": "Code", "spec": "Spec", "skill-gate": "Skill and gate"}
# The H2s every kind shares, which stay in the protocol file.
SHARED_HEADINGS = ("Reuse first, update with evidence", "Recording")

# Rule text that belongs to exactly one kind of artifact. Each fragment is
# quoted from the pre-split document and occurs in one section of it only,
# so finding it anywhere but that kind's file is a split that leaked.
KIND_MARKERS = {
    "code": (
        "**at least three**",
        "Three is the floor, not the target.",
        "a surviving mutant is a test that asserts nothing",
        "path traversal",
        "Prefer cases that live as real tests afterwards.",
    ),
    "spec": (
        "Red-team it",
        "name a behaviour the requirement permits",
        "the migration from what exists today",
    ),
    "skill-gate": (
        "Read the instruction as an agent under time pressure",
        "Attempt the prose temptations verbatim",
        "the same input one character different",
    ),
}


def _flat(text: str) -> str:
    return " ".join(text.split())


def _sections(text: str) -> dict[str, str]:
    """Map each `## ` heading to its flattened body, heading line excluded."""
    sections: dict[str, str] = {}
    heading: str | None = None
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if heading is not None:
                sections[heading] = _flat(" ".join(body))
            heading, body = line[3:].strip(), []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        sections[heading] = _flat(" ".join(body))
    return sections


def _preamble(text: str) -> str:
    """Everything before the first `## ` heading, flattened."""
    return _flat(text.split("\n## ", 1)[0])


def _markers_found(text: str, markers: tuple[str, ...]) -> list[str]:
    """Which of `markers` the text states. Whitespace is flattened first, so
    prose may rewrap freely; the fragments themselves are matched literally."""
    flat = _flat(text)
    return [m for m in markers if m in flat]


def _dropped_sentences(original: str, current: str) -> list[str]:
    """Sentences of `original` that `current` no longer states.

    The preamble is checked for dropped sentences rather than for byte
    equality because the protocol file's preamble is also where the routing
    marker sits and where the routing table will land. An addition there is
    not a rule; a sentence that stopped being stated is.
    """
    return [s for s in re.split(r"(?<=\.)\s+", original) if s and s not in current]


def _note() -> str:
    """The correspondence note, flattened, so that rewrapping its prose
    cannot move a sha out of reach of the patterns above."""
    return _flat(CORRESPONDENCE.read_text(encoding="utf-8"))


def _base_commit() -> str:
    note = _note()
    match = _BASE_COMMIT_RE.search(note)
    assert match, (
        f"{CORRESPONDENCE} must name the commit the pre-split document is read "
        "from, as: at commit `<sha>`"
    )
    return match.group(1)


def _split_commit() -> str:
    note = _note()
    match = _SPLIT_COMMIT_RE.search(note)
    assert match, (
        f"{CORRESPONDENCE} must name the commit the split wrote the recipe "
        "files in, as: at split commit `<sha>`"
    )
    return match.group(1)


def _show(commit: str, path: str, what: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"cannot read the {what} from git at {commit}: {result.stderr.strip()}"
    )
    return result.stdout


def _original() -> str:
    return _show(_base_commit(), ORIGINAL_PATH, "pre-split document")


def _at_split(name: str) -> str:
    """One reference file as the split commit wrote it.

    The migration assertions read this and never the working tree, so a
    later edit to a recipe cannot turn them red; what they check happened
    once and is over.
    """
    return _show(_split_commit(), f"{REFERENCES_PATH}/{name}", f"split {name}")


# --- helper self-tests -----------------------------------------------------

_SYNTHETIC = (
    "# Title\n\nOpening line.\n\n## Code\n\nWrite **at least three** cases.\n\n"
    "## Recording\n\nRecord every attempt.\n"
)


def test_section_and_preamble_helpers_synthetic() -> None:
    assert _sections(_SYNTHETIC) == {
        "Code": "Write **at least three** cases.",
        "Recording": "Record every attempt.",
    }
    assert _preamble(_SYNTHETIC) == "# Title Opening line."
    assert _sections("# Title\n\nNo headings here.\n") == {}


def test_marker_helper_synthetic() -> None:
    """A recipe body left behind is detected; the shared protocol is not."""
    leaked = "## Code\n\nWrite **at least three** cases; three is the floor.\n"
    assert _markers_found(leaked, KIND_MARKERS["code"]) == ["**at least three**"]
    protocol_only = "## Reuse first, update with evidence\n\nReuse a program that covers a case.\n"
    assert _markers_found(protocol_only, KIND_MARKERS["code"]) == []
    assert _markers_found(protocol_only, KIND_MARKERS["spec"]) == []
    assert _markers_found(protocol_only, KIND_MARKERS["skill-gate"]) == []


def test_dropped_sentence_helper_synthetic() -> None:
    original = "It runs at the end of Build. If a case needs the code changed to fail, it is not a case."
    kept = "It runs at the end of Build. A marker sits here. If a case needs the code changed to fail, it is not a case."
    assert _dropped_sentences(original, kept) == []
    assert _dropped_sentences(original, "It runs at the end of Build.") == [
        "If a case needs the code changed to fail, it is not a case."
    ]


def test_base_commit_helper_synthetic() -> None:
    assert _BASE_COMMIT_RE.search("read at commit `5b8dfdce` before the split").group(1) == "5b8dfdce"
    assert _BASE_COMMIT_RE.search("read at an earlier commit before the split") is None


def test_split_commit_helper_synthetic() -> None:
    """The two shas are told apart by their phrasing, in both directions."""
    note = "read at commit `5b8dfdce`, and at split commit `50cf9f8b` after it"
    assert _SPLIT_COMMIT_RE.search(note).group(1) == "50cf9f8b"
    assert _BASE_COMMIT_RE.search(note).group(1) == "5b8dfdce"
    assert _SPLIT_COMMIT_RE.search("read at commit `5b8dfdce` before the split") is None
    wrapped = "read at commit `5b8dfdce`, and at split commit\n`50cf9f8b` after it"
    assert _SPLIT_COMMIT_RE.search(wrapped) is None
    assert _SPLIT_COMMIT_RE.search(_flat(wrapped)).group(1) == "50cf9f8b"


def test_frozen_comparison_catches_a_rule_dropped_by_the_split_synthetic() -> None:
    """A split that dropped or added a sentence fails the section comparison.

    The frozen assertions compare whole section bodies for equality, so a
    split that carried a section across short of one sentence, or with one
    the original never had, cannot pass.
    """
    original = _sections("# T\n\n## Spec\n\nRed-team it. Anchor each finding.\n")["Spec"]
    faithful = _sections("# Adversarial — spec\n\n## Spec\n\nRed-team it.\nAnchor each finding.\n")
    dropped = _sections("# Adversarial — spec\n\n## Spec\n\nRed-team it.\n")
    added = _sections("# Adversarial — spec\n\n## Spec\n\nRed-team it. Anchor each finding. Ship it.\n")
    assert faithful["Spec"] == original
    assert dropped["Spec"] != original
    assert added["Spec"] != original


# --- A1: each recipe file sits beside the protocol, and the folder is flat ---

def test_recipe_files_sit_beside_the_protocol() -> None:
    assert PROTOCOL.is_file(), PROTOCOL
    for kind, path in RECIPES.items():
        assert path.is_file(), (kind, path)
        assert path.parent == PROTOCOL.parent, (kind, path)
    assert PROTOCOL.parent.parent.name == "closing-review", PROTOCOL
    assert [p.name for p in REFERENCES.iterdir() if p.is_dir()] == [], (
        "the repository forbids a subfolder inside a skill subfolder"
    )


def test_protocol_keeps_no_recipe_body() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    headings = _sections(text)
    for kind, heading in KIND_HEADINGS.items():
        assert heading not in headings, (kind, heading)
        assert _markers_found(text, KIND_MARKERS[kind]) == [], kind
    for shared in SHARED_HEADINGS:
        assert shared in headings, shared


# --- A2: a kind's rule lives in that kind's file and nowhere else -----------

def test_each_kind_section_lives_in_its_own_file() -> None:
    """Standing: the kind's section is in the kind's file, in the tree."""
    for kind, path in RECIPES.items():
        assert KIND_HEADINGS[kind] in _sections(path.read_text(encoding="utf-8")), kind


def test_each_kind_rule_lives_in_its_own_file() -> None:
    """Frozen to the migration: the split put each marked rule in its kind's
    file. The markers are sentences quoted from the pre-split document, so
    read against the tree this would fire whenever a recipe was reworded --
    the coupling Acceptance 3 forbids. A rewording is that recipe's own test
    file's business; that the split filed the rule correctly is this one's,
    and it happened once."""
    for kind, path in RECIPES.items():
        found = _markers_found(_at_split(path.name), KIND_MARKERS[kind])
        assert found == list(KIND_MARKERS[kind]), (kind, found)


def test_no_kind_rule_appears_outside_its_own_file() -> None:
    files = {"protocol": PROTOCOL, **RECIPES}
    for kind, markers in KIND_MARKERS.items():
        for name, path in files.items():
            if name == kind:
                continue
            found = _markers_found(path.read_text(encoding="utf-8"), markers)
            assert found == [], (kind, name, found)


# --- A8: every rule survived the split, and no recipe file grew one ---------

def test_every_original_section_lives_in_exactly_one_file() -> None:
    original = _sections(_original())
    assert set(original) == set(SHARED_HEADINGS) | set(KIND_HEADINGS.values()), original.keys()
    homes = {"protocol": PROTOCOL, **RECIPES}
    for heading in original:
        holding = [n for n, p in homes.items() if heading in _sections(p.read_text(encoding="utf-8"))]
        assert len(holding) == 1, (heading, holding)


def test_every_original_rule_is_still_stated_verbatim() -> None:
    """Frozen to the migration: both sides come from git, never the tree."""
    original_text = _original()
    original = _sections(original_text)
    split_protocol = _at_split(PROTOCOL.name)
    protocol = _sections(split_protocol)
    for heading in SHARED_HEADINGS:
        assert protocol[heading] == original[heading], heading
    for kind, path in RECIPES.items():
        heading = KIND_HEADINGS[kind]
        assert _sections(_at_split(path.name))[heading] == original[heading], kind
    dropped = _dropped_sentences(_preamble(original_text), _preamble(split_protocol))
    assert dropped == [], dropped


def test_no_recipe_file_carries_a_rule_the_original_did_not() -> None:
    """Frozen to the migration: both sides come from git, never the tree."""
    original = _sections(_original())
    for kind, path in RECIPES.items():
        headings = _sections(_at_split(path.name))
        assert list(headings) == [KIND_HEADINGS[kind]], (kind, list(headings))
        assert headings[KIND_HEADINGS[kind]] == original[KIND_HEADINGS[kind]], kind


def test_correspondence_note_maps_every_rule_to_a_file_that_exists() -> None:
    note = CORRESPONDENCE.read_text(encoding="utf-8")
    rows = [line for line in note.splitlines() if line.startswith("| ") and " | " in line]
    body = [r for r in rows if not set(r) <= set("|- ")][1:]  # drop the header row
    assert body, "the correspondence note lists no rule"
    original = _sections(_original())
    named_headings: set[str] = set()
    for row in body:
        cells = [c.strip() for c in row.strip("|").split("|")]
        heading, destination = cells[-2].strip("`"), cells[-1].strip("`")
        assert heading in original or heading == "(preamble)", row
        named_headings.add(heading)
        assert (REFERENCES / destination).is_file(), row
    assert set(original) <= named_headings, set(original) - named_headings
