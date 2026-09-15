"""Boundary probes: the Build suite-command source when the declaration is absent or `none`.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-station-gaps-after-dogfood/evidence/probes/test_probe_suite_command_source.py -q

Build now names the `package-tests:` line in `docs/loom/KICKOFF-DEFAULTS.md` as
the suite command. loom-code ships to adopting repos. The checker's
`declared_test_command` falls back to build markers when the line is absent,
and the manifest grammar allows `none`. These probes ask whether Build's text
covers both states. Probes that expose a gap FAIL on purpose (DEFECT_PROBES);
the rest record attempts the change survived.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = REPO_ROOT / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.helpers import kickoff_defaults  # noqa: E402
from loom_checker.probes import NO_PACKAGE_TESTS, declared_test_command  # noqa: E402
from prose_pin import has_negation, split_sentences  # noqa: E402

BUILD = (REPO_ROOT / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
VERIFY = " ".join(BUILD.split("## 3. Verify integration", 1)[1].split("## 4.", 1)[0].split())
STEP_2 = VERIFY.split("3. Run the repository's complete package suite", 1)[1].split("When a check fails", 1)[0]

DEFECT_PROBES = (
    "test_buildsuite_absentdeclaration_namesfallback",
    "test_buildsuite_nonedeclaration_statesmeaning",
)

_AFFIRM = re.compile(r"\b(?:run|use|runs|is|falls back|detect|detects)\b", re.IGNORECASE)


def _affirmative_sentence_with(text: str, keywords: tuple[str, ...]) -> str | None:
    """First sentence that carries a keyword after an affirmative verb and has no negation."""
    for sentence in split_sentences(text):
        for keyword in keywords:
            at = sentence.find(keyword)
            if at < 0:
                continue
            if _AFFIRM.search(sentence[:at]) and not has_negation(sentence):
                return sentence
    return None


def test_affirmhelper_affirmativeexample_accepted() -> None:
    """Synthetic self-test: an affirmative fallback sentence is found."""
    text = "When that line is absent, run the command detected from the build markers."
    assert _affirmative_sentence_with(text, ("build markers",)) is not None


def test_affirmhelper_negatedexample_rejected() -> None:
    """Synthetic self-test: a negated fallback sentence is rejected."""
    text = "When that line is absent, do not run the command detected from the build markers."
    assert _affirmative_sentence_with(text, ("build markers",)) is None


def test_checkerfallback_absentdeclaration_detectsmarker(tmp_path: Path) -> None:
    """The checker itself survives an absent declaration: it detects pyproject.toml."""
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    command, source = declared_test_command(tmp_path)
    assert command == "python3 -m pytest -q"
    assert source == "detected pyproject.toml"


def test_checkerparse_reasonsuffix_stripped() -> None:
    """The real `package-tests:` line yields only the command, not its reason or date."""
    value = kickoff_defaults(REPO_ROOT)["package-tests"]
    assert value.startswith("uv run ")
    assert "—" not in value and "(2026" not in value
    assert declared_test_command(REPO_ROOT) == (value, "docs/loom/KICKOFF-DEFAULTS.md")


def test_buildsuite_absentdeclaration_namesfallback() -> None:
    """Build step 3 states what the suite command is when the `package-tests:` line is absent."""
    found = _affirmative_sentence_with(
        STEP_2, ("absent", "build markers", "detected", "otherwise", "missing")
    )
    assert found is not None, (
        "Build names only the KICKOFF-DEFAULTS line; in a repo without it the agent "
        "guesses again while finalize-review detects a marker command: " + STEP_2
    )


def test_buildsuite_nonedeclaration_statesmeaning(tmp_path: Path) -> None:
    """Build states what a grammar-legal `package-tests: none` means for the end-of-Build suite."""
    kickoff = tmp_path / "docs/loom/KICKOFF-DEFAULTS.md"
    kickoff.parent.mkdir(parents=True)
    kickoff.write_text("- package-tests: none — no suite yet (2026-09-15)\n", encoding="utf-8")
    command, _ = declared_test_command(tmp_path)
    assert command == NO_PACKAGE_TESTS
    found = _affirmative_sentence_with(VERIFY, ("`none`",))
    assert found is not None, (
        "a `none` declaration makes Build's named suite command `none`; finalize-review "
        "refuses it unless package-tests is skipped, and Build never says so"
    )
