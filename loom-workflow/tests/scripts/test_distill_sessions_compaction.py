from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/distill-sessions/SKILL.md"
RUNTIME_PROTOCOL_PATH = (
    REPO_ROOT
    / "loom-workflow/skills/distill-sessions/references/runtime-protocol.md"
)


def test_entrypoint_preserves_essence():
    """Token and path needles only: the artifact names, the approval flag the
    scripts use, and the detail pointer resolving.
    The entrypoint's safety and privacy wording is review-only."""
    text = SKILL_PATH.read_text(encoding="utf-8")

    structural_tokens = ["top.json", "merged.json", "--approved", "references/runtime-protocol.md"]
    missing = [token for token in structural_tokens if token not in text]
    assert not missing, f"entrypoint no longer names: {missing}"

    assert RUNTIME_PROTOCOL_PATH.is_file()
