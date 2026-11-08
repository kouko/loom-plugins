"""Recompute artifact integrity separately from human/agent quality judgments."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def check_links(p, pending=False):
    for token in MarkdownIt().parse(p.read_text()):
        for child in token.children or []:
            if child.type != "link_open":
                continue
            target = child.attrGet("href")
            if target.startswith(("https:", "http:", "#")):
                continue
            resolved = (p.parent / target.split("#")[0]).resolve()
            if pending and resolved == ROOT / "verification.json":
                continue
            assert resolved.is_file(), (p, target)


def read_events(p):
    events = [json.loads(line) for line in p.read_text().splitlines()]
    assert not any(e.get("type") in ["reasoning", "reasoning_summary"] or
                   e.get("item", {}).get("type") in ["reasoning", "reasoning_summary"]
                   for e in events)
    return events


def main():
    prior = json.loads((ROOT / "frozen-prior-files.json").read_text())
    for path, digest in prior.items():
        assert sha(REPO / path) == digest, path
    inputs = json.loads((ROOT / "input-hashes.json").read_text())
    for path, digest in inputs.items():
        assert sha(ROOT / path) == digest, path
    trial = REPO / "docs/loom/2026-11-07-engineering-research-trial"
    for label, revision in [("old", "revision-4-structured-relations"),
                            ("new", "revision-5-framework-selection")]:
        bundle = ROOT / "input" / label / "engineering-research"
        for p in bundle.rglob("*"):
            if p.is_file():
                assert p.read_bytes() == (trial / revision / "candidate/engineering-research" / p.relative_to(bundle)).read_bytes()
    old = (ROOT / "input/old/engineering-research/SKILL.md").read_text()
    new = (ROOT / "input/new/engineering-research/SKILL.md").read_text()
    assert old.split("---", 2)[1] == new.split("---", 2)[1]
    activation = ROOT / "activation"
    a_receipts = [json.loads(p.read_text()) for p in sorted((activation / "runs").glob("*/receipt.json"))]
    assert len(a_receipts) == 50 and len({r["thread_id"] for r in a_receipts}) == 50
    for r in a_receipts:
        assert r["exit_code"] == 0 and not r.get("timed_out") and not r.get("harness_error")
        assert r["auth_symlink_removed"]
        out = activation / "runs" / r["id"]
        events = read_events(out / "events.jsonl")
        outputs = "\n".join(e.get("item", {}).get("aggregated_output", "") for e in events)
        assert r["target_body_read"] == ("Use evidence proportionate to the engineering question." in outputs)
        assert "Use evidence proportionate to the engineering question." not in (out / "catalog.json").read_text()
        for name in ["prompt.txt", "catalog.json", "events.jsonl", "answer.txt"]:
            key = name + "_sha256"
            if key in r:
                assert sha(out / name) == r[key]
    a_counts = {label: sum(r["classification"] == label for r in a_receipts)
                for label in ["true-positive", "true-negative", "trigger-miss", "over-trigger"]}
    execution = ROOT / "execution"
    for path, digest in json.loads((execution / "freeze.json").read_text())["hashes"].items():
        assert sha(execution / path) == digest, path
    b_receipts = [json.loads(p.read_text()) for p in sorted(execution.glob("X*/receipt.json"))]
    assert len(b_receipts) == 12 and len({r["thread_id"] for r in b_receipts}) == 12
    observations = []
    case_prompts = {}
    for r in b_receipts:
        assert r["exit_code"] == 0 and not r["timed_out"] and not r.get("harness_error")
        assert r["source_unchanged"] and r["auth_symlink_removed"]
        out = execution / r["id"]
        prompt = (out / "prompt.txt").read_bytes()
        if r["case"] in case_prompts:
            assert prompt == case_prompts[r["case"]]
        case_prompts[r["case"]] = prompt
        for original in (execution / "fixtures").rglob("*"):
            if original.is_file():
                assert sha(out / "artifacts" / original.relative_to(execution / "fixtures")) == sha(original)
        package = out / "artifacts/skill/engineering-research"
        label = "new" if (package / "references/evaluation-selection.md").exists() else "old"
        source = ROOT / "input" / label / "engineering-research"
        assert {str(p.relative_to(package)): sha(p) for p in package.rglob("*") if p.is_file()} == {
            str(p.relative_to(source)): sha(p) for p in source.rglob("*") if p.is_file()}
        events = read_events(out / "events.jsonl")
        outputs = "\n".join(e.get("item", {}).get("aggregated_output", "") for e in events)
        notes = sorted((out / "artifacts/docs/loom/research").glob("*.md"))
        assert notes, r["id"]
        for p in notes:
            meta = yaml.safe_load(p.read_text().split("---", 2)[1])
            assert meta["type"] == "loom-research" and "loom/research" in meta["tags"]
            assert isinstance(meta["created"], datetime.date) and isinstance(meta["updated"], datetime.date)
            assert all(not isinstance(v, dict) for v in meta.values())
            assert "title" in meta and meta["status"] in ["in-progress", "concluded", "superseded"]
            check_links(p)
        observations.append(dict(id=r["id"], case=r["case"], variant=label,
                                 note_paths=[str(p.relative_to(ROOT)) for p in notes],
                                 note_words=sum(len(p.read_text().split()) for p in notes),
                                 mermaid_blocks=sum(p.read_text().count(chr(96) * 3 + "mermaid") for p in notes),
                                 evaluation_reference_content_observed="# Select an engineering evaluation approach" in outputs,
                                 elapsed_seconds=r["elapsed_seconds"]))
    assert len(case_prompts) == 6
    for case in case_prompts:
        assert {r["variant"] for r in observations if r["case"] == case} == {"old", "new"}
    for n in [1, 2]:
        audit = json.loads((ROOT / f"audits/audit-{n}.json").read_text())
        actors = audit["actors"]
        assert {a["id"] for a in actors} == {r["id"] for r in b_receipts}
    for base in [Path("/private/tmp/framework-probe-b-20261108"),
                 Path("/private/tmp/engineering-research-frameworks-A-20261108")]:
        assert not list(base.glob("*/home/auth.json")), base
    check_links(ROOT / "report.md", pending=True)
    for p in ROOT.glob("*.py"):
        ast.parse(p.read_text())
    result = dict(status="recomputed artifact checks only; no global quality or improvement verdict",
                  prior_artifacts_unchanged=len(prior), frozen_inputs_unchanged=True,
                  description_unchanged=True, activation_runs=50, activation_counts=a_counts,
                  paired_cases=6, explicit_actors=12, independent_auditors=2,
                  per_actor=observations, conditional_selection_policy_tested=True,
                  installed_plugin_tested=False, causal_improvement_proven=False,
                  relative_note_links_resolve=True)
    result["artifact_sha256"] = {str(p.relative_to(ROOT)): sha(p) for p in sorted(ROOT.rglob("*"))
                                  if p.is_file() and p != ROOT / "verification.json"}
    (ROOT / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    check_links(ROOT / "report.md")
    print(json.dumps({k: v for k, v in result.items() if k not in ["artifact_sha256", "per_actor"]}, indent=2))


if __name__ == "__main__":
    main()
