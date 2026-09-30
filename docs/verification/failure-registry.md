# Phase 6 Failure Registry

**Authority:** Eidos Verification Protocol  
**Scope:** Log of All Failures, Discrepancies, and Deviations Encountered During Verification  
**Status:** ALL FAILURES RESOLVED  
**Last Updated:** 2026-09-30  

---

## 1. Failure Log Protocol

In accordance with Eidos epistemic discipline:
- No failure is suppressed or concealed.
- Every test failure encountered during Phase 6 execution must be formally registered with its failure trace, root cause analysis, associated verification level, and resolution pointer.

---

## 2. Failure Incident Catalog

### Incident `FAIL-VER-001`: Incomplete Public API Docstrings
- **Date/Time:** 2026-09-30 16:15 UTC
- **Verification Level:** Level 2 (Static Typing & Code Quality)
- **Failing Test:** `tests/verification/test_level2_static_analysis.py::test_public_api_docstrings`
- **Error Trace:**
  ```text
  AssertionError: Undocumented public classes or functions found: [
      ('src/eidos/contracts/models.py', 'TaskStatus'),
      ('src/eidos/contracts/models.py', 'PipelineStage'),
      ('src/eidos/contracts/models.py', 'ProposalState'),
      ('src/eidos/contracts/models.py', 'ContractEntity'),
      ('src/eidos/intelligence/parser.py', 'EntityExtractor')
  ]
  assert len(missing_docstrings) == 0
  ```
- **Root Cause Analysis:** During Phase 5 implementation, several public enum types and models in `models.py` and the `EntityExtractor` class in `parser.py` were declared without triple-quote docstrings, violating Level 2 public documentation standards.
- **Resolution:** Logged as Repair `REP-001`. Docstrings added to all flagged entities.
- **Current Status:** **RESOLVED** (Re-verification `PASS`).

---

### Incident `FAIL-VER-002`: Google Cloud Secret Redaction Regex Character Range Defect
- **Date/Time:** 2026-09-30 16:16 UTC
- **Verification Level:** Level 8 (Security Sandbox & Secret Redaction)
- **Failing Test:** `tests/verification/test_level8_security_boundaries.py::test_comprehensive_secret_scrubbing`
- **Error Trace:**
  ```text
  AssertionError: Secret not scrubbed: AIzaSyD-sample_key_1234567890abcdef
  assert 'AIzaSyD-sample_key_1234567890abcdef' not in scrubbed
  ```
- **Root Cause Analysis:** The regular expression used for Google Cloud / Gemini API key scrubbing in `src/eidos/security/permissions.py` was defined as `r"AIza[0-9A-Za-z-_]{35}"`. In Python regex character sets, an unescaped `-` between characters forms a range (`s-` to `_`), causing character class errors, and the length was fixed at 35 characters, failing on keys of 39 characters containing hyphens.
- **Resolution:** Logged as Repair `REP-002`. Repaired regex to `r"AIza[0-9A-Za-z\-_]{30,}"` with properly escaped hyphen and variable length quantifier.
- **Current Status:** **RESOLVED** (Re-verification `PASS`).

---

## 3. Summary Statistics
- Total Failures Encountered: 2
- Total Failures Resolved: 2
- Open / Unresolved Failures: 0
- Specification Relaxations / Dilutions: **0**
- Contract Alterations: **0**
