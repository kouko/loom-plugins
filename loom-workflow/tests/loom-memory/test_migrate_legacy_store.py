"""Migration fidelity and failure protection using temporary Git stores.

The completed real-corpus migration proofs are retired; these tests exercise
supported transformations without requiring a historical trunk baseline.
The current repository store still receives validation and index checks.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "skills" / "loom-memory" / "scripts"
REPO_ROOT = SCRIPTS_DIR.parents[3]
STORE = REPO_ROOT / "docs" / "loom" / "memory"
sys.path.insert(0, str(SCRIPTS_DIR))

import loom_memory as lm  # noqa: E402
import migrate_legacy_store as mls  # noqa: E402



# ---------------------------------------------------------------------------
# Fixture helpers (synthetic stores)
# ---------------------------------------------------------------------------


def _write(store: Path, rel: str, text: str) -> None:
    path = store / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _legacy_concept(name: str, description: str, *, type_: str | None = "practice", origin: str | None = "a fixture origin") -> str:
    lines = ["---", f"name: {name}", f"description: {description}"]
    if type_ is not None:
        lines.append(f"type: {type_}")
    if origin is not None:
        lines.append(f"origin: {origin}")
    lines.append("---")
    lines.append("")
    lines.append("The fact body.")
    lines.append("")
    return "\n".join(lines)


def _legacy_readme(index_lines: list[str], *, charter: str = "# Charter\n\nSome prose.\n") -> str:
    body = charter.rstrip("\n") + "\n\n## Index\n\n" + "\n".join(index_lines) + "\n"
    return body


def _make_legacy_store(store: Path) -> None:
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[a-fact](a-fact.md) — A description."]))
    _write(store, "a-fact.md", _legacy_concept("a-fact", "A description."))


def _init_git_repo(root: Path) -> None:
    for cmd in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "test@example.com"],
        ["git", "config", "user.name", "Test"],
    ):
        subprocess.run(cmd, cwd=root, check=True, capture_output=True)


def _commit_all(root: Path, message: str) -> None:
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=root, check=True, capture_output=True)


# ---------------------------------------------------------------------------
# Current real-store validation
# ---------------------------------------------------------------------------


def test_migrated_store_validates_clean_and_regenerates_idempotently():
    assert lm.validate_bundle(STORE) == []
    first = (STORE / "index.md").read_text(encoding="utf-8")
    lm.regenerate_index(STORE)
    second = (STORE / "index.md").read_text(encoding="utf-8")
    assert first == second


# ---------------------------------------------------------------------------
# Synthetic-store unit tests for migrate()/is_legacy_store()
# ---------------------------------------------------------------------------


def test_migrate_transforms_a_legacy_store_into_a_valid_okf_profile(tmp_path):
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    charter = "# Fixture charter\n\nKeep all prose: 中文 and punctuation.\n\n## Recording\n\nOne lesson per file.\n"
    # Expectations are fixture inputs, never migration-derived output.
    lessons = {
        "a-fact.md": {
            "name": "a-fact", "description": "First distinct description.",
            "type": "practice", "origin": "fixture: original source",
            "body": b"\nFirst body.\n\n  Indented bytes.\n",
        },
        "b-fact.md": {
            "name": "b-fact", "description": "Second distinct description.",
            "type": "gotcha", "body": "\nSecond body — 中文.\n".encode(),
        },
    }
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme([
        f"[{item['name']}]({filename}) — {item['description']}"
        for filename, item in lessons.items()
    ], charter=charter))
    for filename, item in lessons.items():
        fields = [f"{key}: {item[key]}" for key in ("name", "description", "type")]
        if "origin" in item:
            fields.append(f"origin: {item['origin']}")
        fields.append("recorded: 2026-11-13")
        (store / filename).write_bytes(
            ("---\n" + "\n".join(fields) + "\n---\n").encode() + item["body"]
        )
    _init_git_repo(repo_root)
    _commit_all(repo_root, "introduce fixture lessons and charter")
    introducing_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo_root,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    # A later commit prevents a latest-commit implementation passing by accident.
    (repo_root / "unrelated.txt").write_text("Later unrelated change.\n")
    _commit_all(repo_root, "later unrelated change")

    assert mls.is_legacy_store(store) is True
    result = mls.migrate(store, repo_root)

    assert result.lessons == len(lessons) == 2
    assert result.guide == 1
    assert {p.name for p in store.glob("*.md")} == {*lessons, "README.md", "index.md"}
    assert lm.validate_bundle(store) == []
    for filename, item in lessons.items():
        migrated = (store / filename).read_bytes()
        fm = lm.parse_frontmatter(migrated.decode())
        for key in ("name", "description", "type"):
            assert fm[key] == item[key], (filename, key)
        assert fm["sources"] == [{"resource": item.get("origin", f"introducing commit {introducing_sha}")}]
        assert "origin" not in fm
        assert fm["recorded"] == "2026-11-13"
        assert migrated.split(b"\n---\n", 1)[1] == item["body"]

    readme = (store / "README.md").read_bytes()
    readme_fm = lm.parse_frontmatter(readme.decode())
    assert readme_fm["type"] == lm.GUIDE_TYPE
    assert readme_fm["name"] == "README"
    assert isinstance(readme_fm["description"], str) and readme_fm["description"].strip()
    assert readme_fm["sources"] == [{"resource": f"introducing commit {introducing_sha}"}]
    # Migration normalizes the pre-index trailing separator to one newline,
    # then inserts one blank line between metadata and the complete charter.
    assert readme.split(b"\n---\n", 1)[1] == b"\n" + charter.encode()
    assert b"## Index" not in readme
    guides = [p.name for p in store.glob("*.md")
              if lm.parse_frontmatter(p.read_text()).get("type") == lm.GUIDE_TYPE]
    assert guides == ["README.md"]
    index = (store / "index.md").read_bytes()
    lm.regenerate_index(store)
    assert (store / "index.md").read_bytes() == index
    assert lm.validate_bundle(store) == []


def test_migrate_assigns_generic_type_and_derives_commit_when_both_absent(tmp_path):
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[bare-fact](bare-fact.md) — No type or origin."]))
    _write(store, "bare-fact.md", _legacy_concept("bare-fact", "No type or origin.", type_=None, origin=None))
    _init_git_repo(repo_root)
    _commit_all(repo_root, "initial")

    mls.migrate(store, repo_root)

    fm = lm.parse_frontmatter((store / "bare-fact.md").read_text(encoding="utf-8"))
    assert fm["type"] == "Memory"
    resource = fm["sources"][0]["resource"]
    assert resource.startswith("introducing commit ")
    sha = resource.removeprefix("introducing commit ")
    assert len(sha) == 40
    # the derived commit is the one that actually introduced the file
    expected = mls.introducing_commit(repo_root, "docs/loom/memory/bare-fact.md")
    assert sha == expected


def test_migrate_preserves_unknown_extra_key(tmp_path):
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[extra-key-fact](extra-key-fact.md) — Carries an extra key."]))
    _write(
        store,
        "extra-key-fact.md",
        "---\nname: extra-key-fact\ndescription: Carries an extra key.\ntype: gotcha\n"
        "origin: a fixture origin\ntype_note: legacy carryover\n---\n\nBody.\n",
    )
    _init_git_repo(repo_root)
    _commit_all(repo_root, "initial")

    mls.migrate(store, repo_root)

    fm = lm.parse_frontmatter((store / "extra-key-fact.md").read_text(encoding="utf-8"))
    assert fm["type_note"] == "legacy carryover"


def test_migrate_body_is_untouched(tmp_path):
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    _make_legacy_store(store)
    _init_git_repo(repo_root)
    _commit_all(repo_root, "initial")

    before_text = (store / "a-fact.md").read_text(encoding="utf-8")
    _, before_body = mls.split_legacy(before_text)

    mls.migrate(store, repo_root)

    after_text = (store / "a-fact.md").read_text(encoding="utf-8")
    _, after_body = mls.split_legacy(after_text)
    assert after_body == before_body


def test_migrate_handles_description_with_colon_and_trailing_quote(tmp_path):
    """The real corpus has descriptions that both contain a colon and end
    in a literal `"` — a generic quoting dumper would corrupt these on
    re-parse (see module docstring). Guard the exact shape."""
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    tricky = 'A gate must ENFORCE the default: never trust by default, unless "opted in"'
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[tricky-fact](tricky-fact.md) — placeholder."]))
    _write(store, "tricky-fact.md", _legacy_concept("tricky-fact", tricky))
    _init_git_repo(repo_root)
    _commit_all(repo_root, "initial")

    mls.migrate(store, repo_root)

    fm = lm.parse_frontmatter((store / "tricky-fact.md").read_text(encoding="utf-8"))
    assert fm["description"] == tricky


def test_migrate_missing_name_on_one_file_leaves_every_other_file_untouched(tmp_path):
    """R4: every rewrite is staged before any write, so a legacy file
    missing 'name' aborts the whole batch and leaves an earlier,
    alphabetically-sorted, valid file exactly as it was found."""
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[aaa-fact](aaa-fact.md) — First.", "[zzz-fact](zzz-fact.md) — No name."]))
    _write(store, "aaa-fact.md", _legacy_concept("aaa-fact", "First lesson."))
    _write(store, "zzz-fact.md", "---\ndescription: No name key.\ntype: gotcha\norigin: PR#1\n---\n\nBody.\n")
    _init_git_repo(repo_root)
    _commit_all(repo_root, "initial")
    before = (store / "aaa-fact.md").read_bytes()

    try:
        mls.migrate(store, repo_root)
        raised = False
    except mls.MigrationError as exc:
        raised = True
        assert "zzz-fact.md" in str(exc)
    assert raised

    assert (store / "aaa-fact.md").read_bytes() == before
    assert not (store / "index.md").exists()


def test_migrate_refuses_a_file_that_already_carries_sources(tmp_path):
    """R4: a legacy-shaped store (no `index.md`, README still has the
    `## Index` heading) whose one concept file already carries a
    `sources` key must be refused rather than re-migrated — treating an
    already-migrated file as legacy is exactly the rerun bug (a verbatim
    `origin` demoted to a stray key) this guard exists to prevent."""
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[already-migrated](already-migrated.md) — Already migrated."]))
    _write(
        store,
        "already-migrated.md",
        "---\nname: already-migrated\ndescription: Already migrated.\ntype: gotcha\n"
        "sources:\n  - resource: PR#1 verbatim\n---\n\nBody.\n",
    )
    _init_git_repo(repo_root)
    _commit_all(repo_root, "initial")
    before = (store / "already-migrated.md").read_bytes()

    with pytest.raises(mls.MigrationError) as excinfo:
        mls.migrate(store, repo_root)

    assert "already-migrated.md" in str(excinfo.value)
    assert (store / "already-migrated.md").read_bytes() == before


def test_migrate_rerun_after_a_fixed_failure_keeps_sources_and_validates_clean(tmp_path):
    """R4: recovering from a failed batch by fixing the offending file and
    re-running must produce a valid store that keeps the first file's
    verbatim `origin` as its `sources[].resource` — the rerun bug this
    guards against silently demoted that string to a stray top-level key."""
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[aaa-fact](aaa-fact.md) — First.", "[zzz-fact](zzz-fact.md) — No name."]))
    _write(store, "aaa-fact.md", _legacy_concept("aaa-fact", "First lesson.", origin="PR#1 verbatim"))
    _write(store, "zzz-fact.md", "---\ndescription: No name key.\ntype: gotcha\norigin: PR#9\n---\n\nBody.\n")
    _init_git_repo(repo_root)
    _commit_all(repo_root, "initial")

    with pytest.raises(mls.MigrationError):
        mls.migrate(store, repo_root)

    _write(store, "zzz-fact.md", _legacy_concept("zzz-fact", "Now fixed.", origin="PR#9"))
    mls.migrate(store, repo_root)

    fm = lm.parse_frontmatter((store / "aaa-fact.md").read_text(encoding="utf-8"))
    sources = fm.get("sources")
    assert isinstance(sources, list) and sources
    assert any(entry.get("resource") == "PR#1 verbatim" for entry in sources)
    assert lm.validate_bundle(store) == []


# ---------------------------------------------------------------------------
# Acceptance A5 negative: no-implicit-migration-and-no-legacy-writer
# ---------------------------------------------------------------------------


def test_migrate_refuses_an_already_migrated_store_and_writes_nothing(tmp_path):
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(
        store,
        "README.md",
        "---\nname: README\ndescription: Charter.\ntype: Memory Store Guide\n"
        'sources:\n  - resource: "commit deadbeef"\n---\n\n# Guide\n',
    )
    _write(
        store,
        "a-fact.md",
        "---\nname: a-fact\ndescription: A description.\ntype: practice\n"
        'sources:\n  - resource: "a fixture origin"\n---\n\nThe fact body.\n',
    )
    lm.regenerate_index(store)
    before = {p.name: p.read_text(encoding="utf-8") for p in store.glob("*.md")}

    assert mls.is_legacy_store(store) is False
    try:
        mls.migrate(store, repo_root)
        raised = False
    except mls.MigrationError:
        raised = True
    assert raised

    after = {p.name: p.read_text(encoding="utf-8") for p in store.glob("*.md")}
    assert after == before


def test_migrate_refuses_a_store_with_no_index_heading_and_writes_nothing(tmp_path):
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", "# Not a legacy store\n\nNo Index heading here.\n")
    _write(store, "a-fact.md", _legacy_concept("a-fact", "A description."))
    before = {p.name: p.read_text(encoding="utf-8") for p in store.glob("*.md")}

    assert mls.is_legacy_store(store) is False
    try:
        mls.migrate(store, repo_root)
        raised = False
    except mls.MigrationError:
        raised = True
    assert raised

    after = {p.name: p.read_text(encoding="utf-8") for p in store.glob("*.md")}
    assert after == before


def test_cli_refuses_and_exits_nonzero_without_writing(tmp_path):
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", "# Not a legacy store\n")
    before = (store / "README.md").read_text(encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "migrate_legacy_store.py"), str(store), "--repo-root", str(repo_root)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert (store / "README.md").read_text(encoding="utf-8") == before


def test_no_other_script_in_the_repo_reads_the_legacy_readme_indexed_shape():
    """REQ-23: the migration command is the ONLY legacy-format reader."""
    legacy_markers = ("INDEX_LINE_RE", "def parse_index_lines", "def splice_index_section", "def build_entries")
    offenders = []
    for candidate_dir in (SCRIPTS_DIR,):
        for py in candidate_dir.glob("*.py"):
            if py.name in ("migrate_legacy_store.py", "test_migrate_legacy_store.py"):
                continue
            text = py.read_text(encoding="utf-8")
            if any(marker in text for marker in legacy_markers):
                offenders.append(py.name)
    assert offenders == []


def test_legacy_validator_and_its_tests_are_retired():
    """REQ-26: no surviving `--write` path can rewrite the migrated store —
    the legacy validator script and its README-index-specific tests are
    gone entirely."""
    assert not (REPO_ROOT / "scripts" / "check_loom_memory_integrity.py").exists()
    assert not (REPO_ROOT / "scripts" / "test_check_loom_memory_integrity.py").exists()


def test_loom_memory_cli_has_no_legacy_write_subcommand():
    """`loom_memory.py`'s CLI exposes `validate` and `regenerate-index` —
    plus, since the auto-create change, `init`, which writes only the
    current profile shape from the bundled templates — and no `--write`-style
    legacy rewriting subcommand survives outside `migrate_legacy_store.py`
    (REQ-26)."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "loom_memory.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert "--write" not in result.stdout
    assert "validate" in result.stdout
    assert "regenerate-index" in result.stdout


