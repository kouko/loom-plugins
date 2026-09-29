from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL = REPO_ROOT / "loom-workflow/skills/git-memory/SKILL.md"
POINTERS = (
    "protocols/compose-commit.md",
    "protocols/compose-pr.md",
    "protocols/recall.md",
    "standards/memory-conventions.md",
)
STRUCTURAL_TOKENS = ("BLOCKED", "`git log --grep`", "memory-grep.sh --verify <ref>")
PROTOCOL_TOKENS = {
    "protocols/compose-commit.md": ["Privacy-Bypass-Reason:"],
    "protocols/compose-pr.md": ["gh pr create"],
    "protocols/recall.md": ["--history", "--path", "--match", "--top"],
    "standards/memory-conventions.md": [
        "Decision:",
        "Learning:",
        "Gotcha:",
        "Supersedes:",
    ],
}


def test_entrypoint_pointers_resolve_and_structural_tokens_stay():
    """Each file the entrypoint points to exists, and the verdict, commands,
    flags and trailer keys stay. The prose wording is review-only."""
    text = SKILL.read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())

    for pointer in POINTERS:
        assert pointer in text, pointer
        assert (SKILL.parent / pointer).is_file(), pointer
    missing = [token for token in STRUCTURAL_TOKENS if token not in normalized_text]
    assert not missing, f"entrypoint no longer names: {missing}"
    for relative, tokens in PROTOCOL_TOKENS.items():
        contract_text = (SKILL.parent / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in contract_text]
        assert not missing, f"{relative} no longer names: {missing}"


def test_contract_regression_checks_do_not_pin_whole_file_hashes():
    source = Path(__file__).read_text(encoding="utf-8")
    assert "UNCHANGED" + "_CONTRACTS" not in source
    assert "sha" + "256" not in source
