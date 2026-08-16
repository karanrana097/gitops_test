import os
from typing import Dict, Any, Tuple
from ruamel.yaml import YAML
from src.core.models import NormalizedAccessRequest
from src.utils.file_utils import read_yaml_roundtrip, write_yaml_roundtrip

def modify_yaml_access(
    request: NormalizedAccessRequest,
    repo_dir: str = "sample_repo/data_products"
) -> Tuple[bool, str, str]:
    """
    Appends a new permission definition to the provider's YAML configuration.
    Validates YAML syntax before saving.
    Returns (success, message, filepath).
    """
    filename = f"{request.provider}.yaml"
    os.makedirs(repo_dir, exist_ok=True)
    filepath = os.path.join(repo_dir, filename)

    yaml_engine = YAML()
    yaml_engine.preserve_quotes = True
    yaml_engine.indent(mapping=2, sequence=4, offset=2)

    if os.path.exists(filepath):
        try:
            data, yaml_engine = read_yaml_roundtrip(filepath)
        except Exception as e:
            return False, f"Failed to parse existing YAML file {filepath}: {str(e)}", filepath
    else:
        # Initialize default structure for new provider file
        data = {
            "data_product": request.provider,
            "owner": request.provider_owner or "unknown.owner@example.com",
            "permissions": []
        }

    if "permissions" not in data or data["permissions"] is None:
        data["permissions"] = []

    # Construct new permission dict
    new_permission = {
        "consumer": request.consumer,
        "source_environment": request.source_environment,
        "target_environment": request.target_environment,
        "access_type": request.access_type,
        "access_scope": request.access_scope,
        "status": "pending_pr"
    }

    # Append permission entry
    data["permissions"].append(new_permission)

    # Validate syntax before writing to disk
    try:
        write_yaml_roundtrip(filepath, data, yaml_engine)
        # Re-parse to verify syntax validity
        read_yaml_roundtrip(filepath)
    except Exception as e:
        return False, f"YAML modification failed syntax validation: {str(e)}", filepath

    return True, f"Successfully added permission definition to {filename}", filepath
