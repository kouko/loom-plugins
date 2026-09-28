from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL = REPO_ROOT / "loom-workflow/skills/git-memory/SKILL.md"
POINTERS = (
    "protocols/compose-commit.md",
    "protocols/compose-pr.md",
    "protocols/recall.md",
    "standards/memory-conventions.md",
)


def test_entrypoint_pointers_resolve():
    """Each file the entrypoint points to exists. Its wording is review-only."""
    text = SKILL.read_text(encoding="utf-8")

    for pointer in POINTERS:
        assert pointer in text, pointer
        assert (SKILL.parent / pointer).is_file(), pointer


def test_contract_regression_checks_do_not_pin_whole_file_hashes():
    source = Path(__file__).read_text(encoding="utf-8")
    assert "UNCHANGED" + "_CONTRACTS" not in source
    assert "sha" + "256" not in source
