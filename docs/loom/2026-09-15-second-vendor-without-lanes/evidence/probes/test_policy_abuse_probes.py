"""Adversarial probes for the lane-free second-vendor policy.

Run from the repo root:

    python3 -m pytest -q -p no:cacheprovider \
        docs/loom/2026-09-15-second-vendor-without-lanes/evidence/probes/test_policy_abuse_probes.py

Every case here asserts the SAFE behaviour and is expected to PASS; each one
is an attack the change survived. Classes: empty/absent, boundary, hostile
input, wrong order / forgotten state, failing dependency (undecodable stdin).
"""
from __future__ import annotations

import copy
import itertools
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "loom-code" / "scripts"
SCRIPT = SCRIPTS / "second_vendor_policy.py"
sys.path.insert(0, str(SCRIPTS))

import second_vendor_policy as policy  # noqa: E402

VENDORS = ("claude", "codex", "gemini")


def packet(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "contract_version": 1,
        "configured_mode": "suggest",
        "host_vendor": "codex",
        "usable_vendors": ["claude", "gemini"],
        "risk_evidence": [],
        "review_started": False,
        "response": "pending",
    }
    value.update(overrides)
    return value


def risk(signal: str, *anchors: str) -> dict[str, object]:
    return {"signal": signal, "anchors": list(anchors)}


def run_cli(stdin: bytes) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, str(SCRIPT)], input=stdin, capture_output=True, check=False,
    )


# --- Acceptance 1: same change, same reviewers, same result -----------------

def test_resolve_permutedCallerOrder_identicalResult() -> None:
    """Caller-side ordering of vendors and risk items never changes the decision."""
    items = [
        risk("irreversible-data-or-architecture", "plan.md :: a"),
        risk("security-or-privacy-boundary", "intent.md :: b"),
        risk("public-contract-or-persistent-format", "spec.md :: c"),
    ]
    results = {
        json.dumps(
            policy.resolve(packet(usable_vendors=list(vs), risk_evidence=list(rs))),
            sort_keys=True,
        )
        for vs in itertools.permutations(["claude", "gemini"])
        for rs in itertools.permutations(items)
    }
    assert len(results) == 1


def test_resolve_callerMutatesResultBetweenRuns_secondRunUnaffected() -> None:
    """Forgotten state: mutating a returned result or the input packet leaks nowhere."""
    evidence = [risk("security-or-privacy-boundary", "intent.md :: privacy")]
    source = packet(risk_evidence=evidence)
    pristine = copy.deepcopy(source)
    first = policy.resolve(source)
    first["recommendation_reasons"][0]["anchors"].append("x :: y")
    evidence[0]["anchors"].append("mutated :: after")
    assert policy.resolve(pristine) == policy.resolve(copy.deepcopy(pristine))
    assert policy.resolve(pristine)["recommendation_reasons"] == [
        {"signal": "security-or-privacy-boundary", "anchors": ["intent.md :: privacy"]}
    ]


# --- Acceptance 3: every change is offered the opt-in ------------------------

def _subsets(seq):
    return itertools.chain.from_iterable(itertools.combinations(seq, n) for n in range(len(seq) + 1))


def test_resolve_everyPendingSuggestPacketWithAVendor_optInEligible() -> None:
    """Exhaustive: host x vendor subset x risk subset, pending and not started."""
    checked = 0
    for host in VENDORS:
        others = [v for v in VENDORS if v != host]
        for vendors in _subsets(others):
            if not vendors:
                continue
            for signals in _subsets(policy.RISK_SIGNALS[:3]):
                evidence = [risk(s, f"plan.md :: {s}") for s in signals]
                result = policy.resolve(packet(
                    host_vendor=host, usable_vendors=list(vendors), risk_evidence=evidence,
                ))
                assert result["opt_in_eligible"] is True, (host, vendors, signals)
                assert result["wait_for_user"] is False
                assert result["notice_vendor"] == vendors[0]
                assert result["notice_kind"] == ("recommendation" if signals else "availability")
                checked += 1
    assert checked == 3 * 3 * 8


