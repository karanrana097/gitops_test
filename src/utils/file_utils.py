import os
import json
import csv
from typing import Any, Dict, List, Optional
import yaml
from ruamel.yaml import YAML

def read_json_file(filepath: str) -> Dict[str, Any]:
    """Reads and parses a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def read_text_file(filepath: str) -> str:
    """Reads raw content from a text file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def read_csv_file(filepath: str) -> List[Dict[str, str]]:
    """Reads CSV file and returns list of row dicts."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def read_yaml_file(filepath: str) -> Dict[str, Any]:
    """Reads YAML file using PyYAML."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"YAML file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def read_yaml_roundtrip(filepath: str) -> tuple[Any, YAML]:
    """Reads YAML preserving comments and structure via ruamel.yaml."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"YAML file not found: {filepath}")
    yaml_obj = YAML()
    yaml_obj.preserve_quotes = True
    yaml_obj.indent(mapping=2, sequence=4, offset=2)
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml_obj.load(f)
    return data, yaml_obj

def write_yaml_roundtrip(filepath: str, data: Any, yaml_obj: Optional[YAML] = None) -> None:
    """Writes YAML preserving structure via ruamel.yaml."""
    if yaml_obj is None:
        yaml_obj = YAML()
        yaml_obj.preserve_quotes = True
        yaml_obj.indent(mapping=2, sequence=4, offset=2)
    with open(filepath, "w", encoding="utf-8") as f:
        yaml_obj.dump(data, f)
