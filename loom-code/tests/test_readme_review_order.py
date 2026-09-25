"""User-facing descriptions follow the Build-then-review order.

Build ends with an independent adversary's adversarial programs and the
complete package suite; closing review only reviews content that passed
them. The four READMEs and the Codex longDescription must say so, and none
may still say closing review dispatches the adversary or creates the
adversarial programs.

Checks work on "units": each table row and each line inside a code fence is
its own unit (a mermaid node, a table row); prose is grouped into
paragraphs / bullets, joined, and split into sentences on `.` and `。`.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT_README = REPO_ROOT / "README.md"
CODE_READMES = [
    REPO_ROOT / "loom-code" / "README.md",
    REPO_ROOT / "loom-code" / "README.ja.md",
    REPO_ROOT / "loom-code" / "README.zh-TW.md",
]
ALL_READMES = [ROOT_README, *CODE_READMES]
CODEX_MANIFEST = REPO_ROOT / "loom-code" / ".codex-plugin" / "plugin.json"

ADVERSARY = re.compile(r"adversar|敵対|対抗|對抗", re.IGNORECASE)
BUILD = re.compile(r"\bbuild\b", re.IGNORECASE)
SUITE = re.compile(r"suite|package", re.IGNORECASE)
CLOSING_REVIEW = re.compile(
    r"closing[- ]review|クロージングレビュー|收尾審查", re.IGNORECASE
)


def _units(text: str) -> list[str]:
    units: list[str] = []
    in_fence = False
    block: list[str] = []

    def flush() -> None:
        if block:
            joined = " ".join(line.strip() for line in block)
            units.extend(
                s for s in re.split(r"(?<=[.。])\s*", joined) if s.strip()
            )
            block.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith("|"):
            flush()
            units.append(stripped)
        elif not stripped or stripped.startswith(("- ", "#")):
            flush()
            if stripped:
                block.append(stripped)
        else:
            block.append(stripped)
    flush()
    return units


@pytest.mark.parametrize("readme", ALL_READMES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_readmes_say_build_runs_adversary_and_suite(readme: Path) -> None:
    units = _units(readme.read_text(encoding="utf-8"))
    hits = [u for u in units if BUILD.search(u) and ADVERSARY.search(u) and SUITE.search(u)]
    assert hits, f"{readme}: no line attributes the adversary and package suite to Build"


@pytest.mark.parametrize("readme", CODE_READMES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_adversary_agent_row_is_dispatched_by_build(readme: Path) -> None:
    rows = [
        line for line in readme.read_text(encoding="utf-8").splitlines()
        if line.startswith("| [`adversary`]")
    ]
    assert len(rows) == 1, f"{readme}: expected one adversary agent row"
    owner = rows[0].split("|")[2].strip()
    assert owner == "`build`", f"{readme}: adversary row owner is {owner}"


@pytest.mark.parametrize("readme", ALL_READMES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_no_readme_says_closing_review_dispatches_adversary(readme: Path) -> None:
    offending = [
        u for u in _units(readme.read_text(encoding="utf-8"))
        if CLOSING_REVIEW.search(u) and ADVERSARY.search(u)
    ]
    assert not offending, f"{readme}: closing review still tied to the adversary: {offending}"


def test_codex_long_description_follows_new_order() -> None:
    desc = json.loads(CODEX_MANIFEST.read_text(encoding="utf-8"))["interface"]["longDescription"]
    assert "programs once" not in desc
    build_sentences = [
        s for s in re.split(r"(?<=[.;])\s+", desc)
        if BUILD.search(s) and ADVERSARY.search(s) and SUITE.search(s)
    ]
    assert build_sentences, "longDescription does not say Build runs the adversary and suite"


LOOM_README = REPO_ROOT / "docs" / "loom" / "README.md"
KICKOFF_DEFAULTS = REPO_ROOT / "docs" / "loom" / "KICKOFF-DEFAULTS.md"
REVIEW_OWNER = re.compile(r"closing[- ]review|review station", re.IGNORECASE)
END_OF_BUILD = re.compile(r"end of build|end-of-build", re.IGNORECASE)


def _package_tests_reason() -> str:
    line = next(
        line for line in KICKOFF_DEFAULTS.read_text(encoding="utf-8").splitlines()
        if line.startswith("- package-tests:")
    )
    return line.split(" — ", 1)[1]


def test_kickoff_and_loom_readme_name_build_end_checks() -> None:
    reason = _package_tests_reason()
    assert END_OF_BUILD.search(reason), f"package-tests reason omits the end of Build: {reason}"
    assert "finalize-review" in reason, f"package-tests reason omits finalize-review: {reason}"
    units = _units(LOOM_README.read_text(encoding="utf-8"))
    hits = [u for u in units if ADVERSARY.search(u) and END_OF_BUILD.search(u)]
    assert hits, f"{LOOM_README}: no unit places the adversary at the end of Build"


@pytest.mark.parametrize(
    "doc", [LOOM_README, KICKOFF_DEFAULTS], ids=lambda p: str(p.relative_to(REPO_ROOT))
)
def test_no_loom_doc_says_review_runs_groups_once(doc: Path) -> None:
    text = doc.read_text(encoding="utf-8")
    units = [*text.splitlines(), *_units(text)]
    offending = sorted({
        u for u in units
        if REVIEW_OWNER.search(u)
        and ((ADVERSARY.search(u) and not END_OF_BUILD.search(u)) or (re.search(r"\bonce\b", u) and re.search(r"group|suite", u)))
    })
    assert not offending, f"{doc}: review still owns the adversary or a run-once suite: {offending}"


def _written_by_cell(row_key: str) -> str:
    row = next(
        line for line in LOOM_README.read_text(encoding="utf-8").splitlines()
        if line.startswith("|") and row_key in line
    )
    return row.split("|")[-2].strip()


def test_loom_readme_written_by_names_no_retired_review_station() -> None:
    """A1 negative (readme-written-by-names-retired-review-station): the
    change-folder row credits `closing-review`, the live station name."""
    cell = _written_by_cell("`<change-id>/`")
    assert "closing-review" in cell, cell
    assert not re.search(r"(?<!-)\breview\b", cell), f"retired station name in {cell!r}"


REVIEW_TO_ADVERSARY = re.compile(r"\breview\s*→\s*adv\b", re.IGNORECASE)
# Retired flow vocabulary: attack catalogue, review.json, lanes, the Build
# memory step, reviewed_sha→HEAD^.
STALE_LOOM_README = re.compile(
    r"attack-catalogue|review\.json|車道|\blanes?\b|memory step|reviewed_sha",
    re.IGNORECASE,
)


def _sequence_messages(text: str) -> list[dict]:
    match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
    assert match, "no JSON sequence payload"
    return json.loads(match.group(1))["messages"]


def _review_dispatches_adversary(text: str) -> list[str]:
    rows = [u for u in _units(text) if REVIEW_TO_ADVERSARY.search(u)]
    rows += [
        m["label"] for m in _sequence_messages(text)
        if m["from"] == "review" and m["to"] == "adv"
    ]
    return rows


def test_readme_adversary_at_build_end_no_lanes_no_review_json() -> None:
    text = LOOM_README.read_text(encoding="utf-8")
    messages = _sequence_messages(text)
    adv = [i for i, m in enumerate(messages) if m["to"] == "adv"]
    impl = [i for i, m in enumerate(messages) if m["to"] == "impl" and m["from"] == "build"]
    assert adv and impl and min(adv) > max(impl), "Build dispatches the adversary only after implementation"
    assert all(messages[i]["from"] == "build" for i in adv), "only Build dispatches the adversary"
    assert not STALE_LOOM_README.findall(text), STALE_LOOM_README.findall(text)


def test_readme_review_dispatches_adversary_rejected() -> None:
    assert not _review_dispatches_adversary(LOOM_README.read_text(encoding="utf-8"))
    seeded = (
        "| 4a | review→adv | extra attacks |\n\n"
        '```json\n{"participants": [], "messages": '
        '[{"from": "review", "to": "adv", "label": "8"}]}\n```\n'
    )
    assert len(_review_dispatches_adversary(seeded)) == 2


def test_units_catch_seeded_closing_review_adversary_sentence() -> None:
    seeded = (
        "- **Build and review** — `build` implements each task.\n"
        "  `closing-review` then dispatches reviewers and adversarial\n"
        "  programs for code changes.\n"
    )
    assert any(CLOSING_REVIEW.search(u) and ADVERSARY.search(u) for u in _units(seeded))
