"""Shape of the acceptance test report template (plan W0-01).

concern: prose-contract drift -- the acceptance tester's contract and report template letting a full-suite run, evidence in rows, or a mismatched verdict back in

The report the user reads at decision point 3 is one table row per
Acceptance criterion -- verdict plus one plain sentence -- while the
evidence behind each row lives in a separate plain-markdown file under
the change's evidence directory. A re-run marks each verdict it did not
re-test as carried over, with a one-line reason; a re-tested row carries
no such reason. These tests pin that structure in the committed
template, not whole paragraphs.

Plan W1-01 adds the tester's side: it leaves the package suite to
finalize-review, re-tests a criterion in full over every surface its
Acceptance line names, and these rules live in the tester's contract and
the template, under no new gate marker.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prose_pin import flat_prose, has_negation, split_sentences  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = (
    REPO_ROOT / "loom-code" / "skills" / "closing-review" / "references"
    / "acceptance-test-report.md"
)
EVIDENCE_PATH = "docs/loom/<change-id>/evidence/acceptance-test-evidence.md"
ROWS_HEADING = "## What you asked for, one line at a time"
CARRIED = re.compile(r"^carried over — \S.*$")


def _fenced_blocks(text: str) -> list[str]:
    return re.findall(r"^```markdown\n(.*?)^```$", text, flags=re.M | re.S)


def _report_block() -> str:
    blocks = _fenced_blocks(TEMPLATE.read_text(encoding="utf-8"))
    assert blocks, "template has no ```markdown report block"
    return blocks[0]


def _criterion_table() -> tuple[list[str], list[list[str]]]:
    report = _report_block()
    assert ROWS_HEADING in report, "report block lost its criteria heading"
    section = report.split(ROWS_HEADING, 1)[1].split("\n## ", 1)[0]
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    assert len(lines) >= 3, "criteria section is not a table with rows"
    cells = [[c.strip() for c in ln.strip("|").split("|")] for ln in lines]
    header, rows = cells[0], cells[2:]
    assert set("".join(cells[1])) <= set("-: "), "second table line is not a separator"
    return header, rows


def _column(header: list[str], name: str) -> int:
    matches = [i for i, h in enumerate(header) if h.lower() == name.lower()]
    assert matches, f"criteria table has no {name!r} column: {header}"
    return matches[0]


def test_template_has_one_row_per_criterion_and_evidence_file_path():
    header, rows = _criterion_table()
    number = _column(header, "#")
    verdict = _column(header, "Verdict")
    assert all(len(r) == len(header) for r in rows), "ragged criteria rows"
    assert [r[number] for r in rows][:2] == ["1", "2"], "rows are not one per criterion"
    for row in rows:
        assert re.search(r"works|partly|not verified|fails", row[verdict]), row
    report = _report_block()
    assert "works / partly / not verified / fails" in TEMPLATE.read_text(encoding="utf-8")
    assert not re.search(r"^### \d+\.", report, flags=re.M), "per-criterion blocks remain"
    assert EVIDENCE_PATH in report, "report does not point to the evidence file"


def test_evidence_file_shape_is_given_and_is_plain_markdown():
    text = TEMPLATE.read_text(encoding="utf-8")
    blocks = _fenced_blocks(text)
    evidence = [b for b in blocks if "acceptance test evidence" in b.splitlines()[0].lower()]
    assert evidence, "template gives no shape for the evidence file"
    assert not evidence[0].startswith("#!")
    assert re.search(r"never[^\n]*`#!`", text), "template does not forbid `#!` evidence"


COLUMNS = ["#", "What you asked for", "Verdict", "What happened", "Re-run"]
# A row cell that reads as evidence: a code span or a command, command
# output, or a source location. Placeholders such as "<one plain sentence>"
# match none of these.
EVIDENCE_IN_CELL = re.compile(
    r"`|evidence|command|file:line"
    r"|\b(?:python3?|pytest|npm|pnpm|uv|git|bash)\b"
    r"|\b\d+ (?:passed|failed|errors?)\b|\bexit(?:ed)? (?:code|status)\b"
    r"|\btraceback\b|\bstdout\b|\bstderr\b"
    r"|[\w./-]+\.\w+:\d+",
    re.I,
)


def test_template_row_carries_no_how_or_evidence_cell():
    header, rows = _criterion_table()
    banned = re.compile(r"how|evidence|command|tried|output|proof", re.I)
    assert not [h for h in header if banned.search(h)], header
    assert header == COLUMNS, f"criteria table columns are {header}, not {COLUMNS}"
    for row in rows:
        assert not [c for c in row if EVIDENCE_IN_CELL.search(c)], row
    report = _report_block()
    assert "**How I tried it**" not in report
    assert "**Evidence**" not in report


def test_row_has_carried_over_marker_with_reason():
    header, rows = _criterion_table()
    rerun = _column(header, "Re-run")
    carried = [r[rerun] for r in rows if r[rerun].startswith("carried over")]
    assert carried, "no row shows the carried-over marker"
    assert all(CARRIED.match(c) for c in carried), carried
    assert all(c.split("—", 1)[1].strip() for c in carried), "carried row has an empty reason"


def test_retested_row_has_no_carry_reason():
    header, rows = _criterion_table()
    rerun = _column(header, "Re-run")
    retested = [r[rerun] for r in rows if r[rerun].startswith("re-tested")]
    assert retested, "no row shows a re-tested verdict"
    assert all(c == "re-tested" for c in retested), retested


# --- plan W1-01: the tester's contract and the station's §3 ------------------

TESTER = REPO_ROOT / "loom-code" / "agents" / "acceptance-tester.md"
STATION = REPO_ROOT / "loom-code" / "skills" / "closing-review" / "SKILL.md"
STATION_GATES = {
    "review.absence-recovery",
    "review.atomic-claude-dispatch",
    "review.probe-graduation",
    "review.bounded-episode",
}


def _tester() -> list[str]:
    return split_sentences(flat_prose(TESTER))


def _section3() -> str:
    text = STATION.read_text(encoding="utf-8")
    return text.split("## 3. Run acceptance testing", 1)[1].split("\n## 4.", 1)[0]


def _affirmed(sentences: list[str], *phrases: str) -> list[str]:
    return [
        s for s in sentences
        if all(p in s for p in phrases) and not has_negation(re.sub(r"`[^`]*`", "", s))
    ]


def test_suite_criterion_cites_finalize_review_command():
    """A1 positive: a suite-settled row cites the check, not a result."""
    sentences = _tester()
    assert _affirmed(
        sentences, "names the suite check", "`finalize-review` executes it",
        "refuses the attestation",
    ), "tester does not cite finalize-review's suite check"
    assert _affirmed(sentences, "committed before `finalize-review` runs")
    assert _affirmed(sentences, "`package-tests` is skipped", "only that criterion's own tests")
    assert _affirmed(sentences, "setup check", "every run")
    section = " ".join(_section3().split())
    assert "names the suite check" in section
    assert "`finalize-review` executes" in section


RUN_VERB = re.compile(r"\b(?:run|runs|running|execute|executes|executing|invoke|invokes)\b", re.I)
WHOLE_TARGET = re.compile(
    r"\b(?:package|whole|full|complete|entire)\s+(?:package\s+)?(?:suite|package)\b", re.I
)
NEGATED_VERB = re.compile(r"\b(?:not|never|no|cannot)\b|n't", re.I)
OTHER_RUNNER = re.compile(r"finalize-review|\bBuild\b|\bchecker\b")


def _full_suite_instructions(sentences: list[str]) -> list[str]:
    """Sentences with a clause that runs the whole package's tests, not negated.

    Only the words just before the run verb decide: "Never run the full
    package suite" is exempt, while "Run the full package suite first,
    unless it is not installed" is not -- its negation sits in another
    clause. A clause whose runner is `finalize-review`, Build or the
    checker is a statement about them, not an instruction to the tester.
    """
    offending = []
    for sentence in sentences:
        for clause in re.split(r"[,:;—]", sentence):
            verb = RUN_VERB.search(clause)
            if not verb or not WHOLE_TARGET.search(clause, verb.end()):
                continue
            before = " ".join(clause[: verb.start()].split()[-3:])
            if NEGATED_VERB.search(before) or OTHER_RUNNER.search(before):
                continue
            offending.append(sentence)
            break
    return offending


def test_no_full_suite_run_instruction():
    """A1 negative: nothing tells the tester to run the whole suite."""
    flat = flat_prose(TESTER)
    assert "the name of a test you ran" not in flat, "evidence wording still invites named tests"
    offending = _full_suite_instructions(_tester())
    assert offending == [], offending
    assert [s for s in _tester() if "full package suite" in s and has_negation(s)], (
        "tester contract does not forbid running the full package suite"
    )


def test_rerun_retests_every_named_surface():
    """A3 positive: a re-tested criterion is re-tested over every surface."""
    sentences = _tester()
    assert _affirmed(sentences, "re-test only the criteria the fix could affect", "in full")
    assert _affirmed(sentences, "every surface its Acceptance line names")
    assert _affirmed(sentences, "`carried over — <one-line reason>`", "Re-run column")
    assert _affirmed(sentences, "against the fix diff")
    assert _affirmed(sentences, "any doubt", "in full")


def test_partial_surface_retest_forbidden():
    """A3 negative: re-testing only the part a fix touched is never allowed."""
    touched = [s for s in _tester() if "the part the fix touched" in s]
    assert touched, "tester contract does not name the partial re-test trap"
    assert all(has_negation(s) for s in touched), touched
    section = [s for s in split_sentences(" ".join(_section3().split())) if "the part the fix touched" in s]
    assert section, "§3 does not name the partial re-test trap"
    assert all(has_negation(s) for s in section), section


def test_rerun_dispatch_passes_earlier_report_evidence_and_fix_range():
    """A re-run gets what step 7 needs to check each carried-over reason."""
    phrases = ("earlier report", "evidence file", "commit range")
    assert _affirmed(_tester(), *phrases), "tester contract does not list the re-run inputs"
    assert _affirmed(split_sentences(" ".join(_section3().split())), "re-dispatch", *phrases), (
        "§3 does not pass the re-run inputs"
    )


def test_identifiers_confined_to_evidence_file_apart_from_pointer():
    """The report's one path is the line pointing to the evidence file."""
    assert _affirmed(
        _tester(), "Identifiers appear only in the evidence file", "the one line that points to it"
    )


