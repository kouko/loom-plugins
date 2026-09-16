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


NEGATION_RE = re.compile(r"\b(?:not|never|no|none|without|unless|except|avoid)\b|n't", re.IGNORECASE)


def gate_sentences(block):
    return re.split(r"(?<=[.!?])\s+", " ".join(block.split()))


def pinned_sentence_ok(sentence, verb, literals):
    """True when every literal is in the sentence, an affirmative `verb`
    precedes the primary literal (literals[0]), and no negation token remains once the
    pinned literals themselves are removed."""
    if not all(lit in sentence for lit in literals):
        return False
    head = sentence[:sentence.index(literals[0])]
    if not re.search(rf"\b{re.escape(verb)}\b", head, re.IGNORECASE):
        return False
    rest = sentence
    for lit in literals:
        rest = rest.replace(lit, " ")
    return not NEGATION_RE.search(rest)


MERMAID_GATE = "loom-visualization.mermaid-only-when-confirmed"
MERMAID_PIN = ("Use", ("Mermaid only when you have no shell", "claude.ai", "Claude Desktop chat"))
TABLE_ASCII_PIN = ("gets", ("markdown table", "Everywhere else"))


def test_pinned_sentence_affirmative_example_accepted():
    sentence = ("Use Mermaid only when you have no shell and your own host is "
                "claude.ai or the Claude Desktop chat.")
    assert pinned_sentence_ok(sentence, *MERMAID_PIN)


def test_pinned_sentence_negated_example_rejected():
    sentence = ("Never use Mermaid only when you have no shell and your own host is "
                "claude.ai or the Claude Desktop chat.")
    assert not pinned_sentence_ok(sentence, *MERMAID_PIN)


def test_mermaid_gate_paragraph_present_requires_confirmed_host():
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(
        rf"<!--\s*gate:\s*{re.escape(MERMAID_GATE)}\s*-->(.*?)<!--\s*/gate\s*-->",
        text, re.DOTALL,
    )
    assert match, f"no {MERMAID_GATE} gate block in SKILL.md"
    sentences = gate_sentences(match.group(1))
    for verb, literals in (MERMAID_PIN, TABLE_ASCII_PIN):
        assert any(pinned_sentence_ok(s, verb, literals) for s in sentences), (
            f"no affirmative, un-negated sentence pins {literals!r}"
        )


OBSIDIAN_GATE = "loom-visualization.obsidian-boundary"
CHAT_PROCEEDS_PIN = ("proceeds", ("even when the working directory is inside an Obsidian vault",
                                  "chat answer"))


def test_chat_proceeds_pin_affirmative_example_accepted():
    sentence = ("A chat answer proceeds normally even when the working directory "
                "is inside an Obsidian vault.")
    assert pinned_sentence_ok(sentence, *CHAT_PROCEEDS_PIN)


def test_chat_proceeds_pin_negated_example_rejected():
    sentence = ("A chat answer never proceeds normally even when the working directory "
                "is inside an Obsidian vault.")
    assert not pinned_sentence_ok(sentence, *CHAT_PROCEEDS_PIN)


def test_obsidian_gate_paragraph_chat_in_vault_cwd_proceeds():
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(
        rf"<!--\s*gate:\s*{re.escape(OBSIDIAN_GATE)}\s*-->(.*?)<!--\s*/gate\s*-->",
        text, re.DOTALL,
    )
    assert match, f"no {OBSIDIAN_GATE} gate block in SKILL.md"
    block = match.group(1)
    assert "--target" in block
    assert any(pinned_sentence_ok(s, *CHAT_PROCEEDS_PIN) for s in gate_sentences(block)), (
        "no affirmative, un-negated sentence says a chat answer proceeds in a vault cwd"
    )


# Acceptance 8: a markdown table is the default form for shaped content, and
# the drawn form is chosen by the destination, never by the client.

CLIENT_MATRIX = SKILL_DIR / "references" / "client-matrix.md"
DETECT_CLIENT = SKILL_DIR / "scripts" / "detect_client.py"

TABLE_DEFAULT_PIN = ("gets", ("markdown table by default",
                              "a destination that does not render markdown"))

# A rule that picks the drawn form because of the client the agent runs in.
ASCII_BY_CLIENT = re.compile(
    r"(?:remote[ _]viewer|terminal client|because of the client)[^.]*\bASCII\b"
    r"|\bstay ASCII\b",
    re.IGNORECASE,
)


def test_table_default_pin_affirmative_example_accepted():
    sentence = ("Shaped content in a chat reply gets a markdown table by default; the "
                "drawn form is for a destination that does not render markdown.")
    assert pinned_sentence_ok(sentence, *TABLE_DEFAULT_PIN)


def test_table_default_pin_negated_example_rejected():
    sentence = ("Shaped content in a chat reply never gets a markdown table by default; the "
                "drawn form is for a destination that does not render markdown.")
    assert not pinned_sentence_ok(sentence, *TABLE_DEFAULT_PIN)


def test_shaped_content_defaults_to_a_markdown_table():
    """A8 positive: the skill and the matrix make the table the default form."""
    text = SKILL_MD.read_text(encoding="utf-8")
    assert any(pinned_sentence_ok(s, *TABLE_DEFAULT_PIN) for s in gate_sentences(text)), (
        "SKILL.md pins no affirmative sentence making the markdown table the default form"
    )

    matrix = CLIENT_MATRIX.read_text(encoding="utf-8")
    rows = [line for line in matrix.splitlines()
            if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|\s*$", line)]
    header, body = rows[0], rows[1:]
    cells = [c.strip() for c in header.strip("|").split("|")]
    assert "Form in a chat reply" in cells, cells
    column = cells.index("Form in a chat reply")
    for row in body:
        form = [c.strip() for c in row.strip("|").split("|")][column]
        assert "markdown table" in form, row


def test_remote_viewer_no_longer_forces_ascii():
    """A8 negative: no rule picks the drawn form because of the client."""
    assert ASCII_BY_CLIENT.search(
        "When `remote_viewer` is `true`, send the ASCII form in a code block."
    ), "detector misses the client-driven rule it exists to catch"
    assert ASCII_BY_CLIENT.search("; remote viewer attached, stay ASCII")
    assert not ASCII_BY_CLIENT.search(
        "The drawn ASCII form is for a destination that does not render markdown."
    ), "detector flags a destination-driven rule"

    for path in (SKILL_MD, CLIENT_MATRIX, DETECT_CLIENT):
        flat = " ".join(path.read_text(encoding="utf-8").split())
        hit = ASCII_BY_CLIENT.search(flat)
        assert not hit, f"{path.name}: {hit.group(0)!r}"


def test_every_ascii_section_names_its_destination_condition():
    """The drawn form is conditioned on the destination in every template."""
    for name in EXPECTED:
        if name == "09-data-model.md":
            continue  # no ASCII form at all; it points at the table substitute
        body = " ".join(sections(_read(name))["ASCII"].split())
        assert "does not render markdown" in body, name
