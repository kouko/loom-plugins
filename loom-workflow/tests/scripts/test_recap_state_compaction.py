from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/recap-state/SKILL.md"
SCHEMA_PATH = (
    REPO_ROOT
    / "loom-workflow/skills/recap-state/references/seven-block-schema.md"
)


def test_entrypoint_routes_to_purpose_first_variable_length_recap():
    text = SKILL_PATH.read_text(encoding="utf-8")
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    assert SCHEMA_PATH.is_file()
    what_to_do = text.split("## What to do", 1)[1].split("## Five principles", 1)[0]
    assert "references/seven-block-schema.md" in what_to_do
    assert "original purpose" in what_to_do
    assert "current position" in what_to_do
    assert "variable-length sections" in what_to_do
    assert "Wait for the user's answer" in what_to_do
    assert "HANDOFF" in text

    active_template = schema.split("## L3 user-visible template", 1)[1].split(
        "## 1 — The Seven Blocks", 1
    )[0]
    assert "lead with the conversation-grounded original purpose" in active_template
    assert "omit sections with no useful content" in active_template
    assert "Stop until the user responds" in active_template
    assert "six-section" not in active_template
    assert "six natural sections" not in active_template
