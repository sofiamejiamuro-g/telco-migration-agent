# CXAS Optimization Audit Report
**Generated:** `2026-09-17 04:49:58 UTC`

## App Details
- **Source DFCX Agent:** `(see bundle)`
- **Target CXAS App:** `telco_voice_central`
- **App Resource:** `projects/fde-bootcamp/locations/us/apps/b6e81008-9b5a-46c8-a1b0-8fb4f5035a5f`
- **Console URL:** https://ces.cloud.google.com/projects/fde-bootcamp/locations/us/apps/b6e81008-9b5a-46c8-a1b0-8fb4f5035a5f

## Consolidation Summary
- **1:1 IR agents (before grouping):** 187
- **Consolidated agents (after):** 7
- **Grouping JSON artifact:** `telco_voice_central_grouping.json`

### Grouping Detail
| Group | Members | Journey | Root |
|---|---|---|---|
| `RootAgent` | Default Start Flow, Routing only, bell_Query_Rewriter(no codeblock), bell_Query_Rewriter, bell_NLU_Query_Rewriter, nga_handling, nga_nlu_entity_extraction, bell_No_Input_3, bell_No_Match_3, bell_global_error_count_check, bell_Steering_Global Fallback, bell_Steering_Wrap-up, bell_Steering_Feedback, bell_wrapup, bell_End the Conversation, bell_Live Agent Handoff, bell_aqd, bell_va_to_ivr_handoff, bell_va_to_ivr_handoff_prepaid, bell_va_to_ivr_handoff_BBM_BNM_SMB, va_to_ivr_business_id_sales, bell_ivr_to_va_handoff, bell_va_to_ivr_smarthome, temp, bell_Feedback, bell_VA_Survey, bell_topic_transitions, bell_determine_handover, bell_specialty_flow, bell_test_wrapper, bell_SMS Trigger, bell_sms_trigger - old, bell_sms_no_match_handling, bell_IVR_Options, bell_VR, bell_get_sdl_mapping_url, bell_apb, bell_UC_Disambiguation, bell_UC_Get_LOB, bell_UC_Get_TV_SUB_Type, bell_uc_ask_LOB, Bell_tech_lob, bell_UC_New_Customer_Context_Rentention, bell_uc_disambiguation_for_vague_account_management, bell_uc_disambiguation_for_vague_billing, bell_uc_disambiguation_for_vague_disconnect, bell_uc_disambiguation_for_vague_equipment, bell_uc_disambiguation_for_vague_others, bell_uc_disambiguation_for_vague_payment, bell_uc_disambiguation_for_vague_sales, bell_uc_disambiguation_for_vague_service, bell_uc_disambiguation_for_vague_tech_support, bell_UC_Other | Intake, Triage, and Global Steering | yes |
| `AuthenticationAgent` | bell_Identification, bell_authentication, bell_agent_transfer_authentication, bell_multiban, bell_UC_Automation_testing, bell_UC_Postal_Code | Customer Authentication and Identification |  |
| `BillingAndPaymentsAgent` | bell_UC_Billing, bell_UC_Payments, bell_billing, bell_payment_CLP_details, bell_payment_account_balance_and_last_payment_details, bell_payment_amount_otcc, bell_payment_arrangement_setup_mutilple_installments, bell_payment_arrangement_setup_pa_amount_date_and_processing, bell_payment_arrangment_setup_id_auth_eligibility_Checks, bell_payment_autopay_cancel, bell_payment_autopay_status, bell_payment_autopay_update, bell_payment_billing_consolidated_flow_identification, bell_payment_cc_details_input, bell_payment_clp_payment_amount, bell_payment_clp_process_payment_and_wrapup, bell_payment_dts_token, bell_payment_not_processing, bell_payment_notification, bell_payment_one_time_CC_payment, bell_payment_pitch_one_time_CC_payment, bell_payment_pitch_one_time_CC_payment 2, bell_payment_pitch_pacc_otcc, bell_payment_process_pacc_registration, bell_payment_process_payment_and_wrapup, bell_payment_request_refund, bell_payment_setup_pacc_or_payment_not_stated, bell_payment_setup_preAuth_pad, bell_payment_update_payment_arrangements, bell_request_for_bill_statement, bell_expired_credit_card, bell_clp_faq_test | Account Billing, Statements, and Payment Processing |  |
| `TechSupportAndRepairAgent` | Bell_UC_Technical_Support_Infobot, Bell_UC_Technical_Support_Infobot_Fr, Bell_UC_Technical_Support_Infobot_deprecated, Bell_UC_Technical_Support_Infobot_Fr_deprecated, bell_UC_Technical Support, bell_UC_Technical Support-1, bell_UC_Technical Support-2, bell_tech_support_intents, bell_tech_service_outage_&_Tech_connection_issue, bell_tech_service_outage_connection_issue_main, bell_tech_intent_apb, Bell_UC_Tech_intents_lob, bell_vr_CDA, bell_vr_CDA_CFL, bell_vr_CFB, bell_vr_consent, bell_vr_kickout_sms, bell_vr_microservice, bell_vr_api_failure_handler, bell_vr_kickout, bell_vr_next_task, bell_vr_post_answer, bell_vr_pre_checks, bell_vr_start_process, bell_rehit, Bell_tv_rehit_SatTV_FibeTV, bell_rehit_Send_Troubleshooting_SMS, bell_rehit_confirmation, bell_rehit_Check_Subscription, bell_rehit_Fibe_TV, bell_rehit_SMS, bell_rehit_Sat_TV, bell_troubleshooting_intents_entry | Technical Troubleshooting, Outages, and Virtual Repair |  |
| `SalesAndEquipmentAgent` | Bell_UC_Sales_Plans_inquiry, bell_UC_Sales, bell_UC_Sales Add To Existing Account, bell_UC_sales_device_related, bell_uc_sales_service_coverage, bell_sales_routing_flow, bell_sales_intent_handling, sales_add_to_existing_account_flow, bell_mob_sales_pitch, Bell_UC_Equipment_Inquires_Infobot, Bell_UC_Equipment_Inquires_Infobot_deprecated, Bell_UC_Equipment_Inquires_Infobot_fr, Bell_UC_Equipment_Inquires_Infobot_fr_deprecated, bell_UC_Equipment Warranty Claim Related, bell_UC_Equipment, bell_equipment_routing, bell_equipment_order_or_upgrade_device_routing, bell_equipment_warranty_claim_cpo_update, bell_UC_Manage Plans and Features, bell_UC_Manage Plans and Features Phase2, bell_UC_Manage Plans and Features Phase2_1, bell_UC_ManagePlansAndFeatures_Infobot_en_fr, bell_UC_ManagePlansAndFeatures_Infobot_en_fr_deprecated, bell_Manage_plan_and_feature_routing, service_change_plan_flow, service_add_feature_flow | Sales, Plan Management, and Equipment Upgrades/Returns |  |
| `AppointmentManagementAgent` | bell_app_mgmt_cancel_ticket, bell_app_mgmt_create_dispatch_start, bell_app_mgmt_ticket_check_for_cancel_ticket, bell_app_mgmt_Tech_visit_Entry, bell_app_mgmt_cancel_ticket_entry, bell_app_mgmt_change_contact_method, bell_app_mgmt_ticket_status_and_change_entry, bell_app_mgmt_omf_change_reschedule_ticket, Bell_appt_mgmt_acut_ticket_chk, bell_appt_mgmt_mya_pitch_1, bell_ticket_mgmt_webhook_failure, bell_ticket_mgmt_change_cancel_ticket, bell_ticket_mgmt_acut_create_a_dispatch, bell_ticket_mgmt_omf_ticket_check_technical_intents, bell_ticket_mgmt_acut_change_reschedule_ticket, bell_ticket_mgmt_acut_change_reschedule_ticket_technical_intents, bell_ticket_mgmt_omf_ticket_check_appointment_mgmt, bell_uc_reschedule_change_ticket_multiple_appointment, bell_uc_reschedule_change_ticket_single_appointment, bell_uc_omf_tkt_chk_appt_mgmt_appt_info_retriever, bell_tech_change_appointment, bell_tech_change_appointment_flow, bell_tech_field_tech_visit, bell_tech_field_tech_visit_cancel_flow, bell_acut_ticket_chk_troubleshooting_intents | Ticketing, Technician Dispatch, and Appointment Scheduling |  |
| `AccountManagementAgent` | bell_UC_Account Management, bell_UC_Account Management 2, bell_UC_AccountManagement_Infobot_en_fr, bell_UC_AccountManagement_Infobot_en_fr_deprecated, bell_UC_CIAM, bell_UC_Disconnect, bell_UC_Temporary Suspension, bell_UC_Usage, bell_FAQ, bell_FAQ_vanity, bell_PPV | General Account Management, Suspensions, and FAQs |  |

