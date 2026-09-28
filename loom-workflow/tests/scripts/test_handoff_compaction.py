from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/handoff/SKILL.md"
SCHEMA_PATH = (
    REPO_ROOT / "loom-workflow/skills/handoff/references/handoff-schema.md"
)


def test_each_mode_reads_the_schema_before_its_artifact_step():
    """Both modes point to the schema before they write or read a HANDOFF.
    The entrypoint's wording is review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    prepare = text.index("## Prepare mode")
    prepare_schema = text.index("references/handoff-schema.md", prepare)
    prepare_author = text.index("2. Write", prepare)
    assert prepare_schema <= prepare_author

    resume = text.index("## Resume mode")
    resume_schema = text.index("references/handoff-schema.md", resume)
    resume_interpret = text.index("2. Read", resume)
    assert resume_schema <= resume_interpret

    assert SCHEMA_PATH.is_file()


def test_prepare_mode_names_goal_create():
    """Only Prepare mode names goal-create. The disclaimer's wording, that the
    user invokes it and Prepare mode never does, is review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    prepare = text.index("## Prepare mode")
    resume = text.index("## Resume mode")
    prepare_section = text[prepare:resume]

    assert "loom-workflow:goal-create" in prepare_section
    assert "goal-create" not in text[resume:]
