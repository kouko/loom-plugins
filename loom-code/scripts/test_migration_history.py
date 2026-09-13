from pathlib import Path

import _migration_history as history


def _repo_with_map(tmp_path: Path) -> Path:
    path = tmp_path / "repo"
    (path / "docs/migration").mkdir(parents=True)
    (path / "docs/migration/commit-map.tsv").write_text(
        "old new\n" + "a" * 40 + " " + "b" * 40 + "\n"
    )
    return path


def test_mapped_revision_is_used_when_rewritten_object_exists(tmp_path, monkeypatch):
    repo = _repo_with_map(tmp_path)
    monkeypatch.setattr(history, "_object_exists", lambda _repo, revision: revision == "b" * 40)
    assert history.migration_git_args(repo, ("git", "show", "a" * 40))[-1] == "b" * 40


def test_source_revision_is_used_when_rewritten_object_is_missing(tmp_path, monkeypatch):
    repo = _repo_with_map(tmp_path)
    monkeypatch.setattr(history, "_object_exists", lambda *_: False)
    assert history.migration_git_args(repo, ("git", "show", "a" * 40))[-1] == "a" * 40
