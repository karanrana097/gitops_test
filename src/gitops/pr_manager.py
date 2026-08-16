from typing import Tuple, Optional
from src.gitops.github_client import GitHubClientWrapper
from src.core.models import NormalizedAccessRequest
from src.utils.logger import setup_logger

logger = setup_logger("pr_manager")

class PullRequestManager:
    def __init__(self, github_client: GitHubClientWrapper):
        self.github_client = github_client

    def create_pull_request(
        self,
        request: NormalizedAccessRequest,
        branch_name: str,
        file_path: str
    ) -> Tuple[bool, Optional[str], str]:
        """
        Creates pull request on GitHub or simulates PR generation.
        Returns (success, pr_url, message).
        """
        title = f"[Access Request] {request.consumer} -> {request.provider} ({request.access_type})"
        body = (
            f"### AI-assisted GitOps Access Provisioning Request\n\n"
            f"**Request ID:** {request.request_id}\n"
            f"**Consumer Data Product:** `{request.consumer}`\n"
            f"**Provider Data Product:** `{request.provider}`\n"
            f"**Source Environment:** `{request.source_environment}`\n"
            f"**Target Environment:** `{request.target_environment}`\n"
            f"**Access Type:** `{request.access_type}`\n"
            f"**Access Scope:** `{request.access_scope}`\n"
            f"**Requested By:** {request.requested_by}\n"
            f"**Business Justification:** {request.business_justification}\n"
            f"**Product Owner:** {request.provider_owner or 'Pending manual verification'}\n\n"
            f"---\n"
            f"**Governance & Approval Requirements:**\n"
            f"- [ ] Data Product Owner Approval Confirmed\n"
            f"- [ ] Access Scope & Security Review Completed\n"
            f"- [ ] Manual PR Review & Approval\n"
        )

        if self.github_client.is_connected():
            try:
                repo = self.github_client.repo_instance
                base_branch = self.github_client.base_branch
                pr = repo.create_pull(
                    title=title,
                    body=body,
                    head=branch_name,
                    base=base_branch
                )
                logger.info(f"Created GitHub PR #{pr.number}: {pr.html_url}")
                return True, pr.html_url, f"Pull request #{pr.number} created successfully."
            except Exception as e:
                logger.error(f"Failed to create GitHub PR: {e}")
                return False, None, str(e)
        else:
            # Simulation mode
            simulated_url = f"https://github.com/simulated-org/simulated-repo/pull/{request.request_id.replace('REQ-', '')}"
            logger.info(f"[LOCAL SIMULATION] Simulated Pull Request generated: {simulated_url}")
            return True, simulated_url, "[SIMULATED] Pull request created locally."
