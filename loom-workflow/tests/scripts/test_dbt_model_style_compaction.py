from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "loom-code/scripts"))
from prose_pin import affirms  # noqa: E402


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
    and commands stay, including the working-language header contract."""
    text = SKILL.read_text(encoding="utf-8")

    for pointer in POINTERS:
        assert pointer in text, pointer
        assert (SKILL.parent / pointer).is_file(), pointer
    missing = [token for token in STRUCTURAL_TOKENS if token not in text]
    assert not missing, f"entrypoint no longer names: {missing}"

    flat = " ".join(text.split())
    example = "`title` (use the user's working language for the model name)."
    rule = ("use", "the user's working language", "`title`")
    assert affirms(example, *rule)
    assert not affirms(example.replace("use", "do not use"), *rule)
    title_rule = next(line for line in text.splitlines() if line.startswith("- **All layers MUST**:"))
    assert affirms(title_rule, *rule)
    assert "`title` (the Chinese name" not in flat
    assert affirms(flat, "Write", "frontmatter *values*", "user's working language")
    assert "examples in this doc stay in Chinese as a demonstration" in flat
    assert "title:   區域 B 每日指標值（雙來源合併）" in text
