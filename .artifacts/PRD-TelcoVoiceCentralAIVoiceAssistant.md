# Product Requirements Document

## Product Name

**Telco Voice Central (Bell Voice Central) — AI Voice Assistant**

&nbsp;

---

## Executive Summary

**Telco Voice Central** is a voice-first conversational customer service application for a major telecommunications provider (Bell Canada). It serves residential and mobility customers across Canada in both English and French (`fr-ca`). The agent resolves the six most common contact reasons—**billing questions, technical support & outages, sales & equipment, appointment management, account management, and service changes**—either through self-contained conversational automation or through a seamless escalation to a live representative that preserves full session context.

&nbsp;

The product replaces rigid, legacy IVR touch-tone and deterministic speech trees with intelligent, generative conversational understanding while upholding strict customer data privacy, brand safety, and regulatory compliance.

&nbsp;

---

## Problem Statement

Telecom customers calling support often face frustrating, rigid IVR phone trees. In legacy systems, callers are forced to navigate complex touch-tone or deterministic menus where slight misunderstandings or topic changes result in failed routing or long hold times.

&nbsp;

Additionally, customer service requests frequently span multiple domains—such as a customer wanting to dispute a billing charge and report an internet outage during the same call. Legacy IVR architectures cannot transition between unrelated topics without forcing callers through repetitive identification steps, leading to high call abandonment and excessive live-agent escalations.

&nbsp;

---

## Goals & Non-Goals

### Goals

- **Voice-Friendly Resolution**: Provide fast, accurate, concise spoken answers (under 50 words per turn where feasible) across Mobility, Internet, TV, and Home Phone services.  
- **Strict 3-Tier Auth Ladder**: Securely transition callers across `Guest` $\\rightarrow$ `Identified` $\\rightarrow$ `Authenticated` states before exposing or modifying account data.  
- **Proactive Outage & Diagnostic Support**: Automatically check regional outage databases by postal code and deliver multi-step troubleshooting guides via SMS.  
- **Bilingual Excellence**: Support seamless English and Canadian French conversations with persistent language locking from the first turn.  
- **Graceful Topic Switching**: Handle mid-conversation pivots (e.g., jumping from billing to tech support) without losing session context.  
- **Verbatim Compliance**: Strictly enforce legal, regulatory, and privacy disclosures without model paraphrasing.

### Non-Goals

- Do not process unauthorized financial transactions or store raw credit card CVV numbers in plaintext.  
- Do not disclose Personally Identifiable Information (PII) or account balances to unauthenticated callers.  
- Do not promise guaranteed technician dispatch arrival times without backend system confirmation.  
- Do not provide unverified or speculative network outage restoration times.  
- Do not impersonate company executives, employees, or third-party service providers.

&nbsp;

---

## Target Audience

- **Residential Customers**: Callers inquiring about home Internet (Fibe/DSL), Fibe TV, Satellite TV, or landline phone services.  
- **Mobility Subscribers**: Mobile phone and smartphone users asking about data usage, roaming, SIM/eSIM, or plan upgrades.  
- **Bilingual Callers**: Canadian consumers communicating in English or Canadian French.  
- **Distressed / Urgent Callers**: Customers experiencing service interruptions, equipment failures, or reporting fraud.

&nbsp;

---

## Section 1 — Global Behavioral Requirements Register

The agent must strictly satisfy the 20 global behavioral requirements (`BR-TV-001` through `BR-TV-020`):

&nbsp;