def test_name_stem_mismatch_aborts_before_any_file_is_written(tmp_path: Path) -> None:
    """A concept whose frontmatter `name` disagrees with its filename stem is
    rejected by index regeneration, which runs at the END of migration. Checking
    it only there meant the batch had already rewritten every earlier file — the
    zero-writes-on-failure guarantee held for a missing `name` and quietly failed
    for a mismatched one. Found by the second-vendor reviewer."""
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[right-name](right-name.md) — Mismatch."]))
    _write(store, "right-name.md", _legacy_concept("wrong-name", "Mismatch."))
    _init_git_repo(repo_root)
    _commit_all(repo_root, "seed")
    before = {p.name: p.read_bytes() for p in sorted(store.glob("*.md"))}

    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "migrate_legacy_store.py"), str(store), "--repo-root", str(repo_root)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "right-name.md" in result.stdout + result.stderr
    assert {p.name: p.read_bytes() for p in sorted(store.glob("*.md"))} == before
    assert not (store / "index.md").exists()


def test_a_legacy_value_the_profile_rejects_aborts_before_any_file_is_written(tmp_path: Path) -> None:
    """The pre-write gate used to list the fields it wanted by hand, so it
    checked PRESENCE while index regeneration checked VALIDITY. A legacy
    `description:` with no value passed the gate and failed the check — after
    the batch had rewritten every earlier file, leaving a store that a rerun
    refuses because the rewritten concepts now carry `sources`. The gate now
    runs the profile's own concept check over the staged frontmatter.
    Found by the second-vendor reviewer."""
    repo_root = tmp_path / "repo"
    store = repo_root / "docs" / "loom" / "memory"
    store.mkdir(parents=True)
    _write(store, "README.md", _legacy_readme(["[x](x.md) — Empty."]))
    _write(store, "x.md", "---\nname: x\ndescription:\ntype: gotcha\norigin: fixture\n---\n\nBody.\n")
    _init_git_repo(repo_root)
    _commit_all(repo_root, "seed")
    before = {p.name: p.read_bytes() for p in sorted(store.glob("*.md"))}

    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "migrate_legacy_store.py"), str(store), "--repo-root", str(repo_root)],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "x.md" in combined and "description" in combined
    assert {p.name: p.read_bytes() for p in sorted(store.glob("*.md"))} == before
    assert not (store / "index.md").exists()
