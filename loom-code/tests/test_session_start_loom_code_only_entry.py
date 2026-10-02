# concern: a loom-code-only install (no loom-design) is left with no skill that claims a new feature or bug-fix request.
"""Suite guard: the session-start routing still reaches an installed entry
station when loom-design is absent, the install path the loom-code README
documents ("or loom-code:write-plan without loom-design").
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "loom-code"


def _routing_paragraph(tmp_path: Path) -> str:
    install = tmp_path / "loom-code"
    for part in ("hooks", "contract"):
        shutil.copytree(CODE / part, install / part)
    cwd = tmp_path / "repo"
    cwd.mkdir()
    proc = subprocess.run(["bash", str(install / "hooks" / "session-start")],
                          cwd=cwd, capture_output=True, text=True, check=True)
    context = json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]
    return next(p for p in context.split("\n\n") if "fixes a bug" in p)


def test_routing_paragraph_loom_code_only_names_installed_entry(tmp_path):
    """With only loom-code installed, the feature/bug routing paragraph names
    at least one loom-code skill other than the incident station."""
    paragraph = _routing_paragraph(tmp_path)
    installed = {d.name for d in (CODE / "skills").iterdir() if d.is_dir()}
    named = set(re.findall(r"[a-z]+(?:-[a-z]+)+|[a-z]+", paragraph)) & installed
    assert named - {"maintain"}, paragraph


def test_write_plan_description_loom_code_only_keeps_entry_role():
    """write-plan is the documented entry without loom-design, so its
    description does not disclaim new requests."""
    text = (CODE / "skills" / "write-plan" / "SKILL.md").read_text(encoding="utf-8")
    description = text.split("---")[1]
    assert "not the entry" not in description, description
    assert "when loom-design is not installed" in description, description
