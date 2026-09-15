"""Adversary mutation probes against the change's prose gates.

Each probe copies the smallest tree a committed test file needs into a temp
dir, flips the polarity of one pinned instruction (keeping word counts so the
150-word cap cannot catch it by accident), runs the committed test file on
the copy, and requires that it FAILS. A passing run is a surviving mutant:
the gate would accept a card or guide telling the agent the opposite.

Run:
    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest -q -p no:cacheprovider \
        docs/loom/2026-09-16-plain-language-replies/evidence/probes/test_probe_prose_gate_mutants.py
"""
from __future__ import annotations

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
NEGATION = re.compile(r"\b(never|not|no|avoid)\b", re.I)


def _sub_once(text: str, pattern: str, repl: str) -> str:
    new, n = re.subn(pattern, repl, text, count=1)
    assert n == 1, f"mutant anchor not found: {pattern}"
    return new


def _pytest(test_file: Path, rootdir: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                           "--rootdir", str(rootdir), str(test_file)],
                          capture_output=True, text=True, timeout=300, cwd=str(rootdir))


# ---------- card mutants (test_visualization_card_hook.py) ----------

# (full-card pattern, full repl, coexist pattern, coexist repl); word counts preserved.
CARD_MUTANTS = {
    "language-negated": (r"in their language\. 1\)", "never in their language. 1)",
                         r"in their language\. 1\)", "never in their language. 1)"),
    "literal-negated": (r"3\) Be literal:", "3) Never literal:",
                        r"3\) Be literal:", "3) Never literal:"),
    "tables-negated": (r"4\) Use tables or", "4) No tables or",
                       r"4\) Tables or diagrams:", "4) No tables or diagrams:"),
}
# An added negation word costs one word; drop one elsewhere so the cap holds.
TRIM = (r"details after\.", "details.")


def _card_tree(tmp: Path, name: str) -> Path:
    root = tmp / "lw"
    shutil.copytree(PLUGIN / "hooks", root / "hooks")
    shutil.copytree(VIS, root / "skills" / "loom-visualization")
    (root / "scripts").mkdir()
    for f in ("test_visualization_card_hook.py", "fixtures_ascii_graph_trigger_card.md"):
        shutil.copy2(PLUGIN / "scripts" / f, root / "scripts" / f)
    fp, fr, cp, cr = CARD_MUTANTS[name]
    assets = root / "skills" / "loom-visualization" / "assets"
    for card, pat, repl in (("trigger-card.md", fp, fr), ("trigger-card-coexist.md", cp, cr)):
        path = assets / card
        text = " ".join(path.read_text(encoding="utf-8").split("\n")[1:])
        head = path.read_text(encoding="utf-8").split("\n")[0]
        text = _sub_once(" ".join(text.split()), pat, repl)
        if len(repl.split()) > len(pat.replace("\\", "").split()):
            text = _sub_once(text, *TRIM)
        path.write_text(head + "\n" + text + "\n", encoding="utf-8")
    return root


@pytest.mark.parametrize("name", sorted(CARD_MUTANTS))
def test_cardTests_negatedRuleMutant_rejected(tmp_path, name):
    """The committed card tests must fail on a card that negates one of the four rules."""
    root = _card_tree(tmp_path, name)
    for card in ("trigger-card.md", "trigger-card-coexist.md"):
        words = (root / "skills/loom-visualization/assets" / card).read_text(encoding="utf-8").split()
        assert len(words) <= 150, (card, len(words))  # mutant is not caught by the cap
    proc = _pytest(root / "scripts" / "test_visualization_card_hook.py", root)
    assert proc.returncode != 0, f"surviving mutant {name}:\n{proc.stdout[-800:]}"


