"""Tests for the eleven shape templates and the Obsidian boundary.

Acceptance 2 (every shape has table, ASCII and Mermaid forms) and
acceptance 7 (no Obsidian-only syntax; the skill declines vault targets).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from checks_kink import find_issues as kink_issues  # noqa: E402
from checks_seam import find_issues as seam_issues  # noqa: E402
from checks_table import find_issues as table_issues  # noqa: E402
from generate import render  # noqa: E402
from glyphs import CORNERS, HORIZONTALS, TEES, VERTICALS  # noqa: E402

SKILL_DIR = SCRIPTS.parent
TEMPLATES = SKILL_DIR / "templates"
SKILL_MD = SKILL_DIR / "SKILL.md"

TARGET_LINE = "target: coding-harness"
SECTIONS = ("When to use", "Table", "ASCII", "Mermaid", "Common mistakes")

EXPECTED = {
    "01-option-comparison.md": ("quadrantChart", "table"),
    "02-linear-steps.md": ("flowchart LR", "flow"),
    "03-branching-decision.md": ("flowchart TD", None),
    "04-reasoning-chain.md": ("flowchart TD", None),
    "05-state-lifecycle.md": ("stateDiagram-v2", None),
    "06-actor-sequence.md": ("sequenceDiagram", "seq"),
    "07-hierarchy.md": ("mindmap", "tree"),
    "08-system-architecture.md": ("flowchart", "arch"),
    "09-data-model.md": ("erDiagram", None),
    "10-timeline.md": ("timeline", None),
    "11-quantity.md": ("xychart-beta", "bar"),
}

BOX_GLYPHS = VERTICALS | HORIZONTALS | CORNERS | TEES
FENCE = re.compile(r"^```([\w-]*)[^\n]*\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
CJK = re.compile(r"[぀-ヿ㐀-鿿]")


def sections(text):
    """Map each H2 title to its body text."""
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def fences(text):
    """Return (language, body) for each fenced block in text."""
    return [(m.group(1), m.group(2)) for m in FENCE.finditer(text)]


def validate_template(text):
    """Return a list of structural errors; empty means the template is valid."""
    errors = []
    if text.splitlines()[:1] != [TARGET_LINE]:
        errors.append(f"first line is not {TARGET_LINE!r}")
    found = sections(text)
    for name in SECTIONS:
        if name not in found:
            errors.append(f"missing section: {name}")
    titles = [t for t in found if t in SECTIONS]
    if titles != [t for t in SECTIONS if t in found]:
        errors.append(f"sections out of order: {titles}")
    if "Mermaid" in found:
        blocks = [b for lang, b in fences(found["Mermaid"]) if lang == "mermaid"]
        if len(blocks) != 1:
            errors.append(f"Mermaid section has {len(blocks)} mermaid blocks, expected 1")
    return errors


def forbidden_syntax(text):
    """Return Obsidian-only or comment syntax found in text."""
    hits = []
    if "[[" in text:
        hits.append("wikilink [[")
    if re.search(r"^\s*> \[!", text, re.MULTILINE):
        hits.append("callout > [!")
    if re.search(r"^\s*%%", text, re.MULTILINE):
        hits.append("%% comment line")
    return hits


def drift(block):
    """Run the ported seam, table and kink checks on one ASCII block."""
    lines = block.splitlines()
    return seam_issues(lines) + table_issues(lines) + kink_issues(lines)


def generator_examples(text):
    """Return (shape, payload, output) for each generator example in ASCII."""
    body = sections(text).get("ASCII", "")
    shapes = re.findall(r"scripts/generate\.py (\w+)", body)
    blocks = fences(body)
    examples = []
    for i, (lang, payload) in enumerate(blocks):
        if lang == "json" and i + 1 < len(blocks):
            examples.append((shapes[0] if shapes else None, json.loads(payload), blocks[i + 1][1]))
    return examples


def _read(name):
    return (TEMPLATES / name).read_text(encoding="utf-8")


def test_eleven_shapes_each_have_table_ascii_mermaid():
    assert sorted(p.name for p in TEMPLATES.glob("*.md")) == sorted(EXPECTED)
    for name, (mermaid_type, _) in EXPECTED.items():
        text = _read(name)
        assert validate_template(text) == [], name
        table = sections(text)["Table"]
        assert re.search(r"^\|.*\|\s*$\n^\|[\s:|-]+\|\s*$", table, re.MULTILINE), name
        (block,) = [b for lang, b in fences(sections(text)["Mermaid"]) if lang == "mermaid"]
        assert block.splitlines()[0].startswith(mermaid_type), name


def test_template_missing_mermaid_section_fails():
    good = _read("02-linear-steps.md")
    assert validate_template(good) == []
    broken = re.sub(r"^## Mermaid$.*?(?=^## Common mistakes$)", "", good, flags=re.MULTILINE | re.DOTALL)
    assert "missing section: Mermaid" in validate_template(broken)


def test_template_with_wikilink_fails():
    for sample in ("see [[x]]", "> [!note]\n> body", "%% comment\nflowchart TD"):
        assert forbidden_syntax(sample), sample
    for name in EXPECTED:
        assert forbidden_syntax(_read(name)) == [], name


def test_ascii_blocks_pass_ported_checks():
    for name, (_, shape) in EXPECTED.items():
        text = _read(name)
        generated = {out for s, _, out in generator_examples(text)}
        for lang, block in fences(sections(text)["ASCII"]):
            if lang in ("json", "mermaid") or not set(block) & BOX_GLYPHS:
                continue
            if shape == "seq" and block in generated:
                # gen_seq is correct by construction; its blank off-span
                # lifelines are outside the vertical-seam model, so it is
                # verified by regeneration below instead.
                continue
            assert drift(block) == [], f"{name}: {drift(block)}"


def test_generator_examples_reproduce_their_output():
    for name, (_, shape) in EXPECTED.items():
        examples = generator_examples(_read(name))
        if shape is None:
            assert examples == [], name
            continue
        assert examples, f"{name}: no generator JSON input plus output"
        for used, payload, output in examples:
            assert used == shape, name
            got = [line.rstrip() for line in render(shape, payload).splitlines()]
            assert got == [line.rstrip() for line in output.splitlines()], name


def test_data_model_ascii_states_table_substitute():
    assert "table substitute" in sections(_read("09-data-model.md"))["ASCII"].lower()


def test_mermaid_flowcharts_use_long_arrows_only():
    for name in EXPECTED:
        (block,) = [b for lang, b in fences(sections(_read(name))["Mermaid"]) if lang == "mermaid"]
        if block.startswith(("flowchart", "stateDiagram")):
            assert not re.search(r"(?<![-=.])->(?!>)", block), name


def test_at_least_three_templates_use_cjk_labels():
    cjk = [n for n in EXPECTED if CJK.search(sections(_read(n))["Mermaid"])]
    assert len(cjk) >= 3, cjk


def test_skill_declines_vault_target(tmp_path):
    text = SKILL_MD.read_text(encoding="utf-8")
    boundary = sections(text).get("Boundary", "")
    assert "scripts/detect_client.py --target" in boundary
    assert "obsidian:obsidian-mermaid-visualizer" in boundary

    vault = tmp_path / "vault"
    (vault / ".obsidian").mkdir(parents=True)
    note = vault / "notes" / "diagram.md"
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "detect_client.py"), "--target", str(note)],
        capture_output=True, text=True, check=True,
    )
    assert json.loads(result.stdout)["obsidian_vault"] is True
