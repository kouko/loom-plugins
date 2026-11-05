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
        affirms(text, "provide", "actual absolute location", "delivering a local document",
                "active project or worktree", "outside that root"),
        affirms(text, "use", "project-relative label", "known to be supported", "local Markdown links",
                "filename for an external document", "absolute target"),
        affirms(text, "show", "full absolute path", "unknown or unsupported"),
        affirms(text, "wrap", "targets containing spaces", "angle brackets"),
        affirms(text, "Preserve", "portable references inside files", "bundled resource references",
                "stored relative paths", "document links"),
        affirms(text, "Leave", "incidental filename mentions", "quoted source examples", "unchanged"),
        affirms(text, "apply", "this rule", "copyable document deliveries"),
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
        assert "/Users/kouko" not in text


def test_path_rule_rejects_negated_or_incomplete_guidance():
    positive = (
        "When delivering a local document, provide its actual absolute location in the "
        "active project or worktree, including files outside that root. "
        "Where local Markdown links are known to be supported, use a project-relative label "
        "(or a filename for an external document) and an absolute target; "
        "wrap targets containing spaces in angle brackets. "
        "When support is unknown or unsupported, show the full absolute path. "
        "Preserve portable references inside files, including bundled resource references, "
        "stored relative paths and repository document links. "
        "Leave incidental filename mentions and quoted source examples unchanged; "
        "apply this rule to copyable document deliveries."
    )
    assert _path_rule(positive)
    assert not _path_rule(positive.replace("provide its", "never provide its"))
    assert not _path_rule(positive.replace("Leave incidental", "Never leave incidental"))
    assert not _path_rule(positive.replace("active project or worktree", "developer checkout"))
    assert not _path_rule(positive.replace("unknown or unsupported", "unsupported"))
    assert not _path_rule(positive.replace("Preserve portable", "Rewrite portable"))
