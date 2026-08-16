import os
from typing import Optional, Dict, Any
from src.core.models import NormalizedAccessRequest, AccessCheckResult
from src.utils.file_utils import read_yaml_file

def check_existing_access(
    request: NormalizedAccessRequest,
    repo_dir: str = "sample_repo/data_products"
) -> AccessCheckResult:
    """
    Locates the provider YAML file and checks whether the requested access permission already exists.
    """
    filename = f"{request.provider}.yaml"
    filepath = os.path.join(repo_dir, filename)

    if not os.path.exists(filepath):
        return AccessCheckResult(
            exists=False,
            matching_entry=None,
            message=f"Provider specification YAML file not found at: {filepath}. Will create/provision new.",
            file_path=filepath
        )

    try:
        data = read_yaml_file(filepath)
    except Exception as e:
        return AccessCheckResult(
            exists=False,
            matching_entry=None,
            message=f"Error reading YAML file {filepath}: {str(e)}",
            file_path=filepath
        )

    permissions = data.get("permissions", [])
    if not isinstance(permissions, list):
        permissions = []

    for entry in permissions:
        if not isinstance(entry, dict):
            continue
        
        # Check matching consumer, environments, access_type, access_scope
        same_consumer = entry.get("consumer") == request.consumer
        same_src_env = entry.get("source_environment") == request.source_environment
        same_tgt_env = entry.get("target_environment") == request.target_environment
        same_scope = entry.get("access_scope") == request.access_scope
        same_access_type = entry.get("access_type") == request.access_type

        if same_consumer and same_src_env and same_tgt_env and same_scope:
            return AccessCheckResult(
                exists=True,
                matching_entry=entry,
                message=f"Access already exists in {filename} for consumer '{request.consumer}' ({request.access_type}, scope: {request.access_scope}).",
                file_path=filepath
            )

    return AccessCheckResult(
        exists=False,
        matching_entry=None,
        message=f"Access does not exist in {filename}. Modification required.",
        file_path=filepath
    )
