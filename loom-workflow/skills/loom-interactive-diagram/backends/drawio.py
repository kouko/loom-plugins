"""Uncompressed draw.io XML backend."""

from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET


def id():
    return "drawio"


def extension():
    return ".drawio"


def generate(path):
    Path(path).write_text('''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="0" name="Page-1">
    <mxGraphModel grid="1" page="1" pageWidth="827" pageHeight="1169">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
''', encoding="utf-8")


def _cells(path):
    path = Path(path)
    if "<!--" in path.read_text(encoding="utf-8"):
        raise ValueError(f"{path}: XML comments are not allowed")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise ValueError(f"{path}: invalid XML: {exc}") from exc
    if root.tag == "mxfile":
        pages = root.findall("diagram")
        if not pages:
            raise ValueError(f"{path}: no diagram page")
        models = []
        for page in pages:
            model = page.find("mxGraphModel")
            if model is None:
                raise ValueError(f"{path}: compressed or missing mxGraphModel page")
            models.append(model)
    elif root.tag == "mxGraphModel":
        models = [root]
    else:
        raise ValueError(f"{path}: expected mxfile or mxGraphModel")
    result = []
    for model in models:
        graph_root = model.find("root")
        if graph_root is None:
            raise ValueError(f"{path}: missing graph root")
        parents = {child: parent for parent in graph_root.iter() for child in parent}
        cells = list(graph_root.iter("mxCell"))
        for cell in cells:
            wrapper = parents.get(cell)
            if not cell.get("id") and wrapper is not None and wrapper.tag == "object":
                cell.set("id", wrapper.get("id", ""))
        ids = [cell.get("id") for cell in cells]
        if not all(ids) or len(ids) != len(set(ids)) or "0" not in ids or "1" not in ids:
            raise ValueError(f"{path}: invalid, duplicate or missing cell IDs 0/1")
        known = set(ids)
        for cell in cells:
            parent = cell.get("parent")
            if parent and parent not in known:
                raise ValueError(f"{path}: cell {cell.get('id')} has unknown parent {parent}")
            if cell.get("edge") == "1":
                source, target = cell.get("source"), cell.get("target")
                if not source or not target or source not in known or target not in known:
                    raise ValueError(f"{path}: edge {cell.get('id')} has invalid endpoints")
            wrapper = parents.get(cell)
            label = cell.get("value", "")
            if wrapper is not None and wrapper.tag == "object":
                label = wrapper.get("label", wrapper.get("value", label))
            result.append((cell, label))
    return result


def check(path):
    _cells(path)


def project(path):
    cells = _cells(path)
    lines = ["backend: drawio", "# Nodes", "# Edges"]
    nodes = []
    edges = []
    for cell, label in cells:
        if cell.get("vertex") == "1":
            nodes.append(f"- {cell.get('id')}: {unescape(label)}")
        elif cell.get("edge") == "1":
            edges.append(f"- {cell.get('id')}: {cell.get('source')} -> {cell.get('target')} | {unescape(label)}")
    return "\n".join([lines[0], lines[1], *(sorted(nodes) or ["- none"]), lines[2], *(sorted(edges) or ["- none"])])
