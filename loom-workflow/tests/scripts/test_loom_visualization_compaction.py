from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO_ROOT / "loom-workflow/skills/loom-visualization"
SKILL_PATH = SKILL_DIR / "SKILL.md"
PAGE_MODE_PATH = SKILL_DIR / "references/page-mode.md"
WORD_CAP = 4_500

TEMPLATES = (
    "01-option-comparison",
    "02-linear-steps",
    "03-branching-decision",
    "04-reasoning-chain",
    "05-state-lifecycle",
    "06-actor-sequence",
    "07-hierarchy",
    "08-system-architecture",
    "09-data-model",
    "10-timeline",
    "11-quantity",
)


def test_entrypoint_has_required_sections_and_routes():
    text = SKILL_PATH.read_text(encoding="utf-8")

    assert text.startswith("---\nname: loom-visualization\n")
    for heading in (
        "## Boundary",
        "## Step 1",
        "## Step 2",
        "## Step 3",
        "## Step 4",
        "## Page mode",
        "## Failure modes to refuse",
    ):
        assert heading in text, heading

    essence = {
        "obsidian boundary": [
            "scripts/detect_client.py --target",
            "obsidian:obsidian-mermaid-visualizer",
        ],
        "shape routing": [f"templates/{name}.md" for name in TEMPLATES],
        "client check": ["scripts/detect_client.py", "references/client-matrix.md"],
        "ascii generation": ["scripts/generate.py", "scripts/align.py"],
        "page mode": ["references/page-mode.md"],
        "plain language": ["references/plain-language.md"],
    }
    for contract, needles in essence.items():
        missing = [needle for needle in needles if needle not in text]
        assert not missing, f"{contract} missing from entrypoint: {missing}"


def test_entrypoint_within_word_cap():
    assert len(SKILL_PATH.read_text(encoding="utf-8").split()) <= WORD_CAP


def test_page_mode_preserves_extraction_render_and_fidelity_gates():
    text = SKILL_PATH.read_text(encoding="utf-8") + PAGE_MODE_PATH.read_text(
        encoding="utf-8"
    )
    essence = {
        "active-reasoning routing": [
            "think-orbit:thinking-session",
            "think-orbit:break-assumption",
        ],
        "source selection": ["File mode", "Conversation mode", "State which mode"],
        "extraction net": [
            "Rejected options",
            "Assumptions",
            "Open questions",
            "Exceptions and withdrawal conditions",
            "Co-premises",
            "author's own hedging",
        ],
        "early exit": ["Fewer than 5", "stop", "answer their question directly"],
        "layout invariants": [
            "graph TB",
            "direction LR",
            "r1 -->|",
            "Rows of at most 3",
            "Every** edge carries a label",
        ],
        "markdown authority": [
            "markdown is the artifact",
            "hand-write the HTML",
            "assets/cot-report-template.md",
        ],
        "fidelity gate": [
            "before anything gets shared",
            "references/fidelity-check.md",
            "<name>.fidelity.md",
            "reviewed_md_sha256:",
        ],
        "temporary paths and publishing consent": [
            "${TMPDIR:-/tmp}/loom-visualization/",
            "both are temporary",
            "Ask once",
            "do not publish unprompted",
        ],
    }
    for contract, needles in essence.items():
        missing = [needle for needle in needles if needle not in text]
        assert not missing, f"{contract} missing from page mode: {missing}"

    commands = "\n".join(
        [
            "python3 <skill-dir>/scripts/render_cot_html.py <file>.md",
            "python3 <skill-dir>/scripts/verify_cot_html.py --render --stamp <file>.html",
            "python3 <skill-dir>/scripts/render_cot_html.py <file>.md",
        ]
    )
    assert commands in text
    assert "cot-explain" not in text
