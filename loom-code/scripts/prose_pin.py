"""Shared negation matcher for prose-pin tests.

A test that pins a sentence of station text rejects any negation token in
that sentence (engineering baseline, prose-pin rule). One regex here, one
place to widen it: nine test modules used to carry private copies of
``\\b(?:not|never|no)\\b|n't`` and none of them caught ``cannot``,
``without`` or ``nothing`` (wave-end adversary, review-sees-complexity).

``none`` and ``nothing`` are deliberately absent: they are quantifiers
that pinned affirmative sentences use ("a reader who raised none keeps its
previous PASS"; "that one intent line, nothing more"), and the hostile
rewrites the adversary built used ``cannot`` and ``without``.

Three graduated probe copies (test_probes_language_policy.py,
test_probes_memory_step.py, test_probes_memory_step_wave_end.py) keep
their own private regex by design: they are byte copies of frozen
evidence and do not import this module.
"""
from __future__ import annotations

import re

NEGATION_RE = re.compile(
    r"\b(?:not|never|no|cannot|without|neither|nobody|nor)\b|n't",
    re.IGNORECASE,
)


def has_negation(sentence: str) -> bool:
    return bool(NEGATION_RE.search(sentence))


def split_sentences(text: str, ends: str = ".;") -> list[str]:
    """Split prose after each character of `ends` that whitespace follows.

    Callers that also treat a colon as a boundary pass ``ends=".:;"``.
    """
    pattern = rf"(?<=[{re.escape(ends)}])\s+"
    return [s for s in re.split(pattern, text) if s]
