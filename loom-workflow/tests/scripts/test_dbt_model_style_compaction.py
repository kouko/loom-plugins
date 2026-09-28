from pathlib import Path


SKILL = (
    Path(__file__).resolve().parents[2]
    / "skills"
    / "dbt-model-style"
    / "SKILL.md"
)
POINTERS = (
    "references/dotstar-passthrough.md",
    "checklists/dbt-model-self-check.md",
    "scripts/validate_header.py",
)


def test_entrypoint_pointers_resolve():
    """Each file the entrypoint points to exists. Its wording is review-only."""
    text = SKILL.read_text(encoding="utf-8")

    for pointer in POINTERS:
        assert pointer in text, pointer
        assert (SKILL.parent / pointer).is_file(), pointer
