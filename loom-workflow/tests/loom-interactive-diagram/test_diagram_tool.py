"""The shared diagram command checks every artifact in a change folder."""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/scripts/diagram.py"
ROOT = SCRIPT.parents[4]


def run_tool(cwd, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, text=True, capture_output=True)


@pytest.fixture
def change_dir(tmp_path):
    change_id = "2026-10-31-example"
    intent = tmp_path / "docs/loom/intent"
    intent.mkdir(parents=True)
    (intent / f"{change_id}.md").write_text("# Example\n")
    change = tmp_path / "docs/loom" / change_id
    change.mkdir()
    return change


def test_root_create_uses_explicit_change_and_preserves_root_diagrams(change_dir):
    root = change_dir.parents[2]
    old = root / "diagrams/old.drawio"
    old.parent.mkdir()
    old.write_text("keep")
    result = run_tool(root, "new", "sample", "--change-id", change_dir.name)
    assert result.returncode == 0, result.stderr
    assert (change_dir / "diagrams/sample.drawio").is_file()
    assert (change_dir / "diagrams/sample.projection.md").is_file()
    assert old.read_text() == "keep"
    assert sorted(path.name for path in old.parent.iterdir()) == ["old.drawio"]


def test_root_create_makes_change_folder_without_root_diagrams(change_dir):
    root = change_dir.parents[2]
    change_dir.rmdir()
    result = run_tool(root, "new", "sample", "--change-id", change_dir.name)
    assert result.returncode == 0, result.stderr
    assert (change_dir / "diagrams/sample.drawio").is_file()
    assert (change_dir / "diagrams/sample.projection.md").is_file()
    assert not (root / "diagrams").exists()


