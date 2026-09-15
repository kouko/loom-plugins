"""Tests for the skill cross-reference dead-link validator.

The validator (`check-skill-crossrefs.py`) walks every loom-code
`skills/*/SKILL.md`, extracts each RELATIVE markdown link `](path)`,
resolves it against that SKILL.md's directory, and reports any link
whose target is missing on disk. Relative-only: http(s) URLs,
anchor-only `#...` links, and absolute paths are skipped. A trailing
`#anchor` on an otherwise-relative link is stripped before the check.
Skill subfolder files (`references/*.md`, ...) are scanned too, and
backtick `.md` paths are checked unless they are placeholders or `docs/`
protocol paths.

These tests drive `find_broken_crossrefs(skills_dir) -> list[str]`
directly against HERMETIC temp fixtures (no dependency on the real
tree's current state). Test A = a broken sibling link is reported;
Test B = an existing target passes clean.

Stdlib only (pathlib + tmp_path fixture). The module is loaded by file
path because its filename uses a hyphen (not importable by name).
"""

import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).parent / "check-skill-crossrefs.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_skill_crossrefs", _MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_skill(skills_dir: Path, name: str, body: str) -> Path:
    skill_dir = skills_dir / name
    skill_dir.mkdir(parents=True)
    md = skill_dir / "SKILL.md"
    md.write_text(body, encoding="utf-8")
    return md


# --- Test A: a relative link to a MISSING sibling is reported broken ---------

def test_broken_relative_link_is_reported(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(
        skills,
        "alpha",
        "See [the spec](references/missing-spec.md) for details.\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)

    assert len(broken) == 1, f"expected one broken link, got: {broken!r}"
    entry = broken[0]
    assert "references/missing-spec.md" in entry, \
        "the broken-link report must name the unresolved target"
    assert "alpha" in entry, \
        "the report must name the SKILL.md the broken link came from"


# --- Test B: a relative link to an EXISTING target passes clean -------------

def test_existing_relative_link_passes(tmp_path):
    skills = tmp_path / "skills"
    md = _make_skill(
        skills,
        "beta",
        "See [the protocol](protocols/review.md) for the gate.\n",
    )
    target = md.parent / "protocols" / "review.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Review protocol\n", encoding="utf-8")

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)

    assert broken == [], f"expected no broken links, got: {broken!r}"


# --- Guard: non-relative links (http, anchor-only) are skipped --------------

