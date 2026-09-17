# Master Migration Execution Plan
## Legacy DFCX (`agent-bell-voice-central-ccaip`) $\rightarrow$ Target CXAS Agent (`Telco Voice Central`)

> [!IMPORTANT]
> This Master Migration Plan details the step-by-step roadmap to migrate Bell Canada's legacy Dialogflow CX agent `agent-bell-voice-central-ccaip` to a production-ready Customer Engagement Suite (CXAS) agent fully aligned with `PRD-TelcoVoiceCentralAIVoiceAssistant.md` and passing the 70 public evaluation benchmarks in `agent_migration_public_evals.md`.

---

## 1. End-to-End Migration Architecture

```mermaid
graph TD
    subgraph Phase 0: Prerequisites & Setup
        SrcDir[".artifacts/agent-bell-voice-central-ccaip (DFCX Export)"]
        EnvSetup["Python 3.10+ & cxas_scrapi Virtual Environment"]
    end

    subgraph Phase 1: 1:1 Base Migration
        MigrateScript["python .agents/skills/cxas-dfcx-migration/scripts/migrate.py"]
        IRBundle["target_ir.json Bundle Persistent Storage"]
        BaseResources["Deploy Base Resources: app.json, {variables}, Tools"]
    end

    subgraph Phase 2: Stage 1 Optimization (Grouping & Dedup)
        Stage1Script["python .agents/skills/cxas-dfcx-migration/scripts/stage_1.py"]
        VarDedup["Deduplicate 150+ $session.params -> 60 Scoped {variables}"]
        AgentConsolidation["Consolidate 72 Playbooks -> 8 Modules (M1 to M8)"]
    end

    subgraph Phase 3: Stage 2 Optimization (Prompts & Tools)
        Stage2Script["python .agents/skills/cxas-dfcx-migration/scripts/stage_2.py"]
        PromptInject["Inject BR-TV-001..020 & 6 Policy Guardrails into instructions.md"]
        VerbatimCopy["Enforce Verbatim Copy Library (10 keys)"]
        OpenAPITools["Convert 63 Webhooks -> OpenAPI 3.0 Tool Specs & Mocks"]
    end

    subgraph Phase 4: Stage 3 Topology Rewiring
        Stage3Script["python .agents/skills/cxas-dfcx-migration/scripts/stage_3.py --architecture hub-and-spoke"]
        RootAgent["Set M1 (Session Lifecycle) as Root Agent Hub"]
        SpokeConnections["Wire Child Delegates: M2, M3, M4, M5, M6, M7, M8"]
    end

    subgraph Phase 5: Evaluation & Quality Assurance
        SimEval["cxas-sim-eval / cxas eval run"]
        PublicEvals["Run 70 Public Evals (agent_migration_public_evals.md)"]
        PassCriteria["Verify >= 90% Pass Rate & Zero PII Hallucinations"]
    end

    SrcDir & EnvSetup --> MigrateScript
    MigrateScript --> IRBundle & BaseResources
    IRBundle --> Stage1Script
    Stage1Script --> VarDedup & AgentConsolidation
    VarDedup & AgentConsolidation --> Stage2Script
    Stage2Script --> PromptInject & VerbatimCopy & OpenAPITools
    PromptInject & VerbatimCopy & OpenAPITools --> Stage3Script
    Stage3Script --> RootAgent & SpokeConnections
    RootAgent & SpokeConnections --> SimEval
    SimEval --> PublicEvals --> PassCriteria
```

---

## 2. Phase-by-Phase Execution Roadmap

### Phase 0: Environment Setup & Pre-Flight Checklist
- **Command:**
  ```bash
  gcloud auth application-default login
  .venv/bin/python -m pip install -e .
  ```
- **Configuration Inputs:**
  - `SOURCE_AGENT`: `.artifacts/agent-bell-voice-central-ccaip`
  - `TARGET_NAME`: `telco_voice_central_cxas`
  - `PROJECT_ID`: Target GCP Project ID
  - `LOCATION`: `us` *(Do NOT use `global` for CXAS app creation)*
  - `MODEL`: `gemini-2.5-flash`

---

### Phase 1: 1:1 Base Migration (`migrate.py`)
- **Objective:** Ingest the legacy DFCX JSON export, extract all 4 flows, 57 pages, 72 playbooks, and 63 webhooks into an intermediate representation (`<target>_ir.json`), and deploy base application manifests.
- **Execution Command:**
  ```bash
  .venv/bin/python .agents/skills/cxas-dfcx-migration/scripts/migrate.py \
    --source-agent-id ".artifacts/agent-bell-voice-central-ccaip" \
    --project-id <PROJECT_ID> --location us \
    --target-name telco_voice_central_cxas --yes
  ```
- **Outputs Created:**
  - `telco_voice_central_cxas_ir.json` (IR Bundle)
  - `telco_voice_central_cxas_tree_preview.html` (Pre-flight structural tree)

---

