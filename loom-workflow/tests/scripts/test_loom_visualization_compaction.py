from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO_ROOT / "loom-workflow/skills/loom-visualization"
SKILL_PATH = SKILL_DIR / "SKILL.md"
PAGE_MODE_PATH = SKILL_DIR / "references/page-mode.md"
WORD_CAP = 4_500

TEMPLATES = (
    "01-option-comparison",
    "02-linear-steps",
    "03-branching-decision",
    "04-reasoning-chain",
    "05-state-lifecycle",
    "06-actor-sequence",
    "07-hierarchy",
    "08-system-architecture",
    "09-data-model",
    "10-timeline",
    "11-quantity",
)
POINTERS = (
    *(f"templates/{name}.md" for name in TEMPLATES),
    "scripts/detect_client.py",
    "scripts/generate.py",
    "scripts/align.py",
    "references/client-matrix.md",
    "references/page-mode.md",
    "references/plain-language.md",
    "references/fidelity-check.md",
    "assets/cot-report-template.md",
)


def test_entrypoint_has_required_sections_and_routes():
    """Headings and the files the entrypoint routes to, each of which exists.
    The entrypoint's wording is review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    assert text.startswith("---\nname: loom-visualization\n")
    for heading in (
        "## Boundary",
        "## Step 1",
        "## Step 2",
        "## Step 3",
        "## Step 4",
        "## Page mode",
        "## Failure modes to refuse",
    ):
        assert heading in text, heading

    for pointer in POINTERS:
        assert pointer in text, pointer
        assert (SKILL_DIR / pointer).is_file(), pointer


def test_entrypoint_within_word_cap():
    assert len(SKILL_PATH.read_text(encoding="utf-8").split()) <= WORD_CAP


def test_page_mode_names_render_and_verify_commands():
    """The render and verify commands, in order; page mode's wording is
    review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8") + PAGE_MODE_PATH.read_text(
        encoding="utf-8"
    )

    commands = "\n".join(
        [
            "python3 <skill-dir>/scripts/render_cot_html.py <file>.md",
            "python3 <skill-dir>/scripts/verify_cot_html.py --render --stamp <file>.html",
            "python3 <skill-dir>/scripts/render_cot_html.py <file>.md",
        ]
    )
    assert commands in text
    assert "cot-explain" not in text
