import re
from src.core.models import RawAccessRequest, NormalizedAccessRequest

def clean_data_product_name(name: str) -> str:
    """
    Normalizes data product name:
    - Strips whitespace
    - Removes trailing _LH or -LH (case insensitive)
    - Replaces underscores with hyphens
    """
    if not name:
        return ""
    
    cleaned = name.strip()
    
    # Remove trailing _LH or -LH
    cleaned = re.sub(r'([_-]LH)$', '', cleaned, flags=re.IGNORECASE)
    
    # Replace underscores with hyphens
    cleaned = cleaned.replace('_', '-')
    
    return cleaned

def generate_access_type(source_env: str, target_env: str) -> str:
    """Generates standard access_type identifier e.g., dev_to_prod."""
    src = (source_env or "").lower().strip()
    tgt = (target_env or "").lower().strip()
    return f"{src}_to_{tgt}"

def normalize_request(raw_request: RawAccessRequest) -> NormalizedAccessRequest:
    """
    Normalizes a RawAccessRequest into a NormalizedAccessRequest.
    """
    consumer_norm = clean_data_product_name(raw_request.consumer)
    provider_norm = clean_data_product_name(raw_request.provider)
    src_env = (raw_request.source_environment or "").lower().strip()
    tgt_env = (raw_request.target_environment or "").lower().strip()
    scope = (raw_request.access_scope or "").lower().strip()
    access_type = generate_access_type(src_env, tgt_env)

    return NormalizedAccessRequest(
        request_id=raw_request.request_id or "REQ-1001",
        consumer=consumer_norm,
        provider=provider_norm,
        source_environment=src_env,
        target_environment=tgt_env,
        access_type=access_type,
        access_scope=scope,
        requested_by=raw_request.requested_by or "unknown@example.com",
        business_justification=raw_request.business_justification or "N/A",
    )
