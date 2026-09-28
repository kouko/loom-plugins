"""expert-mode skill and station reads (plan W3-01; Acceptance 1, 4).

Spec decisions 5, 7, 13 of 2026-09-14-expert-mode-step-selection: only the
user invokes the skill on both hosts, the skill talks and the checker
decides, and an agent suggestion is shown at most once per change while the
full process continues; a plain "yes" binds nothing.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from loom_checker import selection

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PLUGIN_ROOT = SCRIPTS.parent
CHECKER = SCRIPTS / "loom_checker.py"
SKILL_DIR = PLUGIN_ROOT / "skills" / "expert-mode"
STATIONS = ("build", "closing-review", "ship", "write-plan")
CHANGE = "2026-09-14-example"
HOST_SESSION_VARS = ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED",
                     "CLAUDE_CODE_ENTRYPOINT")


@pytest.fixture(autouse=True)
def _no_host_session(monkeypatch: pytest.MonkeyPatch) -> None:
    """Results must not depend on running inside a live host session."""
    for name in HOST_SESSION_VARS:
        monkeypatch.delenv(name, raising=False)


def _clean_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if k not in HOST_SESSION_VARS}


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


# --- Acceptance 4 -----------------------------------------------------------

def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], env=_clean_env(),
                          capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    for name, branch in (("base.py", None), ("work.py", "feature")):
        if branch:
            _git(repo, "checkout", "-q", "-b", branch)
        (repo / name).write_text(name, encoding="utf-8")
        _git(repo, "add", name)
        _git(repo, "commit", "-q", "-m", name)
    return repo


def _selection(repo: Path, *args: str, stdin: str = "") -> subprocess.CompletedProcess:
    result = subprocess.run([sys.executable, str(CHECKER), "selection", *args],
                            capture_output=True, text=True, cwd=str(repo), input=stdin,
                            env=_clean_env())
    assert result.returncode == 0, result.stderr
    return result


def _prompt(repo: Path, prompt: str, ref: str) -> None:
    payload = {"hook_event_name": "UserPromptSubmit", "prompt": prompt,
               "session_id": "sess-1", "prompt_id": ref}
    _selection(repo, "capture", "--hook", stdin=json.dumps(payload, ensure_ascii=False))


def test_suggestion_then_plain_yes_skips_nothing(repo: Path) -> None:
    _selection(repo, "propose", CHANGE, "--origin", "agent", "--skip", "reviewers,adversarial")
    for i, reply in enumerate(("yes", "對", "はい", "/loom-code:expert-mode yes")):
        _prompt(repo, reply, f"prompt-{i}")
        shown = json.loads(_selection(repo, "show", CHANGE).stdout)
        assert shown["bound"] is False and shown["skip"] == [], reply
    assert not [e for e in selection.read_events(repo, CHANGE) if e["event"] == "confirmation"]

    # Auto-skip is active for narrow deltas: .py file keeps floor=2
    # (non-narrow) so no steps are auto-skipped when the user types plain yes
    code = [e for e in selection.read_events(repo, CHANGE) if e["event"] == "proposal"][-1]["code"]
    _prompt(repo, f"/loom-code:expert-mode OK {code}", "prompt-typed")
    assert json.loads(_selection(repo, "show", CHANGE).stdout)["skip"] == ["reviewers", "adversarial"]


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
