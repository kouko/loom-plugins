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
STRUCTURAL_TOKENS = (
    "UPPERCASE",
    "USING (key)",
    "YAML frontmatter",
    "Consumer layers",
    "LISTAGG",
    "UNION ALL",
    "target.type=='redshift'",
    "not `materialization`",
    "python <skill-dir>/scripts/validate_header.py models/",
    "python <skill-dir>/scripts/validate_header.py --manifest target/manifest.json models/",
)


def test_entrypoint_pointers_resolve_and_structural_tokens_stay():
    """Each file the entrypoint points to exists, and its SQL keywords, labels
    and commands stay. Its prose wording is review-only."""
    text = SKILL.read_text(encoding="utf-8")

    for pointer in POINTERS:
        assert pointer in text, pointer
        assert (SKILL.parent / pointer).is_file(), pointer
    missing = [token for token in STRUCTURAL_TOKENS if token not in text]
    assert not missing, f"entrypoint no longer names: {missing}"
