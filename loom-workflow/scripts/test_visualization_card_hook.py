"""Tests for the loom-workflow UserPromptSubmit hook `hooks/visualization-card`.

Covers plan W2-05 acceptance 9 (A9) as unit tests:
  - positive `enabled-toolkit-prints-coexist-card`
  - boundary `disabled-or-other-project-prints-full-card`

Acceptance 8 (A8) cases `comparison-prompt-stream-shows-skill-call-and-table`
and `trivial-control-no-skill-call-no-diagram` are blind-run protocol (spec
design decision "Unprompted-use protocol"), not unit tests: they need a live
agent session and its event stream. Here only the card content they rely on
is checked (the full card names `loom-visualization` and its comparison and
flow triggers).

The hook runs as a subprocess via `python3 -I` with an isolated HOME,
config dir and project dir passed through the environment.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
HOOK = PLUGIN_ROOT / "hooks" / "visualization-card"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
ASSETS = PLUGIN_ROOT / "skills" / "loom-visualization" / "assets"
FULL_CARD = ASSETS / "trigger-card.md"
COEXIST_CARD = ASSETS / "trigger-card-coexist.md"
TOOLKIT_FIXTURE = Path(__file__).resolve().parent / "fixtures_ascii_graph_trigger_card.md"

KEY = "ascii-graph-toolkit@monkey-skills"

# Shape vocabulary used to read trigger phrases. Keys are shape names; values
# are patterns naming that shape. Non-toolkit shapes are included so the
# equality assertion on the toolkit card is not vacuous.
SHAPES = {
    "flow": r"\bflows?\b",
    "state machine": r"\bstate machines?\b",
    "architecture": r"\barchitectures?\b",
    "box-drawing/ASCII diagram": r"box-drawing|\bascii\b",
    "sequence": r"\bsequences?\b",
    "option comparison": r"\bcomparisons?\b",
    "branching decision": r"\bbranching\b",
    "reasoning chain": r"\breasoning chains?\b",
    "timeline": r"\btimelines?\b",
    "data model": r"\bdata models?\b",
}
TOOLKIT_SHAPES = {"flow", "state machine", "architecture", "box-drawing/ASCII diagram"}


# ---------- helpers ----------

def _sentences(text):
    body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith(("<!--", "#")))
    body = re.sub(r"\s+", " ", body)
    return [s for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]


def _trigger_phrases(text):
    """Sentences that instruct invoking a skill."""
    return [s for s in _sentences(text) if re.search(r"\binvo[kc]", s, re.I)]


def _shapes_named(sentences):
    found = set()
    for s in sentences:
        for name, pat in SHAPES.items():
            if re.search(pat, s, re.I):
                found.add(name)
    return found


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(obj if isinstance(obj, str) else json.dumps(obj), encoding="utf-8")


def _install(config, entries):
    _write(config / "plugins" / "installed_plugins.json",
           {"version": 2, "plugins": {KEY: entries}})


@pytest.fixture
def env_dirs(tmp_path):
    home = tmp_path / "home"
    project = tmp_path / "project"
    (home / ".claude").mkdir(parents=True)
    project.mkdir()
    return home, home / ".claude", project


def _run(home, project=None, stdin=None, cwd=None, config_dir=None, extra_env=None):
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
    env["HOME"] = str(home)
    env["CLAUDE_PLUGIN_ROOT"] = str(PLUGIN_ROOT)
    if project is not None:
        env["CLAUDE_PROJECT_DIR"] = str(project)
    if config_dir is not None:
        env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    if extra_env:
        env.update(extra_env)
    if stdin is None:
        stdin = json.dumps({"hook_event_name": "UserPromptSubmit", "session_id": "s1",
                            "cwd": str(cwd or project or home)})
    proc = subprocess.run([sys.executable, "-I", str(HOOK)], input=stdin, capture_output=True,
                          text=True, env=env, cwd=str(cwd or home), timeout=30)
    assert proc.returncode == 0, proc.stderr
    return proc


def _context(proc):
    data = json.loads(proc.stdout)
    ctx = data["hookSpecificOutput"]["additionalContext"]
    assert data["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
    assert data["additional_context"] == ctx
    assert data["additionalContext"] == ctx
    return ctx


def _is_full(ctx):
    return ctx.strip() == FULL_CARD.read_text(encoding="utf-8").strip()


def _is_coexist(ctx):
    return ctx.strip() == COEXIST_CARD.read_text(encoding="utf-8").strip()


# ---------- registration ----------

def test_hooks_json_registers_user_prompt_submit_and_keeps_post_tool_use():
    """A1 positive/negative: the card fires on every prompt, no longer on SessionStart."""
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
    assert hooks["PostToolUse"] == [{
        "matcher": "Write|Edit",
        "hooks": [{"type": "command",
                   "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-skill-folder-structure.sh"}],
    }]
    assert "SessionStart" not in hooks
    (entry,) = hooks["UserPromptSubmit"]
    assert "matcher" not in entry
    (h,) = entry["hooks"]
    assert h["type"] == "command"
    assert h["command"] == '"${CLAUDE_PLUGIN_ROOT}/hooks/visualization-card"'
    assert h["async"] is False
    # A5: a hung read must not stall every prompt past a short host timeout (seconds).
    # Source: Claude Code hooks reference, `timeout` in seconds: https://code.claude.com/docs/en/hooks
    assert h["timeout"] == 5


def test_hook_is_executable_python3_script():
    assert os.access(HOOK, os.X_OK)
    assert HOOK.read_text(encoding="utf-8").splitlines()[0] == "#!/usr/bin/env python3"


# ---------- A9 positive: enabled-toolkit-prints-coexist-card ----------

def test_enabled_toolkit_prints_coexist_card(env_dirs):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    ctx = _context(_run(home, project))
    assert _is_coexist(ctx)
    assert not _is_full(ctx)  # A2 negative: only one diagram trigger reaches the agent


def test_project_scope_detected_from_subdirectory_session(env_dirs):
    home, config, project = env_dirs
    sub = project / "pkg" / "deep"
    sub.mkdir(parents=True)
    _install(config, [{"scope": "project", "installPath": "/x", "version": "0.6.0",
                       "projectPath": str(project)}])
    _write(project / ".claude" / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_coexist(_context(_run(home, project, cwd=sub)))


def test_stdin_cwd_is_project_root_fallback(env_dirs):
    home, config, project = env_dirs
    _install(config, [{"scope": "local", "installPath": "/x", "version": "0.6.0",
                       "projectPath": str(project)}])
    _write(project / ".claude" / "settings.local.json", {"enabledPlugins": {KEY: True}})
    assert _is_coexist(_context(_run(home, None, cwd=project)))


def test_config_dir_override_is_used(env_dirs, tmp_path):
    home, _default_config, project = env_dirs
    override = tmp_path / "alt-config"
    _install(override, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(override / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_coexist(_context(_run(home, project, config_dir=override)))


def test_config_dir_override_ignores_default_dir(env_dirs, tmp_path):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    empty = tmp_path / "empty-config"
    empty.mkdir()
    assert _is_full(_context(_run(home, project, config_dir=empty)))


# ---------- A9 boundary: disabled-or-other-project-prints-full-card ----------

def test_disabled_prints_full_card(env_dirs):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    _write(project / ".claude" / "settings.local.json", {"enabledPlugins": {KEY: False}})
    assert _is_full(_context(_run(home, project)))


def test_other_project_scope_prints_full_card(env_dirs, tmp_path):
    home, config, project = env_dirs
    other = tmp_path / "other"
    other.mkdir()
    _install(config, [{"scope": "project", "installPath": "/x", "version": "0.6.0",
                       "projectPath": str(other)}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_full(_context(_run(home, project)))


def test_not_installed_prints_full_card(env_dirs):
    home, config, project = env_dirs
    _write(config / "plugins" / "installed_plugins.json", {"version": 2, "plugins": {}})
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_full(_context(_run(home, project)))


@pytest.mark.parametrize("target", ["installed", "settings"])
def test_malformed_json_prints_full_card(env_dirs, target):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    bad = config / ("plugins/installed_plugins.json" if target == "installed" else "settings.json")
    _write(bad, "{not json")
    assert _is_full(_context(_run(home, project)))


@pytest.mark.parametrize("stdin", ["", "{not json", "[1, 2]"])
def test_empty_or_malformed_stdin_still_emits_json(env_dirs, stdin):
    home, _config, project = env_dirs
    assert _is_full(_context(_run(home, project, stdin=stdin)))


def test_unreadable_card_exits_zero_with_empty_context(env_dirs, tmp_path):
    """A5 boundary: a hook away from its assets still exits 0, empty context."""
    home, _config, project = env_dirs
    lonely = tmp_path / "plugin" / "hooks" / "visualization-card"
    lonely.parent.mkdir(parents=True)
    lonely.write_bytes(HOOK.read_bytes())
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
    env.update(HOME=str(home), CLAUDE_PROJECT_DIR=str(project))
    proc = subprocess.run([sys.executable, "-I", str(lonely)], input="{not json",
                          capture_output=True, text=True, env=env, cwd=str(home), timeout=30)
    assert proc.returncode == 0, proc.stderr
    assert _context(proc) == ""


# ---------- card content ----------

# Key phrase per plain-language rule (spec design decision "agreed card content").
PLAIN_RULES = {
    "user's language": r"in their language",
    "1 conclusion first": r"conclusion and what it means for the user",
    "2 plain words, term in brackets": r"plain words[^.]*in brackets",
    "3 literal, no metaphors": r"literal[^.]*no metaphors",
    "4 tables or diagrams": r"tables or diagrams",
    "plainer explanation reference": r"plainer explanation[^.]*references/plain-language\.md",
}


NEGATION = re.compile(r"\b(?:never|not|no|avoid|don't)\b", re.I)
# Rule 3's ban list is the one negation a rule sentence must keep.
METAPHOR_BAN = 'no metaphors, analogies, "like" or "imagine"'


def rule_polarity_errors(text):
    """Missing or negated rule sentences in a card; empty = every rule stated affirmatively."""
    errors = []
    sentences = _sentences(text)
    for rule, pattern in PLAIN_RULES.items():
        hits = [s for s in sentences if re.search(pattern, s, re.I)]
        if not hits:
            errors.append(f"{rule}: missing")
        for s in hits:
            if rule.startswith("3") and METAPHOR_BAN not in s:
                errors.append(f"{rule}: metaphor ban list missing")
            if NEGATION.search(s.replace(METAPHOR_BAN, "")):
                errors.append(f"{rule}: negated: {s}")
    return errors


@pytest.mark.parametrize("card", [FULL_CARD, COEXIST_CARD], ids=["full", "coexist"])
@pytest.mark.parametrize("rule", sorted(PLAIN_RULES))
def test_cards_carry_plain_language_rules(card, rule):
    """A1 positive: each card carries the four plain-language rules, stated affirmatively."""
    text = card.read_text(encoding="utf-8")
    body = " ".join(_sentences(text))
    assert re.search(PLAIN_RULES[rule], body, re.I), rule
    assert [e for e in rule_polarity_errors(text) if e.startswith(rule + ":")] == []


def test_affirmative_card_rule_accepted():
    """A1 positive affirmative-card-rule-accepted: a synthetic affirmative card passes."""
    card = ("Reply to the user in their language. 1) First sentence: the conclusion and what it "
            "means for the user. 2) Use plain words, with the term in brackets. 3) Be literal: "
            'who does what; no metaphors, analogies, "like" or "imagine". 4) Use tables or '
            "diagrams for comparisons. For a plainer explanation, read "
            "`references/plain-language.md` first.")
    assert rule_polarity_errors(card) == []


@pytest.mark.parametrize("old, new", [
    ("in their language.", "never in their language."),
    ("3) Be literal:", "3) Never literal:"),
    ("4) Use tables or", "4) Avoid tables or"),
    ('; no metaphors, analogies, "like" or "imagine".', "."),
], ids=["language", "literal", "tables", "metaphor-ban-removed"])
def test_negated_card_rule_rejected(old, new):
    """A1 negative negated-card-rule-rejected: a rule flipped to its opposite is caught."""
    text = FULL_CARD.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert old in flat
    assert rule_polarity_errors(flat.replace(old, new, 1)) != []


def _rules_one_to_three(card):
    body = " ".join(_sentences(card.read_text(encoding="utf-8")))
    match = re.search(r"Reply to the user.*?(?= 4\))", body)
    assert match, card.name
    return match.group(0)


def test_coexist_card_rules_one_to_three_match_full_card_word_for_word():
    """The coexist card is what toolkit users receive; rules 1-3 must not be compressed."""
    assert _rules_one_to_three(COEXIST_CARD) == _rules_one_to_three(FULL_CARD)

MAX_CARD_WORDS = 150


def card_word_errors(text):
    """Word-cap error for a card; empty = within the cap."""
    count = len(text.split())
    return [f"{count} words, cap {MAX_CARD_WORDS}"] if count > MAX_CARD_WORDS else []


@pytest.mark.parametrize("card", [FULL_CARD, COEXIST_CARD], ids=["full", "coexist"])
def test_cards_at_most_150_words(card):
    assert card_word_errors(card.read_text(encoding="utf-8")) == []


def test_card_over_150_words_fails():
    """A1 negative card-over-150-words-fails: a card padded past the cap is caught."""
    text = COEXIST_CARD.read_text(encoding="utf-8")
    padding = " word" * (MAX_CARD_WORDS + 1 - len(text.split()))
    assert card_word_errors(text + padding) != []


GUIDE = "references/plain-language.md"
# Scope shared word-for-word with rule 5 of the guide (spec REQ-7).
DECISION_SCOPE = "asking or answering how to do something"
INLINE_RULE_PHRASES = (DECISION_SCOPE, "2+ workable options", "in a table", "recommend", GUIDE)


def inline_decision_rule_errors(text):
    """Error when no card sentence states the decision rule inline; empty = stated."""
    ok = any(all(p in s for p in INLINE_RULE_PHRASES) and not NEGATION.search(s)
             for s in _sentences(text))
    return [] if ok else ["decision rule not stated inline"]


@pytest.mark.parametrize("card", [FULL_CARD, COEXIST_CARD], ids=["full", "coexist"])
def test_both_cards_state_inline_decision_rule(card):
    """A1/A7 positive both-cards-state-inline-decision-rule."""
    assert inline_decision_rule_errors(card.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("card", [
    "Reply to the user in their language. Before plainer explanations or decisions between "
    "approaches, read loom-visualization's `references/plain-language.md`.",
    "When asking or answering how to do something, never offer 2+ workable options in a table "
    "or recommend one; read loom-visualization's `references/plain-language.md` first.",
], ids=["routing-only", "negated"])
def test_card_without_inline_decision_rule_fails(card):
    """A7 negative: a card that only routes decisions to the guide, or negates the rule, is caught."""
    assert inline_decision_rule_errors(card) != []


def test_coexist_card_skip_sentence_names_the_skill():
    """'Skip it' was ambiguous next to the ascii-graph card; the skip sentence names the skill."""
    body = " ".join(_sentences(COEXIST_CARD.read_text(encoding="utf-8")))
    assert "Skip loom-visualization for one-paragraph answers" in body
    assert "Skip it" not in body


def test_full_card_names_skill_and_comparison_and_flow_triggers():
    phrases = _trigger_phrases(FULL_CARD.read_text(encoding="utf-8"))
    assert any("loom-visualization" in s for s in phrases)
    named = _shapes_named(phrases)
    assert {"option comparison", "flow", "box-drawing/ASCII diagram"} <= named


def test_toolkit_card_trigger_shapes_are_the_expected_four():
    phrases = _trigger_phrases(TOOLKIT_FIXTURE.read_text(encoding="utf-8"))
    assert phrases
    assert _shapes_named(phrases) == TOOLKIT_SHAPES


def test_coexist_card_trigger_phrases_do_not_overlap_toolkit():
    text = COEXIST_CARD.read_text(encoding="utf-8")
    phrases = _trigger_phrases(text)
    assert any("loom-visualization" in s for s in phrases)
    named = _shapes_named(phrases)
    toolkit = _shapes_named(_trigger_phrases(TOOLKIT_FIXTURE.read_text(encoding="utf-8")))
    assert not (named & toolkit)
    assert {"option comparison", "branching decision", "reasoning chain",
            "timeline", "sequence", "data model"} <= named
    assert re.search(r"\bquantit", " ".join(phrases), re.I)
    assert re.search(r"reasoning pages?", " ".join(phrases), re.I)
    assert re.search(r"ascii-graph", text, re.I)


def test_coexist_card_picks_markdown_table_not_mermaid():
    """The hook host always has a shell, so the Mermaid gate never allows Mermaid there."""
    sentences = _sentences(COEXIST_CARD.read_text(encoding="utf-8"))
    assert not re.search(r"mermaid", " ".join(sentences), re.I)
    # Meaning pinned, not wording: comparisons get a markdown table, ASCII only when needed.
    assert any(re.search(r"\bcomparisons?\b", s, re.I) and "markdown table" in s
               and "ASCII only when needed" in s for s in sentences)


def test_coexist_card_box_drawing_split_between_skill_checks_and_toolkit_card():
    """Prescribed box drawing uses loom-visualization's align.py; the toolkit card keeps three shapes."""
    sentences = _sentences(COEXIST_CARD.read_text(encoding="utf-8"))
    body = " ".join(sentences)
    # Meaning pinned, not wording: align.py verifies box diagrams loom-visualization prescribes.
    assert any(re.search(r"\b[Vv]erif", s) and re.search(r"\bbox\b|box-drawing", s)
               and "prescribed" in s and "loom-visualization" in s
               and "`scripts/align.py`" in s for s in sentences)
    assert re.search(r"the ascii-graph card covers flows, state machines and architecture;", body)
    assert not re.search(r"ascii-graph card covers[^.]*sequences", body)
