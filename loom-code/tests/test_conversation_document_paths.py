"""Conversation-only guidance coverage; model compliance needs live acceptance testing."""
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
        affirms(text, "Use", "absolute paths", "local document", "conversation"),
        affirms(text, "Resolve", "actual document location", "active repository or worktree"),
        affirms(text, "Use", "absolute Markdown link targets", "short labels", "supported"),
        affirms(text, "Preserve", "bundled resource references", "stored relative paths", "document links"),
    ))


@pytest.mark.parametrize("name", [
    "capture-intent", "write-spec", "product-principles", "design-system", "architecture-design",
])
def test_direct_design_document_delivery_carries_path_guidance(name):
    skill = DESIGN / name
    text = (skill / "SKILL.md").read_text()
    if name == "capture-intent":
        assert affirms(" ".join(text.split()), "Read", "references/conversation-paths.md",
                       "before sharing document locations")
        text = (skill / "references" / "conversation-paths.md").read_text()
    assert _path_rule(text)


def test_emitted_code_guidance_and_direct_visualization_cover_document_paths(tmp_path):
    proc = subprocess.run(["bash", str(ROOT / "loom-code" / "hooks" / "session-start")],
                          cwd=tmp_path, input="", capture_output=True, text=True, check=True)
    context = json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]
    for text in (
        context,
        (VISUAL / "SKILL.md").read_text(),
        (VISUAL / "references" / "plain-language.md").read_text(),
    ):
        assert _path_rule(text)
        flat = " ".join(text.split())
        assert affirms(flat, "Wrap", "targets containing spaces", "angle brackets")
        assert affirms(flat, "Use", "absolute plain path", "unsupported")
        assert "file://" in text and "Never" in text
        assert "/Users/kouko" not in text


def test_path_rule_rejects_negated_or_incomplete_guidance():
    positive = (
        "Use absolute paths for every local document location in conversation. "
        "Resolve the actual document location in the active repository or worktree. "
        "Use absolute Markdown link targets with short labels where supported. "
        "Preserve bundled resource references, stored relative paths and document links."
    )
    assert _path_rule(positive)
    assert not _path_rule(positive.replace("Use absolute paths", "Never use absolute paths"))
    assert not _path_rule(positive.replace("active repository or worktree", "developer checkout"))
    assert not _path_rule(positive.replace("Preserve bundled", "Never preserve bundled"))
