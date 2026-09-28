from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/distill-sessions/SKILL.md"
RUNTIME_PROTOCOL_PATH = (
    REPO_ROOT
    / "loom-workflow/skills/distill-sessions/references/runtime-protocol.md"
)


def test_entrypoint_points_to_runtime_protocol():
    """The detail pointer resolves. The entrypoint's wording is review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    assert "references/runtime-protocol.md" in text
    assert RUNTIME_PROTOCOL_PATH.is_file()
