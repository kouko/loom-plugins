**It is mostly self-contained for bounded research, but not fully self-contained for its Loom integration or preservation workflow.** I could conduct a standalone investigation and produce a record without asking the author, provided the question, evidence access and authorization were available. The package also explicitly permits an inconclusive result or an unsaved draft when those prerequisites are unavailable.

**Which requests trigger it?**

The stated trigger is a factual uncertainty that could change an engineering decision, including a small capability/version check. Contradictions, repeated failures and unverified assumptions qualify when consequential. A lookup without a consequential gap does not.  
Citations: `SKILL.md`, description and “Engineering research,” steps 1–4.

Two requests whose invocation boundary I am unsure about:

- **“Check whether version 4 supports feature X.”** This could be a routine lookup or consequential research. The request alone does not establish a pending decision, and the package supplies no sharper boundary between those cases. Citation: `SKILL.md`, description and “Engineering research,” step 3.
- **“Review this change for correctness and maintainability.”** The evaluation guidance includes code-health inspection, but the core trigger requires a consequential evidence gap and says ordinary review remains with the owning task. It is unclear whether a general review request invokes research immediately or only after such a gap is identified. Citations: `references/evaluation-selection.md`, “Match the question to the approach”; `SKILL.md`, “Engineering research,” steps 3 and 5.

**Is each mode executable as written?**

The package does not formally define “modes.” Its identifiable operating paths are:

| Path | Assessment |
|---|---|
| Reuse sufficient existing evidence | Executable. Check applicability, explain the method, retain a record and return the decision. Citations: `SKILL.md`, “Return to the owning task”; `templates/research.md`, “Method and rationale.” |
| Inspect local or upstream artifacts | Executable as a bounded research procedure. The required source traversal, revision matching and limits on claims are specified. Source access is an explicit prerequisite; inaccessible source permits a partial assessment. Citation: `references/source-policy.md`, “Repository investigations require source inspection.” |
| Research external documentation and reports | Executable. Source selection, acceptance, attribution and handling inaccessible evidence are described. Accessible supporting content is an explicit prerequisite for claiming it was inspected. Citation: `references/source-policy.md`, “Source selection and acceptance” and “Critical-claim evidence rules.” |
| Diagnose or run experiments | Executable as guidance for designing a bounded investigation, rather than as a ready-made experiment. It requires a learning target, controls, observations and stopping conditions. Tools, resources and authorization are explicit prerequisites; failure or unavailability becomes a limitation. Citation: `references/research-methods.md`, “Research methods.” |
| Evaluate alternatives, effects or risks | Executable for lightweight assessments using the stated criteria and evidence rules. It does **not** supply complete procedures for every named framework. For example, it mentions a possible need for full facilitated ATAM without providing that process. Citation: `references/evaluation-selection.md`, “Frame the decision” and “Match the question to the approach.” |
| Add structural relationships | Executable as an optional representation procedure. Meaning, evidence mapping and readback checks are specified. A parser/renderer is explicitly optional; unavailable validation must be reported. Citation: `references/structured-relations.md`, “Preserve meaning and evidence” and “Check the actual representation.” |
| Retain and update research records | Executable for standalone research. Paths, metadata, collision handling and continuation rules are supplied. The missing integration instruction is how to discover an “active change” and its identifier. Write access is an explicit prerequisite, with an unsaved-draft fallback. Citation: `SKILL.md`, “Retained research records.” |
| Preserve research after merge | Partially executable. Candidate preparation, destination discovery, instance-specific permission, writing and verification are specified. However, the package refers to a “finishing command” and its “printed cleanup destination” without identifying that command or defining successful cleanup. Those are missing workflow instructions. Verified merge, destination, permission and an available write mechanism are explicitly stated prerequisites. Citation: `references/preservation.md`, “Establish eligibility and provenance,” “Prepare a concrete candidate before asking” and “Save only the authorized copy.” |

**Which terms are undefined?**

The consequential omissions are mostly integration vocabulary:

- **“Loom,” “station,” “active station,” “owning review station,” “human decision point,” “active change” and “change-id.”** Their surrounding responsibilities are described, but the package does not define the workflow or how to identify its current state. Citations: `SKILL.md`, “Retained research records” and “Return to the owning task”; `references/evaluation-selection.md`, “Match the question to the approach.”
- **“Finishing command,” “cleanup destination” and successful “cleanup.”** No command or completion criteria are supplied. Citation: `references/preservation.md`, opening and “Establish eligibility and provenance.”
- **“Frozen trial records.”** The preservation constraint is explicit, but how such records are designated is unspecified. Citation: `SKILL.md`, “Retained research records.”
- **“Isolated-loader evidence” and “installed-host behavior.”** They appear as distinctions without identifying the loader or host. Citation: `references/preservation.md`, “Save only the authorized copy.”
- **“Vault” and `obsidian:obsidian-cli`.** The package explains destination safeguards, but does not define the Vault abstraction or how that named capability is accessed. It does provide a fallback when the CLI is unavailable. Citation: `references/preservation.md`, “Prepare a concrete candidate before asking.”

“Consequential,” “sufficient support” and “enduring or cross-repository value” are judgment criteria without operational thresholds. That leaves discretion, although it does not by itself make the procedures unexecutable. Citations: `SKILL.md`, steps 3–4; `references/preservation.md`, “Establish eligibility and provenance.”