| ID | Name | Core Behavioral Requirement |
| :---- | :---- | :---- |
| `BR-TV-001` | **Recording Notice** | The regional privacy disclosure is emitted verbatim on the initial greeting. If asked, the agent repeats it verbatim. |
| `BR-TV-002` | **Restricted Caller Check** | Incoming Caller ID is checked against a blocklist before greeting; blocked calls hear a deflection message and disconnect. |
| `BR-TV-003` | **Regional Service Alert** | Active regional service alerts prepend an advisory banner to the standard greeting. |
| `BR-TV-004` | **Language Locking** | Language is detected at Turn 1 and locked for the call. Only an explicit caller request switches the language. |
| `BR-TV-005` | **Module Coverage** | Every customer intent must route to the correct capability module (`M1` to `M8`). |
| `BR-TV-006` | **Retry Strikes** | 3 consecutive no-input or 3 unresolved no-match events trigger graceful escalation (`no_input_escalation` / `disambig_max_attempts`). |
| `BR-TV-007` | **DTMF Capture** | Spoken or keypad DTMF entries are normalized and written to session variable `dtmf_digits` on the arrival turn. |
| `BR-TV-008` | **Auth Ladder** | Enforce `Guest` $\\rightarrow$ `Identified` $\\rightarrow$ `Authenticated`. Account reads/mutations strictly require `Authenticated`. |
| `BR-TV-009` | **PII Redaction** | Account numbers, reference numbers, and card numbers are spoken back as last-4 digits only. PINs/OTPs are never echoed. |
| `BR-TV-010` | **Tool-Error Tri-State** | System errors end session immediately; business errors surface to model for alternative options; validation errors prompt retry. |
| `BR-TV-011` | **Verbatim Compliance** | All legal and compliance strings must be emitted verbatim without model contraction or paraphrasing. |
| `BR-TV-012` | **Business Handoff** | Business-flagged accounts receive the verbatim `business_handoff` line and escalate immediately without self-serve attempts. |
| `BR-TV-013` | **Fraud Escalation** | Fraud claims trigger the verbatim empathy line and immediate transfer (`fraud_escalation`) without attempting auth. |
| `BR-TV-014` | **After-Hours Awareness** | Outage and fraud queues operate 24/7. Sales, plan changes, and appointments route to next-business-day callback when closed. |
| `BR-TV-015` | **Session-Context Handoff** | Every live-agent escalation carries the full session variable payload to the representative's console. |
| `BR-TV-016` | **Malicious Utterance** | Classifier hits for abusive/malicious input end the session immediately with reason `malicious_input`. |
| `BR-TV-017` | **No Invented Data** | If a tool lookup fails, the agent must never invent account balances or plans. Generation is strictly conditioned on tool success. |
| `BR-TV-018` | **Audio Recording** | Every voice interaction produces an archived session recording verified by compliance audits. |
| `BR-TV-019` | **Mid-Call Topic Switch** | The agent must re-classify and re-route when the caller pivots mid-call rather than forcing the old flow forward. |
| `BR-TV-020` | **Language Non-Degradation** | A call that starts in French or English must remain in that language through self-service or transfer to a matching human agent. |

&nbsp;

---

## Section 2 — Capability Modules Architecture

The conversational application is structured into **8 Functional Capability Modules (`M1` – `M8`)**:

&nbsp;

```
graph TD
    User([Customer Voice Call]) <--> M1[M1: Session Lifecycle & Routing]
    M1 --> M2[M2: Authentication & Identity]
    M1 --> M3[M3: Billing & Payment]
    M1 --> M4[M4: Technical Support & Virtual Repair]
    M1 --> M5[M5: Sales & Equipment]
    M1 --> M6[M6: Appointments & Tickets]
    M1 --> M7[M7: Account Management]
    M1 --> M8[M8: Secondary Language Fallback]

    M2 -.->|Auth Status = Pass| M1
    M3 -.->|Topic Switch / Complete| M1
    M4 -.->|Topic Switch / Complete| M1
    M5 -.->|Topic Switch / Complete| M1
    M6 -.->|Topic Switch / Complete| M1
    M7 -.->|Topic Switch / Complete| M1
    M8 -.->|Topic Switch / Complete| M1
```

### Module Responsibilities & Volume Breakdown

| Module | Name | Call Volume | Purpose & Scope |
| :---- | :---- | :---- | :---- |
| **`M1`** | **Session Lifecycle & Routing** | Entry / Exit | Greet caller, capture identity, lock language, disambiguate intent, route to specialists, and handle closing wrap-up. |
| **`M2`** | **Authentication & Identity** | Gatekeeper | Verify caller via OTP SMS or 4-digit PIN; manage auth ladder; escalate on 3 failed attempts. |
| **`M3`** | **Billing & Payment** | \~25% | Recent bill lookups, charge disputes, autopay enrollment, refund processing within policy thresholds, and payment arrangements. |
| **`M4`** | **Tech Support & Virtual Repair** | \~30% | Outage checks by postal code, TV service sub-type disambiguation, virtual repair diagnostics, and SMS troubleshooting dispatch. |
| **`M5`** | **Sales & Equipment** | \~15% | Service coverage checks, presenting 2–3 curated plan options, order placement, warranty claims, equipment returns, and number porting. |
| **`M6`** | **Appointments & Tickets** | \~10% | Look up active field appointments, offer 2–3 reschedule slots, process cancellations, and check technician en-route status. |
| **`M7`** | **Account Management** | \~15% | Dispatch 30-minute password reset links, MFA management, fraud escalation, profile updates, and service suspension/restoration. |
| **`M8`** | **Secondary Language Fallback** | Variable | Specialized French (`fr-ca`) technical support when primary language content lacks specific regional diagnostic coverage. |

&nbsp;

---

## Section 3 — Intent Coverage & Routing Table

