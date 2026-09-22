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
from prose_pin import has_negation

SCRIPTS = Path(__file__).resolve().parent
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
    invoked = set(re.findall(r"loom_checker\.py (selection [\w-]+|[\w-]+)", text))
    assert invoked == {"selection propose", "selection show", "selection cancel",
                       "selection skipped-review"}
    flat = _flat(text)
    assert "Never evaluate a gate" in flat
    assert "only from `loom_checker.py selection show <change-id>`" in flat


def test_skill_procedure_maps_proposes_reports_withdraws_and_relapses() -> None:
    text = _skill()
    flat = _flat(text)
    affirmative(text, "selection propose <change-id> --origin user --skip", ("run",))
    affirmative(text, "the code shown", ("type",))
    affirmative(text, "hook trust", ("name",))
    affirmative(text, "selection cancel <change-id>", ("run",))
    affirmative(text, "re-run `loom_checker.py selection propose`", ("tell", "lapsed"))
    assert "keep the full process" in flat
    assert "any language" in flat
    assert "Local hooks only remind" in flat
    assert "recorded only when `closing-review` hands it to the checker" in flat


def test_skill_round1_boundary_intent_skip_and_withdrawal_split() -> None:
    text = _skill()
    flat = _flat(text)
    assert "--skip intent" not in flat
    assert "`intent`, `spec`" not in flat
    affirmative(text, "the intent is always kept", ("say",))
    # Literal pin, not affirmative(): the bullet's own "no step" / "no
    # confirmation line" are negation tokens the prose-pin helper rejects.
    assert ("A word that is no step (other than the intent, handled above): name the "
            "item, ask the user to rephrase") in flat
    assert "another selected step needs" not in flat
    affirmative(text, "show the table of the remaining steps", ("say",))
    boundary = _flat(text.split("## Boundary", 1)[1])
    affirmative(boundary, "a typed confirmation stays unrecorded", ("on antigravity cli",))
    sentence = affirmative(boundary, "leave out the confirmation line", ("say",))
    assert "selections take effect only where prompts are captured" in sentence
    assert "keep the full process" in sentence
    assert "hook trust" not in _flat(boundary)
    assert ("`loom_checker.py selection skipped-review` lists merged changes on the default "
            "branch whose attestation skipped reviewers.") in boundary
    assert ("In a checkout without its records, the selection shows as `stale` on the PR; "
            "publishing still proceeds.") in boundary
    assert "a fresh clone refuses it" not in boundary
    assert ("Never evaluate a gate. `finalize-review` re-reads the records and waives only a "
            "bound skip; `publish` discloses the status.") in boundary
    assert ("Local hooks only remind; GitHub rules and the PR-floor check are the trust "
            "boundary.") in boundary
    assert "independent CI stays the trust boundary" not in boundary
    # Acceptance 2: confirmation, finalization and publication share one session,
    # and a new session re-proposes before the user confirms again.
    same = affirmative(boundary, "the same attended Claude Code session", ("must",))
    assert "Confirmation, finalization and publication must all run" in same
    renew = affirmative(boundary, "have the user type the confirmation again", ("re-run",))
    assert "In a new session, re-run `loom_checker.py selection propose`" in renew
    assert ("a confirmation typed before `selection propose` has run in this session "
            "binds nothing; the code shown may be the same as before.") in renew
    assert "reusing the old code" not in boundary
    assert "finalization in another session applies the full process" not in boundary
    for phrase in (
        "A nested unattended session (such as `claude -p`, even wrapped in `timeout`) "
        "never binds.",
        "Codex exports no session variable, so on Codex only the command-text guard applies.",
    ):
        assert phrase in boundary, phrase
    affirmative(text, "only confirm the full process resumed", ("withdraws",))
    affirmative(text, "the hook's lists differed from the table shown", ("show",))
    cancel = next(s for s in re.split(r"(?<=\.)\s+", flat) if "selection cancel <change-id>" in s)
    assert "other withdrawal wording" in cancel
    assert "show the table again" not in cancel


def test_readme_lists_expert_mode() -> None:
    row = ("User-invoked only: choose which Loom steps one change runs or skips; "
           "binds on a typed confirmation")
    plugin_readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    assert "[`expert-mode`](skills/expert-mode/SKILL.md) | " + row in plugin_readme
    assert "**Skills**: 5 stations + 1 router + 1 user-invoked" in plugin_readme
    for name, count, role in (
        ("README.ja.md", "5 ステーション + 1 ルーター + 1 ユーザー起動",
         "ユーザーが明示的に呼び出す場合のみ"),
        ("README.zh-TW.md", "5 個站 + 1 個入口路由 + 1 個使用者呼叫",
         "僅限使用者主動呼叫"),
    ):
        translated = (PLUGIN_ROOT / name).read_text(encoding="utf-8")
        assert count in translated, name
        assert "| [`expert-mode`](skills/expert-mode/SKILL.md) | " + role in translated, name
    root_readme = (PLUGIN_ROOT.parent / "README.md").read_text(encoding="utf-8")
    assert "| `expert-mode` | " + row in root_readme


