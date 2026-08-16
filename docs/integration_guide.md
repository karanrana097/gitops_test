# Enterprise Integration Guide

This guide details how to extend the POC to integrate with enterprise IT systems.

---

## 1. Jira Service Management Integration

### Architecture
Use Webhooks to trigger the Intake Agent upon ticket creation.

```python
# Integration Blueprint: FastAPI Webhook Listener
from fastapi import FastAPI, Request
from src.agent.intake_agent import IntakeAgent

app = FastAPI()

@app.post("/webhooks/jira-access-request")
async def jira_webhook(request: Request):
    payload = await request.json()
    issue = payload.get("issue", {})
    fields = issue.get("fields", {})
    
    # Map Jira custom fields to RawAccessRequest
    raw_request_dict = {
        "request_id": issue.get("key"),
        "consumer": fields.get("customfield_10100"),  # Consumer Data Product
        "provider": fields.get("customfield_10101"),  # Provider Data Product
        "source_environment": fields.get("customfield_10102", {}).get("value"),
        "target_environment": fields.get("customfield_10103", {}).get("value"),
        "access_scope": fields.get("customfield_10104", {}).get("value"),
        "requested_by": fields.get("reporter", {}).get("emailAddress"),
        "business_justification": fields.get("description")
    }
    
    # Invoke main pipeline logic...
    return {"status": "processing", "issue_key": issue.get("key")}
```

---

## 2. Aspen / Corporate Access Request Form Integration

Connect to Aspen or custom enterprise form endpoints by standardizing form submission webhooks into the `RawAccessRequest` model.

---

## 3. SharePoint Data Product Owner Lookup

Replace `owner_lookup.py` CSV reader with Microsoft Graph API calls:

```python
# SharePoint Graph API Lookup snippet
import requests

def get_owner_from_sharepoint(product_name: str, access_token: str) -> str:
    url = f"https://graph.microsoft.com/v1.0/sites/root/lists/'DataProductRegistry'/items?$filter=fields/Title eq '{product_name}'"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers).json()
    items = resp.get("value", [])
    if items:
        return items[0]["fields"]["OwnerEmail"]
    return "unknown.owner@example.com"
```

---

## 4. Databricks Unity Catalog Metadata Lookup

Query Databricks System Tables or Unity Catalog REST API:

```python
# Databricks Unity Catalog SDK snippet
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

def get_unity_catalog_owner(catalog_name: str) -> str:
    catalog = w.catalogs.get(catalog_name)
    return catalog.owner
```

---

## 5. Jenkins Post-Merge Pipeline Automation

Trigger Jenkins pipeline after PR merge event via GitHub Webhook:

```yaml
# GitHub Webhook -> Jenkins Trigger
# Jenkinsfile snippet
pipeline {
    agent any
    stages {
        stage('Sync Databricks Grants') {
            steps {
                sh 'python scripts/apply_gitops_grants.py --manifest sample_repo/data_products/'
            }
        }
    }
}
```

---

## 6. LLM-Based Natural Language Request Parsing

Upgrade `IntakeAgent.parse_natural_language()` to use Google Gemini API:

```python
# LLM Integration via Google GenAI SDK
import google.generativeai as genai
from src.core.models import RawAccessRequest

def parse_with_gemini(text: str) -> RawAccessRequest:
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Extract the following fields from this access request text as JSON:
    request_id, consumer, provider, source_environment, target_environment, access_scope, requested_by, business_justification.
    
    Text: {text}
    """
    response = model.generate_content(prompt)
    # Parse JSON response into RawAccessRequest...
```