def test_standalone_create_requires_explicit_destination(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    result = run_tool(tmp_path, "new", "sample", "--output-dir", str(project))
    assert result.returncode == 0, result.stderr
    assert (project / "sample.drawio").is_file()
    assert (project / "sample.projection.md").is_file()
    assert run_tool(tmp_path, "check", str(project / "sample.drawio")).returncode == 0
    missing = run_tool(tmp_path, "new", "another")
    assert missing.returncode == 1
    assert "destination required outside Loom; use --output-dir DIR" in missing.stderr
    assert not (tmp_path / "diagrams").exists()


def test_standalone_copy_preserves_source_and_rejects_existing_destination(change_dir):
    assert run_tool(change_dir, "new", "source").returncode == 0
    source = change_dir / "diagrams/source.drawio"
    original = source.read_bytes()
    project = change_dir.parents[2] / "other-project"
    project.mkdir()
    copied = run_tool(project, "copy", str(source), "--output-dir", str(project))
    assert copied.returncode == 0, copied.stderr
    assert (project / "source.drawio").read_bytes() == original
    assert (project / "source.projection.md").is_file()
    assert run_tool(project, "check", str(project / "source.drawio")).returncode == 0
    occupied = run_tool(project, "copy", str(source), "--output-dir", str(project))
    assert occupied.returncode == 1
    assert "already exists" in occupied.stderr
    assert source.read_bytes() == original
    assert (project / "source.drawio").read_bytes() == original


def test_loom_copy_uses_change_store_and_rejects_symlinked_store(change_dir):
    assert run_tool(change_dir, "new", "source").returncode == 0
    source = change_dir / "diagrams/source.drawio"
    external = change_dir.parents[2] / "external.drawio"
    external.write_bytes(source.read_bytes())
    original = external.read_bytes()
    copied = run_tool(change_dir, "copy", str(external))
    assert copied.returncode == 0, copied.stderr
    assert (change_dir / "diagrams/external.drawio").read_bytes() == original
    assert (change_dir / "diagrams/external.projection.md").is_file()
    assert external.read_bytes() == original
    change_dir.joinpath("diagrams").rename(change_dir / "old-diagrams")
    outside = change_dir.parents[2] / "outside"
    outside.mkdir()
    (change_dir / "diagrams").symlink_to(outside, target_is_directory=True)
    escaped = run_tool(change_dir, "copy", str(external))
    assert escaped.returncode == 1
    assert list(outside.iterdir()) == []
    explicit_escape = run_tool(change_dir, "new", "wrong", "--output-dir", str(outside))
    assert explicit_escape.returncode == 1
    assert list(outside.iterdir()) == []


def test_external_projection_requires_in_place_and_rejects_symlinks(change_dir):
    assert run_tool(change_dir, "new", "source").returncode == 0
    source = change_dir / "diagrams/source.drawio"
    external = change_dir.parents[2] / "external.drawio"
    external.write_bytes(source.read_bytes())
    without_selection = run_tool(change_dir, "project", str(external))
    assert without_selection.returncode == 1
    assert not (external.parent / "external.projection.md").exists()
    selected = run_tool(change_dir, "project", str(external), "--in-place")
    assert selected.returncode == 0, selected.stderr
    projection = external.parent / "external.projection.md"
    assert projection.is_file()
    assert run_tool(change_dir, "check", str(external)).returncode == 0
    projection.unlink()
    protected = external.parent / "protected.md"
    protected.write_text("keep")
    projection.symlink_to(protected)
    rejected = run_tool(change_dir, "project", str(external), "--in-place")
    assert rejected.returncode == 1
    assert "symlinked projection" in rejected.stderr
    assert protected.read_text() == "keep"
    alias = external.parent / "alias.drawio"
    alias.symlink_to(external)
    rejected_source = run_tool(change_dir, "project", str(alias), "--in-place")
    assert rejected_source.returncode == 1
    assert "symlinked diagram" in rejected_source.stderr


def test_new_rejects_missing_unknown_and_mismatched_change(change_dir):
    root = change_dir.parents[2]
    for cwd, args in (
        (root, ("new", "sample")),
        (root, ("new", "sample", "--change-id", "missing")),
        (root, ("new", "sample", "--change-id", "../escape")),
        (change_dir, ("new", "sample", "--change-id", "other")),
    ):
        result = run_tool(cwd, *args)
        assert result.returncode != 0
        assert not (change_dir / "diagrams").exists()
        assert not (root / "diagrams").exists()


def test_project_rejects_external_diagram_and_projection_symlink(change_dir):
    root = change_dir.parents[2]
    assert run_tool(change_dir, "new", "sample").returncode == 0
    outside = root / "outside.drawio"
    outside.write_text((change_dir / "diagrams/sample.drawio").read_text())
    outside_projection = root / "outside.projection.md"
    outside_projection.write_text("keep")
    result = run_tool(change_dir, "project", str(outside))
    assert result.returncode != 0
    assert outside_projection.read_text() == "keep"
    projection = change_dir / "diagrams/sample.projection.md"
    projection.unlink()
    projection.symlink_to(outside_projection)
    result = run_tool(change_dir, "project", "diagrams/sample.drawio")
    assert result.returncode != 0
    assert outside_projection.read_text() == "keep"


def test_project_from_root_with_explicit_change_only_updates_managed_projection(change_dir):
    root = change_dir.parents[2]
    assert run_tool(change_dir, "new", "sample").returncode == 0
    projection = change_dir / "diagrams/sample.projection.md"
    projection.write_text("backend: drawio\n- stale\n")
    result = run_tool(root, "project", "--change-id", change_dir.name)
    assert result.returncode == 0, result.stderr
    assert "- stale" not in projection.read_text()
    assert not (root / "diagrams").exists()


def test_managed_projection_hardlink_preserves_unselected(change_dir):
    assert run_tool(change_dir, "new", "sample").returncode == 0
    projection = change_dir / "diagrams/sample.projection.md"
    projection.unlink()
    protected = change_dir / "unselected.md"
    protected.write_text("backend: drawio\n# Nodes\n- keep\n")
    os.link(protected, projection)
    before = protected.read_bytes()

    result = run_tool(change_dir, "project", "diagrams/sample.drawio")

    assert result.returncode == 0 or "hardlink" in result.stderr.lower()
    assert protected.read_bytes() == before


def test_new_rejects_escaping_diagrams_symlink(change_dir):
    root = change_dir.parents[2]
    outside = root / "outside"
    outside.mkdir()
    (change_dir / "diagrams").symlink_to(outside, target_is_directory=True)
    result = run_tool(change_dir, "new", "sample")
    assert result.returncode != 0
    assert list(outside.iterdir()) == []


def test_new_rejects_escaping_final_file_symlink(change_dir):
    root = change_dir.parents[2]
    managed = change_dir / "diagrams"
    managed.mkdir()
    outside = root / "outside.drawio"
    outside.write_text("keep")
    (managed / "sample.drawio").symlink_to(outside)
    result = run_tool(change_dir, "new", "sample")
    assert result.returncode != 0
    assert outside.read_text() == "keep"
    assert not (managed / "sample.projection.md").exists()


def test_registry_and_default_drawio(change_dir):
    listed = run_tool(change_dir, "list-backends")
    assert listed.returncode == 0
    assert listed.stdout.splitlines() == ["demo-json", "drawio"]
    created = run_tool(change_dir, "new", "sample")
    assert created.returncode == 0, created.stderr
    assert (change_dir / "diagrams/sample.drawio").exists()
    assert (change_dir / "diagrams/sample.projection.md").read_text().startswith("backend: drawio\n")


def test_empty_registry_lists_nothing(change_dir, monkeypatch, capsys):
    spec = importlib.util.spec_from_file_location("diagram_tool", SCRIPT)
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    monkeypatch.setattr(tool, "BACKENDS", change_dir)
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), "list-backends"])
    assert tool.main() == 0
    assert capsys.readouterr().out.strip() == "(none)"


