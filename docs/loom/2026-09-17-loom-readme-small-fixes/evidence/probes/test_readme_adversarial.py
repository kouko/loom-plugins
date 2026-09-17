"""Adversarial probes for change 2026-09-17-loom-readme-small-fixes.

Run: python3 -m pytest docs/loom/2026-09-17-loom-readme-small-fixes/evidence/probes/test_readme_adversarial.py -q
"""
import re
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[5]
README = REPO / "docs" / "loom" / "README.md"

NEGATIONS = re.compile(r"\b(no|not|never|nor|none|neither|n't|cannot)\b|n't", re.I)
AFFIRM = re.compile(r"\bThe old plans (stay|remain)\b")


def _text():
    return README.read_text(encoding="utf-8")


def _links(text):
    """Every link form: inline (with optional title/angle brackets), reference definitions, HTML href/src."""
    out = []
    for m in re.finditer(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)", text):
        out.append(m.group(1))
    out += re.findall(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)", text, re.M)
    out += re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", text)
    return out


def _sentence_after_history(text):
    flat = re.sub(r"\s+", " ", text)
    tail = flat.split("survive only in git history.", 1)[1].strip()
    return re.split(r"(?<=[.!?])\s", tail, 1)[0]


def _pins_affirmative(sentence):
    # Negation is checked in the pinned clause (up to "because" or a dash);
    # the product sentence's later "but no station reads them" is a separate clause.
    clause = re.split(r"\s(?:because|—|--)\s", sentence, 1)[0]
    return bool(AFFIRM.search(clause)) and not NEGATIONS.search(clause)


def test_pinSelfcheck_affirmativeExample_accepted():
    assert _pins_affirmative("The old plans stay in the tree because they are useful.")


def test_pinSelfcheck_negatedExample_rejected():
    assert not _pins_affirmative("The old plans never stay in the tree.")


def test_historySentence_nextSentence_affirmsOldPlansWithoutNegation():
    """A1: the next sentence names old plans as staying, and no negation reverses it."""
    assert _pins_affirmative(_sentence_after_history(_text()))


def test_readmeLinks_everyLinkForm_resolvesInsideRepo():
    """A2: all relative links of any Markdown/HTML form exist and do not escape the repository."""
    links = _links(_text())
    assert links, "link extraction found nothing"
    for target in links:
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
            continue
        path = (README.parent / unquote(target.split("#")[0])).resolve()
        assert path.exists(), target
        assert path == REPO or REPO in path.parents, target


def test_mapsStore_anyLinkSpelling_notLinked():
    """A2 near-miss: maps/ must not be linked via ./maps, maps (no slash) or a docs/loom/maps path."""
    for target in _links(_text()):
        norm = (README.parent / unquote(target.split("#")[0])).resolve()
        assert norm != (README.parent / "maps").resolve(), target


def test_mapsStore_tableAndTypeMapping_stillNamed():
    """A3: maps/ keeps its store row and its docs/loom/maps/** type mapping."""
    text = _text()
    rows = [l for l in text.splitlines() if re.match(r"^\|\s*`maps/`\s*\|", l)]
    assert len(rows) == 1 and "decision maps" in rows[0]
    assert "decision-map" in rows[0]
    assert "docs/loom/maps/" in text
