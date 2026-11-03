# concern: A new override-free retry must not claim inheritance after the host withdraws its guarantee.
"""Distinguish the completed attempt's profile from the next dispatch's guarantee."""

import importlib.util
from pathlib import Path


def test_retry_lostinheritance_unverified():
    """Retain past success truth while recording a new retry under current host guarantees."""
    root = next(
        parent for parent in Path(__file__).resolve().parents
        if (parent / "loom-code/scripts/dispatch_profile.py").is_file()
    )
    spec = importlib.util.spec_from_file_location(
        "retry_inheritance_resolver", root / "loom-code/scripts/dispatch_profile.py"
    )
    resolver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resolver)
    initial = resolver.resolve({
        "event": "initial",
        "main_profile": {"model": None, "effort": None},
        "capabilities": {},
        "inheritance_guaranteed": True,
        "completed_redispatches": 0,
    })
    assert initial["effective_profile"] == "inherited"
    feedback = {
        "event": "after-execution",
        "capabilities": {},
        "inheritance_guaranteed": False,
        "completed_redispatches": 0,
        "last_attempt": {
            "completed": True, "success": True, "conforming": True,
            "profile": initial["effective_profile"],
        },
    }
    completed = resolver.resolve(feedback)
    assert completed["outcome"] == "routed"
    assert completed["effective_profile"] == "inherited"
    feedback["last_attempt"].update(
        success=False, conforming=False, failure_kind="malformed-response"
    )
    retry = resolver.resolve(feedback)
    assert retry["outcome"] == "dispatch"
    assert retry["overrides"] is None
    assert retry["completed_redispatches"] == 0
    assert retry["next_redispatch"] == 1
    assert retry["effective_profile"] == "host-default/unverified"