def test_rules_live_in_contract_and_template():
    """A4 positive: the tester's contract, the template and §3 carry the rules."""
    flat = flat_prose(TESTER)
    assert "loom-code/skills/closing-review/references/acceptance-test-report.md" in flat
    assert EVIDENCE_PATH in flat
    header, _ = _criterion_table()
    _column(header, "Re-run")
    section = " ".join(_section3().split())
    assert EVIDENCE_PATH in section
    assert _affirmed(split_sentences(section), "committed with the report")


def test_no_new_gate_marker():
    """A4 negative: no gate marker carries these rules."""
    for path in (TESTER, TEMPLATE):
        assert "<!-- gate:" not in path.read_text(encoding="utf-8"), path.name
    text = STATION.read_text(encoding="utf-8")
    assert set(re.findall(r"<!-- gate: ([\w.-]+) -->", text)) == STATION_GATES
    ungated = re.sub(r"<!-- gate: [\w.-]+ -->.*?<!-- /gate -->", "", text, flags=re.S)
    flat = " ".join(ungated.split())
    for phrase in ("names the suite check", "the part the fix touched", EVIDENCE_PATH):
        assert phrase in flat, f"{phrase!r} sits inside a gate block"


# --- graduated adversarial probes ---------------------------------------------
# The build adversary's probes for this change went red on the contract and
# template as first committed. Each attack is carried here: the shape checks
# above must go red on the probes' synthetic bad inputs, and the vocabulary and
# suite-settled checks must hold on the real files.

