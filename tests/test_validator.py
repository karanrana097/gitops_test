import pytest
from src.core.models import NormalizedAccessRequest
from src.core.validator import validate_access_request

def test_valid_request_passes():
    req = NormalizedAccessRequest(
        request_id="REQ-1001",
        consumer="DS-TDA-Governance",
        provider="DS-Digital-AB-Testing-Evaluation",
        source_environment="dev",
        target_environment="prod",
        access_type="dev_to_prod",
        access_scope="schema",
        requested_by="user@example.com",
        business_justification="Valid justification"
    )
    result = validate_access_request(req)
    assert result.is_valid is True
    assert len(result.errors) == 0

def test_invalid_prefix_fails():
    req = NormalizedAccessRequest(
        request_id="REQ-1002",
        consumer="INVALID-Consumer",
        provider="DS-Digital-AB-Testing-Evaluation",
        source_environment="dev",
        target_environment="prod",
        access_type="dev_to_prod",
        access_scope="schema",
        requested_by="user@example.com",
        business_justification="Invalid prefix test"
    )
    result = validate_access_request(req)
    assert result.is_valid is False
    assert any("must start with one of" in err for err in result.errors)

def test_invalid_environment_fails():
    req = NormalizedAccessRequest(
        request_id="REQ-1003",
        consumer="DS-TDA-Governance",
        provider="CADP-Customer-Insights",
        source_environment="sandbox",
        target_environment="production",
        access_type="sandbox_to_production",
        access_scope="schema",
        requested_by="user@example.com",
        business_justification="Invalid env test"
    )
    result = validate_access_request(req)
    assert result.is_valid is False
    assert any("source_environment 'sandbox' is invalid" in err for err in result.errors)
