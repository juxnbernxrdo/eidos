"""Typed exception hierarchy for Eidos."""

class EidosError(Exception):
    """Base exception for all Eidos errors."""
    pass

class ConfigurationError(EidosError):
    """Raised when repository governance or configuration is invalid."""
    pass

class SpecificationError(EidosError):
    """Raised when a specification or contract fails validation."""
    pass

class VerificationError(EidosError):
    """Raised when a verification step fails blocking enforcement."""
    pass

class InvariantViolationError(EidosError):
    """Raised when an architectural invariant is violated."""
    def __init__(self, rule_id: str, message: str, source_file: str | None = None, line: int | None = None):
        self.rule_id = rule_id
        self.source_file = source_file
        self.line = line
        super().__init__(f"Invariant [{rule_id}] violated: {message} ({source_file}:{line})")

class DriftError(EidosError):
    """Raised when unmanaged drift is detected."""
    pass