def test_demo_backend_is_selectable(change_dir):
    created = run_tool(change_dir, "new", "demo-json", "example")
    assert created.returncode == 0, created.stderr
    assert (change_dir / "diagrams/example.json").exists()
    assert run_tool(change_dir, "check").returncode == 0


def test_unknown_backend_lists_registered_ids(change_dir):
    result = run_tool(change_dir, "new", "missing", "example")
    assert result.returncode != 0
    assert "demo-json" in result.stderr and "drawio" in result.stderr


def test_check_all_diagrams_and_name_mismatch(change_dir):
    assert run_tool(change_dir, "new", "drawio", "first").returncode == 0
    assert run_tool(change_dir, "new", "demo-json", "second").returncode == 0
    projection = change_dir / "diagrams/second.projection.md"
    projection.write_text(projection.read_text().replace("- none", "- wrong"))
    result = run_tool(change_dir, "check")
    assert result.returncode != 0
    assert "second" in result.stderr
    assert "wrong" in result.stderr


def test_malformed_drawio_is_rejected_without_external_validator(change_dir):
    assert run_tool(change_dir, "new", "drawio", "broken").returncode == 0
    (change_dir / "diagrams/broken.drawio").write_text("<mxfile><diagram>")
    result = run_tool(change_dir, "check")
    assert result.returncode != 0
    assert "broken.drawio" in result.stderr


def test_project_writes_projection_for_named_diagram(change_dir):
    assert run_tool(change_dir, "new", "drawio", "one").returncode == 0
    projection = change_dir / "diagrams/one.projection.md"
    projection.write_text("backend: drawio\n- stale\n")
    result = run_tool(change_dir, "project", "diagrams/one.drawio")
    assert result.returncode == 0, result.stderr
    assert "- stale" not in projection.read_text()
    assert run_tool(change_dir, "check").returncode == 0


