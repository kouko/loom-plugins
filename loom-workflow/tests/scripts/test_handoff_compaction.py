from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/handoff/SKILL.md"
SCHEMA_PATH = (
    REPO_ROOT / "loom-workflow/skills/handoff/references/handoff-schema.md"
)
STRUCTURAL_TOKENS = (
    "Prepare mode",
    "Resume mode",
    "recap-state",
    "git rev-parse HEAD",
    "git rev-parse --abbrev-ref HEAD",
    "git status --short",
    "git log --oneline -5",
    "claude --version",
    "Recent decisions",
    "Verification commands",
    "Confidence flags",
    "Resume Launcher",
    "USER DIRECTIVE:",
    "conversation_language",
    "ls -t .claude/handoffs/ | head -1",
    "[T1]",
    "[T2]",
    "Synthesis-check",
)


def test_entrypoint_structure_and_schema_before_artifact_steps():
    """The mode names, state commands, block labels, launcher labels and tier
    tags stay, and both modes point to the schema before they write or read a
    HANDOFF. The entrypoint's prose wording is review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    missing = [token for token in STRUCTURAL_TOKENS if token not in text]
    assert not missing, f"entrypoint no longer names: {missing}"

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
