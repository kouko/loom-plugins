"""Adversarial probes for the bare bundled-script path rule in
`check_contract_citations.py` (`find_bare_script_paths` /
`scan_bare_script_paths`).

The rule's stated contract (its source comment): an interpreter run on a
`scripts/` path with no anchor resolves against the working directory, so a
line running `python`/`python3`/`bash`/`sh` on `scripts/` or `./scripts/` is
flagged, fenced code included. Probes that expose an in-contract gap FAIL;
probes the rule survives pass and stay as regressions.
"""
from __future__ import annotations

from pathlib import Path

import pytest

import check_contract_citations as checker


# --- in-contract commands the rule must flag --------------------------------

@pytest.mark.parametrize(
    "line",
    [
        "env python3 scripts/x.py",
        'bash -c "python3 scripts/x.py"',
        "python3\tscripts/x.py",
        "/usr/bin/python3 scripts/x.py",
        ".venv/bin/python ./scripts/x.py",
        "  sh ./scripts/run.sh --flag",
    ],
    ids=["env", "bash-c", "tab", "abs-interp", "venv", "sh-indented"],
)
def test_bare_script_rule_wrapped_interpreter_flagged(line: str) -> None:
    """Interpreter wrappers and separators the regex already covers."""
    assert checker.find_bare_script_paths(line + "\n") == [1]


@pytest.mark.parametrize(
    "line",
    [
        "python3 -u scripts/x.py",
        "python3 -X utf8 scripts/x.py",
        "python3.12 scripts/x.py",
        'python3 "scripts/x.py"',
        "python3 'scripts/x.py'",
    ],
    ids=["flag-u", "flag-X", "versioned", "dquoted", "squoted"],
)
def test_bare_script_rule_flag_or_quoted_path_flagged(line: str) -> None:
    """An interpreter flag, a versioned interpreter name, or a quoted path still
    runs a bare `scripts/` path relative to the working directory."""
    assert checker.find_bare_script_paths(line + "\n") == [1]


def test_bare_script_rule_line_continued_fence_flagged() -> None:
    """A fenced command wrapped with a backslash continuation is one command;
    agents copy it verbatim, so the continuation line must be flagged."""
    text = "```bash\npython3 \\\n  scripts/x.py --flag\n```\n"
    assert checker.find_bare_script_paths(text) != []


def test_bare_script_rule_capitalised_prose_not_flagged() -> None:
    """Case-insensitive matching turns ordinary prose that names a language
    before a folder into a command hit; prose is not a command."""
    text = (
        "The bundled Python scripts/ folder holds the helpers.\n"
        "Bash scripts/ live beside the skill.\n"
    )
    assert checker.find_bare_script_paths(text) == []


# --- boundary attempts the rule survives ------------------------------------

@pytest.mark.parametrize(
    "line",
    [
        "python3 <skill-dir>/scripts/x.py",
        "python3 ${CLAUDE_SKILL_DIR}/scripts/x.py",
        "python3 loom-code/scripts/loom_checker.py",
        "pytest scripts/test_x.py",
        "ssh scripts/host",
        "zsh scripts/x.sh",
        "my-python scripts/x.py",
    ],
    ids=["skill-dir", "env-var", "plugin-rel", "pytest", "ssh", "zsh", "hyphen"],
)
def test_bare_script_rule_anchored_or_other_tool_not_flagged(line: str) -> None:
    assert checker.find_bare_script_paths(line + "\n") == []


@pytest.mark.parametrize(
    "line",
    ["uv run scripts/x.py", "node scripts/x.js", "python3 scripts\\x.py"],
    ids=["uv-run", "node", "backslash-sep"],
)
def test_bare_script_rule_out_of_contract_runner_not_flagged(line: str) -> None:
    """Contract boundary (python/python3/bash/sh on `scripts/`): other runners
    and Windows separators are outside it today. A widening of the rule is
    expected to update this test."""
    assert checker.find_bare_script_paths(line + "\n") == []


def test_bare_script_scan_python_docstring_outside_scope(tmp_path: Path) -> None:
    """Scope boundary: only `.md` runtime prose is scanned. A bundled script's
    usage docstring with a bare path is not reported."""
    script = tmp_path / "loom-workflow/skills/s/scripts/tool.py"
    script.parent.mkdir(parents=True)
    script.write_text('"""Usage:\n    python3 scripts/tool.py <in>\n"""\n', encoding="utf-8")
    assert checker.scan_bare_script_paths(tmp_path) == []


def test_bare_script_scan_skill_template_and_agent_in_scope(tmp_path: Path) -> None:
    """Nested skill templates, skill-local agent prompts, loom-code agents and
    plugin references are all scanned."""
    rels = [
        "loom-workflow/skills/v/templates/01-x.md",
        "loom-workflow/skills/d/agents/prompt.md",
        "loom-code/agents/worker.md",
        "loom-workflow/references/r.md",
    ]
    for rel in rels:
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x\npython3 scripts/x.py\n", encoding="utf-8")
    assert checker.scan_bare_script_paths(tmp_path) == sorted(f"{r}:2" for r in rels)


def test_bare_script_scan_empty_repo_returns_empty(tmp_path: Path) -> None:
    assert checker.scan_bare_script_paths(tmp_path) == []
    assert checker.find_bare_script_paths("") == []
