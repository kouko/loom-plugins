"""
Tests for the tri-language README triplet of the recap skill.

RED check:  test_tri_lang_readmes_consistent MUST FAIL before READMEs exist.
GREEN check: all assertions pass once README.md / README.ja.md / README.zh-TW.md land.
"""
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2] / "skills" / "recap-state"  # loom-workflow/skills/recap/

README_EN   = SKILL_ROOT / "README.md"
README_JA   = SKILL_ROOT / "README.ja.md"
README_ZHTW = SKILL_ROOT / "README.zh-TW.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _headings(text: str) -> list[str]:
    """Return all ATX heading lines (## or ###) stripped of markers."""
    return [
        re.sub(r"^#+\s*", "", line).strip()
        for line in text.splitlines()
        if re.match(r"^#{1,6}\s", line)
    ]


# ---------------------------------------------------------------------------
# Section-concept matchers — each checks ONE required concept by regex
# so each language can use its own natural phrasing.
# ---------------------------------------------------------------------------

# (a) 4 required heading CONCEPTS per README.
# Each tuple: (concept_label, regex) — regex is tested case-insensitively
# against the full list of heading texts joined by newlines.

REQUIRED_CONCEPTS_EN = [
    ("overview",          r"overview|what.+(this|the)\s+skill|what\s+recap\s+does"),
    ("when-to-use",       r"when\s+to\s+use|vs|built.in"),
    ("example-phrases",   r"example|invocation|trigger|phrases|how\s+to\s+(say|invoke|use)"),
    ("v0.2-deferred",     r"v0\.2|defer|coming|future|not\s+yet|what.s\s+(deferred|next)"),
]

REQUIRED_CONCEPTS_JA = [
    ("overview",          r"概要|このスキルは|recap\s*(と|が)|何をするか|使い方"),
    ("when-to-use",       r"使うとき|vs|使い分け|ビルトイン|組み込み|使わない"),
    ("example-phrases",   r"使い方|フレーズ|例|呼び出し|トリガー|言い方"),
    ("v0.2-deferred",     r"v0\.2|保留|今後|将来|延期|次の"),
]

REQUIRED_CONCEPTS_ZHTW = [
    ("overview",          r"概要|這個\s*skill|recap\s*(是什麼|做什麼|介紹)|簡介"),
    ("when-to-use",       r"何時|使用時機|vs|差異|內建|什麼時候"),
    ("example-phrases",   r"範例|呼叫|觸發|怎麼說|怎麼用|片語|說法"),
    ("v0.2-deferred",     r"v0\.2|延後|未來|下一版|保留|暫不"),
]


def _check_concepts(text: str, concepts: list[tuple[str, str]]) -> list[str]:
    """Return list of concept labels NOT found in the heading texts."""
    headings_block = "\n".join(_headings(text))
    missing = []
    for label, pattern in concepts:
        if not re.search(pattern, headings_block, re.IGNORECASE):
            missing.append(label)
    return missing


# ---------------------------------------------------------------------------
# (c) EN trigger consistency — at least one phrase in README.md example
#     section must appear verbatim in SKILL.md description.
# ---------------------------------------------------------------------------

_EN_TRIGGER_RE = re.compile(
    r"where were we|i.?m lost|recap|bring me back|what are we doing",
    re.IGNORECASE,
)


def _en_readme_has_trigger_phrase(readme_text: str) -> bool:
    return bool(_EN_TRIGGER_RE.search(readme_text))


# ---------------------------------------------------------------------------
# (d) JA / zh-TW trigger phrases — at least 3 language-native triggers
#     that also appear in SKILL.md description.
# ---------------------------------------------------------------------------

JA_TRIGGERS_IN_SKILL = [
    "ちょっと振り返って",
    "今どこだっけ",
    "振り返り",
    "振り返りをして",
    "状況を整理して",
]

ZHTW_TRIGGERS_IN_SKILL = [
    "我們剛剛在幹嘛",
    "剛剛講到哪",
    "我跟丟了",
    "帶我回到",
    "我們在做什麼",
]


def _count_triggers_in_readme(readme_text: str, triggers: list[str]) -> int:
    """Count how many trigger phrases appear in the README body."""
    return sum(1 for t in triggers if t in readme_text)


# ---------------------------------------------------------------------------
# The single test
# ---------------------------------------------------------------------------