| Representative Caller Utterance | Route To | Auth Required |
| :---- | :---- | :---- |
| "My bill is wrong" / "Dispute a charge" | `M3` (Billing) | Yes (`Authenticated`) |
| "I want to pay my bill" / "Set up autopay" | `M3` (Billing) | Yes (`Authenticated`) |
| "Refund" / "Credit back my account" | `M3` (Billing) | Yes (`Authenticated`) |
| "Internet is down" / "No service" | `M4` (Tech Support) | Yes (`Authenticated`) |
| "TV says no signal" / "Error 101" | `M4` (Tech Support) | Yes (`Authenticated`) |
| "SIM not working" / "Phone locked" | `M4` (Tech Support) | Yes (`Authenticated`) |
| "I want to add TV" / "New plan" / "Upgrade speed" | `M5` (Sales) | Recommended (`Identified`) |
| "My phone is defective" / "Warranty replacement" | `M5` (Sales) | Yes (`Authenticated`) |
| "Transfer my number in" | `M5` (Sales) | Yes (`Authenticated`) |
| "Book a technician" / "Reschedule my appointment" | `M6` (Appointments) | Yes (`Authenticated`) |
| "Where is my technician?" / "Ticket status" | `M6` (Appointments) | Yes (`Authenticated`) |
| "Forgot my password" / "Reset login" | `M7` (Account) | `Identified` (Dispatches SMS link) |
| "Disable two-factor" / "Enable MFA" | `M7` (Account) | Yes \+ Step-Up Auth |
| "Someone hacked my account" / "Fraud" | `M7` (Account) | No (Immediate Empathy \+ Escalation) |
| "Restore my suspended service" | `M7` (Account) $\\rightarrow$ `M3` (Billing) | Yes (`Authenticated`) |
| "Cancel my service" / "Port out my number" | `M7` (Account) | Yes \+ Mandatory Contract Disclosure |
| "I want to talk to a person" | Live Agent Handoff | None (Immediate Transfer) |

&nbsp;

---

## Section 4 — Verbatim Compliance Copy Library

The following strings must be emitted **verbatim** without model paraphrasing or modification:

&nbsp;

| Key | Primary Language (English) Verbatim String | Secondary Language (French Canadian) |
| :---- | :---- | :---- |
| `greeting_main` | "Welcome to Telco. I can help with billing, technical support, or managing your account. To get started, could you tell me the phone number or account number associated with your service?" | "Bienvenue chez Telco. Je peux vous aider avec la facturation, le soutien technique ou la gestion de votre compte..." |
| `recording_notice` | "This call may be recorded for quality and training purposes." | "Cet appel peut être enregistré à des fins de qualité et de formation." |
| `id_verification_otp` | "For your security, I just sent a 6-digit code to that number — please read it back to me." | "Pour votre sécurité, je viens d'envoyer un code à 6 chiffres à ce numéro..." |
| `id_verification_pin` | "For your security, I'll need to verify your identity. Please enter the 4-digit PIN you set up." | "Pour votre sécurité, veuillez entrer le NIP à 4 chiffres associé à votre compte." |
| `live_agent_handoff` | "I'll connect you to a representative who can help. Please hold." | "Je vous transfère à un représentant qui pourra vous aider. Veuillez patienter." |
| `business_handoff` | "To get you the best support for your business account, I'll transfer you to an agent. You'll need to use your phone keypad instead of talking to the virtual assistant. Just a moment while I connect you." | "Afin d'obtenir le meilleur soutien pour votre compte d'affaires, je vous transfère à un agent..." |
| `refund_confirmation_pattern` | "Your refund of ${amount} will appear on your next statement within {days} business days." | "Votre remboursement de {amount} $ apparaîtra sur votre prochain relevé dans un délai de {days} jours ouvrables." |
| `empathy_protocol` | "I'm very sorry to hear that you are facing challenges. I will ensure we handle your request with the utmost care." | "Je suis sincèrement désolé d'apprendre que vous éprouvez des difficultés..." |
| `outage_active` | "I see there's an active outage in your area. We're working on it. Would you like me to text you when it's restored?" | "Je constate qu'il y a une panne active dans votre secteur. Nous y travaillons..." |
| `transfer_to_specialist` | "I'll connect you to a specialist now — they'll have everything we've already discussed." | "Je vous transfère à un spécialiste dès maintenant..." |

&nbsp;

---

## Section 5 — Session Data Model & Scoped Variables

The agent maintains approximately **60 session-scoped variables** partitioned into isolated functional namespaces:

### 1\. Identity & Profile

- `clid` (string): 10-digit caller ID from telephony.  
- `tfn` (string): Toll-free number dialed (drives brand routing).  
- `cirn` (string, PII): Customer reference number (spoken/logged as last-4 only).  
- `billing_account` (string, PII): 9-digit account number (spoken/logged as last-4 only).  
- `customer_type` (enum): `New` | `Existing`.

