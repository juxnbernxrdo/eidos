"""Native contract schema validator for Eidos Draft 2020-12 JSON Schemas.

Enforces fail-closed validation, structural schema integrity, and payload conformance
without external dependencies (satisfying Constitution Art. V).
"""

import json
import re
from pathlib import Path
from typing import Any


class ContractValidationError(Exception):
    """Raised when a schema or payload violates contractual constraints."""
    pass


class ContractSchemaValidator:
    """Validates Eidos contract schemas and JSON payloads."""

    SUPPORTED_METASCHEMA = "https://json-schema.org/draft/2020-12/schema"

    @classmethod
    def validate_schema_structure(cls, schema: dict[str, Any]) -> list[str]:
        """Validate that a schema definition adheres to Eidos contract standards."""
        errors: list[str] = []

        # 1. Meta-schema validation
        if schema.get("$schema") != cls.SUPPORTED_METASCHEMA:
            errors.append(f"Invalid $schema: expected '{cls.SUPPORTED_METASCHEMA}', got '{schema.get('$schema')}'")

        # 2. Identification
        if not schema.get("$id") or not str(schema.get("$id")).startswith("https://eidos.dev/schemas/contracts/"):
            errors.append(f"Invalid or missing $id URI: '{schema.get('$id')}'")

        if not schema.get("title"):
            errors.append("Schema missing mandatory 'title'")

        # 3. Top-level type
        if schema.get("type") != "object":
            errors.append(f"Root schema type must be 'object', got '{schema.get('type')}'")

        # 4. Properties and required fields
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            errors.append("'properties' must be a dictionary")
        else:
            required = schema.get("required", [])
            if not isinstance(required, list):
                errors.append("'required' must be a list of property names")
            else:
                for req_prop in required:
                    if req_prop not in properties:
                        errors.append(f"Required property '{req_prop}' not defined in 'properties'")

        return errors

    @classmethod
    def validate_payload(cls, schema: dict[str, Any], payload: dict[str, Any], path: str = "root") -> list[str]:
        """Validate a data payload against a contract schema."""
        errors: list[str] = []

        if not isinstance(payload, dict):
            return [f"At {path}: payload must be an object (dict), got {type(payload).__name__}"]

        properties = schema.get("properties", {})
        required = schema.get("required", [])
        additional_allowed = schema.get("additionalProperties", True)

        # Check required fields
        for req in required:
            if req not in payload:
                errors.append(f"At {path}: missing required property '{req}'")

        # Check for disallowed additional properties
        if additional_allowed is False:
            for key in payload:
                if key not in properties:
                    errors.append(f"At {path}: unexpected property '{key}' (additionalProperties: false)")

        # Validate defined properties
        for key, val in payload.items():
            if key not in properties:
                continue

            prop_schema = properties[key]
            val_path = f"{path}.{key}"
            expected_type = prop_schema.get("type")

            # Check const
            if "const" in prop_schema and val != prop_schema["const"]:
                errors.append(f"At {val_path}: value '{val}' does not match const '{prop_schema['const']}'")

            # Check enum
            if "enum" in prop_schema and val not in prop_schema["enum"]:
                errors.append(f"At {val_path}: value '{val}' not in allowed enum {prop_schema['enum']}")

            # Check type
            if expected_type:
                type_err = cls._check_type(val, expected_type, val_path)
                if type_err:
                    errors.append(type_err)
                    continue

            # Check pattern for strings
            if isinstance(val, str) and "pattern" in prop_schema:
                pattern = prop_schema["pattern"]
                if not re.search(pattern, val):
                    errors.append(f"At {val_path}: string '{val}' does not match pattern '{pattern}'")

            # Check nested object
            if isinstance(val, dict) and prop_schema.get("type") == "object":
                nested_errs = cls.validate_payload(prop_schema, val, val_path)
                errors.extend(nested_errs)

            # Check array items
            if isinstance(val, list) and prop_schema.get("type") == "array":
                items_schema = prop_schema.get("items")
                min_items = prop_schema.get("minItems")
                max_items = prop_schema.get("maxItems")

                if min_items is not None and len(val) < min_items:
                    errors.append(f"At {val_path}: array has {len(val)} items, minimum is {min_items}")
                if max_items is not None and len(val) > max_items:
                    errors.append(f"At {val_path}: array has {len(val)} items, maximum is {max_items}")

                if isinstance(items_schema, dict):
                    for idx, item in enumerate(val):
                        item_path = f"{val_path}[{idx}]"
                        if items_schema.get("type") == "object" and isinstance(item, dict):
                            errors.extend(cls.validate_payload(items_schema, item, item_path))
                        elif "enum" in items_schema and item not in items_schema["enum"]:
                            errors.append(f"At {item_path}: item '{item}' not in enum {items_schema['enum']}")

        return errors

    @staticmethod
    def _check_type(val: Any, expected: Any, path: str) -> str | None:
        """Helper to verify type compatibility."""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list,
        }

        # Allow union types, e.g. ["integer", "string"]
        if isinstance(expected, list):
            valid = False
            for exp in expected:
                py_type = type_map.get(exp)
                if py_type and isinstance(val, py_type):
                    # Ensure bool is not counted as int
                    if exp in ("integer", "number") and isinstance(val, bool):
                        continue
                    valid = True
                    break
            if not valid:
                return f"At {path}: expected one of {expected}, got {type(val).__name__}"
            return None

        py_type = type_map.get(expected)
        if py_type:
            # Python bool is a subclass of int, prevent bool matching integer
            if expected in ("integer", "number") and isinstance(val, bool):
                return f"At {path}: expected {expected}, got boolean"
            if not isinstance(val, py_type):
                return f"At {path}: expected {expected}, got {type(val).__name__}"
        return None
