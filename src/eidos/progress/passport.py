"""Feature Passport 12-Dimensional Convergence Bridge.

Implements SPEC-013 (Feature Passport 12-Dimensional Convergence Bridge) and satisfies
REQ-PASS-001, REQ-PASS-002, AC-013-01, AC-013-02:
    - Encapsulates 12 formal traceability dimensions
    - Strictly gates stamping on verification convergence and security gateway PASS
    - Persists passports under .eidos/passports/<feature_id>.json
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from eidos.core.exceptions import (
    ContractViolationError,
    InvalidInputError,
    VerificationError,
)

REQUIRED_DIMENSIONS = (
    "requirement",
    "spec",
    "architecture",
    "dependencies",
    "contracts",
    "implementation",
    "tests",
    "security",
    "documentation",
    "evidence",
    "git",
    "verification",
)


class FeaturePassportManager:
    """Manages creation, dimensional validation, stamping, and persistence of Feature Passports."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.passports_dir = workspace_root / ".eidos" / "passports"
        self.passports_dir.mkdir(parents=True, exist_ok=True)

    def compile_passport(
        self,
        feature_id: str,
        dimensions: dict[str, Any],
        passport_id: str | None = None,
        stamped_by: str = "eidos-orchestrator",
        auto_stamp: bool = True,
    ) -> dict[str, Any]:
        """Compiles and validates a 12-dimensional passport record.

        If auto_stamp is True, attempts to transition to CONVERGED. Stamping will fail
        if verification.converged is not True or security.gateway_verdict is not 'PASS'.
        """
        if not feature_id:
            raise InvalidInputError("feature_id must be provided")

        self.validate_dimensions(dimensions)

        pid = passport_id or f"PASS-{uuid.uuid4().hex[:10].upper()}"
        verif = dimensions["verification"]
        security = dimensions["security"]

        converged = verif.get("converged") is True
        sec_passed = security.get("gateway_verdict") == "PASS"

        if auto_stamp:
            if not converged or not sec_passed:
                reason = "verification not converged" if not converged else "security gateway failed"
                raise VerificationError(
                    f"Refusing to stamp Feature Passport '{pid}' for feature '{feature_id}': {reason}",
                    details={
                        "converged": converged,
                        "gateway_verdict": security.get("gateway_verdict"),
                        "test_passed": dimensions["tests"].get("passed_count"),
                    },
                )
            status = "CONVERGED"
        else:
            status = "DRAFT"

        stamped_at = datetime.now(timezone.utc).isoformat()

        passport_doc = {
            "contract_id": "CORE-CONTRACT-010",
            "contract_version": "1.0.0",
            "passport_id": pid,
            "feature_id": feature_id,
            "status": status,
            "dimensions": dimensions,
            "stamped_at": stamped_at,
            "stamped_by": stamped_by,
        }

        # Persist to disk
        out_file = self.passports_dir / f"{feature_id}.json"
        out_file.write_text(json.dumps(passport_doc, indent=2), encoding="utf-8")

        return passport_doc

    def validate_dimensions(self, dimensions: dict[str, Any]) -> None:
        """Validates all 12 dimensions against structural contracts."""
        missing = [d for d in REQUIRED_DIMENSIONS if d not in dimensions]
        if missing:
            raise ContractViolationError(
                f"Feature Passport missing required dimensions: {', '.join(missing)}",
                details={"missing": missing},
            )

        # Requirement dimension check
        req = dimensions["requirement"]
        if not req.get("req_id") or not req.get("statement") or req.get("provenance") != "USER_CONFIRMED":
            raise InvalidInputError("Dimension 'requirement' requires req_id, statement, and provenance='USER_CONFIRMED'")

        # Verification dimension check
        verif = dimensions["verification"]
        if "verification_id" not in verif or "converged" not in verif:
            raise InvalidInputError("Dimension 'verification' requires 'verification_id' and 'converged'")

        # Security dimension check
        sec = dimensions["security"]
        if "sandbox_policy_id" not in sec or sec.get("gateway_verdict") not in ("PASS", "FAIL"):
            raise InvalidInputError("Dimension 'security' requires sandbox_policy_id and gateway_verdict in ('PASS', 'FAIL')")

    def load_passport(self, feature_id: str) -> dict[str, Any] | None:
        """Loads a stored passport by feature ID."""
        file_path = self.passports_dir / f"{feature_id}.json"
        if not file_path.exists():
            return None
        return json.loads(file_path.read_text(encoding="utf-8"))
