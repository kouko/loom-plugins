# concern: unavailable Codex Goal tool must not be treated as native activation.
"""
Structural tests for SKILL.md, the skill's entry point (Task 5).

Tests:
  1. test_declares_two_modes_and_conditional_arc — both mode names
     (SESSION, ARC) appear as headings.
  2. test_reference_pointers_resolve — cross-seam probe: every relative
     `references/*` and `scripts/*` path written in SKILL.md (Task 2's
     seam) resolves on disk relative to the skill directory.
  3. test_floor_invocation_line_names_the_script — cross-seam probe:
     the invocation line SKILL.md gives for the mechanical floor names
     Task 3's script path, and that path exists.
  4. test_session_activation_rules_are_one_registered_gate — the gate
     block exists in SKILL.md and references/input-floor.md.
  5. test_arc_points_at_the_purpose_template_without_restating_it — ARC
     reproduces none of the purpose template's own field text verbatim;
     that template is the format SSOT.
  6. test_invocation_section_counts_the_offer_sites_that_exist.

The rules' wording is review-only.

The reference-path check (`test_reference_pointers_resolve`) finds
every `references/*` and `scripts/*` path in SKILL.md regardless of
form — backticked, inside a markdown link (with or without a title),
or bare in prose — and strips a trailing `#anchor` fragment before
resolving.
"""

import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / "skills" / "goal-create"
SKILL_PATH = SKILL_DIR / "SKILL.md"
GOAL_LINT_PATH = SKILL_DIR / "scripts" / "goal_lint.py"
# loom 1.0 moved the templates into loom-code's contract package.
PURPOSE_TEMPLATE_PATH = (
    SKILL_DIR.parent.parent.parent / "loom-code" / "contract" / "templates" / "PURPOSE.md"
)


def _read_skill_md() -> str:
    assert SKILL_PATH.exists(), f"SKILL.md does not exist at {SKILL_PATH}"
    return SKILL_PATH.read_text(encoding="utf-8")


def _normalize_ws(s: str) -> str:
    """Collapse runs of whitespace to a single space. Used to compare a
    pinned sentence against SKILL.md prose so a pure re-wrap (line
    breaks moved, words unchanged) still matches, while a genuine
    reword (words added/removed/changed) still fails."""
    return re.sub(r"\s+", " ", s).strip()


def _frontmatter(text: str) -> str:
    """Return the YAML frontmatter body (between the two `---` fences).
    Structural scoping — never a character-distance slice."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, "No YAML frontmatter found in SKILL.md"
    return match.group(1)


def _section(text: str, heading: str) -> str:
    """Return the body of one `## <heading>` section: from just after the
    heading line to the next `##` heading or end of text. Structural
    scoping — never a character-distance slice."""
    pattern = re.compile(
        r"^##\s+" + re.escape(heading) + r"\s*$\n(.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    assert match, f"No '## {heading}' section found in SKILL.md"
    return match.group(1)


def _gate(text: str, gate_id: str) -> str:
    pattern = re.compile(
        r"<!--\s*gate:\s*" + re.escape(gate_id) + r"\s*-->(.*?)"
        r"<!--\s*/gate\s*-->",
        re.DOTALL,
    )
    match = pattern.search(text)
    assert match, f"No gate block found for {gate_id!r}"
    return _normalize_ws(match.group(1))


def test_declares_two_modes_and_conditional_arc():
    text = _read_skill_md()

    # --- Both mode names appear as their own sections. ---
    _section(text, "SESSION mode")
    _section(text, "ARC mode")


def test_reference_pointers_resolve():
    text = _read_skill_md()

    # Extraction covers every form the docstring claims: backticked,
    # inside a markdown link (titled or not), and bare in prose. The
    # path-character class stops at whitespace, backtick, `)`, or `"` —
    # the delimiters each of those forms actually uses — so it doesn't
    # reach past the path into surrounding punctuation.
    raw_matches = re.findall(r"(?:references|scripts)/[^`\s)\"]+", text)
    assert raw_matches, "No relative reference/script paths found in SKILL.md"

    paths = []
    for raw in raw_matches:
        # Strip a trailing sentence period (paths here never bare-end
        # in '.') and an #anchor fragment before resolving.
        candidate = raw[:-1] if raw.endswith(".") else raw
        candidate = candidate.split("#", 1)[0]
        paths.append(candidate)

    for rel_path in paths:
        resolved = SKILL_DIR / rel_path
        assert resolved.exists(), f"Reference path does not resolve: {rel_path}"

    # The two reference files this task points at must both be named.
    assert "references/goal-shape.md" in paths
    assert "references/input-floor.md" in paths


def test_floor_invocation_line_names_the_script():
    text = _read_skill_md()

    assert GOAL_LINT_PATH.exists(), f"Floor script missing: {GOAL_LINT_PATH}"

    # Structural: find the fenced code block that names goal_lint.py —
    # that is the invocation line, not prose mentioning the script.
    invocation_blocks = re.findall(r"```\n(.*?)\n```", text, re.DOTALL)
    matching = [block for block in invocation_blocks if "scripts/goal_lint.py" in block]
    assert matching, "No fenced invocation line names scripts/goal_lint.py"

    invocation_line = matching[0]
    assert "python3 <skill-dir>/scripts/goal_lint.py" in invocation_line


def test_session_activation_rules_are_one_registered_gate():
    """Gate-block presence only; the block's wording is review-only."""
    _gate(_read_skill_md(), "goal-create.session-activation")
    _gate(
        (SKILL_DIR / "references" / "input-floor.md").read_text(),
        "goal-create.session-activation",
    )