def test_resolve_acceptNonFirstUsableVendor_selectsThatVendor() -> None:
    """Boundary: the user picks the second candidate, not the one the notice named."""
    result = policy.resolve(packet(response="accept", response_vendor="gemini"))
    assert result["effective_vendor"] == "gemini"
    assert result["notice_kind"] == "selection-confirmed"


# --- Hostile input: a stale caller still smuggling a lane --------------------

@pytest.mark.parametrize("value", [None, "", "small", "full", 0, False, ["small"]])
def test_resolve_laneKeyAnyValue_rejectedAsUnknown(value: object) -> None:
    with pytest.raises(policy.InputError, match="unknown fields"):
        policy.resolve(packet(lane=value))


@pytest.mark.parametrize("key", ["Lane", "LANE", "lane ", "default-lane"])
def test_resolve_laneKeySpellingVariant_rejectedAsUnknown(key: str) -> None:
    with pytest.raises(policy.InputError, match="unknown fields"):
        policy.resolve(packet(**{key: "small"}))


def test_resolve_laneInsideRiskItem_rejected() -> None:
    item = {"signal": "security-or-privacy-boundary", "anchors": ["a :: b"], "lane": "small"}
    with pytest.raises(policy.InputError):
        policy.resolve(packet(risk_evidence=[item]))


@pytest.mark.parametrize(
    "overrides",
    [
        {"contract_version": True},
        {"contract_version": 1.0},
        {"review_started": 0},
        {"review_started": "false"},
        {"host_vendor": "clаude"},              # Cyrillic a
        {"usable_vendors": ["Claude"]},
        {"usable_vendors": "claude"},
        {"usable_vendors": [["claude"]]},
        {"response": "accept", "response_vendor": "codex"},   # host vendor
        {"response_vendor": "claude"},                 # vendor without accept
        {"fixed_vendor": "claude"},                    # fixed vendor in suggest
        {"risk_evidence": [risk("security-or-privacy-boundary", " :: x")]},
        {"risk_evidence": [risk("security-or-privacy-boundary", "x :: ")]},
        {"risk_evidence": [risk("security-or-privacy-boundary", "x ::y")]},
        {"risk_evidence": [risk("security-or-privacy-boundary", "a :: b", "a :: b")]},
        {"risk_evidence": [risk("security-or-privacy-boundary", "a :: b")] * 2},
        {"risk_evidence": {"signal": "security-or-privacy-boundary"}},
    ],
)
def test_resolve_hostilePacket_rejected(overrides: dict[str, object]) -> None:
    with pytest.raises(policy.InputError):
        policy.resolve(packet(**overrides))


def test_resolve_hugeRiskAnchorList_resolvesCanonically() -> None:
    anchors = [f"plan.md :: row-{i}" for i in range(20000)]
    result = policy.resolve(packet(risk_evidence=[risk("security-or-privacy-boundary", *anchors)]))
    assert result["recommendation_reasons"][0]["anchors"] == anchors


# --- Empty/absent and CLI failure paths ---------------------------------------

@pytest.mark.parametrize("stdin", [b"", b"[]", b"null", b"{}"])
def test_cli_emptyOrNonObjectStdin_exitsTwoWithNoResult(stdin: bytes) -> None:
    proc = run_cli(stdin)
    assert proc.returncode == 2
    assert proc.stdout == b""
    assert proc.stderr.startswith(b"second-vendor-policy: ")


def test_cli_staleCallerSendsLane_exitsTwoLoudly() -> None:
    proc = run_cli(json.dumps(packet(lane="small")).encode())
    assert proc.returncode == 2 and proc.stdout == b""
    assert b"unknown fields" in proc.stderr


def test_cli_undecodableStdin_failsLoudlyWithoutResult() -> None:
    """Failing dependency: a non-UTF-8 pipe must never yield a decision on stdout."""
    proc = run_cli(b"\xff\xfe{")
    assert proc.returncode != 0
    assert proc.stdout == b""
