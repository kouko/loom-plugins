"""Adversary probes against this change's card guards and form rules.

Two shapes of probe live here.

1. Guard-bypass probes call the committed guard helpers in
   `loom-workflow/scripts/test_visualization_card_hook.py` directly and show a
   card text that dissolves the obligation while the guard still reports no
   error. Each such probe asserts the bypass, so it is RED against the intended
   contract and GREEN against the code as committed: when a guard is fixed, the
   matching probe fails and must be flipped with the fix.
2. Mutant probes copy the smallest tree a committed test file needs, mutate one
   file, run the committed test file on the copy and require it to FAIL. A
   passing run is a surviving mutant.

Run:
    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest -q -p no:cacheprovider \
        docs/loom/2026-09-16-plain-language-follow-ups/evidence/probes/test_probe_card_guard_bypasses.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    """Walk upward until a directory holding docs/loom and loom-workflow is found."""
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs" / "loom").is_dir() and (candidate / "loom-workflow").is_dir():
            return candidate
    raise RuntimeError(f"repo root not found above {start}")


ROOT = _find_repo_root(Path(__file__).parent)
PLUGIN = ROOT / "loom-workflow"
VIS = PLUGIN / "skills" / "loom-visualization"
SCOPE = "When asking or answering how to do something"


@pytest.fixture(scope="module")
def hook_tests():
    """The committed card-hook test module, imported for its guard helpers."""
    sys.path.insert(0, str(PLUGIN / "scripts"))
    try:
        import test_visualization_card_hook as module
    finally:
        sys.path.pop(0)
    return module


def _pytest(test_file: Path, rootdir: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                           "--rootdir", str(rootdir), str(test_file)],
                          capture_output=True, text=True, timeout=300, cwd=str(rootdir))


def _sub_once(text: str, pattern: str, repl: str) -> str:
    new, n = re.subn(pattern, repl, text, count=1)
    assert n == 1, f"mutant anchor not found: {pattern}"
    return new


# ---------- 1. the affirmative-verb guards accept a modal softener ----------

# Each entry: the guard helper's name, and a card sentence that keeps every
# pinned literal, carries no token in the guard's NEGATION list, and still
# leaves the agent free to skip the obligation.
SOFTENED = {
    "missed_alternative_verb_errors":
        f"{SCOPE}, you may list or rule out doing nothing or later, a smaller version, "
        "and combining two.",
    "missed_alternative_errors":
        f"{SCOPE}, it is optional to mention doing nothing or later, a smaller version, "
        "and combining two.",
    "inline_decision_rule_errors":
        f"{SCOPE}, it is optional to offer 2+ workable options in a table, recommending one; "
        "for plainer explanations read loom-visualization's `references/plain-language.md` "
        "first.",
}


@pytest.mark.parametrize("guard", sorted(SOFTENED))
def test_cardGuard_modalSoftenedObligation_passesUncaught(hook_tests, guard):
    """A `you may` / `it is optional to` card keeps every literal and clears the guard."""
    assert getattr(hook_tests, guard)(SOFTENED[guard]) == [], guard


def test_cardGuard_imperativeObligation_passesAsIntended(hook_tests):
    """Self-test: the un-softened sentence the committed card carries is accepted."""
    affirmative = (f"{SCOPE}, offer 2+ workable options in a table, recommending one; list or "
                   "rule out doing nothing or later, a smaller version, and combining two.")
    assert hook_tests.missed_alternative_verb_errors(affirmative) == []
    assert hook_tests.missed_alternative_errors(affirmative) == []


def test_cardGuard_negatedObligation_isRejectedAsIntended(hook_tests):
    """Self-test: the one negated form the guard does catch still fails."""
    negated = (f"{SCOPE}, never list or rule out doing nothing or later, a smaller version, "
               "and combining two.")
    assert hook_tests.missed_alternative_verb_errors(negated) != []


# ---------- 2. the guards' negation vocabulary is narrower than the sibling gate's ----------

# `test_templates.py` rejects not|never|no|none|without|unless|except|avoid and any
# `n't`; the card hook's NEGATION knows only never|not|no|avoid|don't. These
# sentences negate the rule using a token only the wider list carries.
NEGATED_PAST_THE_GUARD = {
    "without": f"{SCOPE}, answer without listing doing nothing or later, a smaller version, "
               "and combining two.",
    "isnt-required": f"{SCOPE}, it isn't required to mention doing nothing or later, a smaller "
                     "version, and combining two.",
    "unless-asked": f"{SCOPE}, skip doing nothing or later, a smaller version, and combining "
                    "two unless the user asks.",
}


@pytest.mark.parametrize("token", sorted(NEGATED_PAST_THE_GUARD))
def test_cardGuardNegation_tokenOutsideItsVocabulary_passesUncaught(hook_tests, token):
    """A negation the sibling gate rejects clears the card guard untouched."""
    text = NEGATED_PAST_THE_GUARD[token]
    assert hook_tests.missed_alternative_errors(text) == [], token
    assert hook_tests.NEGATION.search(text) is None, token


def test_cardGuardNegation_widerVocabularyOfSiblingGate_catchesEveryToken():
    """Self-test: the sibling gate's own negation list rejects all three sentences."""
    wider = re.compile(r"\b(?:not|never|no|none|without|unless|except|avoid)\b|n't", re.I)
    for token, text in NEGATED_PAST_THE_GUARD.items():
        assert wider.search(text), token
    assert not wider.search(f"{SCOPE}, list or rule out each alternative.")


