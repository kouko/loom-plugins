"""Adversary probe: hand-written mutants of the mutation-landed rule and its pointers.
# concern: the mutation-landed rule restated in a reader file, or moved out of tests-standard.md section 1 that every pointer names, while the change's own pin tests stay green.

The intent's constraint keeps the rule in tests-standard.md alone, with every
other file carrying only a pointer; baseline.md and adversarial.md point to
it as "§1". Each mutant copies the real files into a temporary directory,
applies its edits there (each anchor must match exactly once and the text
must change, so the mutation is confirmed landed), points
loom-code/tests/test_tests_standard_text.py at the copies and runs every test
in it. A mutant that every test still passes survived. The real files are
never modified.

Run from the repo root:
    python3 -m pytest docs/loom/2026-11-28-mutation-landed-check/evidence/probes/test_probe_mutation_rule_pins.py
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs" / "loom").is_dir() and (candidate / "loom-code").is_dir():
            return candidate
    raise RuntimeError(f"repo root not found above {start}")


ROOT = _find_repo_root(Path(__file__).parent)
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))

# Module attribute in test_tests_standard_text.py -> real file it reads.
FILES = {
    "STANDARD": ROOT / "loom-code/references/tests-standard.md",
    "BASELINE": ROOT / "loom-code/references/engineering-baseline.md",
    "LENSES": ROOT / "loom-code/skills/closing-review/references/lenses.md",
    "ADVERSARIAL": ROOT / "loom-code/skills/closing-review/references/adversarial.md",
}
RULE_PARA = (
    "Whoever forces a RED by deliberately mutating code, a fixture or text must\n"
    "confirm, before counting it as evidence, that the mutation landed — a\n"
    "non-empty diff against the pristine copy, or the edit anchor matched exactly\n"
    "once — and that the unmutated version passes. An unconfirmed RED is not\n"
    "evidence.\n\n"
)
SECTION_3 = "## 3. Tests go through the public interface\n"


def _failing_tests(tmp: Path, edits: list[tuple[str, str, str]]) -> list[str]:
    """Apply each (file, anchor, replacement) to copies; return the pin tests that fail."""
    copies = {}
    for key, path in FILES.items():
        copies[key] = tmp / path.name
        shutil.copy(path, copies[key])
    for key, old, new in edits:
        text = copies[key].read_text(encoding="utf-8")
        assert text.count(old) == 1, f"mutation anchor must occur exactly once in {key}: {old[:50]!r}"
        mutated = text.replace(old, new, 1)
        assert mutated != text, "mutation did not land"
        copies[key].write_text(mutated, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(
        "_probe_tests_standard_text", ROOT / "loom-code/tests/test_tests_standard_text.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    for key, copy in copies.items():
        setattr(module, key, copy)
    failed = []
    for name in sorted(n for n in dir(module) if n.startswith("test_")):
        try:
            getattr(module, name)()
        except Exception:
            failed.append(name)
    return failed


def test_mutationrulepins_unmutatedfiles_pass(tmp_path: Path) -> None:
    """Control: on unmutated copies every pin test passes, so a kill below is real."""
    assert _failing_tests(tmp_path, []) == []


def test_mutationrulepins_guardedweakening_killed(tmp_path: Path) -> None:
    """Control: a weakening the pins do guard ("must confirm" to "may skip confirming") is killed."""
    assert _failing_tests(
        tmp_path, [("STANDARD", "must\nconfirm, before", "may skip\nconfirming, before")]
    ) != []


def test_mutationrulepins_rulerestatedinadversarial_killed(tmp_path: Path) -> None:
    """The rule restated in adversarial.md, a reader that must only point to it, fails a pin test."""
    assert _failing_tests(
        tmp_path, [("ADVERSARIAL", "## Recording\n", RULE_PARA + "## Recording\n")]
    ) != []


def test_mutationrulepins_rulemovedoutofsection1_killed(tmp_path: Path) -> None:
    """The rule moved from section 1 into section 2, leaving every "§1" pointer stale, fails a pin test."""
    assert _failing_tests(
        tmp_path, [("STANDARD", RULE_PARA, ""), ("STANDARD", SECTION_3, RULE_PARA + SECTION_3)]
    ) != []