_THIS = sys.modules[__name__]
SUITE_ANCHOR = "remembered result is not evidence."
ROW1 = "| 1 | <the intent's first Acceptance line, verbatim> | works | <one plain sentence> | re-tested |"
HEADER = "| # | What you asked for | Verdict | What happened | Re-run |\n|---|---|---|---|---|"


def _fails(check) -> bool:
    try:
        check()
    except AssertionError:
        return True
    return False


def _mutated_tester(tmp_path: Path, extra: str) -> Path:
    text = TESTER.read_text(encoding="utf-8")
    assert SUITE_ANCHOR in text, "anchor sentence is gone from the tester contract"
    path = tmp_path / "acceptance-tester.md"
    path.write_text(text.replace(SUITE_ANCHOR, SUITE_ANCHOR + " " + extra, 1), encoding="utf-8")
    return path


def test_suitecheck_pytestoverwholepackage_turnsred(tmp_path, monkeypatch):
    """A sentence telling the tester to run pytest over the whole package turns the check red."""
    path = _mutated_tester(
        tmp_path,
        "Then run `python3 -m pytest loom-code -q` over the whole package and record its output.",
    )
    monkeypatch.setattr(_THIS, "TESTER", path)
    assert _fails(test_no_full_suite_run_instruction)


def test_suitecheck_negationelsewhereinsentence_turnsred(tmp_path, monkeypatch):
    """A negation in another clause does not exempt a full-suite run instruction."""
    path = _mutated_tester(tmp_path, "Run the full package suite first, unless it is not installed.")
    monkeypatch.setattr(_THIS, "TESTER", path)
    assert _fails(test_no_full_suite_run_instruction)