## CXASOptimizer Logs
### Stage 1 — Variable Deduplication
| Stage | Action | Details |
|---|---|---|
| `Stage 1` | `Start` | Building global variable dependency map. |
| `Stage 1` | `LLM Processing` | Requesting deduplication mapping for 1361 variables. |
| `Stage 1` | `LLM Success` | Reduced 1361 variables to 143. |
| `Stage 1` | `Applying` | Rewriting instructions, tools, and callbacks globally. |
| `Stage 1` | `Complete` | Global Variable Deduplication finished successfully. |

### Stage 2 — Instruction State Machines + Tool Mocks
| Stage | Action | Details |
|---|---|---|
| `Stage 2 Instructions` | `Start` | Restructuring instructions to State Machine XML. |
| `Stage 2 Tool Mocks` | `Start` | Injecting native mock_mode branches into Python tools. |
| `Stage 2 Instructions` | `Complete` | Restructured 7 Playbook agents successfully. |
| `Stage 2 Tool Mocks` | `Complete` | Injected native mock_mode into 226 Python tools. |
| `Stage 2 Instructions` | `Self-Healing Gate` | All optimized playbooks passed canonical-schema validation. No healing required. |

## CXAS Version Checkpoints
| Display Name | Description |
|---|---|
| `0.0.3` | Stage 1 Part B: structural consolidation |