# ---------- 3. the situation guard never checks which skill is invoked ----------

FOREIGN_INVOCATION = (
    "4) Use tables or diagrams: for progress, a before and after, what each choice means, "
    "readiness, confirmed against unconfirmed, findings, risks or supported environments, "
    "invoke `some-unrelated-skill` FIRST and lead with its table."
)


def test_situationGuard_situationsUnderAForeignInvocation_passesUncaught(hook_tests):
    """Naming the eight situations while routing them away from loom-visualization clears the guard."""
    assert hook_tests.situation_errors(FOREIGN_INVOCATION) == []
    assert "loom-visualization" not in FOREIGN_INVOCATION


def test_situationGuard_situationsSplitAcrossTwoInvocations_passesUncaught(hook_tests):
    """The guard unions all trigger sentences, so no single sentence need carry the rule."""
    split = ("Invoke `loom-visualization` for comparisons. Separately, invoke `another-skill` "
             "for progress, a before and after, what each choice means, readiness, confirmed "
             "against unconfirmed, findings, risks or supported environments.")
    assert hook_tests.situation_errors(split) == []


def test_situationGuard_noSituationNamed_isRejectedAsIntended(hook_tests):
    """Self-test: a trigger list naming no situation still reports every situation missing."""
    assert hook_tests.situation_errors(
        "4) Use tables: for comparisons, invoke `loom-visualization` FIRST."
    ) == list(hook_tests.SITUATIONS)


# ---------- 4. the word cap is blind to a non-spaced script ----------

def test_cardWordCap_cjkCardWithNoSpaces_passesUncaught(hook_tests):
    """A 1,200-character CJK card counts as one word, so the 181-word cap never fires."""
    cjk = "# 視覺化提醒卡\n" + "表格圖解流程說明" * 150
    assert len(cjk) > 1_000
    assert hook_tests.card_word_errors(cjk) == []


def test_cardWordCap_paddedEnglishCard_isRejectedAsIntended(hook_tests):
    """Self-test: the same cap does fire on space-separated padding."""
    assert hook_tests.card_word_errors("word " * (hook_tests.MAX_CARD_WORDS + 1)) != []


def test_cardWordCap_emptyCard_reportsNoError(hook_tests):
    """Empty and absent: a zero-word card is inside the cap, so the cap alone never proves a card exists."""
    assert hook_tests.card_word_errors("") == []


# ---------- 5. mutants against committed test files ----------

def _vis_tree(tmp: Path) -> Path:
    root = tmp / "skill"
    shutil.copytree(VIS, root, ignore=shutil.ignore_patterns("__pycache__"))
    return root


@pytest.mark.xfail(strict=True, reason="surviving mutant: ASCII_BY_CLIENT scans only SKILL.md, "
                                       "client-matrix.md and detect_client.py, never the templates")
def test_templateTests_clientDrivenAsciiInATemplate_rejected(tmp_path):
    """`stay ASCII` reintroduced in a template must be caught; the guard scans three files only."""
    root = _vis_tree(tmp_path)
    template = root / "templates" / "02-linear-steps.md"
    template.write_text(
        template.read_text(encoding="utf-8")
        + "\nWhen `remote_viewer` is true, stay ASCII in a code block.\n",
        encoding="utf-8",
    )
    proc = _pytest(root / "scripts" / "test_templates.py", root)
    assert proc.returncode != 0, f"surviving mutant:\n{proc.stdout[-1200:]}"