def test_suitecheck_negatedinstruction_exempt():
    """Synthetic: only a negated instruction, or another runner's, is exempt."""
    assert _full_suite_instructions(["Never run the full package suite."]) == []
    assert _full_suite_instructions(["Do not run the whole suite."]) == []
    assert _full_suite_instructions(["Build and `finalize-review` run the package suite."]) == []
    assert _full_suite_instructions(["Execute the entire suite, and do not skip it."])


def test_rowcheck_pastedcommandoutputlocation_turnsred(tmp_path, monkeypatch):
    """A row sentence that is a pasted command, its output and a file location turns the check red."""
    text = TEMPLATE.read_text(encoding="utf-8")
    assert ROW1 in text, "anchor row is gone from the template"
    pasted = ROW1.replace(
        "<one plain sentence>", "ran `python3 -m pytest -q`: 42 passed; see loom-code/x.py:12"
    )
    path = tmp_path / "acceptance-test-report.md"
    path.write_text(text.replace(ROW1, pasted, 1), encoding="utf-8")
    monkeypatch.setattr(_THIS, "TEMPLATE", path)
    assert _fails(test_template_row_carries_no_how_or_evidence_cell)


def test_rowcheck_extradetailscolumn_turnsred(tmp_path, monkeypatch):
    """An extra column holding typed input and captured output turns the check red."""
    text = TEMPLATE.read_text(encoding="utf-8")
    assert HEADER in text, "anchor header is gone from the template"
    text = (
        text.replace(HEADER, "| # | What you asked for | Verdict | What happened | Re-run | Details |\n|---|---|---|---|---|---|", 1)
        .replace("| re-tested |", "| re-tested | <typed input and captured stdout> |", 1)
        .replace(
            "| carried over — <one-line reason> |",
            "| carried over — <one-line reason> | <typed input and captured stdout> |",
            1,
        )
    )
    path = tmp_path / "acceptance-test-report.md"
    path.write_text(text, encoding="utf-8")
    monkeypatch.setattr(_THIS, "TEMPLATE", path)
    assert _fails(test_template_row_carries_no_how_or_evidence_cell)


