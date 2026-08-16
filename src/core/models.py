from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RawAccessRequest(BaseModel):
    request_id: Optional[str] = "REQ-UNKNOWN"
    consumer: str
    provider: str
    source_environment: str
    target_environment: str
    access_scope: str
    requested_by: Optional[str] = "unknown@example.com"
    business_justification: Optional[str] = "No justification provided"

class NormalizedAccessRequest(BaseModel):
    request_id: str
    consumer: str
    provider: str
    source_environment: str
    target_environment: str
    access_type: str
    access_scope: str
    requested_by: str
    business_justification: str
    provider_owner: Optional[str] = None

class PermissionEntry(BaseModel):
    consumer: str
    source_environment: str
    target_environment: str
    access_type: str
    access_scope: str
    status: str = "pending_pr"

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class AccessCheckResult(BaseModel):
    exists: bool
    matching_entry: Optional[Dict[str, Any]] = None
    message: str
    file_path: Optional[str] = None

class ProvisioningReport(BaseModel):
    request_id: str
    normalized_request: NormalizedAccessRequest
    validation_passed: bool
    validation_errors: List[str] = Field(default_factory=list)
    existing_access_found: bool
    existing_access_message: str
    file_modified: Optional[str] = None
    branch_name: Optional[str] = None
    commit_sha: Optional[str] = None
    pr_url: Optional[str] = None
    mode: str = "local"
    manual_approval_required: bool = True
