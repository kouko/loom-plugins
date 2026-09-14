"""W2-01 -- write-plan's station text and the plan template cite the plan
row of the artifact charter (`contract/manifest.yaml`, `artifacts.plan.charter`)
instead of restating its caps or its edits-after policy list.

Three literals are load-bearing and pinned here: the SKILL.md sentence
naming `artifacts.plan.charter`, the `loom_checker.py plan
docs/loom/<change-id>/plan.md` command line the station runs before the
plan commit, and the template's one-sentence spec-change-path comment.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from prose_pin import NEGATION_RE

REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / "loom-code" / "skills" / "write-plan" / "SKILL.md"
TEMPLATE = REPO / "loom-code" / "contract" / "templates" / "plan.md"
SECOND_VENDOR_REFERENCE = (
    REPO
    / "loom-code"
    / "skills"
    / "write-plan"
    / "references"
    / "second-vendor-ask-and-docs-lint.md"
)


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"section {heading!r} missing"
    return match.group(0)


def test_decision_boundary_owns_implementation_not_product_behaviour() -> None:
    section = _section(SKILL.read_text(encoding="utf-8"), "## Decision boundary")
    low = section.lower()
    for concept in (
        "confirmed specification",
        "simplest reversible implementation",
        "product gap",
        "clarification",
        "invent",
        "product behaviour",
    ):
        assert concept in low, concept
    assert len(section.split()) <= 90


def _has_negation(sentence: str) -> bool:
    return bool(NEGATION_RE.search(sentence))


def _flat_sentences(text: str) -> list[str]:
    flat = " ".join(text.split())
    return [p for p in re.split(r"(?<=[.!?])\s+", flat) if p.strip()]


def test_skill_names_the_plan_charter_row() -> None:
    text = SKILL.read_text(encoding="utf-8")
    hits = [
        s for s in _flat_sentences(text)
        if "artifacts.plan.charter" in s and not _has_negation(s)
    ]
    assert hits, (
        "SKILL.md has no affirmative sentence naming artifacts.plan.charter "
        "-- the task fields' content kinds and caps must cite the charter "
        "row instead of restating it"
    )


def test_skill_runs_the_plan_checker_before_commit() -> None:
    text = SKILL.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "loom_checker.py plan docs/loom/<change-id>/plan.md" in flat, (
        "SKILL.md no longer names the `plan docs/loom/<change-id>/plan.md` "
        "checker command run before the plan commit"
    )


def test_template_states_the_spec_change_path() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    sentence = (
        "When a spec requirement changes after this commit, the un-landed "
        "tasks it touches are replaced and the reason is named in the "
        "commit message."
    )
    assert sentence in flat, (
        "contract/templates/plan.md no longer carries the spec-change-path "
        "sentence under its Task DAG heading"
    )
    assert not _has_negation(sentence), (
        "the spec-change-path sentence carries a negation token"
    )


def test_template_spec_change_comment_under_task_dag_heading() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    dag_idx = text.index("## Task DAG")
    comment_idx = text.index(
        "When a spec requirement changes after this commit", dag_idx
    )
    next_heading = text.find("## ", dag_idx + len("## Task DAG"))
    assert dag_idx < comment_idx, (
        "the spec-change sentence must sit at or after the Task DAG heading"
    )
    if next_heading != -1:
        assert comment_idx < next_heading, (
            "the spec-change sentence has drifted past the Task DAG section"
        )


def test_matcher_spec_change_sentence_negated_rejected() -> None:
    sentence = (
        "When a spec requirement changes after this commit, the un-landed "
        "tasks it touches are never replaced and the reason is not named "
        "in the commit message."
    )
    assert _has_negation(sentence)


# --- W0-01/W2-01 fix round: an engineering spec has a home other than the
# ninth artifact the branch-end finding warned against --------------------


def test_skill_names_the_engineering_spec_path() -> None:
    text = SKILL.read_text(encoding="utf-8")
    sentence = (
        "When a task's rationale outgrows its Risk line, write "
        "`docs/loom/<change-id>/spec.md` from "
        "`contract/templates/spec-minimal.md` — Requirements one per "
        "Acceptance line, Design decision one line per agent-decided fork, "
        "Alternatives considered, Current state evidence, UI flows N/A — carrying the template's five sections and leaving the `confirmed-behavior:` line to product changes."
    )
    flat = " ".join(text.split())
    assert sentence in flat, (
        "SKILL.md no longer carries the engineering-spec-for-oversized-"
        "Risk-line sentence in step 4's `no` branch"
    )
    assert not _has_negation(sentence), (
        "the engineering-spec sentence carries a negation token"
    )


def test_matcher_engineering_spec_sentence_negated_rejected() -> None:
    sentence = (
        "When a task's rationale will not fit its Risk line, write "
        "`docs/loom/<change-id>/spec.md` from "
        "`contract/templates/spec-minimal.md` with no `confirmed-behavior:` "
        "line."
    )
    assert _has_negation(sentence)


# --- W1-02 -- suggest is visible after risk evidence, without becoming a
# fourth decision point ----------------------------------------------------


def test_suggest_runs_policy_after_plan_risk_evidence_exists() -> None:
    text = SKILL.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "second_vendor_policy.py" in flat
    assert "after the plan's Risk lines exist" in flat
    assert "recommendation_reasons" in flat
    assert "notice_kind" in flat


def test_suggest_is_non_blocking_and_has_no_background_listener() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "continue without waiting" in flat
    assert "no background listener" in flat
    assert "do not reclassify risk" in flat


def test_ask_still_asks_once_per_full_lane_change() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "second-vendor: ask" in flat
    assert "every full-lane change" in flat
    assert "AskUserQuestion" in text
    assert "request_user_input" in text
    assert "ask_question" not in text  # agy offers no candidate, so it never asks
    assert "render both choices in the user's current conversation language" in flat
    assert "decline this change" in flat
    assert "https://code.claude.com/docs/en/tools-reference" in text
    assert "https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/request_user_input.rs" in text
    assert "這次不使用" not in text
    assert "recommended" in flat


def test_ask_is_host_aware_and_has_complete_fallbacks() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "On Codex, probe `claude` then `gemini`" in flat
    assert "On Claude Code, probe `codex` then `gemini`" in flat
    agy = flat.split("On Antigravity CLI,", 1)[1].split(".", 1)[0]
    assert "probe nothing" in agy
    assert "no verified second-vendor runner yet" in agy
    assert "no such review tool is available" in agy
    for vendor in ("claude", "codex", "gemini"):
        assert f"`{vendor}`" not in agy
    assert "blocking plain-language Markdown question" in flat
    assert "no runnable different-model-family CLI" in flat
    assert "continue without asking" in flat
    assert "第二位讀者" not in text
    assert "second reader" not in text.lower()


def test_suggest_uses_one_cell_markdown_table_with_spacing() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "exactly two blank lines before and after" in flat
    assert "| <heading> |\n|---|\n| <description> |" in text
    assert "one heading and one descriptive cell" in flat
    assert "raw Markdown" in text


def test_small_lane_suggest_is_information_only() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "small lane" in flat
    assert "informational only" in flat
    assert "next-change-only" in flat
    assert "reviewer floor is computed later and independently" in flat
    assert "there is only one reader" not in flat


def test_reference_has_no_none_mode_or_per_change_none_answer() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    assert "second-vendor: <cli> | none" not in text
    assert "`<cli>` / `none`" not in text


def test_confirmed_selection_is_recorded_for_closing_review() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert "selection-confirmed" in flat
    assert "plan's `## Risks` section" in flat
    assert "Closing Review consumes" in flat
    assert "before Closing Review starts" in flat
    assert "`plan-maintained`" in flat
    assert "commit that plan edit" in flat
    assert "before committing the plan" not in flat


# --- typed-branch-names W1-02 -- the branch is `<type>/<change-id>` -------


def test_write_plan_names_typed_branch_and_types() -> None:
    section = _section(
        SKILL.read_text(encoding="utf-8"), "## Step 6 — Commit and hand off"
    )
    flat = " ".join(section.split())
    assert "git switch -c <type>/<change-id>" in flat
    sentences = _flat_sentences(section)
    hits = [
        s for s in sentences
        if "pick" in s and "same type" in s and "commit" in s
        and "PR title" in s and "squash-merge" in s and not _has_negation(s)
    ]
    assert hits, (
        "Step 6 has no affirmative sentence saying the agent picks the type "
        "and reuses it in the PR title, which becomes the squash-merge commit"
    )
    # The type list sits in the pick sentence and matches implementer.md.
    listed = set(re.findall(r"`([a-z]+)`", hits[0]))
    assert listed == {"feat", "fix", "docs", "refactor", "test", "chore", "ci"}, listed
    own = [
        s for s in sentences
        if "task commits" in s and "own" in s and "Conventional Commits" in s
        and "implementer contract" in s and not _has_negation(s)
    ]
    assert own, (
        "Step 6 must say individual task commits keep their own Conventional "
        "Commits type as the implementer contract sets it"
    )
    fixed = [
        s for s in sentences
        if "`docs(loom):`" in s and "intent" in s and "plan commits" in s
        and "fixed form" in s
    ]
    assert fixed, "Step 6 must say the `docs(loom):` intent and plan commits keep their fixed form"


# Split literals so a repo grep for the bare form never matches this file.
_BARE_BRANCH_RE = re.compile(
    r"(?:switch (?:-c|--create)|checkout -[bB]|git branch|worktree add -b"
    r"|branch named)\s+[`'\"]?" + "<change" + r"-id>"
)

_CID = "<change" + "-id>"


@pytest.mark.parametrize(
    "line",
    [
        f"git switch -c {_CID}",
        f"git switch --create {_CID}",
        f"git switch -c `{_CID}`",
        f"git switch -c '{_CID}'",
        f'git switch -c "{_CID}"',
        f"git checkout -b {_CID}",
        f"git checkout -B {_CID}",
        f"git branch {_CID}",
        f"git worktree add -b {_CID} ../wt",
        f"create a branch named `{_CID}`",
    ],
)
def test_bare_branch_re_catches_spelling(line: str) -> None:
    assert _BARE_BRANCH_RE.search(line), line


@pytest.mark.parametrize(
    "line",
    [
        f"git switch -c <type>/{_CID}",
        f"git switch --create `<type>/{_CID}`",
        f"git checkout -B <type>/{_CID}",
        f"git worktree add -b <type>/{_CID} ../wt",
        f"create a branch named `<type>/{_CID}`",
        f"write docs/loom/{_CID}/plan.md",
        f"see `docs/loom/{_CID}/spec.md`",
    ],
)
def test_bare_branch_re_ignores_typed_and_path(line: str) -> None:
    assert not _BARE_BRANCH_RE.search(line), line


def test_write_plan_bare_switch_absent() -> None:
    section = _section(
        SKILL.read_text(encoding="utf-8"), "## Step 6 — Commit and hand off"
    )
    assert not _BARE_BRANCH_RE.search(section), _BARE_BRANCH_RE.search(section)


def test_repo_grep_no_bare_branch() -> None:
    hits = []
    for plugin in ("loom-code", "loom-design", "loom-workflow"):
        for path in sorted((REPO / plugin).rglob("*")):
            if path.suffix not in {".md", ".py", ".sh"} or not path.is_file():
                continue
            rel = path.relative_to(REPO)
            if path.name.startswith("CHANGELOG") or {
                "node_modules", "__pycache__"
            } & set(rel.parts):
                continue
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if _BARE_BRANCH_RE.search(line):
                    hits.append(f"{rel}:{n}")
    assert not hits, hits


def test_current_release_metadata_is_synchronized() -> None:
    claude_manifest = json.loads(
        (REPO / "loom-code/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    codex_manifest = json.loads(
        (REPO / "loom-code/.codex-plugin/plugin.json").read_text(encoding="utf-8")
    )
    changelog = (REPO / "loom-code/CHANGELOG.md").read_text(encoding="utf-8")
    agy_manifest = json.loads(
        (REPO / "loom-code/plugin.json").read_text(encoding="utf-8")
    )
    assert claude_manifest["version"] == "3.5.0"
    assert codex_manifest["version"] == "3.5.0"
    assert agy_manifest["version"] == "3.5.0"
    assert "## [3.5.0]" in changelog


@pytest.mark.parametrize(
    ("readme", "label"),
    [
        ("README.md", "**Version**: "),
        ("README.ja.md", "**バージョン**: "),
        ("README.zh-TW.md", "**版本**："),
    ],
)
def test_readme_version_matches_manifest(readme: str, label: str) -> None:
    manifest = json.loads(
        (REPO / "loom-code/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    text = (REPO / "loom-code" / readme).read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(label)}(\d+\.\d+\.\d+)", text, re.M)
    assert match, f"{readme}: version line missing"
    assert match.group(1) == manifest["version"]


def test_root_readme_loom_code_section_version_matches_manifest() -> None:
    manifest = json.loads(
        (REPO / "loom-code/.claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    section = _section((REPO / "README.md").read_text(encoding="utf-8"), "## loom-code")
    match = re.search(r"^Version (\d+\.\d+\.\d+)\.", section, re.M)
    assert match, "README.md ## loom-code: version line missing"
    assert match.group(1) == manifest["version"]


def test_changelog_3_4_1_session_limit_names_publication() -> None:
    changelog = (REPO / "loom-code/CHANGELOG.md").read_text(encoding="utf-8")
    entry = " ".join(
        _section(
            changelog, "## [3.4.1] — 2026-09-15 — expert-mode follow-up cleanup"
        ).split()
    )
    assert "publication" in entry
    assert "selection propose" in entry
    assert "same attended Claude Code session" in entry
    assert "the root README loom-code section, which still read 3.1.4" in entry


def test_agy_host_passes_empty_usable_vendors() -> None:
    text = SECOND_VENDOR_REFERENCE.read_text(encoding="utf-8")
    probe = " ".join(_section(text, "## Availability probe").split())
    order = next(s for s in re.split(r"(?<=[.:])\s+(?=[A-Z])", probe) if "canonical order" in s)
    assert "On Claude Code and Codex" in order
    assert 'On Antigravity CLI, pass `host_vendor: "gemini"`' in probe
    assert "an empty `usable_vendors` list to `second_vendor_policy.py`" in probe
