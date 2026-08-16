from src.core.models import ProvisioningReport

def generate_cli_report(report: ProvisioningReport) -> str:
    """
    Formats ProvisioningReport into clean CLI markdown output as specified in project requirements.
    """
    req = report.normalized_request
    lines = []
    lines.append("========================================")
    lines.append("AI-assisted GitOps Access Provisioning")
    lines.append("========================================")
    lines.append("")
    lines.append(f"Request ID: {report.request_id}")
    lines.append("")
    lines.append("Normalized Request:")
    lines.append(f"Consumer: {req.consumer}")
    lines.append(f"Provider: {req.provider}")
    lines.append(f"Access: {req.access_type}")
    lines.append(f"Scope: {req.access_scope}")
    lines.append("")
    
    validation_str = "Passed" if report.validation_passed else "Failed"
    lines.append(f"Validation: {validation_str}")
    if report.validation_errors:
        for err in report.validation_errors:
            lines.append(f"  - Error: {err}")
    lines.append("")

    if not report.validation_passed:
        lines.append("Action Taken:")
        lines.append("- Processing halted due to validation failure.")
    elif report.existing_access_found:
        lines.append("Existing Access: Found")
        lines.append(f"Details: {report.existing_access_message}")
        lines.append("")
        lines.append("Action Taken:")
        lines.append("- Access already exists. No file modification, branch, or PR created.")
    else:
        lines.append("Existing Access: Not Found")
        lines.append("")
        lines.append("Action Taken:")
        if report.branch_name:
            lines.append(f"- Feature branch created: {report.branch_name}")
        if report.file_modified:
            lines.append(f"- YAML updated: {report.file_modified}")
            lines.append("- YAML validation passed")
        if report.pr_url:
            lines.append(f"- Pull request created: {report.pr_url}")
        else:
            lines.append("- Pull request simulated (Local Mode)")

    lines.append("")
    lines.append("Manual Step Required:")
    lines.append("- Product owner approval must be confirmed manually")
    lines.append("- PR must be reviewed and approved manually")
    lines.append("- Merge must be performed by authorized reviewer")
    lines.append("")
    lines.append("========================================")

    return "\n".join(lines)