### 2\. Authentication State

- `auth_status` (enum): `Pass` | `Fail` (derived strictly from tool return).  
- `identification_status` (enum): `Pass` | `Fail`.  
- `business_flag` (boolean): Triggers immediate business queue deflection.

### 3\. Routing & Conversation

- `route` (enum): Classified target module (`billing`, `tech`, `sales`, `appointments`, `account`).  
- `lob` (enum): Line of Business (`mobility`, `internet`, `tv`, `homephone`, `smarthome`).  
- `tv_sub_type` (enum): `streaming` | `satellite` | `streaming_only`.  
- `language` (enum): `primary` (en) | `secondary` (fr-ca) (locked at Turn 1).  
- `dtmf_digits` (string): Keypad digits captured on current turn.

### 4\. Error Counters & Diagnostics

- `local_noinput_counter` (int): Consecutive no-input count for current module (escalates at 3).  
- `no_match_confirmation_count` (int): Consecutive no-match count (escalates at 3).  
- `global_err_count` (int): Cumulative system/validation error count (ends session at 3).

&nbsp;

---

## Section 6 — Customer User Journeys (CUJ Test Scenarios)

The evaluation suite validates the agent across **7 core Customer User Journeys**:

### CUJ-1: Account Password Reset (`M7`)

- **User Goal**: Reset self-serve portal password via SMS link.  
- **Success Criteria**: Agent verifies caller identity, dispatches 30-minute valid SMS reset link, and confirms delivery without attempting to handle raw password strings verbally.

### CUJ-2: Billing Charge Dispute (`M3`)

- **User Goal**: Inquire about an unfamiliar $12.50 streaming charge and request credit.  
- **Success Criteria**: Agent verifies account (`Authenticated`), looks up recent bills, identifies charge, credits back amount within policy threshold ($12.50 $\\le$ $25.00 threshold), and emits verbatim `refund_confirmation_pattern`.

### CUJ-3: Tech Support Outage & Virtual Repair (`M4`)

- **User Goal**: Report home internet failure in postal code H3Z 2Y7.  
- **Success Criteria**: Agent prompts for postal code, checks regional outage API, detects active outage, emits verbatim `outage_active`, offers proactive SMS restoration updates, and closes session cleanly.

### CUJ-4: Appointment Reschedule (`M6`)

- **User Goal**: Reschedule a technician installation appointment.  
- **Success Criteria**: Agent looks up active booking, offers 2–3 available time slots, commits selected reschedule, and sends SMS confirmation.

### CUJ-5: Sales Plan Upgrade (`M5`)

- **User Goal**: Inquire about upgrading mobile data plan.  
- **Success Criteria**: Agent presents 2–3 curated plan options, captures customer choice, confirms order, and provides delivery ETA.

### CUJ-6: Service Restoration from Non-Payment (`M7` \-\> `M1` \-\> `M3` \-\> `M7`)

- **User Goal**: Restore suspended mobile line.  
- **Success Criteria**: Agent detects suspension reason (`Non-payment`), routes caller to `M3` to clear balance/arrange payment, and returns to `M7` to execute service restoration.

### CUJ-7: Secondary Language Support (`M8`)

- **User Goal**: Request technical troubleshooting in Canadian French.  
- **Success Criteria**: Agent detects French utterance at Turn 1, locks language to `fr-ca`, and conducts entire interaction in French without language degradation.

&nbsp;

---

## Section 7 — Success Metrics & Acceptance Criteria

### Success Metrics

- **First-Contact Containment**: 75% for self-service billing, outage, and appointment inquiries.  
- **Authentication Success Rate**: 85% self-service verification for returning callers.  
- **Routing Accuracy**: 95% correct intent classification across the 8 capability modules.  
- **Zero PII & Data Hallucination**: $0% unredacted PII exposure and $0%$ fabricated balance/plan claims.  
- **Evaluation Benchmark**: 90% pass rate across the 806 deterministic and simulation evaluation suites.

### Acceptance Criteria

- Every call opens with verbatim recording notice (`BR-TV-001`).  
- Caller language is locked at Turn 1 and maintained throughout (`BR-TV-004`, `BR-TV-020`).  
- Account data reads and mutations are blocked until `auth_status == Pass` (`BR-TV-008`).  
- 3 consecutive no-input or no-match events trigger graceful escalation (`BR-TV-006`).  
- Fraud claims bypass auth and trigger immediate empathetic transfer (`BR-TV-013`).  
- All tool errors follow the tri-state classification (`BR-TV-010`).

&nbsp;