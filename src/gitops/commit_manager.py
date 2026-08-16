import os
from typing import Tuple, Optional
from src.gitops.github_client import GitHubClientWrapper
from src.utils.file_utils import read_text_file
from src.utils.logger import setup_logger

logger = setup_logger("commit_manager")

class CommitManager:
    def __init__(self, github_client: GitHubClientWrapper):
        self.github_client = github_client

    def _is_git_repo(self, path: str) -> bool:
        try:
            import subprocess
            res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=path, capture_output=True, text=True)
            return res.returncode == 0 and res.stdout.strip() == "true"
        except Exception:
            return False

    def commit_yaml_change(
        self,
        local_filepath: str,
        repo_relative_path: str,
        branch_name: str,
        commit_message: str,
        repo_dir: str = "."
    ) -> Tuple[bool, Optional[str], str]:
        """
        Commits modified YAML to GitHub remote, real local Git repo, or simulates commit locally.
        Returns (success, commit_sha, message).
        """
        if self.github_client.is_connected():
            try:
                repo = self.github_client.repo_instance
                content = read_text_file(local_filepath)
                
                # Check if file exists on target branch
                try:
                    remote_file = repo.get_contents(repo_relative_path, ref=branch_name)
                    commit_res = repo.update_file(
                        path=repo_relative_path,
                        message=commit_message,
                        content=content,
                        sha=remote_file.sha,
                        branch=branch_name
                    )
                    sha = commit_res["commit"].sha
                    logger.info(f"Updated {repo_relative_path} on branch {branch_name} (commit {sha[:7]})")
                    return True, sha, f"Committed update to {repo_relative_path}"
                except Exception:
                    # File does not exist remotely, create it
                    commit_res = repo.create_file(
                        path=repo_relative_path,
                        message=commit_message,
                        content=content,
                        branch=branch_name
                    )
                    sha = commit_res["commit"].sha
                    logger.info(f"Created {repo_relative_path} on branch {branch_name} (commit {sha[:7]})")
                    return True, sha, f"Committed new file {repo_relative_path}"
            except Exception as e:
                logger.error(f"Failed to commit file to GitHub: {e}")
                return False, None, str(e)
        else:
            # Check if local directory is a real git repository
            if self._is_git_repo(repo_dir):
                try:
                    import subprocess
                    subprocess.run(["git", "add", local_filepath], cwd=repo_dir, check=True, capture_output=True)
                    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_dir, check=True, capture_output=True)
                    res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, check=True, capture_output=True, text=True)
                    sha = res.stdout.strip()
                    logger.info(f"[LOCAL GIT REPO] Committed change on branch {branch_name} (Commit SHA: {sha[:7]})")
                    return True, sha, f"Committed change to {repo_relative_path} (SHA: {sha[:7]})"
                except Exception as e:
                    logger.warning(f"Local git commit warning: {e}")

            # Local simulation mode fallback
            simulated_sha = "simulated_sha_" + os.urandom(4).hex()
            logger.info(f"[LOCAL SIMULATION] Committed change to {repo_relative_path} on branch {branch_name} (SHA: {simulated_sha[:7]})")
            return True, simulated_sha, f"[SIMULATED] Change committed to {repo_relative_path}"

