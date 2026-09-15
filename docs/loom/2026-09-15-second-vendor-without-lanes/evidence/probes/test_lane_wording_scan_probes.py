"""Adversarial probes for intent Acceptance 2 across the whole runtime tree.

Run from the repo root:

    python3 -m pytest -q -p no:cacheprovider \
        docs/loom/2026-09-15-second-vendor-without-lanes/evidence/probes/test_lane_wording_scan_probes.py

The implementer's lane scans cover five named files. These probes scan every
tracked runtime file in loom-code and loom-design (skills, agents, contract,
hooks, commands, non-test scripts), and pin the "on every change" sentences
with an affirmative verb and no negation. All cases are expected to PASS.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
LANE_RE = re.compile(r"(?i)\b(small|full)[- ]lanes?\b|\blanes?\b")
RUNTIME_PREFIX = re.compile(r"^(loom-code|loom-design)/(skills|agents|contract|hooks|commands|scripts)/")
NEGATION_RE = re.compile(r"(?i)\b(not|never|no|none|without|omit(?:s|ted)?|skip(?:s|ped)?|except|unless)\b|n't\b")


def runtime_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "loom-code", "loom-design"],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout.split()
    keep = [
        p for p in out
        if RUNTIME_PREFIX.match(p)
        and not re.search(r"/test_[^/]*\.py$", p)
        and p.endswith((".md", ".py", ".sh", ".yaml", ".yml", ".json", ".toml"))
    ]
    return [REPO / p for p in keep]


def lane_hits(text: str) -> list[str]:
    return [m.group(0) for m in LANE_RE.finditer(" ".join(text.split()))]


def sentence_with(text: str, literal: str) -> str:
    flat = " ".join(text.split())
    idx = flat.index(literal)
    start = max(flat.rfind(". ", 0, idx), flat.rfind("\n", 0, idx)) + 1
    end = flat.find(". ", idx)
    return flat[start:end if end != -1 else len(flat)]


def affirmed(sentence: str, verb: str, literal: str) -> bool:
    """True only when `verb` precedes `literal` and the sentence has no negation."""
    v = sentence.find(verb)
    return v != -1 and v < sentence.find(literal) and not NEGATION_RE.search(sentence)


# --- synthetic self-tests for the helpers --------------------------------------

def test_laneRegex_syntheticExamples_matchesOnlyLaneWords() -> None:
    assert lane_hits("ask blocks once per full-lane change")
    assert lane_hits("In the small\n lane it is omitted")
    assert lane_hits("Lane-dependent floor")
    assert not lane_hits("planes and a planet on the plane explained")


def test_affirmedPin_syntheticAffirmative_accepted() -> None:
    s = sentence_with("`ask` puts one question to the user on every change. Next.", "on every change")
    assert affirmed(s, "puts", "on every change")


def test_affirmedPin_syntheticNegated_rejected() -> None:
    s = sentence_with("`ask` never puts one question to the user on every change. Next.", "on every change")
    assert not affirmed(s, "puts", "on every change")


# --- the probes -------------------------------------------------------------

def test_runtimeTree_everyLoomCodeAndDesignFile_namesNoLane() -> None:
    files = runtime_files()
    assert len(files) > 50, "scan scope collapsed"
    offenders = {
        str(p.relative_to(REPO)): hits
        for p in files
        if (hits := lane_hits(p.read_text(encoding="utf-8", errors="replace")))
    }
    assert offenders == {}


def test_manifestSecondVendorNote_currentText_namesNoLane() -> None:
    import yaml

    manifest = yaml.safe_load((REPO / "loom-code/contract/manifest.yaml").read_text(encoding="utf-8"))
    entry = next(k for k in manifest["kickoff_defaults"] if k["name"] == "second-vendor")
    assert lane_hits(entry["note"]) == []
    assert "once per change" in entry["note"]


@pytest.mark.parametrize(
    ("path", "verb"),
    [
        ("loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md", "puts"),
        ("loom-design/skills/capture-intent/references/second-vendor.md", "puts"),
    ],
)
def test_askSentence_everyChangePin_affirmedWithoutNegation(path: str, verb: str) -> None:
    text = (REPO / path).read_text(encoding="utf-8")
    sentence = sentence_with(text, "on every change")
    assert affirmed(sentence, verb, "on every change"), sentence
