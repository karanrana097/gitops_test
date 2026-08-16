from typing import Tuple
from src.core.models import RawAccessRequest, NormalizedAccessRequest, ValidationResult
from src.core.normalizer import normalize_request
from src.core.validator import validate_access_request
from src.core.owner_lookup import DataProductOwnerLookup

class ValidationAgent:
    """
    Agent responsible for normalizing access requests, validating naming conventions/scopes,
    resolving data product owners, and explaining validation outcomes.
    """
    def __init__(self, owner_lookup: DataProductOwnerLookup = None):
        self.owner_lookup = owner_lookup or DataProductOwnerLookup()

    def process_validation(
        self, raw_request: RawAccessRequest
    ) -> Tuple[NormalizedAccessRequest, ValidationResult]:
        """
        Normalizes and validates raw request.
        Attaches resolved provider owner if found.
        """
        normalized = normalize_request(raw_request)
        validation_res = validate_access_request(normalized)

        # Attempt to resolve owner
        owner = self.owner_lookup.lookup_owner(normalized.provider)
        if owner:
            normalized.provider_owner = owner

        return normalized, validation_res