def test_check_spec_link_outside_diagrams_directory(change_dir):
    assert run_tool(change_dir, "new", "drawio", "linked").returncode == 0
    shared = change_dir / "shared"
    shared.mkdir()
    source = change_dir / "diagrams/linked.drawio"
    projection = change_dir / "diagrams/linked.projection.md"
    external = shared / source.name
    source.rename(external)
    projection.rename(shared / projection.name)
    (change_dir / "spec.md").write_text("See [the editable graph](shared/linked.drawio).\n")
    assert run_tool(change_dir, "check").returncode == 0
    (shared / projection.name).write_text("backend: drawio\n- stale\n")
    result = run_tool(change_dir, "check")
    assert result.returncode != 0
    assert "shared/linked.projection.md" in result.stderr


def test_spec_link_is_resolved_from_spec_location(change_dir):
    assert run_tool(change_dir, "new", "drawio", "linked").returncode == 0
    (change_dir / "spec.md").write_text("See [graph](diagrams/linked.drawio).\n")
    assert run_tool(change_dir, "check").returncode == 0


@pytest.mark.parametrize("link", [
    "See [a \\] label](shared/bad.drawio).\n",
    "See [a \\] label][flow].\n\n[flow]: shared/bad.drawio\n",
    "See [diagram][a \\] label].\n\n[a \\] label]: shared/bad.drawio\n",
    "See [a \\] label][].\n\n[a \\] label]: shared/bad.drawio\n",
    "See [a \\] label].\n\n[a \\] label]: shared/bad.drawio\n",
])
def test_escaped_bracket_label_still_checks_linked_diagram(change_dir, link):
    shared = change_dir / "shared"
    shared.mkdir()
    bad = shared / "bad.drawio"
    bad.write_text("<mxfile><diagram>")
    (shared / "bad.projection.md").write_text("backend: drawio\n")
    (change_dir / "spec.md").write_text(link)
    result = run_tool(change_dir, "check")
    assert result.returncode != 0
    assert str(bad) in result.stderr


@pytest.mark.parametrize(
    "name,link",
    [
        ("referenced", "See [diagram][flow].\n\n[flow]: shared/referenced.drawio\n"),
        ("nested(test)", "See [diagram](shared/nested(test).drawio).\n"),
        ("titled", 'See [diagram](shared/titled.drawio "Editable diagram").\n'),
        ("angle", 'See [diagram](<shared/angle.drawio> "Editable diagram").\n'),
        ("shortcut", "See [flow].\n\n[flow]: shared/shortcut.drawio\n"),
        ("collapsed", "See [flow][].\n\n[flow]: shared/collapsed.drawio\n"),
    ],
)
def test_reference_and_balanced_inline_links_are_checked(change_dir, name, link):
    assert run_tool(change_dir, "new", "drawio", "source").returncode == 0
    shared = change_dir / "shared"
    shared.mkdir()
    diagram = shared / f"{name}.drawio"
    projection = shared / f"{name}.projection.md"
    diagram.write_text((change_dir / "diagrams/source.drawio").read_text())
    projection.write_text((change_dir / "diagrams/source.projection.md").read_text())
    (change_dir / "spec.md").write_text(link)
    assert run_tool(change_dir, "check").returncode == 0
    projection.write_text("backend: drawio\n- stale\n")
    result = run_tool(change_dir, "check")
    assert result.returncode != 0
    assert str(projection) in result.stderr
    projection.write_text((change_dir / "diagrams/source.projection.md").read_text())
    diagram.write_text("<mxfile><diagram>")
    result = run_tool(change_dir, "check")
    assert result.returncode != 0
    assert str(diagram) in result.stderr


def test_station_documents_point_to_shared_rules():
    for station in ("write-spec", "architecture-design"):
        text = (ROOT / f"loom-design/skills/{station}/SKILL.md").read_text()
        assert "loom-workflow:loom-interactive-diagram" in text


def test_editor_setup_covers_both_hosts():
    text = (SCRIPT.parent.parent / "references/editor-setup.md").read_text()
    for term in ("VS Code", "Draw.io Integration", "draw.io desktop", "autosave", "synchronize"):
        assert term in text