def test_changelog_names_failure_sources_and_limits() -> None:
    changelog = (PLUGIN_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    entry = _flat(changelog.split("## [3.4.0]", 1)[1].split("\n## [", 1)[0])
    assert "skipped-review ledger" not in entry
    for phrase in (
        "failure events recorded by `finalize-review` and `selection record-failure`",
        "`loom_checker.py selection skipped-review` lists merged changes that skipped reviewers",
        "a fresh clone refuses it",
        "Codex older than PR #18391",
        "only when its prompt comes from the attended session that proposed it",
        "an unattended hook process refuses to bind",
        "is a further layer and the only one on Codex",
        "confirmation and finalization must share the same Claude Code session",
        "separate from the net mechanism count",
        "The intent is never skippable",
        "expert-mode selections do not take effect on Antigravity CLI, where the full "
        "process applies",
    ):
        assert phrase in entry, phrase
    root_readme = (PLUGIN_ROOT.parent / "README.md").read_text(encoding="utf-8")
    limits = _flat(root_readme.split("Limits on Antigravity:", 1)[1].split("\n## ", 1)[0])
    assert ("- `expert-mode` selections do not take effect: agy captures no prompt, so "
            "the full process applies.") in limits


def test_expert_mode_keeps_its_typed_confirmation() -> None:
    router = (PLUGIN_ROOT / "skills" / "using-loom-code" / "SKILL.md").read_text(encoding="utf-8")
    assert 'a plain "yes" binds nothing' not in _flat(router)
    assert "Only that typed confirmation applies." in _flat(_skill())
    assert 'A reply such as "yes" or "對" binds nothing' in _flat(_skill())

    sentence = affirmative(_skill(), "the optional typed route", ("is",))
    assert "handled by the station itself" in sentence
    assert "the user still types the confirmation" in sentence
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


SELECTION_READ = "At entry, run `loom_checker.py selection show <change-id>` and omit"
EXPERT_MODE_POINTER = ("[expert-mode](../expert-mode/SKILL.md) stays an optional route "
                       "the user may invoke.")
MOVED_RULES = ("at most once per change", "--origin agent", 'a plain "yes" binds nothing',
               "asks in their own words")


def assert_station_points_to_expert_mode(text: str, pointer: str = EXPERT_MODE_POINTER) -> None:
    """One affirmative sentence reads the bound selection and points to
    expert-mode; the suggestion rules live only in expert-mode."""
    flat = _flat(text)
    assert flat.count(SELECTION_READ) == 1, "selection show step missing or repeated"
    assert flat.count(pointer) == 1, "expert-mode pointer missing or repeated"
    sentence = affirmative(text, "`loom_checker.py selection show <change-id>` and omit", ("run",))
    assert sentence.endswith(pointer), sentence
    for rule in MOVED_RULES:
        assert rule.lower() not in flat.lower(), rule


@pytest.mark.parametrize("station", STATIONS)
def test_station_one_sentence_points_to_expert_mode(station: str) -> None:
    text = (PLUGIN_ROOT / "skills" / station / "SKILL.md").read_text(encoding="utf-8")
    assert_station_points_to_expert_mode(text)


GOOD_STATION = ("Intro. At entry, run `loom_checker.py selection show <change-id>` and omit "
                "only the steps it lists as skipped; " + EXPERT_MODE_POINTER + " Next.")


def test_station_pointer_helper_accepts_the_pointer_sentence() -> None:
    assert_station_points_to_expert_mode(GOOD_STATION)


@pytest.mark.parametrize("mutant", [
    GOOD_STATION.replace(SELECTION_READ, "At entry, omit"),
    GOOD_STATION.replace(" and omit only", " and do not omit"),
    GOOD_STATION.replace(EXPERT_MODE_POINTER, "see expert-mode."),
    GOOD_STATION + " " + GOOD_STATION,
    GOOD_STATION + ' A plain "yes" binds nothing.',
], ids=["station-missing-selection-show-step", "negated", "pointer-missing",
        "repeated", "rule-restated"])
def test_station_pointer_helper_rejects_mutants(mutant: str) -> None:
    with pytest.raises(AssertionError):
        assert_station_points_to_expert_mode(mutant)


def test_expert_mode_holds_the_suggestion_rules_once() -> None:
    text = _skill()
    sentence = affirmative(text, "at most once per change", ("may suggest",))
    assert sentence.startswith(
        "Inside a user-invoked expert-mode session only, the agent may suggest"), sentence
    assert "`loom_checker.py selection propose <change-id> --origin agent`" in sentence
    assert "keeps working on the full process at once" in sentence
    assert ("shows the table and the confirmation line (type `/loom-code:expert-mode` "
            "(Codex: `$expert-mode`) with the code shown)") in sentence
    assert 'a plain "yes" binds nothing' in sentence
    assert _flat(text).count("at most once per change") == 1
    assert _flat(text).count("--origin agent") == 1
