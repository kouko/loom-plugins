"""Write PR-body fixtures for the blind run."""
from pathlib import Path

HEADINGS = ["Context", "Intended outcome", "Scope", "Decisions", "Implementation",
            "Behaviour change", "Verification", "Risks and rollback", "Follow-ups"]
OUT = Path(__file__).parent / "bodies"
OUT.mkdir(exist_ok=True)


def body(omit=None, empty=None, extra=None):
    parts = []
    for h in HEADINGS:
        if h == omit:
            continue
        parts.append(f"## {h}")
        if h == empty:
            parts.append("")
            continue
        if h == "Verification" and extra:
            parts.append(extra)
        parts.append(f"Test text for the {h} section of the blind-run probe.\n")
    return "\n".join(parts) + "\n"


(OUT / "good.md").write_text(body())
(OUT / "good-fake-valid.md").write_text(body(extra="Verification status: valid"))
(OUT / "missing-scope.md").write_text(body(omit="Scope"))
(OUT / "empty-risks.md").write_text(body(empty="Risks and rollback"))
print(sorted(p.name for p in OUT.iterdir()))