def test_cardTests_exitTwoMutant_rejected(tmp_path):
    """Control: a hook that exits 2 (blocks the user's prompt) is killed by the committed tests."""
    root = _card_tree(tmp_path, "literal-negated")
    shutil.copytree(VIS, root / "skills" / "loom-visualization", dirs_exist_ok=True)
    hook = root / "hooks" / "visualization-card"
    hook.write_text(_sub_once(hook.read_text(encoding="utf-8"), r"sys\.exit\(0\)", "sys.exit(2)"),
                    encoding="utf-8")
    proc = _pytest(root / "scripts" / "test_visualization_card_hook.py", root)
    assert proc.returncode != 0


# ---------- guide mutants (test_references.py) ----------

GUIDE_MUTANTS = {
    "yes-no-not-asked-directly": (r"is\s+asked\s+directly", "is never asked directly"),
    "recommend-negated": (r"marks\s+the\s+one\s+you\s+recommend", "never marks the one you recommend"),
    "metaphors-allowed": (r"Do\s+not\s+use\s+metaphors\s+or\s+analogies,\s+and\s+do\s+not\s+reach\s+for",
                          "Use metaphors or analogies, and reach for"),
}


def _guide_tree(tmp: Path, name: str) -> Path:
    root = tmp / "skill"
    shutil.copytree(VIS, root)
    guide = root / "references" / "plain-language.md"
    guide.write_text(_sub_once(guide.read_text(encoding="utf-8"), *GUIDE_MUTANTS[name]),
                     encoding="utf-8")
    return root


@pytest.mark.parametrize("name", sorted(GUIDE_MUTANTS))
def test_referenceTests_negatedGuideMutant_rejected(tmp_path, name):
    """The committed reference tests must fail on a guide whose rule says the opposite."""
    root = _guide_tree(tmp_path, name)
    proc = _pytest(root / "scripts" / "test_references.py", root)
    assert proc.returncode != 0, f"surviving mutant {name}:\n{proc.stdout[-800:]}"


# ---------- README timing mutants (test_readme_card_timing.py) ----------

README_MUTANTS = {
    "hyphenated-en": ("README.md", "\nThe card also arrives at session-start.\n"),
    "japanese-wording": ("README.ja.md", "\nカードはセッション開始時に一度だけ届く。\n"),
    "chinese-wording": ("README.zh-TW.md", "\n卡片只在工作階段開始時送達一次。\n"),
}


@pytest.mark.parametrize("name", sorted(README_MUTANTS))
def test_readmeTimingTests_staleTimingMutant_rejected(tmp_path, name):
    """The committed README timing test must fail when a README again says the card arrives once at start."""
    root = tmp_path / "lw"
    (root / "scripts").mkdir(parents=True)
    (root / ".codex-plugin").mkdir()
    for f in ("README.md", "README.ja.md", "README.zh-TW.md", ".codex-plugin/plugin.json",
              "scripts/test_readme_card_timing.py"):
        shutil.copy2(PLUGIN / f, root / f)
    target, line = README_MUTANTS[name]
    with open(root / target, "a", encoding="utf-8") as fh:
        fh.write(line)
    proc = _pytest(root / "scripts" / "test_readme_card_timing.py", root)
    assert proc.returncode != 0, f"surviving mutant {name}:\n{proc.stdout[-800:]}"


# ---------- self-tests: each mutant really flips polarity ----------

def test_mutantBuilder_cardAndGuideMutants_flipNegation(tmp_path):
    """Synthetic check: every mutant sentence gains a negation, or loses the one it had."""
    for name, (fp, fr, cp, cr) in CARD_MUTANTS.items():
        assert not NEGATION.search(fp.replace("\\", "")) and NEGATION.search(fr), name
        assert not NEGATION.search(cp.replace("\\", "")) and NEGATION.search(cr), name
    for name, (pat, repl) in GUIDE_MUTANTS.items():
        assert bool(NEGATION.search(pat.replace(r"\s+", " "))) != bool(NEGATION.search(repl)), name
    # Rejected example: a replacement that keeps polarity is not a mutant.
    assert not (bool(NEGATION.search("is asked directly")) != bool(NEGATION.search("is asked plainly")))
