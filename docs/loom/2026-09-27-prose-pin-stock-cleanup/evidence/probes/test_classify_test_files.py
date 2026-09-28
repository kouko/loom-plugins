"""Census classifier probes (W3-02): the gate-eval class and the A5 execution count.

concern: a classifier regression that misfiles gate-eval files or miscounts the tests that execute a program (A5).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "classify_test_files", Path(__file__).with_name("classify-test-files.py")
)
ctf = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ctf)

PIN_FILE = 'from prose_pin import flat_prose\nTEXT = "SKILL.md"\n\ndef test_x():\n    assert "a pinned sentence" in TEXT\n'


def test_sentence_pin_named_by_a_gate_eval_is_classified_gate_eval(tmp_path: Path) -> None:
    f = tmp_path / "test_pin.py"
    f.write_text(PIN_FILE)
    assert ctf.classify(f)[0] == "sentence-pin"
    assert ctf.classify(f, gate_evals={f.as_posix()})[0] == "gate-eval"


def test_reader_call_with_no_literal_is_not_a_pin(tmp_path: Path) -> None:
    f = tmp_path / "test_reader.py"
    f.write_text('from prose_pin import flat_prose as _flat\nPROSE = _flat("SKILL.md")\n\ndef test_x():\n    assert PROSE\n')
    assert ctf.classify(f)[0] != "sentence-pin"


LOOP_HEAD = 'TEXT = open("SKILL.md").read()\nPHRASES = ("the rule is stated here", "x")\n\ndef test_h():\n    assert TEXT.startswith("# T")\n\n'


def _pinned(tmp_path: Path, body: str) -> bool:
    f = tmp_path / "test_loop.py"
    f.write_text(LOOP_HEAD + body)
    cls, secondary = ctf.classify(f)
    return cls == "sentence-pin" or secondary.get("has_pins") == "yes"


def test_loop_over_prose_phrases_asserted_in_counts_as_pin(tmp_path: Path) -> None:
    assert _pinned(tmp_path, "def test_x():\n    for p in PHRASES:\n        assert p in TEXT\n")


def test_path_exists_loop_and_absence_loop_are_not_pins(tmp_path: Path) -> None:
    body = ('def test_x():\n    for p in ("a b c.md", "d e f.md"):\n        assert Path(p).exists()\n'
            "    for p in PHRASES:\n        assert p not in TEXT\n")
    assert not _pinned(tmp_path, body)


def test_direct_literal_in_md_text_flagged(tmp_path: Path) -> None:
    assert _pinned(tmp_path, 'def test_x():\n    assert "the rule is stated here" in TEXT\n')


def test_literal_in_subprocess_output_not_flagged(tmp_path: Path) -> None:
    body = ('import subprocess\n\ndef test_x():\n'
            '    r = subprocess.run(["python3", "x.py"], capture_output=True, text=True)\n'
            '    assert "the rule is stated here" in r.stdout\n')
    assert not _pinned(tmp_path, body)


def test_short_heading_literal_not_flagged(tmp_path: Path) -> None:
    assert not _pinned(tmp_path, 'def test_x():\n    assert "## Scope and rules" in TEXT\n    assert "Scope rules" in TEXT\n')


YAML_SPLIT = ('import yaml\nP = "agents/prompt.md"\n\ndef _split(text):\n    fm = yaml.safe_load(text.split("---")[1])\n'
              '    return fm, text.split("---", 2)[2]\n\ndef test_x():\n    fm, body = _split(open(P).read())\n')


def test_yaml_helper_body_pin_flagged() -> None:
    assert ctf.direct_pin_lines(YAML_SPLIT + '    assert "never mention the truth" in body.lower()\n') == [10]


def test_parsed_frontmatter_value_not_flagged() -> None:
    assert ctf.direct_pin_lines(YAML_SPLIT + '    assert "never mention the truth" in str(fm["rules"])\n') == []


def test_installed_copy_skill_read_counts_as_prose() -> None:
    src = ('def test_x(tmp_path):\n    root = tmp_path / "cache"\n'
           '    text = (root / "skills" / "SKILL.md").read_text()\n    assert "the rule is stated here" in text\n')
    assert ctf.direct_pin_lines(src) == [4]


def test_two_word_literal_against_skill_text_flagged(tmp_path: Path) -> None:
    assert _pinned(tmp_path, 'def test_x():\n    assert "never dispatch" in TEXT\n')


def test_short_literal_in_checker_output_not_flagged(tmp_path: Path) -> None:
    body = ('import subprocess\n\ndef test_x():\n'
            '    r = subprocess.run(["python3", "loom_checker.py"], capture_output=True, text=True)\n'
            '    assert "never dispatch" in r.stdout\n')
    assert not _pinned(tmp_path, body)


def test_heading_marker_field_key_classed_structural() -> None:
    body = ('def test_x():\n    assert "## Scope" in TEXT\n    assert "<!-- gate: a.b -->" in TEXT\n'
            '    assert "status:" in TEXT\n')
    found = ctf.pin_candidates(LOOP_HEAD + body)
    assert [c["cls"] for c in found if c["func"] == "test_x"] == ["structural"] * 3, found


def test_helper_fed_prose_and_index_and_regex_flagged() -> None:
    body = ('import re\n\ndef _errors(text):\n    if "never dispatch" not in text:\n        return ["x"]\n    return []\n\n'
            'def test_x():\n    assert not _errors(TEXT)\n    TEXT.index("never dispatch")\n'
            '    assert re.search(r"never\\s+dispatch", TEXT)\n')
    assert ctf.direct_pin_lines(LOOP_HEAD + body) == [10, 16, 17]


def test_count_executing_tests_counts_only_functions_with_an_execution_signal(tmp_path: Path) -> None:
    root = tmp_path / "loom-code" / "tests"
    root.mkdir(parents=True)
    (root / "test_a.py").write_text(
        "import subprocess\n\n"
        "def test_runs():\n"
        '    r = subprocess.run(["python3", "loom_checker.py"])\n'
        "    assert r.returncode == 0\n\n"
        "def test_reads():\n"
        '    assert "x" in "xy"\n'
    )
    assert ctf.count_executing_tests(tmp_path) == 1


def _count_one(tmp_path: Path, body: str) -> int:
    root = tmp_path / "tests"
    root.mkdir()
    (root / "test_one.py").write_text(body)
    return ctf.count_executing_tests(tmp_path)


def test_subprocess_call_counts_as_exec(tmp_path: Path) -> None:
    assert _count_one(tmp_path, 'import subprocess\n\ndef test_x():\n    subprocess.run(["git", "status"])\n') == 1


def test_loom_checker_string_literal_not_counted(tmp_path: Path) -> None:
    assert _count_one(tmp_path, 'TEXT = ""\n\ndef test_x():\n    assert "loom_checker.py selection show" in TEXT\n') == 0


def test_census_at_head_places_every_prose_reader_in_a_named_class(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["classify-test-files.py"])
    assert ctf.main() == 0
    assert "'other': 0" in capsys.readouterr().out


def test_unlisted_file_fails_census_and_is_printed(tmp_path: Path, monkeypatch, capsys) -> None:
    (tmp_path / "t").mkdir()
    (tmp_path / "t" / "test_unlisted.py").write_text('DOC = "SKILL.md"\n\ndef test_x():\n    assert DOC\n')
    monkeypatch.setattr(ctf, "REPO", tmp_path)
    monkeypatch.setattr(ctf, "load_gate_evals", lambda: set())
    monkeypatch.setattr("sys.argv", ["classify-test-files.py", "--roots", "t"])
    assert ctf.main() == 1
    assert any(line.startswith("t/test_unlisted.py") and " other " in line for line in capsys.readouterr().out.splitlines())
