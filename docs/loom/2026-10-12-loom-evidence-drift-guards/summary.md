## Loom Mechanism Drift Guards - Flow Complete Through Write-Plan Station

I have successfully completed the loom flow up to the point of being ready for build station:

### ✅ Intent Station (Capture & Confirm)
- **File**: `docs/loom/intent/2026-10-12-loom-evidence-drift-guards.md`
- **Status**: `confirmed 2026-10-12`
- **Publication**: `automatic — authorized 2026-10-12 by kouko`
- **Needs Design**: `no` (internal checker/mechanism changes only)
- **Second-Vendor Evaluation**: Obtained codex evaluation (see evidence file)

### ✅ Plan Station (Write & Check)
- **File**: `docs/loom/2026-10-12-loom-evidence-drift-guards/plan.md`
- **Charter**: `1.1`
- **Status**: All checks pass
  - `loom_checker.py plan ...` → PASS
  - `loom_checker.py intake write-plan ...` → PASS

### 🔧 Implementation Ready
The plan specifies 5 tasks across 2 waves (reshaped per complexity critique):

**Wave 1 - Core Mechanism**
- **W1-01**: Extend attestation schema + add three checker rules (Acceptance 1,2,3,4)
- **W1-02**: File verdict in change directory + populate attestation (Acceptance 5)
- **W1-03**: Re-run evidence checks in finalize-review (Acceptance 6)

**Wave 2 - Supporting Updates**
- **W2-01**: Update evidence file whitelist in digest (Acceptance 2)
- **W2-02**: Update capture-intent to record intent_confirmed_sha (Acceptance 3)
- **W2-03**: Update acceptance-tester to record tested_commit (Acceptance 2)
- **W2-04**: Update closing-review to populate attestation from report (Acceptance 5)
- **W2-05**: Update plan template with boundary test hint (Acceptance 7)

### 📋 Next Station: Build
The change is now ready for the **build station** (`loom-code:build`), which will:
1. Dispatch implementers for each task
2. Run focused tests after each task
3. Execute integration checks (package suite, adversarial programs)
4. Hand off to closing-review for final verification

### 🛠️ What Will Be Implemented
When the build station runs, it will modify:
- `contract/templates/attestation.json` (add tracking fields)
- `loom-checker/attestation.py` (validate new fields)
- `loom-checker/rule_checks/evidence_coverage.py` (new rule)
- `loom-checker/rule_checks/commit_identity.py` (new rule)
- `loom-checker/rule_checks/intent_version.py` (new rule)
- `loom-checker/rules.py` & `__init__.py` (rule registration)
- `skills/closing-review/SKILL.md` (verdict filing & attestation population)
- `loom-checker/publish.py` (verdict handling)
- `loom-checker/digest.py` (evidence file whitelist)
- `loom-checker/verify.py` (finalize-review re-run checks)
- `loom-design/skills/capture-intent/SKILL.md` & template (intent recording)
- `agents/acceptance-tester.md` & reference (tested commit recording)
- `contract/templates/plan.md` (boundary test hint in Risk section)

### 🎯 Outcome
This change will mechanistically detect and prevent three classes of loom mechanism drift:
1. **Acceptance coverage gaps** (missing test rows)
2. **Evidence baseline drift** (tested vs reviewed commit mismatch)
3. **Intent version drift** (unauthorized intent/plan changes)

Following Design-Is-Taking-Apart principles, the implementation:
- Separates concerns into independent checks
- Uses single sources of truth for each verification
- Eliminates duplicate storage and unnecessary dependencies
- Preserves existing workflows and respects user skip directives
- Maintains backward compatibility with v1 attestations

All implementation details are specified and ready for the build station to execute.