"""The 2.0 runtime has no legacy publication ledgers or replay gates."""

from pathlib import Path
import re
import subprocess

import yaml


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "loom-code/scripts/loom_checker.py"
MANIFEST = ROOT / "loom-code/contract/manifest.yaml"

# The acceptance-test step's retired name, in its id, agent and prose forms:
# any run of `-`, `_`, whitespace (a line break and a non-breaking space
# included) or a Unicode dash between the two words, none for the camel form,
# and the Chinese term.
RETIRED_STEP_NAME = re.compile(
    r"blind[-_\s‐-―]*run(?:ner)?|" + "盲" + "跑", re.IGNORECASE
)
RUNTIME_TREES = (
    "loom-code/", "loom-design/", "loom-workflow/",
    "scripts/", ".claude/", ".claude-plugin/", ".github/",
)
RUNTIME_FILES = (
    "README.md", "AGENTS.md", "PRINCIPLES.md", "docs/loom/README.md",
    "docs/loom/evidence/mechanisms.yaml",
)
# The two places the retired name is still meant to be read: the phrase that
# maps a user's old words onto the renamed step, and PRINCIPLES.md's
# ratification history. CHANGELOG.md files are release history and are skipped.
FORMER_NAME_PHRASE = 'formerly called "' + "blind" + ' run"'
RATIFIED_BY_PREFIX = "ratified-by:"


def retired_step_names(path: str, text: str) -> list[str]:
    """Each `path:line` that names the step by its retired name.

    The exempt spans are blanked line by line, then the whole text is searched,
    so a name split by a hard wrap is reported on the line where it starts.
    """
    masked = [
        "" if path == "PRINCIPLES.md" and line.startswith(RATIFIED_BY_PREFIX)
        else line.replace(FORMER_NAME_PHRASE, "")
        for line in text.splitlines()
    ]
    joined = "\n".join(masked)
    hits = []
    for match in RETIRED_STEP_NAME.finditer(joined):
        hit = f"{path}:{joined.count(chr(10), 0, match.start()) + 1}"
        if hit not in hits:
            hits.append(hit)
    return hits


def test_retired_step_name_helper_synthetic() -> None:
    old = "blind" + "-run"
    assert retired_step_names("x.md", f"skip {old}\nok") == ["x.md:1"]
    assert retired_step_names("x.md", "Blind" + " Runner here") == ["x.md:1"]
    assert retired_step_names("x.md", f"the step {FORMER_NAME_PHRASE}") == []
    assert retired_step_names("x.md", f"{FORMER_NAME_PHRASE} and {old}") == ["x.md:1"]
    ratified = f"{RATIFIED_BY_PREFIX} kouko; {old}"
    assert retired_step_names("PRINCIPLES.md", ratified) == []
    assert retired_step_names("README.md", ratified) == ["README.md:1"]


def test_retired_step_name_helper_near_miss_spellings() -> None:
    word = "blind"
    for text in (
        f"{word}_run_report: x",          # identifier / YAML key
        f"a {word}–run",             # en dash
        f"a {word} run",             # non-breaking space
        f"a {word}\t run",                # several whitespace characters
        f"{word.capitalize()}Runner()",   # camel form, no separator
        f"{word.upper()}_RUNNER",
        "③" + "盲" + "跑報告",             # the Chinese term
    ):
        assert retired_step_names("x.md", text) == ["x.md:1"], text
    wrapped = f"intro\nwhen a {word}\nrun is needed"
    assert retired_step_names("x.md", wrapped) == ["x.md:2"]
    # Exemptions stay exact, and a split string literal is not a spelling.
    assert retired_step_names("x.md", '"' + word + '" + "-run"') == []
    assert retired_step_names("x.md", f"{word} judging, {word} test") == []
    ratified = f"{RATIFIED_BY_PREFIX} kouko; {word}_run"
    assert retired_step_names("PRINCIPLES.md", ratified) == []
    assert retired_step_names("x.md", f"{FORMER_NAME_PHRASE}\n{word}_run") == ["x.md:2"]


def test_retired_name_scan_covers_the_root_tooling_trees() -> None:
    for tree in ("scripts/", ".claude/", ".claude-plugin/", ".github/"):
        assert tree in RUNTIME_TREES, tree


def test_no_runtime_file_names_the_retired_step_name() -> None:
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")
    paths = [
        p for p in listed
        if (p in RUNTIME_FILES or p.startswith(RUNTIME_TREES))
        and Path(p).name != "CHANGELOG.md" and (ROOT / p).is_file()
    ]
    hits = []
    for path in paths:
        try:
            text = (ROOT / path).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        hits.extend(retired_step_names(path, text))
    assert hits == []


def test_manifest_declares_no_review_ledger() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert "review" not in manifest["artifacts"]
    assert not (ROOT / "loom-code/contract/templates/review.json").exists()


def test_public_rule_inventory_has_only_current_publication_contracts() -> None:
    result = subprocess.run(
        ["python3", str(CHECKER), "--list-rules"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    push_rules = {
        line.split("\t", 1)[0]
        for line in result.stdout.splitlines()
        if line.startswith("push.")
    }
    assert push_rules == {"push.contextual-body"}


def test_removed_package_replay_flag_is_rejected() -> None:
    result = subprocess.run(
        ["python3", str(CHECKER), "push", "--skip-package-tests"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2
    assert "push runs only as a hook" in result.stderr


def test_live_consumers_require_contract_two() -> None:
    consumers = [
        ROOT / "loom-code/skills/write-plan/SKILL.md",
        *(ROOT / "loom-design/skills").glob("*/SKILL.md"),
        ROOT / "loom-workflow/skills/decision-map/SKILL.md",
    ]
    for path in consumers:
        text = path.read_text(encoding="utf-8")
        if "contract --require" in text:
            expected = "2.0" if "loom-workflow" in str(path) else "2.1"
            assert f"contract --require {expected}" in text, path
            assert "contract --require 1.0" not in text, path


def test_implementer_runs_focused_tests_not_the_package_suite() -> None:
    text = (ROOT / "loom-code/agents/implementer.md").read_text(encoding="utf-8")
    assert (
        "The complete package suite runs at the end of Build and again in "
        "`finalize-review`, never per task."
    ) in " ".join(text.split())
    assert "Closing Review owns the single package-level run" not in text
    assert "plus the package test command passing" not in text
    assert "the package suite ran green" not in text