## Deterministic Unit Tests
- **Artifact:** `telco_voice_central_unit_tests.json`
- **Tests per agent:**
  - `RootAgent`: 8
  - `AuthenticationAgent`: 2
  - `BillingAndPaymentsAgent`: 17
  - `TechSupportAndRepairAgent`: 21
  - `SalesAndEquipmentAgent`: 10
  - `AppointmentManagementAgent`: 12
  - `AccountManagementAgent`: 8

## Lint
- **Status:** ⚠️ issues found

<details><summary>Lint output (excerpt)</summary>

```
Linting app: telco_voice_central
============================================================
  Model:     gemini-2.5-flash-001
  Agents:    7
  Tools:     200
  Callbacks: 14
  Evals:     0

============================================================
LINT RESULTS
============================================================
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central [V001] Missing required fields for  Schema: ['required']
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AccountManagementAgent/AccountManagementAgent.json [S007] Agent 'AccountManagementAgent' is referenced as a child by multiple parents: ['AppointmentManagementAgent', 'RootAgent']. Each sub-agent must have at most one parent.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AccountManagementAgent/instruction.txt:219 [S002] Instruction references tool 'FR_Bell_AccountManagement' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AccountManagementAgent/instruction.txt:239 [S002] Instruction references tool 'FR_Generic_Datastore' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AccountManagementAgent/instruction.txt:215 [S002] Instruction references tool 'EN_Bell_AccountManagement' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AccountManagementAgent/instruction.txt:235 [S002] Instruction references tool 'EN_Generic_Datastore' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AppointmentManagementAgent/AppointmentManagementAgent.json [S007] Agent 'AppointmentManagementAgent' is referenced as a child by multiple parents: ['RootAgent', 'TechSupportAndRepairAgent']. Each sub-agent must have at most one parent.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AppointmentManagementAgent/instruction.txt:162 [S002] Instruction references tool 'trigger_sms_notification_wrapper' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/AuthenticationAgent/AuthenticationAgent.json [S007] Agent 'AuthenticationAgent' is referenced as a child by multiple parents: ['BillingAndPaymentsAgent', 'RootAgent']. Each sub-agent must have at most one parent.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/BillingAndPaymentsAgent/BillingAndPaymentsAgent.json [S007] Agent 'BillingAndPaymentsAgent' is referenced as a child by multiple parents: ['AccountManagementAgent', 'RootAgent', 'TechSupportAndRepairAgent']. Each sub-agent must have at most one parent.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/BillingAndPaymentsAgent/instruction.txt:188 [S002] Instruction references tool 'check_preauth_payment_status' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/BillingAndPaymentsAgent/instruction.txt:138 [S002] Instruction references tool 'get_clp_details_wrapper' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/SalesAndEquipmentAgent/SalesAndEquipmentAgent.json [S007] Agent 'SalesAndEquipmentAgent' is referenced as a child by multiple parents: ['AccountManagementAgent', 'AppointmentManagementAgent', 'BillingAndPaymentsAgent', 'RootAgent', 'TechSupportAndRepairAgent']. Each sub-agent must have at most one parent.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/SalesAndEquipmentAgent/instruction.txt:211 [S002] Instruction references tool 'FR_Bell_Manage_plans_and_features' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/SalesAndEquipmentAgent/instruction.txt:168 [S002] Instruction references tool 'FR_Bell_Equipment_Inquires' but it's not in the agent's tool list.
  [E] /tmp/cxas_lint_e6k5vnpv/telco_voice_central/agents/SalesAndEquipmentAgent/instruction.txt:207 [S002] Instruction references tool 'EN_Bell_Manage_plans_and_features' but it's not in the agent's tool list.
  [E] 
```

</details>