@pytest.mark.xfail(strict=True, reason="surviving mutant: no committed test forbids a "
                                       "client-driven ASCII rule inside the per-turn cards")
def test_cardTests_clientDrivenAsciiInTheTriggerCard_rejected(tmp_path):
    """`stay ASCII` reintroduced in the per-turn card must be caught by some committed test."""
    root = tmp_path / "lw"
    shutil.copytree(PLUGIN / "hooks", root / "hooks")
    shutil.copytree(VIS, root / "skills" / "loom-visualization",
                    ignore=shutil.ignore_patterns("__pycache__"))
    (root / "scripts").mkdir()
    for f in ("test_visualization_card_hook.py", "fixtures_ascii_graph_trigger_card.md"):
        shutil.copy2(PLUGIN / "scripts" / f, root / "scripts" / f)
    card = root / "skills" / "loom-visualization" / "assets" / "trigger-card.md"
    head, *body = card.read_text(encoding="utf-8").split("\n")
    flat = _sub_once(" ".join(" ".join(body).split()),
                     r"Skip loom-visualization for one-paragraph answers; never decorate\.",
                     "With a remote viewer attached, stay ASCII; never decorate.")
    card.write_text(head + "\n" + flat + "\n", encoding="utf-8")
    assert len(card.read_text(encoding="utf-8").split()) <= 181  # not caught by the cap
    proc = _pytest(root / "scripts" / "test_visualization_card_hook.py", root)
    assert proc.returncode != 0, f"surviving mutant:\n{proc.stdout[-1200:]}"


@pytest.mark.xfail(strict=True, reason="surviving mutant: test_detect_client.py asserts only that "
                                       "`reason` is a non-empty string, so both rewritten "
                                       "strings are unpinned")
def test_detectClientTests_rewrittenReasonStrings_rejected(tmp_path):
    """The `reason` strings this change rewrote must be pinned by the committed detector tests."""
    root = _vis_tree(tmp_path)
    script = root / "scripts" / "detect_client.py"
    text = script.read_text(encoding="utf-8")
    text = _sub_once(text, r'"no known client marker; Mermaid rendering is unverified"',
                     '"mutant reason string"')
    text = _sub_once(text, r'"; remote viewer attached, Mermaid stays unsafe"',
                     '"; mutant remote-viewer note"')
    script.write_text(text, encoding="utf-8")
    proc = _pytest(root / "scripts" / "test_detect_client.py", root)
    assert proc.returncode != 0, f"surviving mutant:\n{proc.stdout[-1200:]}"


def test_detectClient_mutatedReason_isReallyEmitted(tmp_path):
    """Self-test: the mutated detector really prints the mutant string, so the probe is honest."""
    root = _vis_tree(tmp_path)
    script = root / "scripts" / "detect_client.py"
    script.write_text(
        _sub_once(script.read_text(encoding="utf-8"),
                  r'"no known client marker; Mermaid rendering is unverified"',
                  '"mutant reason string"'),
        encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", str(script)],
                          capture_output=True, text=True, timeout=60, env={"PATH": "/usr/bin:/bin"})
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["reason"] == "mutant reason string"


# ---------- 6. the sibling skill still carries the rule this change forbids ----------

def _templates_module():
    sys.path.insert(0, str(VIS / "scripts"))
    try:
        import test_templates as module
    finally:
        sys.path.pop(0)
    return module


RECAP_SKILL = PLUGIN / "skills" / "recap-state" / "SKILL.md"


@pytest.mark.xfail(strict=True, reason="live contradiction: recap-state/SKILL.md still says "
                                       "'for an unknown or terminal client, use ASCII', and "
                                       "test_recap_state_compaction.py pins that phrase")
def test_clientDrivenAsciiRule_acrossEveryLoomWorkflowSkill_isAbsent():
    """The change's own detector, pointed at the sibling skill the plan listed, still fires."""
    module = _templates_module()
    flat = " ".join(RECAP_SKILL.read_text(encoding="utf-8").split())
    hit = module.ASCII_BY_CLIENT.search(flat)
    assert not hit, f"recap-state/SKILL.md: {hit.group(0)!r}"


