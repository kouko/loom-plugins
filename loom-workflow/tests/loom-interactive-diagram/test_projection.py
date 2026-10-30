"""Projection captures actual node and edge labels after a manual file edit."""

import importlib.util
from pathlib import Path


BACKENDS = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/backends"


def load(name):
    spec = importlib.util.spec_from_file_location(name, BACKENDS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_drawio_projection_reads_nodes_and_edges(tmp_path):
    backend = load("drawio")
    path = tmp_path / "flow.drawio"
    backend.generate(path)
    path.write_text(path.read_text().replace(
        "</root>",
        '<mxCell id="n1" value="Start" vertex="1" parent="1"><mxGeometry x="20" y="20" width="80" height="40" as="geometry"/></mxCell>'
        '<mxCell id="n2" value="End" vertex="1" parent="1"><mxGeometry x="200" y="20" width="80" height="40" as="geometry"/></mxCell>'
        '<mxCell id="e1" value="next" edge="1" parent="1" source="n1" target="n2"><mxGeometry relative="1" as="geometry"/></mxCell>'
        '</root>',
    ))
    assert backend.project(path) == (
        "backend: drawio\n# Nodes\n- n1: Start\n- n2: End\n# Edges\n- e1: n1 -> n2 | next"
    )


def test_empty_projection_has_both_sections(tmp_path):
    backend = load("drawio")
    path = tmp_path / "empty.drawio"
    backend.generate(path)
    assert backend.project(path) == "backend: drawio\n# Nodes\n- none\n# Edges\n- none"
