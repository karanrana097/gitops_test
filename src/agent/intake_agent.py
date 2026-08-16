import re
import json
import os
from typing import Dict, Any
from src.core.models import RawAccessRequest
from src.utils.file_utils import read_json_file, read_text_file

class IntakeAgent:
    """
    Agent responsible for ingesting access requests from JSON files, CLI strings, or natural language text files.
    Extracts structured parameters into RawAccessRequest.
    """
    def process_input(self, input_path_or_str: str) -> RawAccessRequest:
        """Processes input file path or raw string."""
        if os.path.exists(input_path_or_str):
            if input_path_or_str.endswith(".json"):
                data = read_json_file(input_path_or_str)
                return RawAccessRequest(**data)
            else:
                raw_text = read_text_file(input_path_or_str)
                return self.parse_natural_language(raw_text)
        elif input_path_or_str.strip().startswith("{"):
            # Direct JSON string
            data = json.loads(input_path_or_str)
            return RawAccessRequest(**data)
        else:
            # Direct Natural Language string
            return self.parse_natural_language(input_path_or_str)

    def parse_natural_language(self, text: str) -> RawAccessRequest:
        """
        Rule-based NLP parser extracting entities using key-value and pattern matching.
        Can be upgraded to LLM (e.g. Gemini / OpenAI) seamlessly in future.
        """
        req_id_match = re.search(r'(?:Request ID|REQ[-_]?ID)[:\s]+([A-Z0-9-]+)', text, re.IGNORECASE)
        consumer_match = re.search(r'(?:Consumer|Consumer Product|Consumer Data Product)[:\s]+([A-Za-z0-9_-]+)', text, re.IGNORECASE)
        provider_match = re.search(r'(?:Provider|Provider Product|Provider Data Product)[:\s]+([A-Za-z0-9_-]+)', text, re.IGNORECASE)
        src_env_match = re.search(r'(?:Source Environment|Source Env|From Env)[:\s]+([A-Za-z0-9_-]+)', text, re.IGNORECASE)
        tgt_env_match = re.search(r'(?:Target Environment|Target Env|To Env)[:\s]+([A-Za-z0-9_-]+)', text, re.IGNORECASE)
        scope_match = re.search(r'(?:Access Scope|Scope)[:\s]+([A-Za-z0-9_-]+)', text, re.IGNORECASE)
        requested_by_match = re.search(r'(?:Requested by|Email|User)[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text, re.IGNORECASE)
        justification_match = re.search(r'(?:Justification|Business Justification)[:\s]+(.+)', text, re.IGNORECASE)

        return RawAccessRequest(
            request_id=req_id_match.group(1) if req_id_match else "REQ-NL-1001",
            consumer=consumer_match.group(1) if consumer_match else "",
            provider=provider_match.group(1) if provider_match else "",
            source_environment=src_env_match.group(1) if src_env_match else "",
            target_environment=tgt_env_match.group(1) if tgt_env_match else "",
            access_scope=scope_match.group(1) if scope_match else "schema",
            requested_by=requested_by_match.group(1) if requested_by_match else "unstructured.user@example.com",
            business_justification=justification_match.group(1).strip() if justification_match else "Extracted from natural language input"
        )
