import os
import pytest
from ruamel.yaml import YAML
from src.core.models import NormalizedAccessRequest
from src.core.yaml_modifier import modify_yaml_access
from src.utils.file_utils import read_yaml_file

def test_modify_yaml_adds_permission(tmp_path):
    repo_dir = str(tmp_path)
    provider_file = tmp_path / "DS-Digital-AB-Testing-Evaluation.yaml"
    provider_file.write_text(
        "data_product: DS-Digital-AB-Testing-Evaluation\n"
        "owner: sample.owner@example.com\n"
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
        business_justification="Add new dev to prod permission"
    )

    success, msg, filepath = modify_yaml_access(req, repo_dir=repo_dir)
    assert success is True
    assert os.path.exists(filepath)

    # Read back modified content and verify
    content = read_yaml_file(filepath)
    permissions = content["permissions"]
    assert len(permissions) == 2
    added = permissions[1]
    assert added["consumer"] == "DS-TDA-Governance"
    assert added["source_environment"] == "dev"
    assert added["target_environment"] == "prod"
    assert added["access_type"] == "dev_to_prod"
    assert added["access_scope"] == "schema"
    assert added["status"] == "pending_pr"

def test_yaml_syntax_valid_after_modification(tmp_path):
    repo_dir = str(tmp_path)
    req = NormalizedAccessRequest(
        request_id="REQ-1004",
        consumer="CADP-Customer-Insights",
        provider="DS-TDA-Governance",
        source_environment="stage",
        target_environment="prod",
        access_type="stage_to_prod",
        access_scope="table",
        requested_by="user@example.com",
        business_justification="Test fresh file syntax validation"
    )

    success, msg, filepath = modify_yaml_access(req, repo_dir=repo_dir)
    assert success is True

    # Re-parse using ruamel.yaml to ensure syntax is valid
    yaml_engine = YAML()
    with open(filepath, "r", encoding="utf-8") as f:
        parsed = yaml_engine.load(f)
    assert parsed["data_product"] == "DS-TDA-Governance"
    assert len(parsed["permissions"]) == 1
