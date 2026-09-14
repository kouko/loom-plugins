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


def test_units_catch_seeded_closing_review_adversary_sentence() -> None:
    seeded = (
        "- **Build and review** — `build` implements each task.\n"
        "  `closing-review` then dispatches reviewers and adversarial\n"
        "  programs for code changes.\n"
    )
    assert any(CLOSING_REVIEW.search(u) and ADVERSARY.search(u) for u in _units(seeded))
