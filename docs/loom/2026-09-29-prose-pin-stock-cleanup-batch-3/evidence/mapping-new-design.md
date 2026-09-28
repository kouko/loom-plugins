# W1-06 mapping — newly flagged loom-design files

Defect class: a sentence pin against `design-system/references/knowledge-triage.md` or
`product-principles/SKILL.md` — an assert that passes only while one literal phrase of
runtime prose keeps its exact wording, including a lookup by `.index()` the census
detector does not see. Files: `loom-design/tests/interface/test_knowledge_triage.py`,
`loom-design/tests/principles/test_principles_ratified_line.py`. "Lens" means
`loom-code/skills/closing-review/references/lenses.md`.

| file::function(s) | defect class it guarded | named replacement | kind |
|---|---|---|---|
| `test_knowledge_triage.py::test_triage_names_shaping_and_deferrable_tiers` (pruned: `"flow structure"`, `"state machine"`, `"semantic display convention"`, `"color semantic"`, `"sign convention"`, `"period definition"`) | knowledge-triage.md drops or rewords one of the shaping criteria or its worked examples | skill lens `omission`; the same function keeps the SHAPING/DEFERRABLE tier-label presence checks | review lens dimension |
| `test_knowledge_triage.py::test_shaping_supplement_present_verbatim` (deleted, with the `SHAPING_SUPPLEMENT` constant) | knowledge-triage.md drops the SHAPING-never-ships-non-blocking supplement sentence | skill lens `omission` | review lens dimension |
| `test_knowledge_triage.py::test_shaping_supplement_after_pin_never_inside` (deleted: located `SHAPING_SUPPLEMENT` by `.index()`, a pin form the detector does not see) | the supplement sentence moves before or inside the pin fence | skill lens `inconsistency` (fence-vs-supplement ordering) | review lens dimension |
| `test_knowledge_triage.py::test_tier_label_supplement_present_verbatim` (deleted, with the `TIER_LABEL_SUPPLEMENT` constant) | knowledge-triage.md drops the literal-SHAPING/DEFERRABLE-label-on-every-open-question supplement sentence | skill lens `omission` | review lens dimension |
| `test_knowledge_triage.py::test_tier_label_supplement_after_first_supplement` (deleted: located both supplements by `.index()`, a pin form the detector does not see) | the tier-label supplement moves before the SHAPING supplement | skill lens `inconsistency` (supplement ordering) | review lens dimension |
| `test_principles_ratified_line.py::test_interview_template_path_is_referenced` (pruned: `"the interview is the same one"`) | PRINCIPLES SKILL.md stops saying the interview it points to is the very one it references, and starts copying its content in | skill lens `omission`; the same function keeps the `contract/templates/PRINCIPLES-interview.md` path-pointer check | review lens dimension |

## Boundary judgment — index-lookup pins

`test_shaping_supplement_after_pin_never_inside` and
`test_tier_label_supplement_after_first_supplement` locate their target sentences with
`text.index(SHAPING_SUPPLEMENT)` / `text.index(TIER_LABEL_SUPPLEMENT)`, not `in` or
`.count(...)`, so the classifier's heuristic (3+ word literal asserted with `in`, `==`,
`.startswith()`, `.endswith()` or `.count(...) >= 1`) does not flag them. They still
break the instant either supplement sentence is reworded, which is exactly the pin
defect class, so they are judged pins per the plan's Risk note and deleted alongside
the presence checks they depend on. Once all four functions that referenced
`SHAPING_SUPPLEMENT` and `TIER_LABEL_SUPPLEMENT` were gone, the two constants were
orphans of this edit and were removed with their explanatory comment blocks (module
criteria: no reference to them survives).

## Classifier recheck (P5)

`python3 docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py`
from the repo root, after the edit:
- `loom-design/tests/interface/test_knowledge_triage.py` — class `behavior`, `has_pins=no`
- `loom-design/tests/principles/test_principles_ratified_line.py` — class `structure`, no `has_pins` marker (clean)
