# Stakeholder Demo Guide & Script

Use this script to present the **AI-assisted GitOps Access Provisioning Agent** POC to stakeholders, architects, and engineering leadership.

---

## Demo Agenda (15 Minutes)

1. **Introduction & Context (3 min)**: Manual pain points vs. Hybrid Agentic GitOps automation.
2. **Scenario 1: Valid Cross-Product Access Provisioning (4 min)**: Ingestion, normalization, validation, YAML update, branch & PR generation.
3. **Scenario 2: Duplicate Access Prevention (3 min)**: Pre-existing access detection.
4. **Scenario 3: Validation Safeguards (2 min)**: Prefix and environment rule enforcement.
5. **Governance & Q&A (3 min)**: Human-in-the-loop safeguards and enterprise architecture.

---

## Step-by-Step Presentation Script

### Step 1: Initialize Environment
Open terminal in `ai-gitops-access-agent/` directory:

```bash
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### Step 2: Demo Scenario 1 - Valid Access Request

**Presenter Talking Points:**
> "Let's look at a standard access request where `DS_TDA_Governance_LH` requests `dev` to `prod` schema access to data product `DS_Digital_AB_Testing_Evaluation_LH`."

**Command:**
```bash
python src/main.py --request sample_requests/request_valid.json --mode local
```

**What to Point Out:**
- Notice how the agent automatically strips `_LH` suffixes and converts underscores to hyphens.
- Validation checks pass against allowed prefixes (`DS-`) and environment whitelists.
- The system inspects `DS-Digital-AB-Testing-Evaluation.yaml` and finds no existing `dev_to_prod` permission entry.
- Feature branch `feature/REQ-1001-dev-to-prod-access` is created.
- The YAML manifest is updated with `status: pending_pr` and syntax-checked.
- A pull request is generated with an explicit human approval checklist.

---

### Step 3: Demo Scenario 2 - Pre-Existing Access Prevention

**Presenter Talking Points:**
> "What happens if a user requests access that was already granted? The system must be idempotent and prevent duplicate entries."

**Command:**
```bash
python src/main.py --request sample_requests/request_existing_access.json --mode local
```

**What to Point Out:**
- The existing access check scans the YAML permissions array and detects `dev_to_dev` access already exists.
- The system prints `Existing Access: Found`, halts execution without editing the YAML file, and creates no branch or PR.

---

### Step 4: Demo Scenario 3 - Validation Error Handling

**Presenter Talking Points:**
> "Now let's demonstrate governance safeguards when incoming request data violates naming conventions or policies."

**Command:**
```bash
python src/main.py --request sample_requests/request_invalid_name.json --mode local
```

**What to Point Out:**
- The agent flags invalid prefixes (`INVALID_Consumer`), invalid environments (`sandbox`, `production`), and invalid access scopes (`database`).
- Clear error messages are reported in the audit log, preventing invalid configurations from entering version control.

---

### Step 5: Demo Scenario 4 - Unstructured Natural Language Intake

**Presenter Talking Points:**
> "Finally, let's process an unstructured natural language email/ticket request."

**Command:**
```bash
python src/main.py --request sample_requests/request_natural_language.txt --mode local
```

**What to Point Out:**
- The `IntakeAgent` extracts entities directly from free-form text into structured request models.

---

## Key Takeaways for Leadership

- **Speed & Efficiency**: Reduces provisioning overhead from hours to seconds.
- **Data Quality & Syntax Safety**: Eliminates human YAML formatting errors.
- **Audit & Compliance**: Full Git history for all permissions changes.
- **Safety**: Approvals and merges remain 100% human-controlled.
