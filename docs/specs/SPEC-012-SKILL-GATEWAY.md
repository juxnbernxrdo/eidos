# SPEC-012 — Skill Gateway & Lifecycle Verification

## 1. Status
`ACCEPTED`

## 2. Purpose
Specifies the behavior of the Skill Gateway: inspecting, auditing, validating, installing, and hash-pinning external agent skills, preventing supply-chain malware and prompt injection vectors.

## 3. Scope
Skill discovery, static AST analysis, YARA scanning, risk scoring, lockfile pinning in `skills-lock.json`, and invocation guardrails.

## 4. Non-Goals
- Does not author skill packages.
- Does not permit uninspected dynamic installation of remote packages.
- Does not grant skills root or host filesystem execution permissions.

## 5. Source Requirements
- `REQ-SKILL-001`: Pre-Installation Static & YARA Scanning
- `REQ-SKILL-002`: Cryptographic Hash Pinning in Manifest

## 6. Architectural Basis
- `docs/architecture/skills.md`: Skill unit, lifecycle, and security boundaries.
- `docs/adr/P2-ADR-006`: Skill Gateway and sandbox supervisor.
- `docs/research/evidence-registry.md`: EVD-008 (skill supply-chain risk and repo-aware scanning), SRC-108 (NVIDIA T1-T3 eval).

## 7. Contract Dependencies
- `CORE-CONTRACT-008`: Capability & Permission Contract.
- `CORE-CONTRACT-006`: Finding Contract.

## 8. Behavioral Requirements
The Skill Gateway governs the skill lifecycle:
$$\text{DISCOVER} \to \text{VALIDATE} \to \text{INSTALL} \to \text{INVOKE} \to \text{DEPRECATE}$$
- During `VALIDATE`, scans Python scripts with AST inspection and YARA rules for suspicious syscalls (`os.system`, socket calls, obfuscation).
- Evaluates risk score: skills exceeding the risk cutoff (default: $\text{risk} \ge 25$, open DESIGN_CHOICE) are rejected.
- During `INSTALL`, records package git commit hash and SHA-256 digest in `skills-lock.json`.
- During `INVOKE`, applies progressive disclosure: exposes only YAML description to LLM until explicitly triggered.

## 9. Inputs
- Candidate skill package containing `SKILL.md` (metadata) and `scripts/` directory.
- Security scan policies and active risk threshold.

## 10. Outputs
- On Pass: Stamped entry in `skills-lock.json` and activation grant.
- On Fail: Security `Finding` with category `SECURITY`, severity `CRITICAL`, and detailed rejection reasons.

## 11. State Model
Skill Lifecycle: `DISCOVERED → SCANNED → LOCKED → ACTIVE → DEPRECATED`.

## 12. Invariants
- Constitution Art. III: Zero unaudited skills installed in the repository.
- `INV-008`: Installed skills run strictly within declared capability permissions.

## 13. Preconditions
- Skill package must contain valid YAML frontmatter in `SKILL.md` with name and description $\le 1024$ characters.
- Must carry an OSI-approved permissive license (MIT, Apache-2.0, BSD per Constitution Art. V).

## 14. Postconditions
- `skills-lock.json` is updated with the exact SHA-256 digest of all script files.

## 15. Failure Semantics
Detection of dangerous execution primitives (e.g. `eval()`, network sockets, subprocess execution without grant) triggers an immediate `PERMISSION_DENIED` rejection.

## 16. Security Requirements
- Skills are treated as untrusted code until all security layers pass.
- Skill scripts must be executed inside isolated sandbox processes.

## 17. Observability Requirements
- Emits telemetry logging scanned line count, static AST warnings, YARA match counts, and calculated risk score.

## 18. Edge Cases
- Modified installed skill: If local script bytes differ from SHA-256 in `skills-lock.json`, the gateway halts execution and flags tampering.
- Duplicate skill name: Rejects installation unless explicit namespace is specified.

## 19. Acceptance Criteria
### `AC-012-01` (Malicious Pattern Rejection)
```gherkin
Given a skill script containing socket connection to an external IP
When the gateway performs static security analysis
Then the skill must be rejected with a CRITICAL security finding and installation must abort.
```

### `AC-012-02` (Lockfile Hash Pinning)
```gherkin
Given a valid, audited skill package
When skill installation completes
Then an entry with the exact SHA-256 digest must be committed to skills-lock.json.
```

## 20. Verification Strategy
Automated tests in `tests/specs/test_skill_gateway.py` verifying detection of known malicious script patterns, lockfile generation, and integrity tampering detection.

## 21. Traceability
- Research: EVD-008, SRC-108
- ADR: `P2-ADR-006`
- Contract: `CORE-CONTRACT-008`, `CORE-CONTRACT-006`
- Requirements: `REQ-SKILL-001`, `REQ-SKILL-002`

## 22. Open Questions & Phase 5 Notes
- Risk threshold calibration ($< 25$) to be empirically calibrated in Phase 7 (`EXP-005`).
- Phase 5 note: Use Python standard `ast` module and regex scanner for initial lightweight implementation.
