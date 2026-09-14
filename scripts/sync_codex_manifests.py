#!/usr/bin/env python3
"""Repo-level Codex manifest sync engine — sync a plugin's Codex manifest from
its Claude SSOT.

For a given plugin directory, the Claude manifest
(``<plugin>/.claude-plugin/plugin.json``) is the single source of truth for the
shared plugin metadata. The Codex manifest
(``<plugin>/.codex-plugin/plugin.json``) derives those same fields but adds a
Codex-only ``interface`` block. This engine copies the shared fields into the
Codex manifest in lock-step while preserving ``interface`` (and any other
Codex-only key) verbatim.

It also generates the Antigravity CLI (agy) root manifest
(``<plugin>/plugin.json``). That file is wholly derived — ``AGY_FIELDS`` copied
from the Claude SSOT, nothing hand-authored — so any difference from the
derived form is drift. Claude Code and Codex ignore a root ``plugin.json``.
Every mode below (sync, ``--check``, ``--scaffold``, ``--all``) covers both
derived manifests; a MISSING root manifest fails only ``--all --check``.

It also generates the agy plugin rule ``<plugin>/rules/AGENTS.md`` for each
plugin in ``AGY_RULE_SOURCES`` (only loom-workflow: its visualization trigger
card, prefixed with a one-line generated-file header). Every mode covers it;
a MISSING or drifted rule fails both ``--check`` and ``--all --check``.

This engine is REPO-LEVEL (not self-locating to a single plugin): the plugin to
sync is passed in as a
directory name or path. The public surface (``sync_plugin`` + a CLI taking a
plugin arg) is shaped so a later task can add ``--scaffold``, an eligible-plugin
list, and ``--all`` without reworking it.

Usage:
    python3 scripts/sync_codex_manifests.py <plugin>
        Rewrite <plugin>'s Codex manifest shared fields from its Claude SSOT.

    python3 scripts/sync_codex_manifests.py --check <plugin>
        Pure read. Exit 0 if the manifests are in sync, non-zero on
        divergence. Used as a CI drift gate.

Stdlib only (json/pathlib/argparse). String equality for the version comparison
— no third-party ``packaging``.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Fields the Codex manifest derives from the Claude SSOT, in lock-step.
SHARED_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)

CLAUDE_MANIFEST = (".claude-plugin", "plugin.json")
CODEX_MANIFEST = (".codex-plugin", "plugin.json")
AGY_MANIFEST = ("plugin.json",)

# agy needs only ``name``; ``version`` and ``description`` are accepted by
# ``agy plugin validate`` and keep the listing informative. Nothing else, so
# the root file carries no host wiring another loader could adopt.
AGY_FIELDS = ("name", "version", "description")

# The independent repository publishes exactly the three Loom plugins; the same
# set gets both the Codex and the agy root manifest.
CODEX_ELIGIBLE = ("loom-code", "loom-design", "loom-workflow")

# agy keeps a plugin's ``rules/AGENTS.md`` active in every session; Claude Code
# and Codex ignore it. It is generated from one source file per plugin — an
# explicit map, not a scan: only loom-workflow ships a trigger card.
AGY_RULE = ("rules", "AGENTS.md")
AGY_RULE_SOURCES = {
    "loom-workflow": ("skills", "loom-visualization", "assets", "trigger-card.md"),
}


def sync_shared_fields(source: dict, target: dict) -> dict:
    """Return a new target dict with SHARED_FIELDS copied from ``source``.

    Codex-only keys on ``target`` (e.g. ``interface``) are preserved verbatim.
    Key ordering of ``target`` is preserved so the diff stays minimal.
    """
    result = dict(target)
    for field in SHARED_FIELDS:
        if field in source:
            result[field] = source[field]
    return result


def manifests_synced(source: dict, target: dict) -> bool:
    """True iff every shared field on ``target`` already matches ``source``."""
    return sync_shared_fields(source, target) == target


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, data: dict) -> None:
    # 2-space indent + trailing newline to match the existing manifest style.
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def claude_manifest_path(plugin_dir: Path) -> Path:
    return plugin_dir.joinpath(*CLAUDE_MANIFEST)


def codex_manifest_path(plugin_dir: Path) -> Path:
    return plugin_dir.joinpath(*CODEX_MANIFEST)


def sync_plugin(plugin_dir, check: bool = False) -> bool:
    """Sync one plugin's Codex manifest shared fields from its Claude SSOT.

    ``plugin_dir`` is a directory name or path containing ``.claude-plugin`` and
    ``.codex-plugin`` subdirs. Returns whether the Codex manifest is in sync:

    - ``check=True``  — pure read; return True iff already synced (no mutation).
    - ``check=False`` — rewrite the Codex manifest when it diverges, then
      return True (in sync after the write).
    """
    plugin_dir = Path(plugin_dir)
    source = _load(claude_manifest_path(plugin_dir))
    target_path = codex_manifest_path(plugin_dir)
    target = _load(target_path)

    if check:
        return manifests_synced(source, target)

    synced = sync_shared_fields(source, target)
    if synced != target:
        _dump(target_path, synced)
    return True


def agy_manifest_path(plugin_dir: Path) -> Path:
    return plugin_dir.joinpath(*AGY_MANIFEST)


def derive_agy_manifest(source: dict) -> dict:
    """The agy root manifest: ``AGY_FIELDS`` from the Claude SSOT, in order."""
    return {field: source[field] for field in AGY_FIELDS if field in source}


def sync_agy_manifest(plugin_dir, check: bool = False) -> bool:
    """Generate (or, with ``check=True``, verify) ``<plugin>/plugin.json``.

    ``check=True`` is a pure read: True iff the file exists and equals the
    derived manifest exactly (an extra key is drift). ``check=False`` writes
    the derived manifest when it differs and returns True.
    """
    plugin_dir = Path(plugin_dir)
    derived = derive_agy_manifest(_load(claude_manifest_path(plugin_dir)))
    target_path = agy_manifest_path(plugin_dir)
    try:
        current = _load(target_path)
    except (OSError, ValueError):
        # Absent, a directory, or undecodable: not the derived manifest, so
        # --check reports drift and sync regenerates a regular file.
        current = None

    if check:
        return current == derived

    if current != derived:
        _dump(target_path, derived)
    return True


def _check_agy(plugin_dir: Path, require: bool = True) -> int:
    """CLI helper: print MISSING/DRIFT for the agy root manifest; 0 when clean.

    ``require=False`` (single-plugin ``--check``, also run by the Codex drift
    edit hook on any plugin) skips an absent root manifest; ``--all`` requires
    it for every eligible plugin.
    """
    path = agy_manifest_path(plugin_dir)
    if not path.exists():
        if not require:
            return 0
        print(f"MISSING: {path} — run: python3 {Path(__file__).name} {plugin_dir}",
              file=sys.stderr)
        return 1
    if not sync_agy_manifest(plugin_dir, check=True):
        print(
            f"DRIFT: {path} differs from the fields {list(AGY_FIELDS)} of "
            f"{claude_manifest_path(plugin_dir)}. "
            f"Run: python3 {Path(__file__).name} {plugin_dir}",
            file=sys.stderr,
        )
        return 1
    return 0


def agy_rule_path(plugin_dir: Path) -> Path:
    return Path(plugin_dir).joinpath(*AGY_RULE)


def _agy_rule_source(plugin_dir: Path):
    """The source path tuple for this plugin's rule, or None when it has none."""
    return AGY_RULE_SOURCES.get(Path(plugin_dir).resolve().name)


