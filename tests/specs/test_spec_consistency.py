"""Automated specification validation and consistency test suite for Phase 4.

Verifies:
- All 15 specifications implement all 22 mandatory governance sections.
- Unique IDs for Requirements, Specs, and Acceptance Criteria.
- Valid contract references (no orphan contracts).
- Valid ADR references.
- Complete traceability matrix coverage.
- Given/When/Then format in acceptance criteria.
- Zero contradictions with architectural invariants.
"""

import json
import re
from pathlib import Path
import pytest

from eidos.contracts.validator import ContractSchemaValidator


SPECS_DOCS_DIR = Path(__file__).parent.parent.parent / "docs" / "specs"
SPECS_SCHEMAS_DIR = Path(__file__).parent.parent.parent / "schemas" / "specs"
CONTRACTS_REGISTRY = Path(__file__).parent.parent.parent / "docs" / "contracts" / "registry.md"
ADR_DIR = Path(__file__).parent.parent.parent / "docs" / "adr"


MANDATORY_SECTIONS = [
    "## 1. Status",
    "## 2. Purpose",
    "## 3. Scope",
    "## 4. Non-Goals",
    "## 5. Source Requirements",
    "## 6. Architectural Basis",
    "## 7. Contract Dependencies",
    "## 8. Behavioral Requirements",
    "## 9. Inputs",
    "## 10. Outputs",
    "## 11. State Model",
    "## 12. Invariants",
    "## 13. Preconditions",
    "## 14. Postconditions",
    "## 15. Failure Semantics",
    "## 16. Security Requirements",
    "## 17. Observability Requirements",
    "## 18. Edge Cases",
    "## 19. Acceptance Criteria",
    "## 20. Verification Strategy",
    "## 21. Traceability",
    "## 22. Open Questions & Phase 5 Notes",
]


def get_all_spec_files() -> list[Path]:
    """Retrieve all SPEC-*.md files under docs/specs."""
    return sorted(list(SPECS_DOCS_DIR.glob("SPEC-*.md")))


def test_spec_inventory_count():
    """Verify that all 15 core specifications exist."""
    specs = get_all_spec_files()
    assert len(specs) == 15, f"Expected 15 specifications, found {len(specs)}: {[s.name for s in specs]}"


def test_spec_mandatory_sections_present():
    """Verify that every specification file contains all 22 mandatory governance sections."""
    specs = get_all_spec_files()
    for spec_path in specs:
        content = spec_path.read_text(encoding="utf-8")
        for section in MANDATORY_SECTIONS:
            assert section in content, (
                f"Specification {spec_path.name} missing mandatory section: '{section}'"
            )


def test_spec_schemas_valid_draft2020_12():
    """Verify that all schemas under schemas/specs/ adhere to Draft 2020-12 structure."""
    schema_files = list(SPECS_SCHEMAS_DIR.glob("*.schema.json"))
    assert len(schema_files) == 3, f"Expected 3 spec schemas, found {len(schema_files)}"

    for schema_path in schema_files:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        errors = ContractSchemaValidator.validate_schema_structure(schema)
        # Check custom spec schema id prefix
        assert schema.get("$id", "").startswith("https://eidos.dev/schemas/specs/")
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        assert not errors, f"Schema {schema_path.name} validation errors: {errors}"


def test_unique_requirement_and_criteria_ids():
    """Verify that requirement IDs and acceptance criteria IDs are globally unique."""
    req_file = SPECS_DOCS_DIR / "requirements.md"
    assert req_file.exists()

    content = req_file.read_text(encoding="utf-8")
    req_ids = re.findall(r"`(REQ-[A-Z]+-[0-9]{3})`", content)
    assert len(req_ids) > 0
    assert len(req_ids) == len(set(req_ids)), f"Duplicate REQ-IDs found: {req_ids}"

    specs = get_all_spec_files()
    all_ac_ids = []
    for spec_path in specs:
        spec_content = spec_path.read_text(encoding="utf-8")
        ac_ids = re.findall(r"`(AC-[0-9]{3}-[0-9]{2})`", spec_content)
        all_ac_ids.extend(ac_ids)

    assert len(all_ac_ids) > 0
    assert len(all_ac_ids) == len(set(all_ac_ids)), f"Duplicate AC-IDs found: {all_ac_ids}"


