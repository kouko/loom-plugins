# concern: the Record-section digest guard must not be defeatable by a
# duplicate `### Record` heading planted earlier in SKILL.md — the guard's
# `_section()` helper takes the FIRST heading match, so a decoy carrying the
# original text keeps the sha256 pin green while the real Record section is
# softened. A dilution rewrite that stays green is the exact defect this
# change's eval guard exists to stop.
"""Adversarial probe — the Record-section digest guard accepts a softening
rewrite when a decoy `### Record` heading precedes the real section.

The guard test `test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against`
hashes the whitespace-flattened body of the *first* heading named ``Record``.
This probe plants an earlier `### Record` heading whose body is the original
Record section verbatim, then softens the real Record section (the init step
becomes "ask the user to hand-create the store"). It then runs the real guard
test against the mutated SKILL.md and requires the guard to go RED.

RED today: the guard reads the decoy, matches the pinned digest, and stays
green — the probe's assertion fails.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[5]
SKILL_REL = "loom-workflow/skills/loom-memory/SKILL.md"
CONTRACT_TEST = (
    "loom-workflow/tests/loom-memory/test_skill_contract.py"
    "::test_record_section_matches_the_digest_the_cold_reader_eval_was_run_against"
)

SOFTEN_FROM = "run the creation subcommand"
SOFTEN_TO = "ask the user to hand-create the store"
TEMPLATE_CLAUSE_FROM = "from the bundled templates and refuses an existing populated store"
TEMPLATE_CLAUSE_TO = "— templates optional, agent hand-copying is fine"


def _extract_head(dest: pathlib.Path) -> None:
    """A clean-tree copy of HEAD so the guard's real code is exercised."""
    archive = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "archive", "HEAD"],
        capture_output=True,
        check=True,
    ).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)


def _mutate_skill(text: str) -> str:
    """Plant a decoy `### Record` heading with the original body, then soften
    the real Record section below it."""
    real_pos = text.index("### Record")
    orig_section = text[real_pos:]
    # body of the real section runs up to the next same-level heading
    later = re.compile(r"^#{1,3}\s+\S", re.MULTILINE).search(orig_section, pos=len("### Record"))
    orig_body = orig_section[len("### Record") : later.start()] if later else orig_section
    decoy = "\n### Record\n" + orig_body.lstrip("\n")
    prefix, rest = text[:real_pos], text[real_pos:]
    assert SOFTEN_FROM in rest, "expected the init step wording in the real Record section"
    rest_soft = rest.replace(SOFTEN_FROM, SOFTEN_TO)
    assert TEMPLATE_CLAUSE_FROM in rest_soft, "expected the bundled-templates clause"
    rest_soft = rest_soft.replace(TEMPLATE_CLAUSE_FROM, TEMPLATE_CLAUSE_TO)
    return prefix + decoy + rest_soft


def test_digest_guard_decoy_bypass_red() -> None:
    """Digest guard: a decoy-heading softening rewrite must turn the guard
    red; the guard stays green today, so this probe is RED."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="loom-adv-a-"))
    try:
        _extract_head(tmp)
        skill = tmp / SKILL_REL
        mutated = _mutate_skill(skill.read_text(encoding="utf-8"))
        # the softening must really be in the second (real) Record section
        second = mutated[mutated.index("### Record", mutated.index("### Record") + 1) :]
        assert SOFTEN_TO in second, "probe precondition: real Record section not softened"
        skill.write_text(mutated, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(tmp / CONTRACT_TEST), "-q"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1, (
            "the digest guard accepted a softened Record section behind a decoy "
            f"heading (pytest exit {result.returncode}, stderr: {result.stderr[-500:]})"
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