def test_tri_lang_readmes_consistent():
    # -----------------------------------------------------------------------
    # (a) All 3 README files exist
    # -----------------------------------------------------------------------
    for path in [README_EN, README_JA, README_ZHTW]:
        assert path.exists(), f"Missing README: {path}"

    en_text   = _read(README_EN)
    ja_text   = _read(README_JA)
    zhtw_text = _read(README_ZHTW)

    # -----------------------------------------------------------------------
    # (b) Each README has 4 required section heading concepts
    # -----------------------------------------------------------------------
    en_missing   = _check_concepts(en_text,   REQUIRED_CONCEPTS_EN)
    ja_missing   = _check_concepts(ja_text,   REQUIRED_CONCEPTS_JA)
    zhtw_missing = _check_concepts(zhtw_text, REQUIRED_CONCEPTS_ZHTW)

    assert not en_missing,   f"EN README missing heading concepts: {en_missing}"
    assert not ja_missing,   f"JA README missing heading concepts: {ja_missing}"
    assert not zhtw_missing, f"zh-TW README missing heading concepts: {zhtw_missing}"

    # -----------------------------------------------------------------------
    # (c) EN README contains >=1 trigger phrase that also appears in SKILL.md
    # -----------------------------------------------------------------------
    assert _en_readme_has_trigger_phrase(en_text), (
        "EN README example section must contain at least one trigger phrase "
        "recognisable in SKILL.md description (e.g. 'where were we', 'I'm lost', "
        "'recap', 'bring me back', 'what are we doing')"
    )

    # -----------------------------------------------------------------------
    # (d) JA README: >=3 language-native triggers also in SKILL.md
    # -----------------------------------------------------------------------
    ja_in_readme = _count_triggers_in_readme(ja_text, JA_TRIGGERS_IN_SKILL)
    assert ja_in_readme >= 3, (
        f"JA README must contain >=3 JA trigger phrases that appear in SKILL.md; "
        f"found {ja_in_readme}: "
        f"{[t for t in JA_TRIGGERS_IN_SKILL if t in ja_text]}"
    )

    # -----------------------------------------------------------------------
    # (d) zh-TW README: >=3 language-native triggers also in SKILL.md
    # -----------------------------------------------------------------------
    zhtw_in_readme = _count_triggers_in_readme(zhtw_text, ZHTW_TRIGGERS_IN_SKILL)
    assert zhtw_in_readme >= 3, (
        f"zh-TW README must contain >=3 zh-TW trigger phrases that appear in SKILL.md; "
        f"found {zhtw_in_readme}: "
        f"{[t for t in ZHTW_TRIGGERS_IN_SKILL if t in zhtw_text]}"
    )


def test_tri_lang_readmes_show_localized_goal_grounded_alignment_loop():
    readmes = {
        "en": (_read(README_EN), ("Purpose and current position", "Ask for the original purpose", "Ask about the next step")),
        "ja": (_read(README_JA), ("目的と現在地", "元の目的を尋ねる", "次の一歩を確認する")),
        "zh-TW": (_read(README_ZHTW), ("目的與現在位置", "詢問原始目的", "確認下一步")),
    }

    for language, (text, labels) in readmes.items():
        assert "Goal-Grounded Alignment Loop" in text, f"{language} README lacks loop name"
        assert "```mermaid" in text, f"{language} README lacks Mermaid loop diagram"
        for label in labels:
            assert label in text, f"{language} README lacks localized label: {label}"

    assert "7-block schema" not in readmes["en"][0]
    assert "7 ブロックスキーマ" not in readmes["ja"][0]
    assert "7 格式" not in readmes["zh-TW"][0]
    for language, (text, _) in readmes.items():
        assert "recap-state/" in text, f"{language} README uses a stale directory root"
        assert "\nrecap/\n" not in text, f"{language} README names a nonexistent directory"


def test_tri_lang_readmes_keep_final_question_conditional() -> None:
    readmes = {
        "en": (_read(README_EN), "purpose is unknown", "purpose is grounded", "Ask for the original purpose"),
        "ja": (_read(README_JA), "目的が不明", "目的が確認できる", "元の目的を尋ねる"),
        "zh-TW": (_read(README_ZHTW), "目的不明", "目的已確認", "詢問原始目的"),
    }
    for language, (text, unknown, grounded, ask_purpose) in readmes.items():
        prose, diagram = text.split("```mermaid", 1)
        diagram = diagram.split("```", 1)[0]
        assert unknown in prose, f"{language} README omits unknown-purpose behavior"
        assert grounded in prose, f"{language} README omits grounded-purpose behavior"
        assert ask_purpose in diagram, f"{language} diagram omits purpose question"
        assert "WaitPurpose" in diagram and "WaitNext" in diagram, (
            f"{language} diagram must keep the two waiting states separate"
        )
        assert re.search(r"Check\s+-->[^\n]*AskPurpose", diagram)
        assert re.search(r"Check\s+-->[^\n]*Next", diagram)
        assert "AskPurpose --> WaitPurpose" in diagram
        assert "Next --> WaitNext" in diagram
        assert "WaitPurpose -->" in diagram and "| Purpose" in diagram
        assert not re.search(r"WaitPurpose\s+-->[^\n]*Continue", diagram)


def test_tri_lang_readmes_describe_flexible_recap_and_pause_without_six_section_claim():
    localized_contract = {
        "en": (_read(README_EN), ("purpose", "only the sections", "waits for your answer", "writes nothing to disk")),
        "ja": (_read(README_JA), ("目的", "必要なセクションだけ", "返答を待つ", "ファイルには何も書かない")),
        "zh-TW": (_read(README_ZHTW), ("目的", "只保留有用的段落", "等待你的回答", "不會寫入任何檔案")),
    }
    stale_claims = {
        "en": ("six-section", "six sections", "fixed six-section"),
        "ja": ("6 つの", "6 セクション", "同じ 6"),
        "zh-TW": ("六個段落", "六段結構", "六個自然段落"),
    }

    for language, (text, required) in localized_contract.items():
        for phrase in required:
            assert phrase in text, f"{language} README lacks: {phrase}"
        for claim in stale_claims[language]:
            assert claim not in text, f"{language} README retains fixed-format claim: {claim}"
