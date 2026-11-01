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
    assert "Otherwise, wait for the user's answer" in " ".join(what_to_do.split())
    assert "HANDOFF" in text

    active_template = schema.split("## L3 user-visible template", 1)[1].split(
        "## 1 — The Seven Blocks", 1
    )[0]
    normalized_template = " ".join(active_template.split())
    assert "lead with the conversation-grounded original purpose" in normalized_template
    assert "omit sections with no useful content" in normalized_template
    assert "Stop until the user responds" in active_template
    assert "six-section" not in active_template
    assert "six natural sections" not in active_template

    for contract in (text, schema):
        normalized = " ".join(contract.split())
        assert "If the original purpose is unknown, ask only for the purpose." in normalized
        assert (
            "When the original purpose is grounded, ask about the proposed next step."
            in normalized
        )
        assert "Do not invent a proposed work step when the purpose is unknown." in normalized
        assert "If asking for purpose, wait for the user to state or clarify it." in normalized
