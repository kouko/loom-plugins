"""expert-mode skill and station reads (plan W3-01; Acceptance 1, 4).

Spec decisions 5, 7, 13 of 2026-09-14-expert-mode-step-selection: only the
user invokes the skill on both hosts, the skill talks and the checker
decides, and an agent suggestion is shown at most once per change while the
full process continues; a plain "yes" binds nothing.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from loom_checker import selection
from prose_pin import has_negation

SCRIPTS = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS.parent
CHECKER = SCRIPTS / "loom_checker.py"
SKILL_DIR = PLUGIN_ROOT / "skills" / "expert-mode"
STATIONS = ("build", "review", "ship", "write-plan")
CHANGE = "2026-09-14-example"


def _skill() -> str:
    return (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _frontmatter(text: str) -> dict:
    assert text.startswith("---\n")
    return yaml.safe_load(text[4:].split("\n---\n", 1)[0])


def affirmative(text: str, anchor: str, verbs: tuple[str, ...]) -> str:
    """The sentence holding `anchor` carries an affirmative verb before it and
    no negation token (engineering baseline, prose-pin rule)."""
    sentence = next((s for s in re.split(r"(?<=\.)\s+", _flat(text)) if anchor in s), None)
    assert sentence is not None, f"no sentence pins {anchor!r}"
    assert not has_negation(sentence), sentence
    before = sentence[: sentence.index(anchor)].lower()
    assert any(re.search(rf"\b{re.escape(verb)}\b", before) for verb in verbs), sentence
    return sentence


def test_affirmative_helper_accepts_an_affirmative_sentence() -> None:
    assert affirmative("The agent may suggest it at most once per change.", "at most once", ("may",))


def test_affirmative_helper_rejects_a_negated_sentence() -> None:
    with pytest.raises(AssertionError):
        affirmative("The agent may not suggest it at most once per change.", "at most once", ("may",))


# --- Acceptance 1 -----------------------------------------------------------

def test_frontmatter_disables_model_invocation_and_openai_yaml_blocks_implicit() -> None:
    front = _frontmatter(_skill())
    assert front["name"] == "expert-mode"
    assert front["disable-model-invocation"] is True
    description = " ".join(str(front["description"]).split())
    assert "Only for the user typing /loom-code:expert-mode" in description
    assert "advanced" not in description.lower()

    policy = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    assert policy["policy"]["allow_implicit_invocation"] is False


def test_skill_text_evaluates_no_gate() -> None:
    text = _skill()
    assert "<!-- gate:" not in text
    invoked = set(re.findall(r"loom_checker\.py (selection \w+|[\w-]+)", text))
    assert invoked == {"selection propose", "selection show", "selection cancel"}
    flat = _flat(text)
    assert "Never evaluate a gate" in flat
    assert "only from `loom_checker.py selection show <change-id>`" in flat


def test_skill_procedure_maps_proposes_reports_withdraws_and_relapses() -> None:
    text = _skill()
    flat = _flat(text)
    affirmative(text, "also skips spec, plan and blind-run", ("skipping",))
    affirmative(text, "selection propose <change-id> --origin user --skip", ("run",))
    affirmative(text, "the code shown", ("type",))
    affirmative(text, "hook trust", ("name",))
    affirmative(text, "selection cancel <change-id>", ("run",))
    affirmative(text, "re-run `loom_checker.py selection propose`", ("tell", "lapsed"))
    assert "keep the full process" in flat
    assert "any language" in flat
    assert "stops shortcuts, not deliberately disguised commands" in flat
    assert "recorded only when Review hands it to the checker" in flat


# --- Acceptance 4 -----------------------------------------------------------

def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    for name, branch in (("base.txt", None), ("work.txt", "feature")):
        if branch:
            _git(repo, "checkout", "-q", "-b", branch)
        (repo / name).write_text(name, encoding="utf-8")
        _git(repo, "add", name)
        _git(repo, "commit", "-q", "-m", name)
    return repo


def _selection(repo: Path, *args: str, stdin: str = "") -> subprocess.CompletedProcess:
    result = subprocess.run([sys.executable, str(CHECKER), "selection", *args],
                            capture_output=True, text=True, cwd=str(repo), input=stdin)
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

    # Control: the same store binds once the user types the code, so the
    # assertions above can fail.
    code = [e for e in selection.read_events(repo, CHANGE) if e["event"] == "proposal"][-1]["code"]
    _prompt(repo, f"/loom-code:expert-mode OK {code}", "prompt-typed")
    assert json.loads(_selection(repo, "show", CHANGE).stdout)["skip"] == ["reviewers", "adversarial"]


@pytest.mark.parametrize("station", STATIONS)
def test_station_text_suggests_once_without_waiting(station: str) -> None:
    text = (PLUGIN_ROOT / "skills" / station / "SKILL.md").read_text(encoding="utf-8")
    sentence = affirmative(text, "at most once per change", ("may suggest",))
    assert "`loom_checker.py selection propose <change-id> --origin agent`" in sentence
    assert "keeps working on the full process at once" in sentence
    assert 'a plain "yes" binds nothing' in sentence
    assert _flat(text).count("at most once per change") == 1
