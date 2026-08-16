import pytest
from src.core.models import RawAccessRequest
from src.core.normalizer import clean_data_product_name, generate_access_type, normalize_request

def test_clean_data_product_name():
    raw_name = "DS_Digital_AB_Testing_Evaluation_LH"
    cleaned = clean_data_product_name(raw_name)
    assert cleaned == "DS-Digital-AB-Testing-Evaluation"

def test_clean_data_product_name_cadp():
    raw_name = "CADP_Customer_Insights-LH"
    cleaned = clean_data_product_name(raw_name)
    assert cleaned == "CADP-Customer-Insights"

def test_generate_access_type():
    assert generate_access_type("dev", "prod") == "dev_to_prod"
    assert generate_access_type("DEV ", " DEV") == "dev_to_dev"

def test_normalize_request_full():
    raw = RawAccessRequest(
        request_id="REQ-1001",
        consumer="DS_TDA_Governance_LH",
        provider="DS_Digital_AB_Testing_Evaluation_LH",
        source_environment="dev",
        target_environment="prod",
        access_scope="schema",
        requested_by="test@example.com",
        business_justification="Unit test normalization"
    )
    normalized = normalize_request(raw)
    assert normalized.consumer == "DS-TDA-Governance"
    assert normalized.provider == "DS-Digital-AB-Testing-Evaluation"
    assert normalized.access_type == "dev_to_prod"
    assert normalized.access_scope == "schema"