def derive_agy_rule(plugin_dir) -> str:
    """A one-line generated-file header, then the source file verbatim."""
    source = _agy_rule_source(plugin_dir)
    rel = "/".join(source)
    header = (
        f"<!-- Generated from {rel} by scripts/{Path(__file__).name}; "
        f"edit {rel}, not this file. -->\n"
    )
    return header + Path(plugin_dir).joinpath(*source).read_text(encoding="utf-8")


def sync_agy_rule(plugin_dir, check: bool = False) -> bool:
    """Generate (or, with ``check=True``, verify) ``<plugin>/rules/AGENTS.md``.

    A plugin without an ``AGY_RULE_SOURCES`` entry has no rule: always True,
    nothing written. A mapped plugin whose source file is absent gets no rule
    either, so a leftover rule there is drift. ``check=True`` is a pure read.
    """
    plugin_dir = Path(plugin_dir)
    source = _agy_rule_source(plugin_dir)
    if source is None:
        return True
    target_path = agy_rule_path(plugin_dir)
    if not plugin_dir.joinpath(*source).is_file():
        return not (check and target_path.exists())
    derived = derive_agy_rule(plugin_dir)
    try:
        current = target_path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        current = None

    if check:
        return current == derived

    if current != derived:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(derived, encoding="utf-8")
    return True


def _check_agy_rule(plugin_dir: Path) -> int:
    """CLI helper: print MISSING/DRIFT for the agy plugin rule; 0 when clean."""
    rel = _agy_rule_source(plugin_dir)
    if rel is None:
        return 0
    path = agy_rule_path(plugin_dir)
    source = Path(plugin_dir).joinpath(*rel)
    fix = f"Run: python3 {Path(__file__).name} {plugin_dir}"
    if source.is_file() and not path.is_file():
        print(f"MISSING: {path} — {fix}", file=sys.stderr)
        return 1
    if not sync_agy_rule(plugin_dir, check=True):
        print(f"DRIFT: {path} differs from its source {source} "
              f"(or the source is gone). {fix}", file=sys.stderr)
        return 1
    return 0


