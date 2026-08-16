# AI-assisted GitOps Access Provisioning Agent

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture: Hybrid Agentic GitOps](https://img.shields.io/badge/Architecture-Hybrid%20Agentic%20GitOps-green.svg)](#proposed-hybrid-architecture)

> A production-grade Proof of Concept (POC) demonstrating **AI-assisted, automated cross-data product access provisioning** using a hybrid architecture combining rule-based/agentic intake with deterministic GitOps Python automation.

---

## Executive Summary & Problem Statement

In enterprise data meshes and data lakehouses, data product consumers frequently require cross-data product access across environments (`dev`, `qa`, `stage`, `prod`). 

Historically, this manual process required data engineers to:
1. Parse unstructured access request tickets.
2. Manually verify data product naming conventions and owner mappings.
3. Inspect version-controlled YAML permissions manifests across repositories.
4. Manually edit permissions files, create Git branches, and open pull requests.

This manual workflow introduced significant operational friction, long turnaround times, duplicate access entries, and human errors in YAML syntax formatting.

---

## Current Manual Process vs. Automated POC

```
[ Manual Workflow ]
Request Ticket -> Human Parsing -> Manual Owner Lookup -> Manual Repo Inspection -> Manual YAML Edit -> Manual Branch & PR -> Manual Review -> Pipeline Merge

[ Hybrid Agentic GitOps POC ]
Request Input -> Agentic Intake & Normalization -> Rule-based Validation -> Automated YAML Check -> Deterministic YAML Edit & Git Branch -> Automated PR Creation -> [HUMAN IN THE LOOP: Owner Approval & PR Review & Merge]
```

### What is Automated:
- Intake ingestion (JSON files, CLI payloads, or natural language text).
- Data product name normalization (e.g., stripping `_LH` suffixes, converting `_` to `-`).
- Policy validation (prefix checks, environment whitelist, access scope verification).
- Automated ownership lookup from CSV/YAML registries.
- Detection of existing permissions to prevent duplicate entries.
- Validated YAML modification preserving formatting and comments (`ruamel.yaml`).
- Feature branch creation (`feature/<request_id>-<access_type>-access`).
- Commit creation and pull request generation (GitHub API or Local Simulation).
- Executive CLI audit summary generation.

### What Remains Strictly Manual (Human-in-the-Loop Safeguards):
- **Data Product Owner Approval**: Access permissions require explicit sign-off.
- **Pull Request Review & Merge**: Human peer review and code merge are mandatory.
- **Production Pipeline Execution**: Pipeline triggers after merge remain controlled by enterprise CI/CD gates.

---

## Proposed Hybrid Architecture

The architecture enforces a strict boundary between **Agentic Intelligence** and **Deterministic Automation**:

```
                              +---------------------------------------+
                              |         Incoming Access Request        |
                              |   (JSON / CLI / Natural Language)     |
                              +---------------------------------------+
                                                  |
                                                  v
                              +---------------------------------------+
                              |             Agentic Layer             |
                              |  - IntakeAgent: Structured parsing    |
                              |  - ValidationAgent: Normalization &   |
                              |    Rule Validation & Owner Resolution |
                              +---------------------------------------+
                                                  |
                                                  v
                              +---------------------------------------+
                              |     Deterministic Core Logic Layer    |
                              |  - Existing Access Checker            |
                              |  - Validated YAML Modifier            |
                              +---------------------------------------+
                                                  |
                                                  v
                              +---------------------------------------+
                              |          GitOps Automation            |
                              |  - BranchManager: Feature branch      |
                              |  - CommitManager: Git commit          |
                              |  - PullRequestManager: GitHub PR      |
                              +---------------------------------------+
                                                  |
                                                  v
                              +---------------------------------------+
                              |             Summary Agent             |
                              |  - CLI & Executive Audit Summary      |
                              |  - Human-in-the-Loop Governance Notice|
                              +---------------------------------------+
```

---

## Project Structure

```
ai-gitops-access-agent/
│
├── README.md                          # Comprehensive documentation & guide
├── requirements.txt                   # Python package dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
│
├── config/
│   ├── settings.yaml                  # System rules, prefixes, environment specs
│   └── owner_mapping.csv              # Product owner mapping table
│
├── sample_requests/
│   ├── request_valid.json             # Valid access request sample
│   ├── request_existing_access.json   # Request for pre-existing permission
│   ├── request_invalid_name.json      # Invalid request (failing validation)
│   └── request_natural_language.txt   # Unstructured natural language request
│
├── sample_repo/
│   └── data_products/                 # Mock enterprise GitOps repository
│       ├── DS-Digital-AB-Testing-Evaluation.yaml
│       ├── DS-TDA-Governance.yaml
│       └── CADP-Customer-Insights.yaml
│
├── src/
│   ├── main.py                        # CLI application entry point
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── intake_agent.py            # Parses JSON & Natural Language
│   │   ├── validation_agent.py        # Normalizes & checks rules
│   │   └── summary_agent.py           # Formats audit reports
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py                  # Pydantic data models
│   │   ├── normalizer.py              # Name cleaning & access_type builder
│   │   ├── validator.py               # Governance policy validator
│   │   ├── owner_lookup.py            # Owner resolution service
│   │   ├── yaml_access_checker.py     # Existing permission checker
│   │   ├── yaml_modifier.py           # YAML modification & syntax check
│   │   └── report_generator.py        # CLI report formatter
│   │
│   ├── gitops/
│   │   ├── __init__.py
│   │   ├── github_client.py           # PyGithub / API wrapper
│   │   ├── branch_manager.py          # Feature branch manager
│   │   ├── commit_manager.py          # Commit manager
│   │   └── pr_manager.py              # Pull Request manager
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                  # Standardized logging
│       └── file_utils.py              # YAML, JSON, CSV & text file IO
│
├── tests/
│   ├── test_normalizer.py             # Normalizer unit tests
│   ├── test_validator.py              # Validator unit tests
│   ├── test_yaml_access_checker.py    # Access checker unit tests
│   └── test_yaml_modifier.py          # YAML modifier unit tests
│
└── docs/
    ├── architecture.md                # System architecture documentation
    ├── integration_guide.md           # Enterprise integration blueprints
    └── demo_guide.md                  # Stakeholder presentation demo script
```

---

## Quick Start & Setup Instructions

### Environment Setup (Windows)

Open Command Prompt or PowerShell:

```cmd
:: 1. Navigate to project folder
cd ai-gitops-access-agent

:: 2. Create virtual environment
python -m venv .venv

:: 3. Activate virtual environment
.venv\Scripts\activate

:: 4. Install dependencies
pip install -r requirements.txt

:: 5. Copy environment template
copy .env.example .env
```

### Environment Setup (macOS / Linux)

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env configuration file
cp .env.example .env
```

---

## Running the Agent

### Mode 1: Local Simulation Mode (Default)

Does not require GitHub credentials or internet access. Operates safely on files in `sample_repo/`.

**Run Valid Request:**
```bash
python src/main.py --request sample_requests/request_valid.json --mode local
```

**Run Existing Access Request:**
```bash
python src/main.py --request sample_requests/request_existing_access.json --mode local
```

**Run Invalid Request (Validation Failure):**
```bash
python src/main.py --request sample_requests/request_invalid_name.json --mode local
```

**Run Natural Language Request:**
```bash
python src/main.py --request sample_requests/request_natural_language.txt --mode local
```

---

### Mode 2: Real GitHub Mode

To execute live branch creation, commits, and PRs against a GitHub repository:

1. Edit `.env` with your credentials:
```env
GITHUB_TOKEN=ghp_your_personal_access_token_here
GITHUB_OWNER=your_github_username_or_org
GITHUB_REPO=your_repository_name
BASE_BRANCH=main
MODE=github
```

2. Execute CLI:
```bash
python src/main.py --request sample_requests/request_valid.json --mode github
```

---

## Sample Input & Output

### Sample Input (`sample_requests/request_valid.json`)

```json
{
  "request_id": "REQ-1001",
  "consumer": "DS_TDA_Governance_LH",
  "provider": "DS_Digital_AB_Testing_Evaluation_LH",
  "source_environment": "dev",
  "target_environment": "prod",
  "access_scope": "schema",
  "requested_by": "sample.user@example.com",
  "business_justification": "Need dev to prod access for governance validation"
}
```

### Sample Terminal Output

```text
========================================
AI-assisted GitOps Access Provisioning
========================================

Request ID: REQ-1001

Normalized Request:
Consumer: DS-TDA-Governance
Provider: DS-Digital-AB-Testing-Evaluation
Access: dev_to_prod
Scope: schema

Validation: Passed

Existing Access: Not Found

Action Taken:
- Feature branch created: feature/REQ-1001-dev-to-prod-access
- YAML updated: DS-Digital-AB-Testing-Evaluation.yaml
- YAML validation passed
- Pull request created or simulated

Manual Step Required:
- Product owner approval must be confirmed manually
- PR must be reviewed and approved manually
- Merge must be performed by authorized reviewer

========================================
```

---

## Running Unit Tests

Execute the comprehensive unit test suite:

```bash
python -m pytest tests/ -v
```

---

## Security & Governance Principles

1. **Never Approve Automatically**: The agent prepares requests; product owners decide.
2. **Never Merge PR Automatically**: Peer review ensures code control.
3. **Never Deploy Automatically**: Production releases require standard pipeline gates.
4. **Credential Isolation**: GitHub tokens are loaded strictly via `.env` environment variables. No secrets are stored in code.
5. **YAML Preserving**: Formatting and comment structures are preserved during modification.
6. **Idempotent Execution**: Duplicate access requests are detected before file edits or branch creation.

---

## Limitations

- **Rule-based NLP**: Natural language parsing currently uses regex pattern matching. Can be enhanced with LLMs.
- **Local Ownership Lookup**: Product owner lookup currently uses a static CSV mapping table or file header metadata.
- **Single File Modification**: Each request currently targets a single provider YAML file.

---

## Future Enhancements & Integration Roadmap

1. **Jira Integration**: Automatically consume tickets from Jira service management webhooks.
2. **Aspen Form Integration**: Direct ingestion from corporate access request forms.
3. **SharePoint Owner Lookup**: Query enterprise SharePoint list / Graph API for product owners.
4. **Approval Task Creation**: Automatically trigger approval workflows in Jira / ServiceNow.
5. **Approval Status Polling**: Wait for owner approval before initiating GitOps automation.
6. **Teams / Slack Notifications**: Send real-time updates to product owners.
7. **Jenkins Pipeline Trigger**: Post-merge webhook to invoke automated provisioning jobs.
8. **Databricks Table Lookup**: Query Unity Catalog metadata for product ownership.
9. **LLM-Based Parser**: Plug in Gemini / OpenAI API for advanced ambiguous request parsing.
10. **Audit Logging**: Write structured JSON audit logs to CloudWatch / Datadog.
11. **Role-Based Access Control (RBAC)**: Enforce consumer access request limits based on user role.
12. **Human Approval Dashboard**: Web-based UI for approving pending GitOps access requests.

---

## Demo Script for Stakeholder Presentation

See [docs/demo_guide.md](docs/demo_guide.md) for a complete step-by-step presentation script.