def _norm(word: str) -> str:
    return word.strip().replace("-", " ").lower()


def _template_verdicts() -> set[str]:
    text = " ".join(TEMPLATE.read_text(encoding="utf-8").split())
    match = re.search(r"Verdict is one of ([a-z /-]+?)\.", text)
    assert match, "template no longer lists its verdicts"
    return {_norm(w) for w in match.group(1).split("/")}


def test_verdictvocabulary_returnedset_equalstemplateset():
    """Every verdict the report may carry has the same name in the tester's return, and no other."""
    match = re.search(r"result: ([a-z |-]+?),", TESTER.read_text(encoding="utf-8"))
    assert match, "tester contract no longer lists its returned results"
    returned = {_norm(w) for w in match.group(1).split("|")}
    assert returned == _template_verdicts(), f"{sorted(returned)} vs {sorted(_template_verdicts())}"


def test_verdictvocabulary_untriedline_usestemplateword():
    """The contract's word for a line it could not try is one of the template's verdicts."""
    text = " ".join(TESTER.read_text(encoding="utf-8").split())
    match = re.search(r"An Acceptance line you could not try is `([^`]+)`", text)
    assert match, "tester contract no longer names the untried-line verdict"
    assert _norm(match.group(1)) in _template_verdicts(), match.group(1)


VERDICTS = ("not verified", "works", "partly", "fails")
AFFIRM = r"\b(?:is|gets|marks|reports|records|carries|gives|says|writes)\b"


def _affirms_verdict(sentence: str) -> bool:
    """A sentence about the suite that affirmatively assigns a quoted verdict to the row."""
    if "suite" not in sentence:
        return False
    for verdict in VERDICTS:
        pattern = AFFIRM + r"[^.;]*[`\"]" + re.escape(verdict) + r"[`\"]"
        if re.search(pattern, sentence):
            rest = sentence.replace(f"`{verdict}`", "").replace(verdict, "")
            return not has_negation(rest)
    return False


def _affirms_skip_row(sentence: str) -> bool:
    """A sentence about a skipped package-tests step that affirmatively says what the row carries."""
    if "`package-tests` is skipped" not in sentence:
        return False
    if not re.search(AFFIRM + r"[^.;]*\brow\b|\brow\b[^.;]*" + AFFIRM, sentence):
        return False
    return not has_negation(sentence)


def test_suiterowhelpers_syntheticsentences_discriminate():
    """Synthetic: both matchers accept the affirmative form and reject negated or unquoted ones."""
    assert _affirms_verdict("A row the suite settles is `not verified` until its result exists")
    assert not _affirms_verdict("A row the suite settles never says `works`")
    assert not _affirms_verdict("The row says finalize-review refuses the attestation when the suite fails")
    assert _affirms_skip_row("When `package-tests` is skipped, the row reports that criterion's own test result")
    assert not _affirms_skip_row("When `package-tests` is skipped, the row does not cite anything")


def test_suiterow_verdict_isnamed():
    """The contract names the verdict a suite-settled row carries, so works is not the unforced reading."""
    assert [s for s in _tester() if _affirms_verdict(s)], (
        "tester contract names no verdict for a row that cites the suite instead of a result"
    )


def test_suiterow_packagetestsskipped_saysrowcontent():
    """With package-tests skipped, the contract says what the row carries instead of a finalize-review run."""
    assert [s for s in _tester() if _affirms_skip_row(s)], (
        "with `package-tests` skipped the row still cites a finalize-review suite run that will not happen"
    )