def test_arc_points_at_the_purpose_template_without_restating_it():
    text = _read_skill_md()
    arc_body = _section(text, "ARC mode")

    # --- Never restated: the template's own field-label text must not
    # appear verbatim in this skill's ARC section. ---
    assert PURPOSE_TEMPLATE_PATH.exists(), (
        f"Purpose template missing at {PURPOSE_TEMPLATE_PATH} — "
        "cannot verify non-restatement against it"
    )
    template_text = PURPOSE_TEMPLATE_PATH.read_text(encoding="utf-8")

    # Extract the template's field-label lines (the SSOT prose this
    # skill must point at, never copy) and confirm none of them shows
    # up verbatim in ARC's own section.
    field_lines = [
        line.strip()
        for line in template_text.splitlines()
        if line.strip().startswith("**Why:**") or line.strip().startswith("**Done when:**")
    ]
    assert field_lines, "Could not locate the template's field-label lines"

    for field_line in field_lines:
        assert field_line not in arc_body, (
            f"ARC section restates the purpose template's field text verbatim: {field_line!r}"
        )


# The token the Invocation section must contain for each surface that
# offers this skill. The surfaces themselves are read out of the repo,
# never from this map; an entry here only says how the section is
# expected to refer to one. A scanned path missing from this map fails
# loudly, because a new offer site the section has never heard of is the
# exact drift this test exists for.
# loom 1.0 deleted the purpose-link check and the finishing station, so
# handoff is the only surviving offer site.
_OFFER_SITE_MARKERS = {
    "loom-workflow/skills/handoff/SKILL.md": "loom-workflow:handoff",
}
_COUNT_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def _scan_offer_sites() -> set[str]:
    """Every runtime surface outside this skill that names it to a user.

    Every plugin in the repo is scanned, not the two that happen to offer
    it today — the Invocation section's claim is about the repo, so
    narrowing the scan to the known answer would make it unfalsifiable.
    Tests are excluded: a test asserting an offer exists is not itself an
    offer. So are READMEs and changelogs, which describe rather than run.
    """
    root = SKILL_DIR.parent.parent.parent
    plugins = sorted(p.parent for p in root.glob("*/.claude-plugin"))
    assert plugins, "no plugin directories found; the scan would pass vacuously"
    found = set()
    for plugin in plugins:
        for path in plugin.rglob("*"):
            if path.suffix not in {".md", ".py"} or not path.is_file():
                continue
            if SKILL_DIR in path.parents or path == SKILL_DIR:
                continue
            if path.name.startswith(("README", "CHANGELOG", "test_")):
                continue
            if "loom-workflow:goal-create" in path.read_text(encoding="utf-8"):
                found.add(path.relative_to(root).as_posix())
    return found


def test_invocation_section_counts_the_offer_sites_that_exist():
    """The stated number of offer points must be the number that exist.

    `test_invocation_contract_is_offer_not_trigger` pins that sentence
    verbatim, which guards its wording and nothing about its arithmetic.
    The count went stale the moment a third surface started naming this
    skill, and a verbatim pin cannot notice that — it is satisfied by the
    stale sentence surviving unedited. This reads the sites out of the
    repo instead, so adding one forces the sentence to be re-counted.
    """
    sites = _scan_offer_sites()
    unknown = sites - set(_OFFER_SITE_MARKERS)
    assert not unknown, (
        f"{sorted(unknown)} names this skill but the Invocation section has "
        "never been told about it; name it there and add its marker to "
        "_OFFER_SITE_MARKERS"
    )

    invocation_body = _section(_read_skill_md(), "Invocation")
    # "one point", "two points" — the sentence has to read as English.
    expected = (
        f"exactly {_COUNT_WORDS[len(sites)]} point"
        + ("" if len(sites) == 1 else "s")
    )
    assert expected in invocation_body, (
        f"{len(sites)} surfaces offer this skill "
        f"({sorted(sites)}), but the Invocation section does not say "
        f"{expected!r}"
    )
    for site in sorted(sites):
        assert _OFFER_SITE_MARKERS[site] in invocation_body, (
            f"{site} offers this skill but the Invocation section never "
            f"names it (looked for {_OFFER_SITE_MARKERS[site]!r})"
        )
