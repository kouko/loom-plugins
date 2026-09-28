from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/recap-state/SKILL.md"
SCHEMA_PATH = (
    REPO_ROOT
    / "loom-workflow/skills/recap-state/references/seven-block-schema.md"
)


def test_entrypoint_reads_schema_before_the_ordered_six_section_template():
    """The schema pointer precedes the template, whose six headings keep their
    order and carry no internal tags. The entrypoint's wording is review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    what_to_do = text.index("## What to do")
    schema_read = text.index("references/seven-block-schema.md", what_to_do)
    template_start = text.index("### Purpose and current position", schema_read)
    template_end = text.index("3. Apply", template_start)
    rendered_template = text[template_start:template_end]
    sections = (
        "### Purpose and current position",
        "### Essential background",
        "### Gap and current assessment",
        "### Why confirmation is needed now",
        "### Pending work",
        "### Align purpose and next step",
    )
    positions = [text.index(section, template_start) for section in sections]
    assert positions == sorted(positions)
    for forbidden in ("<thinking>", "</thinking>", "<recap>", "</recap>", "Block "):
        assert forbidden not in rendered_template

    assert SCHEMA_PATH.is_file()