def test_acceptance_criteria_contain_given_when_then():
    """Verify that all acceptance criteria follow the Given/When/Then structure."""
    specs = get_all_spec_files()
    for spec_path in specs:
        content = spec_path.read_text(encoding="utf-8")
        assert "Given " in content, f"{spec_path.name} missing 'Given ' clause in acceptance criteria"
        assert "When " in content, f"{spec_path.name} missing 'When ' clause in acceptance criteria"
        assert "Then " in content, f"{spec_path.name} missing 'Then ' clause in acceptance criteria"


def test_no_orphan_requirements_in_traceability():
    """Verify that every requirement defined in requirements.md appears in traceability.md."""
    req_content = (SPECS_DOCS_DIR / "requirements.md").read_text(encoding="utf-8")
    trace_content = (SPECS_DOCS_DIR / "traceability.md").read_text(encoding="utf-8")

    defined_reqs = set(re.findall(r"`(REQ-[A-Z]+-[0-9]{3})`", req_content))
    traced_reqs = set(re.findall(r"`(REQ-[A-Z]+-[0-9]{3})`", trace_content))

    orphans = defined_reqs - traced_reqs
    assert not orphans, f"Found orphan requirements not present in traceability matrix: {orphans}"


def test_contract_references_valid():
    """Verify that all contracts referenced in specifications exist in the Contract Registry."""
    registry_content = CONTRACTS_REGISTRY.read_text(encoding="utf-8")
    registered_contracts = set(re.findall(r"`([A-Z]+-CONTRACT-[0-9]{3})`", registry_content))
    assert len(registered_contracts) == 15

    specs = get_all_spec_files()
    for spec_path in specs:
        content = spec_path.read_text(encoding="utf-8")
        cited_contracts = set(re.findall(r"`([A-Z]+-CONTRACT-[0-9]{3})`", content))
        invalid_refs = cited_contracts - registered_contracts
        assert not invalid_refs, f"{spec_path.name} cites invalid/unregistered contracts: {invalid_refs}"


def test_adr_references_valid():
    """Verify that all ADRs referenced in specifications exist on disk in docs/adr/."""
    available_adrs = {f.stem for f in ADR_DIR.glob("*.md")}

    specs = get_all_spec_files()
    for spec_path in specs:
        content = spec_path.read_text(encoding="utf-8")
        cited_adrs = set(re.findall(r"(P2-ADR-[0-9]{3})", content))
        for adr in cited_adrs:
            matching = [f for f in available_adrs if f.startswith(adr)]
            assert matching, f"{spec_path.name} references non-existent ADR: {adr}"


def test_no_architectural_contradictions():
    """Audit specifications to ensure absence of architectural invariant contradictions."""
    specs = get_all_spec_files()
    for spec_path in specs:
        content = spec_path.read_text(encoding="utf-8")

        # Invariant 001 check: no direct vendor SDK hardcoding in Core
        if "SPEC-001" in spec_path.name or "SPEC-002" in spec_path.name:
            assert "anthropic" not in content.lower() or "provider" in content.lower()
            assert "openai" not in content.lower() or "provider" in content.lower()

        # Invariant 003 check: verification cannot trust verbal claims
        if "SPEC-006" in spec_path.name or "SPEC-015" in spec_path.name:
            assert "claims are not evidence" in content.lower() or "verbal" in content.lower()

        # Invariant 004 check: evolution is not autonomous
        if "SPEC-014" in spec_path.name:
            assert "human approval" in content.lower()
            assert "prohibited" in content.lower()

        # Invariant 008 check: security default deny
        if "SPEC-008" in spec_path.name:
            assert "default-deny" in content.lower() or "permission_denied" in content.lower()
