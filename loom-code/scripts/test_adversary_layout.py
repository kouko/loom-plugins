"""Each artifact kind owns its attack recipe file beside the shared protocol.

Acceptance 1, 2 and 8 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

The three assertions this module makes, in the words of the plan:

1. every recipe file sits beside the protocol in the same skill reference
   folder, and the folder stays flat (A1 positive);
   the protocol keeps no recipe body (A1 negative);
2. a rule that belongs to one kind of artifact lives in that kind's file
   (A2 positive) and in neither the protocol nor another kind's file
   (A2 negative);
3. every rule of the pre-split document is still there, section for section
   (A8 positive), and no recipe file grew one (A8 boundary).

The pre-split document is read out of git history at the commit the
correspondence note names, so this module compares against the real
original rather than against a copy of it that could drift with it.
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

ORIGINAL_PATH = "loom-code/skills/closing-review/references/adversarial.md"
_BASE_COMMIT_RE = re.compile(r"at commit `([0-9a-f]{7,40})`")

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


def _base_commit() -> str:
    note = CORRESPONDENCE.read_text(encoding="utf-8")
    match = _BASE_COMMIT_RE.search(note)
    assert match, (
        f"{CORRESPONDENCE} must name the commit the pre-split document is read "
        "from, as: at commit `<sha>`"
    )
    return match.group(1)


def _original() -> str:
    commit = _base_commit()
    result = subprocess.run(
        ["git", "show", f"{commit}:{ORIGINAL_PATH}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"cannot read the pre-split document from git at {commit}: {result.stderr.strip()}"
    )
    return result.stdout


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

def test_each_kind_rule_lives_in_its_own_file() -> None:
    for kind, path in RECIPES.items():
        text = path.read_text(encoding="utf-8")
        found = _markers_found(text, KIND_MARKERS[kind])
        assert found == list(KIND_MARKERS[kind]), (kind, found)
        assert KIND_HEADINGS[kind] in _sections(text), kind


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
    original_text = _original()
    original = _sections(original_text)
    protocol = _sections(PROTOCOL.read_text(encoding="utf-8"))
    for heading in SHARED_HEADINGS:
        assert protocol[heading] == original[heading], heading
    for kind, path in RECIPES.items():
        heading = KIND_HEADINGS[kind]
        assert _sections(path.read_text(encoding="utf-8"))[heading] == original[heading], kind
    dropped = _dropped_sentences(
        _preamble(original_text), _preamble(PROTOCOL.read_text(encoding="utf-8"))
    )
    assert dropped == [], dropped


def test_no_recipe_file_carries_a_rule_the_original_did_not() -> None:
    original = _sections(_original())
    for kind, path in RECIPES.items():
        headings = _sections(path.read_text(encoding="utf-8"))
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
