"""Typed exception hierarchy for Eidos conforming to Phase 3 Contract Error Semantics."""

from typing import Any


class EidosError(Exception):
    """Base exception for all Eidos errors."""
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class InvalidInputError(EidosError):
    """Raised when parameters or schemas fail validation."""
    code = "INVALID_INPUT"


class ContractViolationError(EidosError):
    """Raised when an operation violates a formal contract precondition or postcondition."""
    code = "CONTRACT_VIOLATION"


class PermissionDeniedError(EidosError):
    """Raised when an action violates security capabilities or path confinement."""
    code = "PERMISSION_DENIED"


class UnsupportedCapabilityError(EidosError):
    """Raised when a requested capability is not supported by the environment or adapter."""
    code = "UNSUPPORTED_CAPABILITY"


class ResourceUnavailableError(EidosError):
    """Raised when a required resource (file, graph node, context item) is missing."""
    code = "RESOURCE_UNAVAILABLE"


class VerificationError(EidosError):
    """Raised when a verification step fails blocking enforcement."""
    code = "VERIFICATION_FAILED"


VerificationFailedError = VerificationError


class VersionMismatchError(EidosError):
    """Raised when schema or component versions are incompatible."""
    code = "VERSION_MISMATCH"


class InvariantViolationError(EidosError):
    """Raised when an architectural invariant is violated."""
    code = "INVARIANT_VIOLATION"

    def __init__(
        self,
        rule_id: str,
        message: str,
        source_file: str | None = None,
        line: int | None = None,
        details: dict[str, Any] | None = None,
    ):
        self.rule_id = rule_id
        self.source_file = source_file
        self.line = line
        loc = f" ({source_file}:{line})" if source_file else ""
        super().__init__(f"Invariant [{rule_id}] violated: {message}{loc}", details=details)


class ProvenanceError(EidosError):
    """Raised when provenance, epistemic origin, or hash verification fails."""
    code = "PROVENANCE_ERROR"


class ExecutionTimeoutError(EidosError):
    """Raised when subprocess or tool execution exceeds allocated timeout."""
    code = "EXECUTION_TIMEOUT"


class ConfigurationError(EidosError):
    """Raised when repository governance or configuration is invalid."""
    code = "CONFIGURATION_ERROR"


class SpecificationError(EidosError):
    """Raised when a specification fails validation or consistency check."""
    code = "SPECIFICATION_ERROR"


class DriftError(EidosError):
    """Raised when unmanaged drift is detected between spec and code."""
    code = "DRIFT_ERROR"