def test_clientDrivenAsciiDetector_onTheSiblingSkill_reallyMatches():
    """Self-test: the detector matches recap-state's wording, so the probe above is not vacuous."""
    module = _templates_module()
    assert module.ASCII_BY_CLIENT.search("for an unknown or terminal client, use ASCII")
    assert not module.ASCII_BY_CLIENT.search(
        "for a destination that does not render markdown, use ASCII")


# ---------- 7. the word cap was raised twice inside one change ----------

CAP_LINE = re.compile(r"^\+MAX_CARD_WORDS = (\d+)", re.M)


def _cap_raises(values_newest_first):
    """Every (new, old) pair where the cap went up, oldest raise first."""
    pairs = list(zip(values_newest_first, values_newest_first[1:]))  # (newer, older)
    return [(new, old) for new, old in reversed(pairs) if new > old]


@pytest.mark.xfail(strict=True, reason="the repository's own memory entry "
                                       "a-cap-raised-at-every-touch-is-not-a-cap: the cap went "
                                       "150 -> 165 -> 181, two raises inside one change")
def test_cardWordCap_historyOfTheCapLine_showsAtMostOneRaise():
    """A cap raised more than once has become a running total, not a ceiling."""
    proc = subprocess.run(
        ["git", "log", "--no-merges", "-p", "--format=%h",
         "--", "loom-workflow/scripts/test_visualization_card_hook.py"],
        capture_output=True, text=True, timeout=120, cwd=str(ROOT), check=True)
    values = [int(v) for v in CAP_LINE.findall(proc.stdout)]  # newest first
    assert values, "no MAX_CARD_WORDS line found in the file's history"
    raises = _cap_raises(values)
    assert len(raises) <= 1, f"cap raised {len(raises)} times: {raises}"


def test_capRaiseCounter_syntheticHistory_countsOnlyIncreases():
    """Self-test: the counter counts raises, and ignores the introduction and a lowering."""
    assert _cap_raises([181, 165, 150]) == [(165, 150), (181, 165)]
    assert _cap_raises([150]) == []
    assert _cap_raises([140, 150]) == []  # a lowering is not a raise


# ---------- 8. the sole remaining form rests on unverified evidence ----------

def _matrix_rows():
    text = (VIS / "references" / "client-matrix.md").read_text(encoding="utf-8")
    rows = [line for line in text.splitlines()
            if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|\s*$", line)]
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    return header, [[c.strip() for c in r.strip("|").split("|")] for r in rows[1:]]


@pytest.mark.xfail(strict=True, reason="this change dropped the ASCII half of the form, so the "
                                       "whole reply now rests on a GFM column the matrix marks "
                                       "unverified in 8 of 10 rows")
def test_clientMatrix_everyRowsOnlyForm_restsOnAVerifiedCell():
    """The matrix's own rule — unverified means 'does not render' — applied to the form it now prescribes."""
    header, rows = _matrix_rows()
    gfm, form = header.index("GFM table"), header.index("Form in a chat reply")
    unbacked = [(r[0], r[gfm]) for r in rows
                if "markdown table" in r[form] and r[gfm] == "unverified"]
    assert unbacked == [], f"{len(unbacked)} of {len(rows)} rows prescribe an unverified form: {unbacked}"


def test_clientMatrix_columnsItReadsFrom_arePresent():
    """Self-test: the probe reads real columns, so an empty result would mean evidence, not a typo."""
    header, rows = _matrix_rows()
    assert "GFM table" in header and "Form in a chat reply" in header, header
    assert len(rows) >= 10
    assert {r[header.index("GFM table")] for r in rows} <= {"yes", "unverified"}


# ---------- 9. the gate's table pin was loosened, not only moved ----------

def test_gatePin_sentenceThatDropsAsciiEntirely_acceptedByTheLoosenedPin(tmp_path):
    """The pin no longer constrains the drawn form: a table-only sentence satisfies it."""
    sys.path.insert(0, str(VIS / "scripts"))
    try:
        import test_templates as module
    finally:
        sys.path.pop(0)
    assert module.pinned_sentence_ok(
        "Everywhere else the reply gets a markdown table and a drawn diagram is dropped.",
        *module.TABLE_ASCII_PIN,
    )
    # The pin it replaced required the drawn form to be named alongside the table.
    assert not module.pinned_sentence_ok(
        "Everywhere else the reply gets a markdown table and a drawn diagram is dropped.",
        "use", ("markdown table plus ASCII", "Everywhere else"),
    )
