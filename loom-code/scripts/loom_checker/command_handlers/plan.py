from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import read_text
from loom_checker.preparation_output import error_result, report_result
from loom_checker.rule_checks.intake import check_plan_field_caps
from pathlib import Path
import sys


def cmd_plan(args: list[str], out=sys.stdout, err=sys.stderr, *, result=None) -> int:
    """`loom_checker.py plan <path>` -- runs `plan.field-caps` (and any other
    `plan.*` rule) against one plan file directly, independent of a
    change-id -- the shape the `plan` subcommand's own tests and the
    write-plan / push callers both rely on. This is a raw-content check on
    whatever file `<path>` names, by design: `plan-edits` and `push`
    instead resolve and read the canonical `docs/loom/<change-id>/plan.md`
    for that change-id."""
    if not args:
        raise UsageError("plan needs a path.")
    if len(args) > 1:
        raise UsageError(f"unexpected argument {args[1]!r}.")
    path = Path(args[0])
    if not path.is_file():
        if result is not None:
            error_result(result, "usage", f"no such plan file: {path}")
            return 2
        err.write(f"no such plan file: {path}\n")
        return 2
    try:
        text = read_text(path)
    except OSError as exc:
        if result is not None:
            error_result(result, "usage", f"cannot read plan file {path}: {exc}")
            return 2
        err.write(f"cannot read plan file {path}: {exc}\n")
        return 2
    return report_result(check_plan_field_caps(text), err, result)
