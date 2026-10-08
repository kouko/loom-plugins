#!/usr/bin/env python3
"""Resolve one host-neutral second-vendor suggestion decision."""
from __future__ import annotations

import json
import sys
from typing import Any


VENDORS = ("claude", "codex", "gemini")
EXECUTORS = ("claude", "codex", "agy")
MODES = {"ask", "suggest", "fixed"}
RESPONSES = {"pending", "decline", "accept"}
RISK_SIGNALS = (
    "security-or-privacy-boundary",
    "public-contract-or-persistent-format",
    "cross-system-or-provider-integration",
    "review-verification-or-publication-mechanism",
    "critical-behavior-not-fully-automated",
    "irreversible-data-or-architecture",
)


class InputError(ValueError):
    """The observed-state packet is malformed or contradictory."""


def _result(
    *,
    notice_kind: str = "no-notice",
    reason_code: str,
    effective_vendor: str | None = None,
    notice_vendor: str | None = None,
    reasons: list[dict[str, object]] | None = None,
    eligible: bool = False,
) -> dict[str, object]:
    # This shared result shape is interpreted only by suggest callers. Ask and
    # fixed orchestration ignore its notice, eligibility, and waiting fields.
    return {
        "effective_vendor": effective_vendor,
        "notice_vendor": notice_vendor,
        "notice_kind": notice_kind,
        "recommendation_reasons": reasons or [],
        "opt_in_eligible": eligible,
        "wait_for_user": False,
        "reason_code": reason_code,
    }


