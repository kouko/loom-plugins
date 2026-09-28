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