def test_non_relative_links_are_skipped(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(
        skills,
        "gamma",
        "External [site](https://example.com/page.md), "
        "absolute [root](/etc/passwd), "
        "and anchor [here](#section) — none should be checked.\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)

    assert broken == [], \
        f"http/absolute/anchor links must be skipped, got: {broken!r}"


# --- Guard: a trailing #anchor is stripped before the existence check -------

def test_anchor_suffix_is_stripped_before_existence_check(tmp_path):
    skills = tmp_path / "skills"
    md = _make_skill(
        skills,
        "delta",
        "Jump to [the section](references/guide.md#step-2).\n",
    )
    target = md.parent / "references" / "guide.md"
    target.parent.mkdir(parents=True)
    target.write_text("# Guide\n", encoding="utf-8")

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)

    assert broken == [], \
        f"the #anchor suffix must be stripped before checking, got: {broken!r}"


# --- Guard: agent files are scanned too ------------------------------------

def test_a_dangling_link_in_a_skills_agent_file_is_reported(tmp_path):
    """Agent prose carries the same relative links SKILL.md does, and the
    station rewrite left a dead one in `agents/implementer.md` that only an
    isolated-install test noticed. The dead-link gate reads agent files."""
    skills = tmp_path / "skills"
    _make_skill(skills, "epsilon", "No links here.\n")
    agents = skills / "epsilon" / "agents"
    agents.mkdir(parents=True)
    (agents / "worker.md").write_text(
        "Follow [the catalogue](../references/gone.md).\n", encoding="utf-8"
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)

    assert any("gone.md" in entry for entry in broken), \
        f"a dangling link in an agent file must be reported, got: {broken!r}"


def test_a_resolving_link_in_an_agent_file_is_accepted(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(skills, "zeta", "No links here.\n")
    references = skills / "zeta" / "references"
    references.mkdir(parents=True)
    (references / "here.md").write_text("# here\n", encoding="utf-8")
    agents = skills / "zeta" / "agents"
    agents.mkdir(parents=True)
    (agents / "worker.md").write_text(
        "Follow [the catalogue](../references/here.md).\n", encoding="utf-8"
    )

    checker = _load_checker()
    assert checker.find_broken_crossrefs(skills) == []


def test_the_plugin_level_agents_directory_is_scanned(tmp_path):
    """loom-code's agents live beside `skills/`, not inside it."""
    skills = tmp_path / "skills"
    _make_skill(skills, "eta", "No links here.\n")
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "implementer.md").write_text(
        "Read [the baseline](../references/engineering-baseline.md).\n",
        encoding="utf-8",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)
    assert any("engineering-baseline.md" in entry for entry in broken), \
        f"the plugin-level agents/ tree must be scanned, got: {broken!r}"


# --- References files and backtick paths ------------------------------------

def _write(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def test_missing_link_in_references_is_reported(tmp_path):
    """A dead link inside `references/*.md` used to pass unseen — the
    attack-catalogue links lived in exactly such a file."""
    skills = tmp_path / "skills"
    _make_skill(skills, "theta", "No links here.\n")
    _write(
        skills / "theta" / "references" / "guide.md",
        "See [the catalogue](gone-catalogue.md).\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)

    assert len(broken) == 1, f"expected one broken link, got: {broken!r}"
    assert "gone-catalogue.md" in broken[0]
    assert "guide.md" in broken[0], \
        "the report must name the references file the link came from"


def test_link_in_references_resolves_against_its_own_directory(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(skills, "iota", "No links here.\n")
    _write(skills / "iota" / "references" / "sibling.md", "# sibling\n")
    _write(
        skills / "iota" / "references" / "guide.md",
        "See [the sibling](sibling.md).\n",
    )

    checker = _load_checker()
    assert checker.find_broken_crossrefs(skills) == []


def test_existing_backtick_path_passes(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(skills, "kappa", "Read `references/lenses.md` first.\n")
    _write(skills / "kappa" / "references" / "lenses.md", "# lenses\n")
    _write(
        skills / "kappa" / "references" / "adversarial.md",
        "The lens table is in `references/lenses.md`.\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)
    assert broken == [], f"expected no broken paths, got: {broken!r}"


def test_missing_backtick_path_is_reported(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(skills, "lambda", "No links here.\n")
    _write(
        skills / "lambda" / "references" / "adversarial.md",
        "Run each attack in `references/attack-catalogue.md`.\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)
    assert len(broken) == 1, f"expected one broken path, got: {broken!r}"
    assert "references/attack-catalogue.md" in broken[0]
    assert "adversarial.md" in broken[0]


def test_plugin_root_relative_backtick_path_resolves(tmp_path):
    plugin = tmp_path / "loom-code"
    skills = plugin / "skills"
    _make_skill(skills, "mu", "No links here.\n")
    _write(skills / "nu" / "SKILL.md", "No links here.\n")
    _write(skills / "nu" / "references" / "target.md", "# target\n")
    _write(plugin / "agents" / "reviewer.md", "# reviewer\n")
    _write(
        skills / "mu" / "references" / "notes.md",
        "Repo-rooted `loom-code/skills/nu/references/target.md`, "
        "plugin-rooted `skills/nu/references/target.md`, "
        "plugin-rooted `agents/reviewer.md`, "
        "sibling-skill `../nu/references/target.md`.\n",
    )

    checker = _load_checker()
    assert checker.find_broken_crossrefs(skills) == []

    _write(
        skills / "mu" / "references" / "dead.md",
        "Gone: `loom-code/skills/nu/references/missing.md`.\n",
    )
    broken = checker.find_broken_crossrefs(skills)
    assert len(broken) == 1, f"expected one broken path, got: {broken!r}"
    assert "loom-code/skills/nu/references/missing.md" in broken[0]


def test_placeholder_and_docs_backtick_paths_are_skipped(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(
        skills,
        "xi",
        "Protocol paths `docs/loom/intent/<change-id>.md`, "
        "`docs/loom/KICKOFF-DEFAULTS.md`, `skills/*/SKILL.md`, "
        "`references/{name}.md`, `$ROOT/references/x.md`, "
        "bare `SKILL.md`, and a URL `https://example.com/a/b.md`.\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)
    assert broken == [], \
        f"placeholders and docs/ protocol paths must be skipped, got: {broken!r}"


# --- Plugin-level references and bare backtick names -------------------------

def test_plugin_level_references_dead_link_is_reported(tmp_path):
    """`loom-code/references/*.md` (dispatch-profile.md, ...) is linked by
    stations; a dead link or backtick path inside it must be reported."""
    plugin = tmp_path / "loom-code"
    skills = plugin / "skills"
    _make_skill(skills, "omicron", "No links here.\n")
    _write(
        plugin / "references" / "shared.md",
        "See [gone](missing.md) and `skills/nope/SKILL.md`.\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)
    assert any("shared.md" in e and "missing.md" in e for e in broken), broken
    assert any("skills/nope/SKILL.md" in e for e in broken), broken


def test_plugin_level_references_resolving_paths_pass(tmp_path):
    plugin = tmp_path / "loom-code"
    skills = plugin / "skills"
    _make_skill(skills, "pi", "No links here.\n")
    _write(plugin / "references" / "baseline.md", "# baseline\n")
    _write(
        plugin / "references" / "shared.md",
        "See [sibling](baseline.md), `skills/pi/SKILL.md` and "
        "`loom-code/references/baseline.md`.\n",
    )

    checker = _load_checker()
    assert checker.find_broken_crossrefs(skills) == []


def test_bare_backtick_missing_name_is_reported(tmp_path):
    """A slash-free `.md` name the prose tells the agent to load is checked
    against the scanning file's own directory."""
    skills = tmp_path / "skills"
    _make_skill(skills, "rho", "No links here.\n")
    _write(skills / "rho" / "references" / "one-way-door.md", "# classes\n")
    _write(
        skills / "rho" / "references" / "confirm.md",
        "Load `one-way-dor.md` before deciding.\n",
    )

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)
    assert len(broken) == 1, f"expected one broken name, got: {broken!r}"
    assert "one-way-dor.md" in broken[0]
    assert "confirm.md" in broken[0]


def test_existing_bare_backtick_name_passes(tmp_path):
    skills = tmp_path / "skills"
    _make_skill(skills, "sigma", "No links here.\n")
    _write(skills / "sigma" / "references" / "one-way-door.md", "# classes\n")
    _write(
        skills / "sigma" / "references" / "confirm.md",
        "Per `one-way-door.md` — load that file before deciding.\n",
    )

    checker = _load_checker()
    assert checker.find_broken_crossrefs(skills) == []


def test_root_protocol_bare_names_are_skipped(tmp_path):
    skills = tmp_path / "skills"
    names = ("DESIGN.md", "PRINCIPLES.md", "README.md", "CHANGELOG.md",
             "AGENTS.md", "CLAUDE.md", "SKILL.md", "KICKOFF-DEFAULTS.md",
             "<change-id>.md")
    body = " ".join(f"Read `{n}` first." for n in names) + "\n"
    _make_skill(skills, "tau", body)
    _write(skills / "tau" / "references" / "notes.md", body)

    checker = _load_checker()
    broken = checker.find_broken_crossrefs(skills)
    assert broken == [], f"root protocol names must be skipped, got: {broken!r}"


def test_bare_name_docstring_names_its_upgrade_path():
    """A4 positive (bare-name-docstring-names-upgrade-path): the docstring
    states the read/load-sentence ceiling AND how to lift it."""
    doc = _load_checker()._loaded_bare_names.__doc__
    assert "_LOAD_VERB_RE" in doc, doc
    assert "docs/" in doc, doc


def test_bare_name_outside_a_read_or_load_sentence_is_skipped(tmp_path):
    """Names of user-repo artifacts (`plan.md`) or tool trivia (`report.md`)
    are mentioned, not loaded; a link text naming a resolving link is the
    link's business."""
    plugin = tmp_path / "loom-code"
    skills = plugin / "skills"
    _make_skill(
        skills,
        "upsilon",
        "The plan itself — `plan.md` — is written in English. "
        "It works from the recipes in [`adv.md`](references/adv.md).\n",
    )
    _write(skills / "upsilon" / "references" / "adv.md", "# adv\n")
    _write(plugin / "agents" / "worker.md",
           "The Write tool refuses the filename `report.md`.\n")

    checker = _load_checker()
    assert checker.find_broken_crossrefs(skills) == []
