# concern: Incorrect document delivery locations and portable-reference rewrites.
"""Delivery guidance coverage; model compliance needs live acceptance testing."""
import json
import subprocess
from pathlib import Path

import pytest

from prose_pin import affirms

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "loom-design" / "skills"
VISUAL = ROOT / "loom-workflow" / "skills" / "loom-visualization"


def _path_rule(text):
    text = " ".join(text.split())
    return all((
        affirms(text, "Deliver", "local documents", "actual absolute paths",
                "active worktree", "external location", "copyable instructions"),
        affirms(text, "use", "project-relative path as link text", "known local Markdown support",
                "external files: basename", "absolute targets"),
        affirms(text, "show", "full absolute paths", "otherwise"),
        affirms(text, "Enclose", "targets with spaces", "angle brackets"),
        affirms(text, "Preserve", "bundled references", "stored relative paths",
                "quoted examples", "incidental filenames"),
    ))


@pytest.mark.parametrize("name", [
    "capture-intent", "write-spec", "product-principles", "design-system", "architecture-design",
])
def test_direct_design_document_delivery_carries_path_guidance(name):
    skill = DESIGN / name
    text = (skill / "SKILL.md").read_text()
    assert _path_rule(text)
    assert "/Users/kouko" not in text


def test_emitted_code_guidance_and_direct_visualization_cover_document_paths(tmp_path):
    proc = subprocess.run(["bash", str(ROOT / "loom-code" / "hooks" / "session-start")],
                          cwd=tmp_path, input="", capture_output=True, text=True, check=True)
    context = json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]
    launcher = ROOT / "loom-code" / "hooks" / ".." / "scripts" / "loom-python"
    command = f'`"{launcher}" --ready delivery --json`'
    assert context.count(command) == 1
    for text in (
        context.replace(command, "", 1),
        (VISUAL / "SKILL.md").read_text(),
        (VISUAL / "references" / "plain-language.md").read_text(),
    ):
        assert _path_rule(text)
        assert "/Users/kouko" not in text


def test_path_rule_rejects_negated_or_incomplete_guidance():
    positive = (
        "Deliver local documents with actual absolute paths from the active worktree or "
        "external location, including in copyable instructions. "
        "For known local Markdown support, use the document's project-relative path as "
        "link text (external files: basename) and absolute targets; otherwise show full "
        "absolute paths. Enclose targets with spaces in angle brackets. "
        "Preserve bundled references, stored relative paths, quoted examples and incidental filenames."
    )
    assert _path_rule(positive)
    for clause in (
        "local documents", "actual absolute paths", "active worktree", "external location",
        "copyable instructions", "known local Markdown support", "project-relative path as link text",
        "external files: basename", "absolute targets", "otherwise", "full absolute paths",
        "targets with spaces", "angle brackets", "bundled references", "stored relative paths",
        "quoted examples", "incidental filenames",
    ):
        assert not _path_rule(positive.replace(clause, "omitted")), clause
    for verb in ("Deliver", "use", "show", "Enclose", "Preserve"):
        assert not _path_rule(positive.replace(verb, f"never {verb}")), verb
