"""Backend format checks remain active without optional external tools."""

import importlib.util
from pathlib import Path

import pytest


BACKENDS = Path(__file__).resolve().parents[2] / "skills/loom-interactive-diagram/backends"


def load(name):
    spec = importlib.util.spec_from_file_location(name, BACKENDS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_drawio_rejects_compressed_page(tmp_path):
    path = tmp_path / "compressed.drawio"
    path.write_text('<mxfile><diagram id="0">compressed-data</diagram></mxfile>')
    with pytest.raises(ValueError, match="compressed.drawio.*compressed"):
        load("drawio").check(path)


def test_drawio_rejects_comments(tmp_path):
    path = tmp_path / "comment.drawio"
    load("drawio").generate(path)
    path.write_text(path.read_text().replace("<root>", "<root><!-- hidden -->"))
    with pytest.raises(ValueError, match="comment.drawio.*comment"):
        load("drawio").check(path)


def test_demo_json_rejects_invalid_edge(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text('{"backend":"demo-json","nodes":[],"edges":[{"id":"e","source":"a","target":"b","label":"next"}]}')
    with pytest.raises(ValueError, match="invalid.json.*endpoints"):
        load("demo_json").check(path)
