# Structural relationships in research records

## Decide whether structure helps

Use this optional representation when the relationships are part of the answer:
branches and exceptions, dependencies, interaction order, state transitions, or
competing explanations. Prefer prose for a simple fact and a table for a small
comparison. Omit the template's optional section when it adds no information.
Do not draw a diagram merely because a research record exists.

A file-reading agent receives Mermaid source unless a rendered image is also
provided. Legible diagram code and accompanying prose matter. No general
improvement in agent understanding is assumed or established by this policy.

## Preserve meaning and evidence

- Choose a diagram suited to the question: flowchart for branches/dependencies,
  sequence diagram for interactions over time, state diagram for transitions.
  A causal hypothesis can use a labeled flowchart; the notation is not proof.
- Explain what arrows mean: calls, occurs before, depends on, supports a claim,
  or hypothesized influence. Separate or explicitly label mixed relations.
  Temporal order, association and a dependency do not establish causation.
- Identify evidence status in words: observed, source-inferred, hypothesis,
  disproved under stated conditions, or untested. Use node/edge labels or an
  adjacent keyed legend; colors and line styles alone are insufficient.
  Evidence that failed to support a hypothesis does not by itself disprove it.
- Give nodes stable short IDs and meaningful labels. Map decision-critical
  nodes/edges to evidence entries with source paths/anchors or experiment
  results and applicable conditions. A compact adjacent table is sufficient.
  Do not add a plausible edge as fact to make the diagram look complete.
- Preserve material branches, exceptions, failures and unknown links. Keep the
  graph bounded to the question; split it only when that improves inspection.
- Retain the conclusion, scope, evidence and uncertainty in ordinary text.
  The diagram must agree with those statements, including negative results.

## Check the actual representation

Prefer basic portable syntax and quoted labels over decorative or recent
features. Do not assume the latest online renderer matches the target Obsidian
or GitHub renderer; identify the tested renderer/version when known.

Read back the saved diagram and check edge direction, relationship meaning,
branch coverage, evidence mapping and consistency with the source and findings.
When a compatible parser/renderer is already available, check the actual saved
Mermaid blocks and inspect output for parser errors rather than relying on exit
status alone. If unavailable, record that syntax/render validation remains
untested; do not install tools solely for this optional section without existing
authorization. Rendering success establishes syntax/display only, not factual
accuracy, causal validity or improved agent comprehension.
