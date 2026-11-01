"""The documented diagram choices remain executable and affirmative."""

import re
import subprocess
import sys
from pathlib import Path


SKILL = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/SKILL.md"
SCRIPT = SKILL.parent / "scripts/diagram.py"


def affirmative_instruction(text, verb, target):
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(text.split()))
    return any(
        target in sentence
        and re.search(rf"\b{verb}\b", sentence.split(target, 1)[0], re.I)
        and not re.search(r"\b(?:not|never|no)\b", sentence, re.I)
        for sentence in sentences
    )


def run_tool(cwd, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, text=True, capture_output=True)


def test_external_edit_guidance_asks_and_waits_before_writing():
    assert affirmative_instruction("Ask whether to copy the diagram.", "ask", "whether to copy")
    assert not affirmative_instruction("Do not ask whether to copy the diagram.", "ask", "whether to copy")
    text = SKILL.read_text(encoding="utf-8")
    assert affirmative_instruction(text, "ask", "whether to copy")
    assert affirmative_instruction(text, "wait", "before copying or editing")
    assert "each external edit" in text


def test_documented_standalone_and_loom_paths_work(tmp_path):
    text = SKILL.read_text(encoding="utf-8")
    assert "new example --output-dir <project-dir>" in text
    assert "copy <source> --change-id <change-id>" in text
    project = tmp_path / "project"
    project.mkdir()
    missing = run_tool(tmp_path, "new", "unplaced")
    assert missing.returncode == 1
    assert "destination required outside Loom" in missing.stderr
    created = run_tool(tmp_path, "new", "example", "--output-dir", str(project))
    assert created.returncode == 0, created.stderr
    source = project / "example.drawio"
    original = source.read_bytes()
    change_id = "2026-11-01-example"
    intent = tmp_path / "docs/loom/intent"
    intent.mkdir(parents=True)
    (intent / f"{change_id}.md").write_text("# Example\n", encoding="utf-8")
    copied = run_tool(tmp_path, "copy", str(source), "--change-id", change_id)
    assert copied.returncode == 0, copied.stderr
    assert (tmp_path / "docs/loom" / change_id / "diagrams/example.drawio").read_bytes() == original
    assert source.read_bytes() == original
    assert not (project / "diagrams").exists()
