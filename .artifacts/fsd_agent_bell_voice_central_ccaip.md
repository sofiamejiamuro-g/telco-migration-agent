# Functional Specification Document (FSD)
## Agent: `agent-bell-voice-central-ccaip`

> [!NOTE]
> This document outlines the technical architecture, dialog flow state machine, playbook organization, parameter specifications, and integration design for `agent-bell-voice-central-ccaip`.

---

## 1. System Architecture Overview

`agent-bell-voice-central-ccaip` uses a hybrid execution engine:
1. **Deterministic Flows & State Pages:** 4 structured flows with 57 total pages handling transactional logic (e.g., date formatting, interval validation, SMS triggers).
2. **Generative Playbooks:** 72 specialized Playbooks powered by Gemini 2.5 Flash for natural language intake, intent disambiguation, and user instruction parsing.
3. **Webhook Integration Layer:** 63 REST API webhooks connecting to Bell enterprise backends (IBM Middleware, DEAI, WFAS, ACUT, OMF, AQD, CPM).

```
+-----------------------------------------------------------------------------------+
|                            CCAIP Telephony Platform                               |
+-----------------------------------------------------------------------------------+
                                        | (Voice / SIP)
                                        v
+-----------------------------------------------------------------------------------+
|                        Google CXAS / DFCX Agent Engine                            |
|  +-------------------------------------+  +------------------------------------+  |
|  |     Deterministic Flows (4)         |  |      Generative Playbooks (72)     |  |
|  | - intake & order summary (Default)  |  | - bell_UC_Technical_Support        |  |
|  | - acut_change_reschedule_ticket     |  | - bell_UC_Billing                  |  |
|  | - tech_visit_cancel_flow            |  | - bell_UC_Account_Management       |  |
|  | - appt_mgmt_mya_pitch_1              |  | - bell_rehit_confirmation          |  |
|  | - rehit_Sat_TV                      |  | - bell_UC_Disambiguation           |  |
|  +-------------------------------------+  +------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                        | (REST Webhooks)
                                        v
+-----------------------------------------------------------------------------------+
|                           Bell Middleware & Backends                              |
|  [WFAS Calendar] [ACUT Trouble Tkt] [OMF Orders] [IBM MW Authentication] [AQD]    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Flows & Page Specifications

### 2.1. Default Flow (`00000000-0000-0000-0000-000000000000`)
- **Role:** Agent root intake and order summary evaluation.
- **Pages (20):**
  - `Categorize LOB - ACUT`
  - `Check LOB` & `Check LOB - OMF summary`
  - `Check Find response` & `Check OMF Order Summary response`
  - `Check number of ACUT tickets`
  - `%5bwhk%5d ACUT Search Find - Home phone`, `Internet`
  - `%5bwhk%5d OMF Order Summary - Homephone`, `Internet`, `TV`
  - `If correct ACUT ticket?` / `If correct OMF ticket?`
  - `Global Error handling` & `Webhook Failure - Troubleshooting Intents`

### 2.2. Reschedule & Ticket Management Flow (`bell_ticket_mgmt_acut_change_reschedule_ticket`)
- **Role:** Handles complex appointment rescheduling, slot confirmation, WFAS calendar integration, date validation.
- **Pages (40):**
  - `Appointment Prerequisite`, `Ask Date Again`, `Ask Time Slot`, `Ask What Day Works`
  - `Date Confirmation`, `Date Formatter`, `Date Outside Range Check`
  - `Earliest Available Appointment Check`, `Earliest Available Appointment Details`
  - `Interval Check`, `Dynamic Interval Names`, `Time Slot Confirmation`
  - `Webhook - ACUT Modify`, `Webhook - WFAS Appointment`, `Webhook - WFAS Cancel`, `Webhook - WFAS Check Availability`
  - `Summarize Updated Appointment`, `MYA Pitch 2`

### 2.3. Field Tech Visit Cancel Flow (`bell_tech_field_tech_visit_cancel_flow`)
- **Role:** Handles cancellation of field technician visits.
- **Pages (3):** `Webhook MYA Eligibility`, `SMS Mya`, `SMS Appointment Changes`.

### 2.4. MYA Pitch Flow (`bell_appt_mgmt_mya_pitch_1`)
- **Role:** Dispatches SMS links for self-service appointment management.
- **Pages (5):** `Offer SMS - en`, `Offer SMS - fr-ca`, `%5bwhk%5d If MYA eligible`, `Check MYA URL availability`, `Global Error Handling`.

### 2.5. Satellite TV Signal Rehit Flow (`bell_rehit_Sat_TV`)
- **Role:** Triggers receiver refresh signals for satellite and Fibe TV receivers.
- **Pages (9):** `Trigger rehit`, `Check CX Input`, `Follow-up 1` to `Follow-up 5`, `Local Error handling`, `Global Error handling`.

---

## 3. Generative Playbook Architecture (72 Playbooks)

The playbooks handle conversational sub-dialogs with LLM instruction enforcement:

- **Technical Support Cluster:** `Bell_UC_Technical_Support_Infobot`, `Bell_UC_Technical_Support_Infobot_Fr`, `bell_UC_Technical Support-1`, `bell_UC_Technical Support-2`, `bell_tv_rehit_SatTV_FibeTV`.
- **Billing & Account Cluster:** `bell_UC_Billing`, `bell_UC_Account Management`, `bell_UC_Account Management 2`, `bell_UC_Payments`, `bell_UC_Temporary Suspension`, `bell_UC_Usage`.
- **Sales & Plans Cluster:** `bell_UC_Sales`, `bell_UC_Sales Add To Existing Account`, `Bell_UC_Sales_Plans_inquiry`, `bell_uc_sales_service_coverage`.
- **Disambiguation Cluster:** `bell_UC_Disambiguation`, `bell_uc_disambiguation_for_vague_billing`, `bell_uc_disambiguation_for_vague_tech_support`, `bell_uc_disambiguation_for_vague_equipment`, `bell_uc_disambiguation_for_vague_sales`.
- **Steering & Utility Cluster:** `bell_Steering_Wrap-up`, `bell_Steering_Feedback`, `bell_Steering_Global Fallback`, `nga_nlu_entity_extraction`, `bell_vr_microservice`, `bell_vr_CDA`.

---

## 4. Generative AI & Safety Settings

- **Default LLM:** `gemini-2.5-flash`
- **Temperature:** `0.89999998`
- **Context Window:** `CONTEXT_WINDOW_INDEFINITE`
- **Languages:** `en` (English), `fr-ca` (Canadian French)
- **RAI Security Filters:**
  - `DANGEROUS_CONTENT`: `BLOCK_FEW`
  - `SEXUALLY_EXPLICIT_CONTENT`: `BLOCK_SOME`
  - `HARASSMENT`: `BLOCK_SOME`
  - `HATE_SPEECH`: `BLOCK_SOME`
- **Prompt Security:** Sensitivity Level 3, Minimum Query Length 15 characters.

---

## 5. Webhook Integration Specifications

- **Total Webhook Endpoints:** 63 REST services.
- **Timeout Thresholds:** 15s (`ugyt-dss-dts`), 20s (`acut/search`), 30s (all standard transaction webhooks).
- **Primary Domain Services:**
  1. `/v1/ticket_management/acut/search` (ACUT trouble ticket query)
  2. `/v1/ticket_management/omf/calendar#availability` (WFAS calendar slots)
  3. `/v1/ticket_management/wfas#appointment` (Appointment update)
  4. `v1/customer-identification#search-by-ban` (Customer BAN search)
  5. `v1/customer-authentication#send-otp` (SMS OTP delivery)
  6. `v1/agent-queue-determination` (AQD handoff routing)
  7. `v1/digital-tools/outage-check#status-update` (Outage lookup)
  8. `v1/sat-rehit` (TV signal refresh trigger)
