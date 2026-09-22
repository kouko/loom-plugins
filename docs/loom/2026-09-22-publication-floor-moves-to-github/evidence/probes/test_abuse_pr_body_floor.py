"""Adversarial probe: can the nine-section PR-body floor be bypassed?

REQ-1, REQ-5 and REQ-6 put one validator (`validate_contextual_pr_body`)
behind the CI check, `publish` and `land`. The attack: feed it bodies whose
headings a reader of the rendered PR never sees, or whose sections render
empty, and the near-miss look-alikes (case, zero-width, NBSP, full-width,
trailing space) that must still be refused.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-22-publication-floor-moves-to-github/evidence/probes/test_abuse_pr_body_floor.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.rule_checks.publish import CONTEXTUAL_PR_HEADINGS
from loom_checker.rule_checks.publish import validate_contextual_pr_body


def good_body(heading_line=lambda h: f"## {h}", content=None) -> str:
    parts = []
    for heading in CONTEXTUAL_PR_HEADINGS:
        text = content(heading) if content else (
            f"The {heading.lower()} section says something concrete here.")
        parts.append(f"{heading_line(heading)}\n\n{text}\n")
    return "\n".join(parts)


def test_body_floor_good_body_accepted() -> None:
    """Control: the well-formed nine-section body passes."""
    assert validate_contextual_pr_body(good_body()) is None


@pytest.mark.parametrize("name, mutate", [
    ("lowercase", lambda h: f"## {h.lower()}"),
    ("zero-width", lambda h: f"## {h[0]}​{h[1:]}"),
    ("nbsp-after-hashes", lambda h: f"## {h}"),
    ("fullwidth-hash", lambda h: f"＃＃ {h}"),
    ("trailing-space", lambda h: f"## {h} "),
    ("h3", lambda h: f"### {h}"),
    ("cyrillic-o", lambda h: "## " + h.replace("o", "о")),
])
def test_body_floor_lookalike_heading_refused(name: str, mutate) -> None:
    """A look-alike of every heading must not satisfy the floor."""
    # cyrillic-o leaves headings without an `o` genuine; the first with one must fault.
    assert validate_contextual_pr_body(good_body(heading_line=mutate)) is not None, name


def test_body_floor_headings_inside_html_comment_refused() -> None:
    """GitHub renders nothing inside `<!-- ... -->`. A body whose nine
    headings and their content all sit inside one HTML comment renders as an
    empty PR description, so it must not pass the floor. The validator
    already strips comments when judging emptiness, so comment text is not
    content by its own rule."""
    body = "<!--\n" + good_body() + "\n-->\n"
    assert validate_contextual_pr_body(body) is not None, (
        "a body rendered entirely empty (all nine sections inside one HTML "
        "comment) passes the nine-section floor")


def test_pr_floor_hidden_body_exits_one(tmp_path: Path, monkeypatch) -> None:
    """The same hidden body through the CI entry point: `pr-floor` must exit 1."""
    from loom_checker.command_handlers.pr_floor import cmd_pr_floor

    body_file = tmp_path / "body.md"
    body_file.write_text("<!--\n" + good_body() + "\n-->\n", encoding="utf-8")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.chdir(Path(__file__).resolve().parents[5])
    err = io.StringIO()
    code = cmd_pr_floor(["--body-file", str(body_file), "--base", "HEAD", "--head", "HEAD"],
                        io.StringIO(), err)
    assert code == 1, "pr-floor passes a PR body that renders empty"


def test_body_floor_invisible_link_section_refused() -> None:
    """A section whose only content is an empty-text link renders as nothing
    visible; the eight-alphanumeric floor counts the URL instead."""
    body = good_body(content=lambda h: "[](https://example.com/aaaaaaaa)"
                     if h == "Risks and rollback" else f"The {h} section says something real.")
    assert validate_contextual_pr_body(body) is not None, (
        "a section rendering no visible text passes the emptiness floor")


def test_body_floor_error_line_cannot_start_workflow_command() -> None:
    """The refusal quotes a PR-controlled heading. On CI the runner parses
    `::command::` lines from the step's output; the fault must stay on one
    line so a hostile heading cannot open a workflow command."""
    hostile = "## Context\n\nThe context section says something concrete here.\n\n" \
              "## x ::error::injected\n"
    fault = validate_contextual_pr_body(hostile) or ""
    assert "\n" not in fault and "\r" not in fault
    assert not any(line.startswith("::") for line in f"BLOCK ci.pr-floor: PR body {fault}".split("\n"))
