# concern: a deleted memory entry's lesson (a CI check that runs outside the package suite fails while the local suite is green) still applies but no surviving entry carries it
"""Adversary probe for Acceptance 3 of 2026-11-20-stale-doc-references.

The branch deleted verified-gate-pytest-suite-misses-skill-structure-word-cap
and leading-at-req-comment-trips-living-spec-checker as lessons that "only
concerned the removed tool". Their shared lesson is general: CI runs check
scripts as steps outside `run_package_tests.py`, so a green local package
suite can still fail CI. The lesson still applies while CI runs any such
script. This probe derives those scripts from .github/workflows and requires
a living memory entry that mentions the package suite and names at least one
of them.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]

RUN_PY = re.compile(r"python3\s+\"?(?:\$GITHUB_WORKSPACE/\w+/)?([\w./-]+\.py)")


def _ci_only_scripts(workflow_texts):
    names = set()
    for text in workflow_texts:
        for path in RUN_PY.findall(text):
            name = pathlib.PurePosixPath(path).name
            if name not in {"run_package_tests.py", "sync_codex_manifests.py"}:
                names.add(name)
    return names


def _carriers(entries, scripts):
    return [
        rel for rel, text in entries
        if "package suite" in text and any(s in text for s in scripts)
    ]


def test_memory_ci_only_check_lesson_cited():
    """A living memory entry carries the CI-only-check lesson while CI runs such checks."""
    workflows = [p.read_text(encoding="utf-8") for p in (ROOT / ".github/workflows").glob("*.yml")]
    scripts = _ci_only_scripts(workflows)
    assert scripts, "precondition: CI runs no check script outside the package suite"
    entries = [
        (p.name, p.read_text(encoding="utf-8"))
        for p in (ROOT / "docs/loom/memory").glob("*.md")
        if p.name not in {"index.md", "README.md"}
    ]
    assert _carriers(entries, scripts), (
        "no memory entry carries the deleted lesson; CI-only checks: " + ", ".join(sorted(scripts))
    )


def test_carriers_need_suite_and_script():
    """Synthetic: an entry counts only when it names both the package suite and a CI-only script."""
    scripts = _ci_only_scripts(["run: python3 loom-code/scripts/check_doc_citations.py"])
    assert scripts == {"check_doc_citations.py"}
    good = ("a.md", "The package suite is green but check_doc_citations.py fails in CI.")
    bad = ("b.md", "The package suite is green.")
    assert _carriers([good, bad], scripts) == ["a.md"]
