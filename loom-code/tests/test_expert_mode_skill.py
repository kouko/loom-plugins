"""expert-mode skill and station reads (plan W3-01; Acceptance 1, 4).

Spec decisions 5, 7, 13 of 2026-09-14-expert-mode-step-selection: only the
user invokes the skill on both hosts, the skill talks and the checker
decides, and an agent suggestion is shown at most once per change while the
full process continues; a plain "yes" binds nothing.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PLUGIN_ROOT = SCRIPTS.parent
SKILL_DIR = PLUGIN_ROOT / "skills" / "expert-mode"
STATIONS = ("build", "closing-review", "ship", "write-plan")
def _skill() -> str:
    return (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    return yaml.safe_load(text[4:].split("\n---\n", 1)[0])


# --- Acceptance 1 -----------------------------------------------------------

def test_frontmatter_disables_model_invocation_and_openai_yaml_blocks_implicit() -> None:
    front = _frontmatter(_skill())
    assert front["name"] == "expert-mode"
    assert front["disable-model-invocation"] is True
    description = " ".join(str(front["description"]).split())
    assert "advanced" not in description.lower()

    policy = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert policy["policy"]["allow_implicit_invocation"] is False


def test_skill_text_evaluates_no_gate() -> None:
    text = _skill()
    assert "<!-- gate:" not in text
    invoked = set(re.findall(r"loom_checker\.py (selection [\w-]+|[\w-]+)", text))
    assert invoked == {"selection propose", "selection show", "selection cancel",
                       "selection skipped-review"}


def test_skill_round1_boundary_intent_skip_and_withdrawal_split() -> None:
    text = _skill()
    flat = _flat(text)
    assert "--skip intent" not in flat
    assert "`intent`, `spec`" not in flat
    assert "another selected step needs" not in flat
    boundary = _flat(text.split("## Boundary", 1)[1])
    assert "hook trust" not in boundary
    assert "a fresh clone refuses it" not in boundary
    assert "independent CI stays the trust boundary" not in boundary
    assert "reusing the old code" not in boundary
    assert "finalization in another session applies the full process" not in boundary
    cancel = next((s for s in re.split(r"(?<=\.)\s+", flat) if "selection cancel <change-id>" in s), "")
    assert "show the table again" not in cancel


def test_expert_mode_keeps_its_typed_confirmation() -> None:
    router = (PLUGIN_ROOT / "skills" / "using-loom-code" / "SKILL.md").read_text(encoding="utf-8")
    assert 'a plain "yes" binds nothing' not in _flat(router)
    assert "from ordinary conversation" not in _flat(_skill())


MOVED_RULES = ("at most once per change", "--origin agent", 'a plain "yes" binds nothing',
               "asks in their own words")


@pytest.mark.parametrize("station", STATIONS)
def test_station_one_sentence_points_to_expert_mode(station: str) -> None:
    """The suggestion rules live only in expert-mode, never in a station."""
    flat = _flat((PLUGIN_ROOT / "skills" / station / "SKILL.md").read_text(encoding="utf-8")).lower()
    for rule in MOVED_RULES:
        assert rule.lower() not in flat, rule


def test_expert_mode_holds_the_suggestion_rules_once() -> None:
    text = _skill()
    assert _flat(text).count("at most once per change") <= 1
    assert _flat(text).count("--origin agent") == 1
