"""Tri-language SESSION discovery, native host tools and manual recovery."""

import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "goal-create"
README_EN = SKILL_DIR / "README.md"
README_JA = SKILL_DIR / "README.ja.md"
README_ZHTW = SKILL_DIR / "README.zh-TW.md"

READMES = {
    "README.md (EN)": README_EN,
    "README.ja.md (JA)": README_JA,
    "README.zh-TW.md (zh-TW)": README_ZHTW,
}

# What SESSION produces: the four goal-shape field labels are literal
# English tokens used identically across languages — goal-shape.md is
# their SSOT and no README may translate or restate their definitions.
SESSION_FIELD_LABELS = ("Outcome", "Constraints", "Verification", "Stop-when")

SKILL_MD_POINTER = "SKILL.md"

def test_tri_language_set_exists_and_names_session_only():
    # 1. All three README files exist.
    for label, path in READMES.items():
        assert path.exists(), f"{label} does not exist at {path}"

    for label, path in READMES.items():
        text = path.read_text(encoding="utf-8")

        assert "SESSION" in text, label
        assert "ARC" not in text, label
        assert "PURPOSE.md" not in text, label

        # 3. Each names what SESSION produces: at least one of the four
        # field labels the four-field goal shape is written in.
        assert any(field in text for field in SESSION_FIELD_LABELS), (
            f"{label}: does not name what SESSION produces "
            f"(expected one of {SESSION_FIELD_LABELS})"
        )

        # 5. Each points at SKILL.md for the contract, rather than restating it.
        assert SKILL_MD_POINTER in text, (
            f"{label}: does not point at {SKILL_MD_POINTER} for the contract"
        )


def test_tri_language_discovery_names_host_goal_tools():
    for label, path in READMES.items():
        text = path.read_text(encoding="utf-8")
        assert re.search(r"Codex[^.!?。]*`create_goal`", text), label
        assert re.search(r"Claude Code[^.!?。]*`ProposeGoal`[^.!?。]*`/goal`", text), label

    assert "`/goal clear`" in README_EN.read_text(encoding="utf-8")
    assert "`/goal clear`" in README_JA.read_text(encoding="utf-8")
    assert "`/goal clear`" in README_ZHTW.read_text(encoding="utf-8")


def test_invocation_documents_only_the_handoff_offer_site():
    for label, path in READMES.items():
        text = path.read_text(encoding="utf-8")
        invocation = re.split(r"^## (?:Invocation|呼び出し|呼叫)\s*$", text, flags=re.M)[1]
        invocation = invocation.split("\n## ", 1)[0]
        references = set(re.findall(r"`(loom-[^`]+)`", invocation))
        assert references == {"loom-workflow:handoff"}, label
        assert "purpose-link" not in text, label