def _require_string(value: object, name: str, allowed: set[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise InputError(f"{name} must be one of {', '.join(sorted(allowed))}")
    return value


def _model_vendor(model: str) -> str | None:
    name = model.lower()
    if name.startswith(("claude-", "anthropic/")) or name in {"opus", "sonnet", "haiku"}:
        return "claude"
    if name.startswith(("gpt-", "openai/", "o3", "o4")):
        return "codex"
    if name.startswith(("gemini-", "google/")):
        return "gemini"
    return None


def _vendors(value: object, host_vendor: str) -> tuple[list[str], dict[str, dict[str, str]], list[str]]:
    if not isinstance(value, list):
        raise InputError("usable_vendors must be an array")
    if all(isinstance(item, str) for item in value):
        if any(item not in VENDORS for item in value):
            raise InputError("usable_vendors must contain known vendors")
        if len(value) != len(set(value)):
            raise InputError("usable_vendors must be unique")
        if host_vendor in value:
            raise InputError("usable_vendors must exclude host_vendor")
        return [vendor for vendor in VENDORS if vendor in value], {}, []
    if any(not isinstance(item, dict) or set(item) not in
           ({"executor"}, {"executor", "model", "vendor"})
           for item in value):
        raise InputError("usable_vendors candidates need executor or executor, model, vendor")
    candidates: dict[str, dict[str, str]] = {}
    unverified: list[str] = []
    for item in value:
        if set(item) == {"executor"}:
            executor = item["executor"]
            if executor not in EXECUTORS or executor in unverified:
                raise InputError("usable_vendors unverified executor is invalid or duplicate")
            unverified.append(executor)
            continue
        executor, model, vendor = item["executor"], item["model"], item["vendor"]
        if executor not in EXECUTORS or not isinstance(model, str) or not model.strip():
            raise InputError("usable_vendors candidate executor or model is invalid")
        if vendor not in VENDORS or _model_vendor(model) != vendor:
            raise InputError("usable_vendors candidate model family is unknown or mismatched")
        if vendor == host_vendor:
            continue
        key = (EXECUTORS.index(executor), model)
        previous = candidates.get(vendor)
        if previous is None or key < (EXECUTORS.index(previous["executor"]), previous["model"]):
            candidates[vendor] = {"executor": executor, "model": model}
    return ([vendor for vendor in VENDORS if vendor in candidates], candidates,
            [executor for executor in EXECUTORS if executor in unverified])


def _risks(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise InputError("risk_evidence must be an array")
    by_signal: dict[str, dict[str, object]] = {}
    for item in value:
        if not isinstance(item, dict) or set(item) != {"signal", "anchors"}:
            raise InputError("risk evidence must contain exactly signal and anchors")
        signal = item["signal"]
        anchors = item["anchors"]
        if signal not in RISK_SIGNALS:
            raise InputError("risk evidence contains an unknown signal")
        if signal in by_signal:
            raise InputError("risk evidence signals must be unique")
        if (
            not isinstance(anchors, list)
            or not anchors
            or any(
                not isinstance(anchor, str)
                or " :: " not in anchor
                or not all(part.strip() for part in anchor.split(" :: ", 1))
                for anchor in anchors
            )
            or len(anchors) != len(set(anchors))
        ):
            raise InputError("risk evidence anchors must be unique path :: anchor strings")
        by_signal[signal] = {"signal": signal, "anchors": anchors.copy()}
    return [by_signal[signal] for signal in RISK_SIGNALS if signal in by_signal]


def resolve(packet: dict[str, Any]) -> dict[str, object]:
    """Resolve one decision without I/O, persistence, or provider execution."""
    if not isinstance(packet, dict):
        raise InputError("input must be an object")
    allowed = {
        "contract_version", "configured_mode", "fixed_vendor", "host_vendor",
        "usable_vendors", "risk_evidence", "review_started",
        "response", "response_vendor",
    }
    if set(packet) - allowed:
        raise InputError("input contains unknown fields")
    if packet.get("contract_version") != 1 or type(packet.get("contract_version")) is not int:
        raise InputError("contract_version must be integer 1")
    mode = _require_string(packet.get("configured_mode"), "configured_mode", MODES)
    host_vendor = _require_string(packet.get("host_vendor"), "host_vendor", set(VENDORS))
    response = _require_string(packet.get("response"), "response", RESPONSES)
    review_started = packet.get("review_started")
    if type(review_started) is not bool:
        raise InputError("review_started must be a boolean")
    vendors, candidates, unverified = _vendors(packet.get("usable_vendors"), host_vendor)
    risks = _risks(packet.get("risk_evidence"))

    fixed_vendor = packet.get("fixed_vendor")
    if mode == "fixed":
        _require_string(fixed_vendor, "fixed_vendor", set(VENDORS))
    elif fixed_vendor is not None:
        raise InputError("fixed_vendor is valid only for fixed mode")

    response_vendor = packet.get("response_vendor")
    if response == "accept":
        if response_vendor is None:
            if vendors or not unverified:
                raise InputError("response_vendor required unless only an unverified executor is available")
        else:
            accepted = _require_string(response_vendor, "response_vendor", set(VENDORS))
            if accepted not in vendors:
                raise InputError("response_vendor must identify a usable vendor")
    elif response_vendor is not None:
        raise InputError("response_vendor is valid only for accept")

    def with_candidate(result: dict[str, object], vendor: str | None,
                       *, effective: bool = False) -> dict[str, object]:
        if candidates and vendor is not None:
            prefix = "effective" if effective else "notice"
            result[f"{prefix}_executor"] = candidates[vendor]["executor"]
            result[f"{prefix}_model"] = candidates[vendor]["model"]
        return result

    if mode != "suggest":
        return _result(reason_code="mode-not-suggest")
    if not vendors and unverified:
        if response == "decline":
            return _result(reason_code="selection-declined")
        if review_started:
            if response == "accept":
                return _result(notice_kind="next-change-only",
                               reason_code="response-too-late")
            return _result(reason_code="no-response")
        if response == "accept":
            result = _result(notice_kind="discovery-authorized",
                             reason_code="model-discovery-authorized")
            result["effective_executor"] = unverified[0]
            result["allowed_vendors"] = [vendor for vendor in VENDORS
                                         if vendor != host_vendor]
            return result
        result = _result(notice_kind="availability-unverified", eligible=True,
                         reason_code="model-family-unverified")
        result["notice_executor"] = unverified[0]
        return result
    if not vendors:
        return _result(reason_code="no-usable-vendor")

    candidate = vendors[0]
    if response == "accept":
        if review_started:
            return with_candidate(_result(
                notice_kind="next-change-only",
                notice_vendor=response_vendor,
                reason_code="response-too-late",
            ), response_vendor)
        return with_candidate(_result(
            notice_kind="selection-confirmed",
            effective_vendor=response_vendor,
            notice_vendor=response_vendor,
            reason_code="selection-accepted",
        ), response_vendor, effective=True)
    if response == "decline":
        return _result(reason_code="selection-declined")
    if review_started:
        return _result(reason_code="no-response")
    if risks:
        return with_candidate(_result(
            notice_kind="recommendation",
            notice_vendor=candidate,
            reasons=risks,
            eligible=True,
            reason_code="risk-recommendation",
        ), candidate)
    return with_candidate(_result(
        notice_kind="availability",
        notice_vendor=candidate,
        eligible=True,
        reason_code="availability",
    ), candidate)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        result = resolve(payload)
    except (json.JSONDecodeError, InputError) as exc:
        print(f"second-vendor-policy: {exc}", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
