"""One-home, gate-registration and packaging checks for Loom's shared dispatch profile.

The profile's routing wording is review-only; its behaviour is proven by
test_dispatch_profile_resolver.py and test_claude_reviewer.py.
"""

from __future__ import annotations

import shutil
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
PROFILE = PLUGIN / "references" / "dispatch-profile.md"
MECHANISMS = PLUGIN.parent / "docs" / "loom" / "evidence" / "mechanisms.yaml"
STATIONS = (
    PLUGIN / "skills" / "build" / "SKILL.md",
    PLUGIN / "skills" / "closing-review" / "SKILL.md",
)


def _contract() -> str:
    return PROFILE.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


RESOLVER_INVOCATION_PHRASES = (
    "classify the task from its evidence",
    "resolve the atomic model-and-effort profile",
    "active task context only",
    "static model or effort pin",
    "python3 <loom-code>/scripts/dispatch_profile.py",
    "pass the resolver's deterministic JSON result to the host-native spawn",
    "apply both fields from `overrides`, or apply neither when it is `null`",
    "apply the resolved overrides at invocation time",
    "feed every completed result back as an `after-execution` event before any redispatch",
    "post-execution capability-quality failure",
    "as a pre-execution host rejection",
    "selects the one atomic fallback instead of model escalation",
)


def test_stations_do_not_restate_the_resolver_invocation() -> None:
    for phrase in RESOLVER_INVOCATION_PHRASES:
        for station in STATIONS:
            flat = _flat(station.read_text(encoding="utf-8")).lower()
            assert phrase.lower() not in flat, f"{station.parent.name} restates: {phrase}"


def test_external_dispatch_gate_is_registered_with_executable_eval() -> None:
    gate_id = "review.external-dispatch"
    review = (PLUGIN / "skills" / "closing-review" / "SKILL.md").read_text(encoding="utf-8")
    mechanisms = MECHANISMS.read_text(encoding="utf-8")

    assert review.count(f"<!-- gate: {gate_id} -->") == 1
    assert review.count("<!-- /gate -->", review.find(f"<!-- gate: {gate_id} -->")) >= 1
    assert f'- id: "{gate_id}"' in mechanisms
    assert (
        "eval: loom-code/tests/test_loom_attestation.py::"
        "test_external_dispatch_gate_integrates_runner_verdict_and_attestation"
    ) in mechanisms


def test_packaged_station_reference_resolves_after_isolated_install(tmp_path: Path) -> None:
    isolated = tmp_path / "standalone-loom-code"
    shutil.copytree(PLUGIN, isolated)

    for relative in (Path("skills/build/SKILL.md"), Path("skills/closing-review/SKILL.md")):
        station = isolated / relative
        target = (station.parent / "../../references/dispatch-profile.md").resolve()
        assert target.is_relative_to(isolated.resolve())
        assert target.is_file()


def test_shared_routing_gate_is_registered_once_with_executable_eval() -> None:
    gate_id = "dispatch-profile.relative-routing"
    marker = f"<!-- gate: {gate_id} -->"
    profile = _contract()
    mechanisms = MECHANISMS.read_text(encoding="utf-8")

    assert profile.count(marker) == 1
    assert f'- id: "{gate_id}"' in mechanisms
    assert (
        "eval: loom-code/tests/test_dispatch_profile_resolver.py::"
        "test_mechanical_route_computes_each_model_tier"
    ) in mechanisms
