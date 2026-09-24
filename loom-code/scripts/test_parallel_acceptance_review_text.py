"""Acceptance testing starts with the first-round reviewers, who are resumed with its committed
report before their Round 1 verdict (plan W0-01; intent 2026-09-24-parallel-acceptance-testing-
and-review Acceptance 1, 2, 3, 4, 6). concern: false-green prose pin — each rule sentence is
pinned exactly and the §3 rules whole, so a reversed, re-assigned or appended rule must fail.
"""
import subprocess
import sys
from pathlib import Path
from prose_pin import flat_prose, pins_exact_sentence

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "loom-code"
SKILL = CODE / "skills/closing-review/SKILL.md"
REVIEW = flat_prose(SKILL)
DEPTH = REVIEW.split("## 2. Compute review depth", 1)[1].split("## 3.", 1)[0]
HEAD, TAIL = "is publication metadata. ", " When `acceptance-test` is skipped"
PARA = REVIEW.partition("## 3. Run acceptance testing ")[2].partition(HEAD)[2].split(TAIL)[0]
SECTION = flat_prose(CODE / "agents/reviewer.md").partition(
    "## Round 1 alongside acceptance testing ")[2].split(" ## Fix rounds")[0]
S2 = ("When acceptance testing is needed, it starts together with the first-round reviewers on the "
      "same functional content (§3), and the reviewers give their Round 1 verdict only after reading "
      "its committed report.",)
NEW_RULES = (
    "Start the acceptance tester and the first-round reviewers on the same commit at the same time.",
    "Finish acceptance testing and commit that report on the change branch before running "
    "`finalize-review`.",
    "Its evidence file, `docs/loom/<change-id>/evidence/acceptance-test-evidence.md`, is functional "
    "content too and is committed with the report under the same deadline.",
    "Once the report and its evidence file are committed, resume each of those reviewers, the same "
    "agent rather than a new one, with the delta from the commit it started on to the report commit.",
    "Each reads the report and evidence against the change it already reviewed, and only then "
    "returns its Round 1 verdict.",
    "A reviewer's return before that resume is not a verdict.",
    "The commit the reviewers started from and the report commit form Round 1's single "
    "functional-content digest.",
    "A reviewer that cannot be resumed, such as a one-shot vendor CLI, starts after the report is "
    "committed.",
    "A report committed after their verdicts is new functional content and needs the next round.")
S3 = NEW_RULES  # the paragraph's kept head and skip sentence border it (test below)
REV = (
    "When closing review runs acceptance testing, it starts at the same time as your Round 1 review.",
    "First review the change as usual.",
    "You are then resumed with the delta from the commit you started on to the report commit, which "
    "adds the acceptance test report and its evidence file.",
    "Read them against the change you reviewed: a verdict the evidence does not support is an "
    "overclaim, and an untried Acceptance line is an omission.",
    "Add your findings on them and return one verdict covering both the change and the report.",
    "What you returned before that resume is not your verdict.")
WEAKENED = (
    (S3, NEW_RULES[0], "Start the reviewers after the report is committed."),
    (S3, "the same agent rather than a new one", "a new reviewer"), (S3, "is not a", "is its"),
    (S3, "form Round 1's single functional-content digest", "form two separate digests"),
    (S3, "and only then returns its Round 1 verdict", "after returning its Round 1 verdict"),
    (S3, "with the delta from the commit it started on to the report commit",
     "with the report commit as its new `reviewed_sha`"),
    (REV, "the delta from the commit you started on to the report commit", "a new `reviewed_sha`"),
    (S3, "needs the next round.", "needs the next round. The report commit is a separate digest."),
    (S2, "only after reading", "before reading"), (S2, "it starts together with", "it finishes before"),
    (REV, "is not your verdict.", "is your verdict."), (REV, "return one verdict", "return a second verdict"))


def pinned(text: str, sentences: tuple[str, ...]) -> bool:
    return text == " ".join(sentences) and all(pins_exact_sentence(text, s) for s in sentences)


def test_new_rules_are_pinned_exactly() -> None:
    assert DEPTH.count(f"<!-- /gate --> {S2[0]} After Build commits completed functional content, "
                       "run: ```text python3 <loom-code>/scripts/loom_checker.py reviewer-count") == 1
    assert REVIEW.count(HEAD + " ".join(S3) + TAIL) == 1
    assert pinned(PARA, S3) and pinned(SECTION, REV)


def test_weakened_or_appended_rewrites_fail() -> None:
    for sentences, old, new in WEAKENED:
        text = " ".join(sentences)
        weakened = text.replace(old, new, 1)
        assert weakened != text, old
        assert not pinned(weakened, sentences), new


def test_one_fix_list_report_shape_gates_and_rules_kept() -> None:
    assert ("reviewers and independent acceptance testing returned on the current "
            "functional-content digest into one list.") in REVIEW
    report = (CODE / "skills/closing-review/references/acceptance-test-report.md").read_text()
    assert "| # | What you asked for | Verdict | What happened | Re-run |" in report
    main = subprocess.run(["git", "show", "origin/main:loom-code/skills/closing-review/SKILL.md"],
                          cwd=ROOT, capture_output=True, text=True, check=True).stdout
    assert SKILL.read_text().count("<!-- gate") == main.count("<!-- gate")
    assert not any(w in " ".join(S2 + NEW_RULES + REV) for w in ("dispatch", "new step"))
    rules = subprocess.run([sys.executable, str(CODE / "scripts/loom_checker.py"), "--list-rules"],
                           capture_output=True, text=True, check=True).stdout.splitlines()
    assert len(rules) == 26
