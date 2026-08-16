import os
from typing import Optional, Any
from src.utils.logger import setup_logger

logger = setup_logger("github_client")

class GitHubClientWrapper:
    """
    Wrapper around PyGithub client to handle authentication and repo access.
    Gracefully falls back when token or repo is not configured or in local mode.
    """
    def __init__(
        self,
        token: Optional[str] = None,
        owner: Optional[str] = None,
        repo_name: Optional[str] = None,
        base_branch: str = "main",
        mode: str = "local"
    ):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.owner = owner or os.getenv("GITHUB_OWNER")
        self.repo_name = repo_name or os.getenv("GITHUB_REPO")
        self.base_branch = base_branch or os.getenv("BASE_BRANCH", "main")
        self.mode = mode.lower()
        self.github_instance = None
        self.repo_instance = None

        if self.mode == "github":
            self._init_github()

    def _init_github(self):
        if not self.token or self.token == "your_token_here":
            logger.warning("GITHUB_TOKEN is missing or set to placeholder. Falling back to simulation details.")
            return

        try:
            from github import Github
            self.github_instance = Github(self.token)
            full_repo_name = f"{self.owner}/{self.repo_name}"
            self.repo_instance = self.github_instance.get_repo(full_repo_name)
            logger.info(f"Connected to GitHub repo: {full_repo_name}")
        except Exception as e:
            logger.error(f"Failed to initialize PyGithub client: {e}")

    def is_connected(self) -> bool:
        return self.mode == "github" and self.repo_instance is not None
