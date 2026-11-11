# Independent synthetic task sources

These are synthetic fixture inputs, not claims about real users or production.
Date: 2026-11-12. Scope: bounded analysis; no installation, publication or product edits.

F1: Choose a local ZIP-writing integration for a one-file export. Mandatory:
already installed tools, one ordinary UTF-8 text member named receipt.txt,
round-trip readable content. Prefer fewer subprocess boundaries. Candidates:
existing /usr/bin/zip subprocess or Python standard-library zipfile. Overall
integration is a local export; the material nested tool choice is independent.
No speed or universal compatibility requirement. A recommendation is requested,
not authorization to implement the product.

D1: Synthetic observation: three keyboard-only operators lost draft edits when
a confirmation dialog moved focus away from the edited row. Synthetic interview:
one operator preferred modal confirmations because they felt safer. Goal already
confirmed: prevent accidental removal while preserving keyboard work. Options:
modal confirmation, reversible inline undo, current immediate removal.
Mandatory: recovery without a pointer; unknown: screen-reader announcement quality.
D2: User explicitly chose reversible inline undo; supplied keyboard walkthrough
shows focused undo restores the draft. Do not reopen the preference.
D3: Architecture choice: local-only export ownership versus remote service.
User requires local-only data. Nested question: does installed zip support stdin?

C1 planning: proposed ZIP dependency is claimed unavailable; installed tools may
contradict this. Decide whether dependency installation is required.
C2 build: two failures are reported as missing zip; receipt says exit 12,
"Nothing to do". Distinguish absent executable from empty input.
C3 review: author says export test passed; only test definition exists, no run log.
C4 ship: source contains a release workflow; no remote publication/check observation.
C5 maintain: alert says export executable disappeared; current path may contradict
the report. Establish present capability, not historical cause; no fix authorized.
N1-N5: same stages, but current applicable receipt already records installed tool,
successful round-trip, actual test output, observed check success, and bounded
incident diagnosis respectively. No new contradictory fact or pending gap.
Immaterial fact: spelling of a sample filename does not change tool choice.
