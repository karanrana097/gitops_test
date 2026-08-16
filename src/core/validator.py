from typing import List
from src.core.models import NormalizedAccessRequest, ValidationResult

ALLOWED_ENVIRONMENTS = {"dev", "qa", "stage", "prod"}
ALLOWED_SCOPES = {"schema", "table", "volume"}
ALLOWED_PREFIXES = ("DS-", "CADP-")

def validate_access_request(request: NormalizedAccessRequest) -> ValidationResult:
    """
    Validates normalized access request against organizational policies and naming rules.
    """
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Consumer checks
    if not request.consumer:
        errors.append("Consumer data product name is required.")
    else:
        if not any(request.consumer.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            errors.append(
                f"Consumer '{request.consumer}' must start with one of: {', '.join(ALLOWED_PREFIXES)}"
            )
        if "_" in request.consumer:
            errors.append(f"Consumer '{request.consumer}' contains illegal underscores after normalization.")

    # 2. Provider checks
    if not request.provider:
        errors.append("Provider data product name is required.")
    else:
        if not any(request.provider.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            errors.append(
                f"Provider '{request.provider}' must start with one of: {', '.join(ALLOWED_PREFIXES)}"
            )
        if "_" in request.provider:
            errors.append(f"Provider '{request.provider}' contains illegal underscores after normalization.")

    # 3. Environment checks
    if not request.source_environment:
        errors.append("source_environment is required.")
    elif request.source_environment not in ALLOWED_ENVIRONMENTS:
        errors.append(
            f"source_environment '{request.source_environment}' is invalid. Must be one of: {', '.join(sorted(ALLOWED_ENVIRONMENTS))}"
        )

    if not request.target_environment:
        errors.append("target_environment is required.")
    elif request.target_environment not in ALLOWED_ENVIRONMENTS:
        errors.append(
            f"target_environment '{request.target_environment}' is invalid. Must be one of: {', '.join(sorted(ALLOWED_ENVIRONMENTS))}"
        )

    # 4. Access Scope checks
    if not request.access_scope:
        errors.append("access_scope is required.")
    elif request.access_scope not in ALLOWED_SCOPES:
        errors.append(
            f"access_scope '{request.access_scope}' is invalid. Must be one of: {', '.join(sorted(ALLOWED_SCOPES))}"
        )

    # 5. Business rules & cross-product validation
    if request.consumer and request.provider and request.consumer == request.provider:
        warnings.append("Consumer and Provider data products are identical.")

    is_valid = len(errors) == 0
    return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)
