"""The shared diagram command checks every artifact in a change folder."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/diagram.py"
ROOT = SCRIPT.parents[4]


def run_tool(cwd, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, text=True, capture_output=True)


def test_registry_and_default_drawio(tmp_path):
    listed = run_tool(tmp_path, "list-backends")
    assert listed.returncode == 0
    assert listed.stdout.splitlines() == ["demo-json", "drawio"]
    created = run_tool(tmp_path, "new", "sample")
    assert created.returncode == 0, created.stderr
    assert (tmp_path / "diagrams/sample.drawio").exists()
    assert (tmp_path / "diagrams/sample.projection.md").read_text().startswith("backend: drawio\n")


def test_empty_registry_lists_nothing(tmp_path, monkeypatch, capsys):
    spec = importlib.util.spec_from_file_location("diagram_tool", SCRIPT)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    monkeypatch.setattr(tool, "BACKENDS", tmp_path)
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), "list-backends"])
    assert tool.main() == 0
    assert capsys.readouterr().out.strip() == "(none)"


def test_demo_backend_is_selectable(tmp_path):
    created = run_tool(tmp_path, "new", "demo-json", "example")
    assert created.returncode == 0, created.stderr
    assert (tmp_path / "diagrams/example.json").exists()
    assert run_tool(tmp_path, "check").returncode == 0


def test_unknown_backend_lists_registered_ids(tmp_path):
    result = run_tool(tmp_path, "new", "missing", "example")
    assert result.returncode != 0
    assert "demo-json" in result.stderr and "drawio" in result.stderr


def test_check_all_diagrams_and_name_mismatch(tmp_path):
    assert run_tool(tmp_path, "new", "drawio", "first").returncode == 0
    assert run_tool(tmp_path, "new", "demo-json", "second").returncode == 0
    projection = tmp_path / "diagrams/second.projection.md"
    projection.write_text(projection.read_text().replace("- none", "- wrong"))
    result = run_tool(tmp_path, "check")
    assert result.returncode != 0
    assert "second" in result.stderr
    assert "wrong" in result.stderr


def test_malformed_drawio_is_rejected_without_external_validator(tmp_path):
    assert run_tool(tmp_path, "new", "drawio", "broken").returncode == 0
    (tmp_path / "diagrams/broken.drawio").write_text("<mxfile><diagram>")
    result = run_tool(tmp_path, "check")
    assert result.returncode != 0
    assert "broken.drawio" in result.stderr


def test_project_writes_projection_for_named_diagram(tmp_path):
    assert run_tool(tmp_path, "new", "drawio", "one").returncode == 0
    projection = tmp_path / "diagrams/one.projection.md"
    projection.write_text("backend: drawio\n- stale\n")
    result = run_tool(tmp_path, "project", "diagrams/one.drawio")
    assert result.returncode == 0, result.stderr
    assert "- stale" not in projection.read_text()
    assert run_tool(tmp_path, "check").returncode == 0


def test_check_spec_link_outside_diagrams_directory(tmp_path):
    assert run_tool(tmp_path, "new", "drawio", "linked").returncode == 0
    shared = tmp_path / "shared"
    shared.mkdir()
    source = tmp_path / "diagrams/linked.drawio"
    projection = tmp_path / "diagrams/linked.projection.md"
    external = shared / source.name
    source.rename(external)
    projection.rename(shared / projection.name)
    (tmp_path / "spec.md").write_text("See [the editable graph](shared/linked.drawio).\n")
    assert run_tool(tmp_path, "check").returncode == 0
    (shared / projection.name).write_text("backend: drawio\n- stale\n")
    result = run_tool(tmp_path, "check")
    assert result.returncode != 0
    assert "shared/linked.projection.md" in result.stderr


def test_spec_link_is_resolved_from_spec_location(tmp_path):
    assert run_tool(tmp_path, "new", "drawio", "linked").returncode == 0
    (tmp_path / "spec.md").write_text("See [graph](diagrams/linked.drawio).\n")
    assert run_tool(tmp_path, "check").returncode == 0


@pytest.mark.parametrize(
    "name,link",
    [
        ("referenced", "See [diagram][flow].\n\n[flow]: shared/referenced.drawio\n"),
        ("nested(test)", "See [diagram](shared/nested(test).drawio).\n"),
    ],
)
def test_reference_and_balanced_inline_links_are_checked(tmp_path, name, link):
    assert run_tool(tmp_path, "new", "drawio", "source").returncode == 0
    shared = tmp_path / "shared"
    shared.mkdir()
    diagram = shared / f"{name}.drawio"
    projection = shared / f"{name}.projection.md"
    diagram.write_text((tmp_path / "diagrams/source.drawio").read_text())
    projection.write_text((tmp_path / "diagrams/source.projection.md").read_text())
    (tmp_path / "spec.md").write_text(link)
    assert run_tool(tmp_path, "check").returncode == 0
    projection.write_text("backend: drawio\n- stale\n")
    result = run_tool(tmp_path, "check")
    assert result.returncode != 0
    assert str(projection) in result.stderr


def test_station_documents_point_to_shared_rules():
    for station in ("write-spec", "architecture-design"):
        text = (ROOT / f"loom-design/skills/{station}/SKILL.md").read_text()
        assert "loom-workflow:loom-interactive-diagram" in text


def test_editor_setup_covers_both_hosts():
    text = (SCRIPT.parent.parent / "references/editor-setup.md").read_text()
    for term in ("VS Code", "Draw.io Integration", "draw.io desktop", "autosave", "synchronize"):
        assert term in text
