"""Minimal JSON backend proving registration and selection."""

import json
from pathlib import Path


def id():
    return "demo-json"


def extension():
    return ".json"


def generate(path):
    Path(path).write_text(json.dumps({"backend": id(), "nodes": [], "edges": []}, indent=2) + "\n", encoding="utf-8")


def _data(path):
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict) or data.get("backend") != id():
        raise ValueError(f"{path}: expected backend {id()}")
    nodes, edges = data.get("nodes"), data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError(f"{path}: nodes and edges must be lists")
    ids = set()
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not isinstance(node.get("label"), str):
            raise ValueError(f"{path}: invalid node")
        if node["id"] in ids:
            raise ValueError(f"{path}: duplicate node {node['id']}")
        ids.add(node["id"])
    for edge in edges:
        if not isinstance(edge, dict) or not all(isinstance(edge.get(key), str) for key in ("id", "source", "target", "label")):
            raise ValueError(f"{path}: invalid edge")
        if edge["source"] not in ids or edge["target"] not in ids:
            raise ValueError(f"{path}: edge {edge['id']} has invalid endpoints")
    return data


def check(path):
    _data(path)


def project(path):
    data = _data(path)
    nodes = sorted(f"- {node['id']}: {node['label']}" for node in data["nodes"])
    edges = sorted(f"- {edge['id']}: {edge['source']} -> {edge['target']} | {edge['label']}" for edge in data["edges"])
    return "\n".join(["backend: demo-json", "# Nodes", *(nodes or ["- none"]), "# Edges", *(edges or ["- none"])])