### Phase 2: Stage 1 Optimization (`stage_1.py`)
- **Objective:** Run parameter deduplication and structural grouping to reduce agent fragmentation.
- **Key Tasks:**
  1. **Variable Deduplication:** Deduplicate **150+ `$session.params`** into **60 CXAS `{variables}`** across 4 namespaces:
     - *Identity:* `{clid}`, `{tfn}`, `{cirn}`, `{billing_account}`, `{customer_type}`
     - *Auth State:* `{auth_status}`, `{identification_status}`, `{business_flag}`
     - *Routing:* `{route}`, `{lob}`, `{tv_sub_type}`, `{language}`, `{dtmf_digits}`
     - *Counters:* `{local_noinput_counter}`, `{no_match_confirmation_count}`, `{global_err_count}`
  2. **N$\rightarrow$M Agent Consolidation:** Consolidate 72 playbooks into **8 Target Functional Sub-Agents (`M1`–`M8`)**:
     - `M1`: Session Lifecycle & Routing
     - `M2`: Authentication & Identity (3-Tier Auth Gatekeeper)
     - `M3`: Billing & Payment
     - `M4`: Technical Support & Virtual Repair
     - `M5`: Sales & Equipment
     - `M6`: Appointments & Tickets
     - `M7`: Account Management
     - `M8`: Secondary Language Fallback (`fr-ca`)
- **Execution Command:**
  ```bash
  .venv/bin/python .agents/skills/cxas-dfcx-migration/scripts/stage_1.py \
    --target-name telco_voice_central_cxas
  ```

---

### Phase 3: Stage 2 Optimization (`stage_2.py`)
- **Objective:** Synthesize state-machine instruction prompts (`instructions.md`), bind OpenAPI 3.0 tools, and enforce global behavioral rules.
- **Key Tasks:**
  1. **Behavioral Rules Injection:** Inject `BR-TV-001` to `BR-TV-020` into sub-agent prompts.
  2. **Public Evals Guardrails Enforcement:**
     - **$\$25.00$ Self-Service Refund Cap** in `M3` (escalates to specialist if $> \$25$).
     - **Mandatory Contract Disclosure** in `M7` for cancellations and port-outs.
     - **Step-Up Authentication** in `M7` / `M2` for disabling MFA.
     - **Warranty Physical/Water Damage Screening** and **Swollen Battery Safety Priority** in `M5`.
     - **Multi-Step Auth Locking** across pivots in `app.json`.
  3. **Verbatim Copy Library:** Lock 10 verbatim strings (`greeting_main`, `recording_notice`, `id_verification_otp`, `live_agent_handoff`, `business_handoff`, `refund_confirmation_pattern`, `empathy_protocol`, `outage_active`, `transfer_to_specialist`).
  4. **OpenAPI Tool Conversion:** Convert 63 legacy REST webhooks to OpenAPI 3.0 specs with mock response generators.
- **Execution Command:**
  ```bash
  .venv/bin/python .agents/skills/cxas-dfcx-migration/scripts/stage_2.py \
    --target-name telco_voice_central_cxas
  ```

---

### Phase 4: Stage 3 Topology Rewiring (`stage_3.py`)
- **Objective:** Wire parent-child agent topology according to Spoke-Hub architecture.
- **Key Tasks:**
  - Set `M1` (Session Lifecycle & Routing) as the `root_agent` hub.
  - Wire `M2` through `M8` as child delegate spokes under `M1`.
  - Ensure full `{variables}` payload is propagated during inter-agent transitions and live-agent transfers (`BR-TV-015`).
- **Execution Command:**
  ```bash
  .venv/bin/python .agents/skills/cxas-dfcx-migration/scripts/stage_3.py \
    --target-name telco_voice_central_cxas \
    --architecture hub-and-spoke
  ```

---

### Phase 5: Evaluation & Quality Assurance Validation
- **Objective:** Run the automated evaluation suite against the 70 public evaluations in `agent_migration_public_evals.md`.
- **Target Pass Criteria:**
  - Overall Evaluation Pass Rate: **$\ge 90\%$** (across all 70 test scenarios).
  - Routing Accuracy across `M1`–`M8`: **$\ge 95\%$**.
  - PII Redaction & Zero Hallucination: **$100\%$ compliance** (0 plaintext PIN/OTP echoing, 0 unverified account balances).
- **Execution Command:**
  ```bash
  cxas eval run --app-name telco_voice_central_cxas --eval-file .artifacts/telco_voice_central_cxas_unit_tests.json
  ```

---

## 3. Summary of Deliverables & Output Artifacts

| Deliverable Artifact | Description | Status |
|---|---|---|
| [`prd_agent_bell_voice_central_ccaip.md`](file:///usr/local/google/home/sofiamejiamuro/src/gecx-fde-bootcamp/telco-migration-agent/.artifacts/prd_agent_bell_voice_central_ccaip.md) | Reverse-Engineered DFCX Product Requirement Document | **Complete** |
| [`fsd_agent_bell_voice_central_ccaip.md`](file:///usr/local/google/home/sofiamejiamuro/src/gecx-fde-bootcamp/telco-migration-agent/.artifacts/fsd_agent_bell_voice_central_ccaip.md) | Reverse-Engineered DFCX Functional Specification Document | **Complete** |
| [`audit_asset_inventory_bell_voice.md`](file:///usr/local/google/home/sofiamejiamuro/src/gecx-fde-bootcamp/telco-migration-agent/.artifacts/audit_asset_inventory_bell_voice.md) | Asset Inventory (63 Webhooks, Data Stores, 150+ Params) | **Complete** |
| [`migration_gap_analysis.md`](file:///usr/local/google/home/sofiamejiamuro/src/gecx-fde-bootcamp/telco-migration-agent/.artifacts/migration_gap_analysis.md) | Gap Analysis & 70 Public Evals Alignment Report | **Complete** |
| [`migration_plan_bell_voice.md`](file:///usr/local/google/home/sofiamejiamuro/src/gecx-fde-bootcamp/telco-migration-agent/.artifacts/migration_plan_bell_voice.md) | Master Migration Execution Plan (This Document) | **Complete** |
