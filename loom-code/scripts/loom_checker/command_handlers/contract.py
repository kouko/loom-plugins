from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import load_manifest
from loom_checker.preparation_output import report_result
from loom_checker.rule_checks.contract import check_contract_requires
from loom_checker.rule_checks.contract import parse_required_version
import sys


def cmd_contract(args: list[str], out=sys.stdout, err=sys.stderr, *, result=None) -> int:
    """`loom_checker.py contract --require <major>.<minor>` -- the check
    loom-design and loom-workflow run at station start (concept-model §1).
    Same major and a high enough minor passes; anything else blocks with the
    one instruction the user can act on."""
    required = None
    rest = list(args)
    while rest:
        token = rest.pop(0)
        if token != "--require":
            raise UsageError(f"unexpected argument {token!r}.")
        if not rest:
            raise UsageError("--require needs a <major>.<minor> version.")
        required = rest.pop(0)
    if required is None:
        raise UsageError("contract needs `--require <major>.<minor>`.")
    parse_required_version(required)
    version = str(load_manifest().get("version", "")).strip()
    failures = check_contract_requires(version, required)
    if result is not None:
        result["data"].update(contract_version=version, required_version=required, compatible=not failures)
        return report_result(failures, err, result)
    if failures:
        return report_result(failures, err, None)
    out.write(f"contract {version} satisfies requires-contract >={required}\n")
    return 0
