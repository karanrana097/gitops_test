import os
from typing import Optional
from src.utils.file_utils import read_csv_file, read_yaml_file

class DataProductOwnerLookup:
    """
    Lookup service for resolving data product ownership details from CSV map or YAML specs.
    """
    def __init__(self, csv_filepath: str = "config/owner_mapping.csv", sample_repo_dir: str = "sample_repo/data_products"):
        self.csv_filepath = csv_filepath
        self.sample_repo_dir = sample_repo_dir
        self._cache = {}

    def lookup_owner(self, data_product_name: str) -> Optional[str]:
        """Looks up product owner email address."""
        if not data_product_name:
            return None
        
        # 1. Try CSV lookup
        if os.path.exists(self.csv_filepath):
            rows = read_csv_file(self.csv_filepath)
            for row in rows:
                if row.get("data_product") == data_product_name:
                    return row.get("owner")

        # 2. Try YAML repo file lookup
        yaml_filename = f"{data_product_name}.yaml"
        yaml_path = os.path.join(self.sample_repo_dir, yaml_filename)
        if os.path.exists(yaml_path):
            try:
                content = read_yaml_file(yaml_path)
                return content.get("owner")
            except Exception:
                pass

        return None
