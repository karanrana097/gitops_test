import os
import subprocess
from typing import Tuple
from src.gitops.github_client import GitHubClientWrapper
from src.utils.logger import setup_logger

logger = setup_logger("branch_manager")

def construct_branch_name(request_id: str, access_type: str) -> str:
    """Generates standardized branch name e.g. feature/REQ-1001-dev-to-prod-access."""
    req_clean = request_id.replace(" ", "-")
    acc_clean = access_type.replace("_", "-")
    return f"feature/{req_clean}-{acc_clean}-access"

class BranchManager:
    def __init__(self, github_client: GitHubClientWrapper):
        self.github_client = github_client

    def _is_git_repo(self, path: str) -> bool:
        try:
            res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=path, capture_output=True, text=True)
            return res.returncode == 0 and res.stdout.strip() == "true"
        except Exception:
            return False

    def create_feature_branch(self, branch_name: str, repo_dir: str = ".") -> Tuple[bool, str]:
        """
        Creates feature branch on GitHub remote, real local Git repo, or simulates branch creation.
        """
        if self.github_client.is_connected():
            try:
                repo = self.github_client.repo_instance
                base_branch_name = self.github_client.base_branch
                base_ref = repo.get_git_ref(f"heads/{base_branch_name}")
                base_sha = base_ref.object.sha
                
                # Check if branch already exists
                try:
                    repo.get_git_ref(f"heads/{branch_name}")
                    logger.info(f"Branch {branch_name} already exists on GitHub.")
                    return True, f"Existing branch {branch_name} reused"
                except Exception:
                    pass

                repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_sha)
                logger.info(f"Created branch {branch_name} on GitHub from {base_branch_name} ({base_sha[:7]})")
                return True, f"GitHub branch {branch_name} created"
            except Exception as e:
                logger.error(f"Failed to create GitHub branch {branch_name}: {e}")
                return False, str(e)
        else:
            # Check if local directory is a real git repository
            if self._is_git_repo(repo_dir):
                try:
                    res = subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_dir, capture_output=True, text=True)
                    if res.returncode != 0:
                        subprocess.run(["git", "checkout", branch_name], cwd=repo_dir, capture_output=True, text=True)
                    
                    # Try pushing feature branch to origin remote
                    push_res = subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=repo_dir, capture_output=True, text=True)
                    if push_res.returncode == 0:
                        logger.info(f"[REAL GITHUB REMOTE] Created & pushed branch '{branch_name}' to origin.")
                    else:
                        logger.info(f"[LOCAL GIT REPO] Created & checked out real git branch: {branch_name}")
                    return True, f"Real git branch '{branch_name}' created"
                except Exception as e:
                    logger.warning(f"Local git branch creation warning: {e}")

            # Local mode simulation fallback
            logger.info(f"[LOCAL SIMULATION] Created feature branch: {branch_name}")

