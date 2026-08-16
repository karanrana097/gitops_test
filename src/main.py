import os
import sys
import argparse
from dotenv import load_dotenv

# Add parent directory to path to enable package execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent.intake_agent import IntakeAgent
from src.agent.validation_agent import ValidationAgent
from src.agent.summary_agent import SummaryAgent
from src.core.yaml_access_checker import check_existing_access
from src.core.yaml_modifier import modify_yaml_access
from src.core.models import ProvisioningReport
from src.gitops.github_client import GitHubClientWrapper
from src.gitops.branch_manager import BranchManager, construct_branch_name
from src.gitops.commit_manager import CommitManager
from src.gitops.pr_manager import PullRequestManager
from src.utils.logger import setup_logger

logger = setup_logger("main")

def run_pipeline(request_path: str, mode: str, repo_dir: str = "sample_repo/data_products") -> int:
    """
    Executes the end-to-end access provisioning pipeline.
    """
    load_dotenv()
    
    # 1. Intake Agent Phase
    intake_agent = IntakeAgent()
    try:
        raw_request = intake_agent.process_input(request_path)
    except Exception as e:
        logger.error(f"Intake parsing failed for '{request_path}': {e}")
        print(f"Error parsing request input: {e}")
        return 1

    # 2. Validation Agent Phase
    validation_agent = ValidationAgent()
    normalized_request, validation_result = validation_agent.process_validation(raw_request)

    # 3. Check for validation errors
    if not validation_result.is_valid:
        report = ProvisioningReport(
            request_id=normalized_request.request_id,
            normalized_request=normalized_request,
            validation_passed=False,
            validation_errors=validation_result.errors,
            existing_access_found=False,
            existing_access_message="Validation failed.",
            mode=mode,
            manual_approval_required=True
        )
        summary_agent = SummaryAgent()
        print(summary_agent.generate_summary(report))
        return 1

    # 4. Existing Access Check Phase
    access_check = check_existing_access(normalized_request, repo_dir=repo_dir)

    if access_check.exists:
        report = ProvisioningReport(
            request_id=normalized_request.request_id,
            normalized_request=normalized_request,
            validation_passed=True,
            existing_access_found=True,
            existing_access_message=access_check.message,
            file_modified=None,
            branch_name=None,
            pr_url=None,
            mode=mode,
            manual_approval_required=True
        )
        summary_agent = SummaryAgent()
        print(summary_agent.generate_summary(report))
        return 0

    # 5. Provisioning & GitOps Automation Phase (Access does NOT exist)
    github_client = GitHubClientWrapper(mode=mode)
    branch_mgr = BranchManager(github_client)
    commit_mgr = CommitManager(github_client)
    pr_mgr = PullRequestManager(github_client)

    # a. Create branch
    branch_name = construct_branch_name(normalized_request.request_id, normalized_request.access_type)
    branch_ok, branch_msg = branch_mgr.create_feature_branch(branch_name, repo_dir=repo_dir)

    # b. Modify YAML file & validate syntax
    mod_ok, mod_msg, modified_filepath = modify_yaml_access(normalized_request, repo_dir=repo_dir)
    if not mod_ok:
        logger.error(f"YAML modification failed: {mod_msg}")
        return 1

    # c. Commit changes
    repo_relative_path = os.path.relpath(modified_filepath, start=os.getcwd()).replace("\\", "/")
    commit_msg = f"feat(access): provision {normalized_request.access_type} access for {normalized_request.consumer}"
    commit_ok, commit_sha, commit_res_msg = commit_mgr.commit_yaml_change(
        local_filepath=modified_filepath,
        repo_relative_path=repo_relative_path,
        branch_name=branch_name,
        commit_message=commit_msg,
        repo_dir=repo_dir
    )

    # d. Create Pull Request
    pr_ok, pr_url, pr_msg = pr_mgr.create_pull_request(
        request=normalized_request,
        branch_name=branch_name,
        file_path=modified_filepath
    )

    # 6. Summary Report Phase
    report = ProvisioningReport(
        request_id=normalized_request.request_id,
        normalized_request=normalized_request,
        validation_passed=True,
        existing_access_found=False,
        existing_access_message=access_check.message,
        file_modified=os.path.basename(modified_filepath),
        branch_name=branch_name,
        commit_sha=commit_sha,
        pr_url=pr_url,
        mode=mode,
        manual_approval_required=True
    )

    summary_agent = SummaryAgent()
    print(summary_agent.generate_summary(report))
    return 0

def main():
    parser = argparse.ArgumentParser(description="AI-assisted GitOps Access Provisioning Agent CLI")
    parser.add_argument("--request", required=True, help="Path to request file (JSON or Natural Language text)")
    parser.add_argument("--mode", choices=["local", "github"], default="local", help="Execution mode (local simulation or github API)")
    parser.add_argument("--repo-dir", default="sample_repo/data_products", help="Path to target data products repository directory")

    args = parser.parse_args()
    exit_code = run_pipeline(args.request, args.mode, args.repo_dir)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