def _derive_interface(source: dict) -> dict:
    """Build a fresh Codex ``interface`` block from the Claude SSOT.

    Mechanically-derivable fields are filled from ``source``; judgment fields
    Phase 2 must author by hand are seeded with the literal string ``"TODO"``.
    Key set + order mirror loom-code/.codex-plugin/plugin.json (the schema
    template). ``author`` may be a ``{"name", "url"}`` dict or a bare string.
    """
    name = source.get("name", "")
    author = source.get("author")
    developer = author.get("name", "") if isinstance(author, dict) else (author or "")
    repository = source.get("repository", "")
    homepage = source.get("homepage", "")
    # websiteURL fallback chain: a repository derives the canonical GitHub subdir
    # URL; absent that, the homepage IS already that tree URL; the bare name is a
    # last resort only when neither URL is present.
    if repository and name:
        website = f"{repository}/tree/main/{name}"
    elif homepage:
        website = homepage
    else:
        website = repository or name
    return {
        "displayName": name,
        "shortDescription": "TODO",
        "longDescription": "TODO",
        "developerName": developer,
        "category": "TODO",
        "capabilities": "TODO",
        "defaultPrompt": "TODO",
        "websiteURL": website,
        "brandColor": "TODO",
    }


def scaffold_plugin(plugin_dir, sync: bool = True) -> bool:
    """Create a missing Codex manifest for ``plugin_dir`` from its Claude SSOT.

    Seeds the 8 SHARED_FIELDS plus a TODO-placeholder ``interface`` block (see
    ``_derive_interface``). Returns ``True`` iff a manifest was created.

    Never clobbers an existing Codex manifest: if one is already present this is
    a no-op (or a shared-field sync when ``sync=True``) and returns ``False`` —
    human-authored ``interface`` values are preserved.
    """
    plugin_dir = Path(plugin_dir)
    target_path = codex_manifest_path(plugin_dir)
    if target_path.exists():
        if sync:
            sync_plugin(plugin_dir)
        return False

    source = _load(claude_manifest_path(plugin_dir))
    manifest: dict = {}
    for field in SHARED_FIELDS:
        if field in source:
            manifest[field] = source[field]
    manifest["interface"] = _derive_interface(source)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    _dump(target_path, manifest)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "plugin",
        type=Path,
        nargs="?",
        help="plugin directory (name or path); omit when using --all",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="pure read; exit non-zero on divergence (CI drift gate)",
    )
    parser.add_argument(
        "--scaffold",
        action="store_true",
        help="create a missing Codex manifest (TODO placeholders) then sync; never clobbers",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="iterate every CODEX_ELIGIBLE plugin under the repo root",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="repo root for --all (defaults to this script's parent repo)",
    )
    args = parser.parse_args(argv)

    if args.all:
        repo_root = (
            args.repo_root
            if args.repo_root is not None
            else Path(__file__).resolve().parent.parent
        )
        # In --check mode this stays read-only and accumulates a non-zero exit
        # if ANY plugin is out of sync; otherwise sync_plugin always returns
        # True (after writing) so the loop never trips the drift branch.
        exit_code = 0
        for name in CODEX_ELIGIBLE:
            plugin_dir = repo_root / name
            if args.scaffold:
                scaffold_plugin(plugin_dir)
            elif args.check and not codex_manifest_path(plugin_dir).exists():
                print(
                    f"MISSING: {codex_manifest_path(plugin_dir)} — run --scaffold",
                    file=sys.stderr,
                )
                exit_code = 1
            elif not sync_plugin(plugin_dir, check=args.check):
                print(
                    f"DRIFT: {codex_manifest_path(plugin_dir)} shared fields "
                    f"diverge from {claude_manifest_path(plugin_dir)}. "
                    f"Run: python3 {Path(__file__).name} {plugin_dir}",
                    file=sys.stderr,
                )
                exit_code = 1
            if args.check:
                exit_code |= _check_agy(plugin_dir)
                exit_code |= _check_agy_rule(plugin_dir)
            else:
                sync_agy_manifest(plugin_dir)
                sync_agy_rule(plugin_dir)
        return exit_code

    if args.plugin is None:
        parser.error("a plugin directory is required unless --all is given")

    if args.scaffold:
        scaffold_plugin(args.plugin)
        sync_agy_manifest(args.plugin)
        sync_agy_rule(args.plugin)
        return 0

    if args.check:
        if not codex_manifest_path(args.plugin).exists():
            print(
                f"MISSING: {codex_manifest_path(args.plugin)} — run --scaffold",
                file=sys.stderr,
            )
            return 1
        if not sync_plugin(args.plugin, check=True):
            print(
                f"DRIFT: {codex_manifest_path(args.plugin)} shared fields diverge "
                f"from {claude_manifest_path(args.plugin)}. "
                f"Run: python3 {Path(__file__).name} {args.plugin}",
                file=sys.stderr,
            )
            return 1
        return _check_agy(args.plugin, require=False) | _check_agy_rule(args.plugin)

    sync_plugin(args.plugin)
    sync_agy_manifest(args.plugin)
    sync_agy_rule(args.plugin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
