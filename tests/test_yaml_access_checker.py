import os
import pytest
from src.core.models import NormalizedAccessRequest
from src.core.yaml_access_checker import check_existing_access

def test_existing_access_detected(tmp_path):
    # Setup temporary sample repo
    provider_file = tmp_path / "DS-Digital-AB-Testing-Evaluation.yaml"
    provider_file.write_text(
        "data_product: DS-Digital-AB-Testing-Evaluation\n"
        "permissions:\n"
        "  - consumer: DS-TDA-Governance\n"
        "    source_environment: dev\n"
        "    target_environment: dev\n"
        "    access_type: dev_to_dev\n"
        "    access_scope: schema\n"
        "    status: active\n"
    )

    req = NormalizedAccessRequest(
        request_id="REQ-1002",
        consumer="DS-TDA-Governance",
        provider="DS-Digital-AB-Testing-Evaluation",
        source_environment="dev",
        target_environment="dev",
        access_type="dev_to_dev",
        access_scope="schema",
        requested_by="user@example.com",
        business_justification="Existing access check"
    )

    res = check_existing_access(req, repo_dir=str(tmp_path))
    assert res.exists is True
    assert "already exists" in res.message

def test_missing_access_not_found(tmp_path):
    provider_file = tmp_path / "DS-Digital-AB-Testing-Evaluation.yaml"
    provider_file.write_text(
        "data_product: DS-Digital-AB-Testing-Evaluation\n"
        "permissions:\n"
        "  - consumer: DS-TDA-Governance\n"
        "    source_environment: dev\n"
        "    target_environment: dev\n"
        "    access_type: dev_to_dev\n"
        "    access_scope: schema\n"
        "    status: active\n"
    )

    req = NormalizedAccessRequest(
        request_id="REQ-1001",
        consumer="DS-TDA-Governance",
        provider="DS-Digital-AB-Testing-Evaluation",
        source_environment="dev",
        target_environment="prod",
        access_type="dev_to_prod",
        access_scope="schema",
        requested_by="user@example.com",
        business_justification="New access check"
    )

    res = check_existing_access(req, repo_dir=str(tmp_path))
    assert res.exists is False
    assert "does not exist" in res.message
