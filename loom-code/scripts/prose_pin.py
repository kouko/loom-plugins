"""Shared readers and matchers for prose-pin tests.

A test that pins a sentence of station text rejects any negation token in
that sentence (engineering baseline, prose-pin rule). One regex here, one
place to widen it: nine test modules used to carry private copies of
``\\b(?:not|never|no)\\b|n't`` and none of them caught ``cannot``,
``without`` or ``nothing`` (wave-end adversary, review-sees-complexity).

``none`` and ``nothing`` are deliberately absent: they are quantifiers
that pinned affirmative sentences use ("a reader who raised none keeps its
previous PASS"; "that one intent line, nothing more"), and the hostile
rewrites the adversary built used ``cannot`` and ``without``.

The readers below joined it for the same reason: `flat_prose`, `rule_prose`,
`affirms` and `pins_exact_sentence` stood as byte-identical private copies,
docstring included, in the protocol's test module, in each recipe's, and in
`test_build_mechanical_checks.py`. Widening any of them meant finding all
five.

Three graduated probe copies (test_probes_language_policy.py,
test_probes_memory_step.py, test_probes_memory_step_wave_end.py) keep
their own private regex by design: they are byte copies of frozen
evidence and do not import this module.
"""
from __future__ import annotations

import re
from pathlib import Path

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


def flat_prose(path: Path) -> str:
    """The file's text, flattened, with any blockquote marker stripped."""
    return " ".join(re.sub(r"^> ?", "", path.read_text(encoding="utf-8"), flags=re.M).split())


def rule_prose(path: Path) -> str:
    """The file's prose, flattened, with its heading lines dropped.

    A heading is structure, not a rule, and `test_adversary_layout.py` owns
    it. Left in, it would be swept into the first sentence after it and a
    rename would break a pin that is not about names.
    """
    text = re.sub(r"^#{1,6} .*$", "", path.read_text(encoding="utf-8"), flags=re.M)
    return " ".join(re.sub(r"^> ?", "", text, flags=re.M).split())


def affirms(text: str, verb: str, literal: str, *extras: str) -> bool:
    """Some sentence carries `verb` before `literal`, every extra, and no negation."""
    for sentence in split_sentences(text):
        v, lit = sentence.find(verb), sentence.find(literal)
        if 0 <= v < lit and all(e in sentence for e in extras) and not has_negation(sentence):
            return True
    return False


def pins_exact_sentence(text: str, sentence: str) -> bool:
    """`text` states `sentence` exactly once, as a sentence of its own."""
    return split_sentences(text).count(sentence) == 1
