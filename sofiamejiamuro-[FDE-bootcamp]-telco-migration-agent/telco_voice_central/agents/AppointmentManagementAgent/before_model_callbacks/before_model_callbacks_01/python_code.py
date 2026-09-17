NATIVE_TRANSFER_TARGETS = {"AppointmentManagementAgent", "RootAgent"}

NATIVE_TRANSFER_TARGETS = {"AppointmentManagementAgent", "RootAgent"}

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # --- MIGRATION AUTO-GENERATED: TOOL TRANSFER --- 
    if llm_request.contents and llm_request.contents[-1].parts:
        for p in llm_request.contents[-1].parts:
            if getattr(p, "function_response", None):
                rd = getattr(
                    p.function_response, "response", {}
                )
                rd = (
                    rd.get("result", rd)
                    if isinstance(rd, dict)
                    else {}
                )
                if isinstance(rd, dict):
                    t = (
                        rd.get("target") or rd.get("target_agent")
                    )
                    a = rd.get("action")
                    if a in ("agentTransfer", "Transfer") and t:
                        if t not in NATIVE_TRANSFER_TARGETS:
                            return LlmResponse.from_parts(
                                parts=[
                                    Part.from_agent_transfer(
                                        agent=t
                                    )
                                ]
                            )

    # --- MIGRATION AUTO-GENERATED: SYSTEM DIRECTIVES ---
    if llm_request.contents and llm_request.contents[-1].parts:
        for part in llm_request.contents[-1].parts:
            if any(
                part.has_function_response(t)
                for t in ["extract_entities"]
            ):
                if part.function_response and hasattr(
                    part.function_response, "response"
                ):
                    response_data = part.function_response.response

                    directives = []
                    if isinstance(response_data, dict):
                        if "__cxas_system_directives__" in response_data:
                            directives = response_data[
                                "__cxas_system_directives__"
                            ]
                        elif (
                            "result" in response_data
                            and isinstance(response_data["result"], dict)
                            and "__cxas_system_directives__"
                            in response_data["result"]
                        ):
                            directives = response_data["result"][
                                "__cxas_system_directives__"
                            ]

                    if directives:
                        parts_to_return = []
                        for directive in directives:
                            action = directive.get("action")
                            if action == "add_override":
                                t_raw = str(directive.get("target", ""))
                                target = t_raw.split(".")[-1]
                                params = directive.get("parameters", {})
                                if isinstance(params, dict):
                                    for k, v in params.items():
                                        callback_context.variables[k] = v
                                        print(f"Injected routing: {k}={v}")
                                print(f"Executing add_override: {target}")
                                if target in ["agentTransfer", "Transfer"]:
                                    parts_to_return.append(
                                        Part.from_end_session(
                                            reason="escalate_to_human",
                                            escalated=True,
                                        )
                                    )
                                else:
                                    parts_to_return.append(
                                        Part.from_agent_transfer(
                                            agent=target
                                        )
                                    )
                        if parts_to_return:
                            return LlmResponse.from_parts(parts=parts_to_return)

    # --- MIGRATION AUTO-GENERATED: TOOL TRANSFER --- 
    if llm_request.contents and llm_request.contents[-1].parts:
        for p in llm_request.contents[-1].parts:
            if getattr(p, "function_response", None):
                rd = getattr(
                    p.function_response, "response", {}
                )
                rd = (
                    rd.get("result", rd)
                    if isinstance(rd, dict)
                    else {}
                )
                if isinstance(rd, dict):
                    t = (
                        rd.get("target") or rd.get("target_agent")
                    )
                    a = rd.get("action")
                    if a in ("agentTransfer", "Transfer") and t:
                        if t not in NATIVE_TRANSFER_TARGETS:
                            return LlmResponse.from_parts(
                                parts=[
                                    Part.from_agent_transfer(
                                        agent=t
                                    )
                                ]
                            )

    # --- MIGRATION AUTO-GENERATED: SYSTEM DIRECTIVES ---
    if llm_request.contents and llm_request.contents[-1].parts:
        for part in llm_request.contents[-1].parts:
            if any(
                part.has_function_response(t)
                for t in ["extract_entities"]
            ):
                if part.function_response and hasattr(
                    part.function_response, "response"
                ):
                    response_data = part.function_response.response

                    directives = []
                    if isinstance(response_data, dict):
                        if "__cxas_system_directives__" in response_data:
                            directives = response_data[
                                "__cxas_system_directives__"
                            ]
                        elif (
                            "result" in response_data
                            and isinstance(response_data["result"], dict)
                            and "__cxas_system_directives__"
                            in response_data["result"]
                        ):
                            directives = response_data["result"][
                                "__cxas_system_directives__"
                            ]

                    if directives:
                        parts_to_return = []
                        for directive in directives:
                            action = directive.get("action")
                            if action == "add_override":
                                t_raw = str(directive.get("target", ""))
                                target = t_raw.split(".")[-1]
                                params = directive.get("parameters", {})
                                if isinstance(params, dict):
                                    for k, v in params.items():
                                        callback_context.variables[k] = v
                                        print(f"Injected routing: {k}={v}")
                                print(f"Executing add_override: {target}")
                                if target in ["agentTransfer", "Transfer"]:
                                    parts_to_return.append(
                                        Part.from_end_session(
                                            reason="escalate_to_human",
                                            escalated=True,
                                        )
                                    )
                                else:
                                    parts_to_return.append(
                                        Part.from_agent_transfer(
                                            agent=target
                                        )
                                    )
                        if parts_to_return:
                            return LlmResponse.from_parts(parts=parts_to_return)

    # 1. Tool Failure Interception and Routing
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('modify_close_ticket_wrapper'):
            response_dict = part.function_response.response.get('result', {})
            if 'error' in response_dict or not response_dict.get('webhook_success', True):
                print("Executing Tool Failure detected, initiating transfer to bell_ticket_mgmt_webhook_failure.")
                callback_context.variables['error_code'] = 'acut'
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, we encountered a technical error while cancelling your ticket. Let me transfer you."),
                    Part.from_agent_transfer(agent='AppointmentManagementAgent')
                ])

    # 2. Local/Global Counter Management & Exits
    local_noinput_counter = callback_context.variables.get('no_input_counter', 0)
    local_nomatch_counter = callback_context.variables.get('no_match_counter', 0)
    global_error_counter = callback_context.variables.get('global_error_counter', 0)

    # Dynamically tracking No-Input triggers from generic user silence intents
    for part in callback_context.get_last_user_input():
        text = part.text.lower() if part.text else ""
        if "no user activity detected" in text:
            local_noinput_counter += 1
            global_error_counter += 1
            callback_context.variables['no_input_counter'] = local_noinput_counter
            callback_context.variables['global_error_counter'] = global_error_counter
            print(f"No-input detected. Counter: {local_noinput_counter}")

    # Evaluate strict exit conditions per state machine blueprint
    if local_noinput_counter >= 3:
        print("No-input counter reaches 3, routing to bell_No_Input_3.")
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
        
    if local_nomatch_counter >= 3:
        print("No-match counter reaches 3, routing to bell_No_Match_3.")
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
        
    if global_error_counter >= 3:
        print("Global error counter reaches 3, routing to bell_aqd.")
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No input detected, incrementing counter to: {retry_count}')
            if retry_count >= 3:
                print('Max no-input retries reached, executing transfer to bell_No_Input_3')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            print('No input detected, reprompting user.')
            return LlmResponse.from_parts(parts=[Part.from_text('Hi, are you still there?')])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            print(f"No-Input detected. Count: {retry_count}")
            if retry_count >= 3:
                print("Max No-Input reached, transferring to bell_No_Input_3.")
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])
            return LlmResponse.from_parts(parts=[Part.from_text("Hi, are you still there?")])
    
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('evaluate_ticket_status_wrapper') or part.has_function_response('modify_close_ticket_wrapper'):
            if 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected in function response, initiating transfer to webhook failure route.")
                callback_context.variables["error_code"] = "acut"
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="AppointmentManagementAgent")])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Webhook Error Detection & Routing
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('fetch_active_omf_and_acut_tickets') or part.has_function_response('fetch_finalized_acut_tickets')):
            if 'error' in part.function_response.response.get('result', {}):
                print('Executing Tool Failure detected, initiating transfer to webhook failure queue.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We are experiencing technical difficulties fetching your tickets. Let me get someone to help you.'),
                    Part.from_agent_transfer(agent='AppointmentManagementAgent')
                ])

    # No-Input / No-Match Error Handling & Routing
    for part in callback_context.get_last_user_input():
        text_lower = part.text.lower() if part.text else ""
        if "no user activity detected" in text_lower or "sys.no-input" in text_lower:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No-input detected. Count: {retry_count}')
            if retry_count >= 3:
                print('Max no-input reached, transferring to bell_No_Input_3.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text("I didn't hear anything. Are you still there?")])
        
        if "sys.no-match" in text_lower:
            retry_count = callback_context.variables.get('no_match_counter', 0) + 1
            callback_context.variables['no_match_counter'] = retry_count
            print(f'No-match detected. Count: {retry_count}')
            if retry_count >= 3:
                print('Max no-match reached, transferring to bell_No_Match_3.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I'm having trouble understanding. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text("I didn't quite catch that. Could you please rephrase?")])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "no user activity detected" in text_lower or "no match" in text_lower:
                err_count = callback_context.variables.get("global_error_counter", 0) + 1
                callback_context.variables["global_error_counter"] = err_count
                print(f"Executing Conversational error detected. Count: {err_count}")
                if err_count >= 3:
                    print("Executing Conversational Error threshold reached, initiating transfer to bell_No_Input_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We seem to be having trouble. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                    
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('fetch_omf_orders_wrapper') or part.has_function_response('fetch_acut_tickets_wrapper'):
                resp = part.function_response.response.get('result', {})
                if 'error' in resp:
                    callback_context.variables['error_code'] = 1
                    print("Executing Tool Failure detected, initiating transfer to bell_ticket_mgmt_webhook_failure.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, something went wrong with our systems. Let me transfer you."),
                        Part.from_agent_transfer(agent='AppointmentManagementAgent')
                    ])
                    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('validate_and_format_phone_number') and 'error' in part.function_response.response.get('result', {})) or (part.has_function_response('check_home_phone_wrapper') and 'error' in part.function_response.response.get('result', {})):
            print("Executing Tool Failure detected, initiating transfer to bell_aqd.")
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                Part.from_agent_transfer(agent='RootAgent')
            ])
    
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            if retry_count >= 3:
                print("Max no-input retries reached, transferring to bell_No_Input_3.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            print("No input detected, prompting user again.")
            return LlmResponse.from_parts(parts=[Part.from_text("Hi, are you still there?")])
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print('Executing before_model_callback logic')
    
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('fetch_and_process_customer_tickets') and 'error' in part.function_response.response.get('result', {}):
            print('Executing Tool Failure detected, initiating transfer to bell_ticket_mgmt_webhook_failure.')
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, we are experiencing technical difficulties. Let me transfer you.'),
                Part.from_agent_transfer(agent='AppointmentManagementAgent')
            ])

    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'Executing No input detected. Count: {retry_count}')
            if retry_count >= 3:
                print('Executing Max no input reached, transferring to bell_No_Input_3.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text('Hi, are you still there?')])
            
    no_match_count = callback_context.variables.get('no_match_counter', 0)
    if no_match_count >= 3:
        print('Executing Max no match reached, transferring to bell_No_Match_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am having trouble understanding. Let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback for routing checks.")
    
    # 1. No Input & No Match Routing Checks
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "no user activity detected" in text_lower or "silence" in text_lower:
                print("Silence detected. Incrementing no_input counter.")
                retry = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry
                if retry >= 3:
                    print("Max no_input limit reached. Initiating transfer to bell_No_Input_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I'm sorry, are you still there?")
                ])
            
            if "unrecognized intent" in text_lower or "no match" in text_lower:
                print("Unrecognized intent detected. Incrementing no_match counter.")
                retry = callback_context.variables.get("no_match_counter", 0) + 1
                callback_context.variables["no_match_counter"] = retry
                if retry >= 3:
                    print("Max no_match limit reached. Initiating transfer to bell_No_Match_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm having trouble understanding. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't quite get that. Could you please repeat?")
                ])
    
    # 2. Webhook Error Handling -> Route to bell_ticket_mgmt_webhook_failure
    if llm_request.contents and len(llm_request.contents) > 0:
        for part in llm_request.contents[-1].parts:
            if (part.has_function_response("check_calendar_availability") or 
                part.has_function_response("select_calendar_interval") or 
                part.has_function_response("reserve_and_submit_appointment")):
                
                resp = part.function_response.response
                if "error" in resp or "error" in resp.get("result", {}):
                    print("Tool Failure detected, initiating transfer to webhook failure agent.")
                    callback_context.variables["error_code"] = "omf"
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm sorry, we are experiencing some technical difficulties. Let me transfer you."),
                        Part.from_agent_transfer(agent="AppointmentManagementAgent")
                    ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    global_err = callback_context.variables.get('global_error_counter', 0)
    local_nomatch = callback_context.variables.get('no_match_counter', 0)
    try:
        global_err = int(global_err)
    except:
        global_err = 0
    try:
        local_nomatch = int(local_nomatch)
    except:
        local_nomatch = 0
    if global_err >= 3 or local_nomatch >= 3:
        print('Error threshold reached, transferring to bell_aqd')
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])

    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('retrieve_and_enrich_acut_ticket') and 'error' in part.function_response.response.get('result', {}):
                print('Executing Tool Failure detected, initiating transfer.')
                callback_context.variables['error_code'] = 'acut'
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                    Part.from_agent_transfer(agent='AppointmentManagementAgent')
                ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents and llm_request.contents[-1].parts:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response("evaluate_mya_eligibility_and_format_sms"):
                res = part.function_response.response
                if "error" in res or "error" in res.get("result", {}):
                    print("Executing Tool Failure detected, terminating session.")
                    return LlmResponse.from_parts(parts=[Part.from_end_session(reason="Tool Failure")])

    user_inputs = callback_context.get_last_user_input()
    if user_inputs:
        for part in user_inputs:
            if part.text:
                text_lower = part.text.lower()
                if "no user activity detected" in text_lower:
                    print("No input detected.")
                    no_input_count = callback_context.variables.get("no_input_counter", 0) + 1
                    callback_context.variables["no_input_counter"] = no_input_count
                    global_error = callback_context.variables.get("global_error_counter", 0) + 1
                    callback_context.variables["global_error_counter"] = global_error
                    if global_error >= 3:
                        print("Global error counter >= 3, transferring to bell_aqd.")
                        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="TargetAgent_bell_aqd")])
                    if no_input_count >= 3:
                        print("Consecutive No Input >= 3, transferring to bell_No_Input_3.")
                        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="TargetAgent_bell_No_Input_3")])
                    lang = callback_context.variables.get("language", "en").lower()
                    if "fr" in lang:
                        msg = "Connaissez-vous notre appli Gérez votre rendez-vous? Il s'agit d'un moyen pratique de consulter, de replanifier ou d'annuler votre rendez-vous directement à partir de votre téléphone. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez, afin de vous permettre de commencer. Est-ce que cela vous convient?"
                    else:
                        msg = "Are you aware of our Manage Your Appointment App? It is a convenient way to view, reschedule, or cancel your appointment directly from your phone. I'll send you a text to the device you're calling from, so that you can get started. Is that alright? You can say 'Yes' or 'No'."
                    return LlmResponse.from_parts(parts=[Part.from_text(msg)])
                elif "no match" in text_lower or "sys.no-match" in text_lower:
                    print("No match detected.")
                    no_match_count = callback_context.variables.get("no_match_counter", 0) + 1
                    callback_context.variables["no_match_counter"] = no_match_count
                    global_error = callback_context.variables.get("global_error_counter", 0) + 1
                    callback_context.variables["global_error_counter"] = global_error
                    if global_error >= 3:
                        print("Global error counter >= 3, transferring to bell_aqd.")
                        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="TargetAgent_bell_aqd")])
                    if no_match_count >= 3:
                        print("Consecutive No Match >= 3, transferring to bell_No_Match_3.")
                        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="TargetAgent_bell_No_Match_3")])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('update_special_queue') and 'error' in part.function_response.response.get('result', {})):
            print("Executing Tool Failure detected, initiating transfer.")
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                Part.from_agent_transfer(agent='escalation_agent')
            ])

    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            print("No user activity detected. Checking error counters.")
            retry_count = int(callback_context.variables.get("global_error_counter", 0)) + 1
            callback_context.variables["global_error_counter"] = retry_count
            
            lang = str(callback_context.variables.get("language", "en")).lower()
            
            if retry_count >= 3:
                print("Max retries reached. Terminating session due to no input.")
                msg = "We haven't heard from you. Let me transfer you to an agent." if lang == "en" else "Nous n'avons rien entendu. Permettez-moi de vous transférer à un agent."
                return LlmResponse.from_parts(parts=[
                    Part.from_text(msg),
                    Part.from_end_session(reason="Max errors reached")
                ])
                
            print("Sending standard fallback prompt.")
            fallback_msg = "I didn't get that. Can you say it again?" if lang == "en" else "J'ai du mal à comprendre cette question."
            return LlmResponse.from_parts(
                parts=[Part.from_text(fallback_msg)]
            )
            
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback: bell_ticket_mgmt_change_cancel_ticket")
    
    # Pattern C: Deterministic Greeting
    if callback_context.variables.get("first_turn", True):
        print("First turn detected. Sending initial greeting.")
        callback_context.variables["first_turn"] = False
        lang = str(callback_context.variables.get("language", "English")).lower()
        if "fr" in lang or "french" in lang:
            msg = "Voulez-vous changer ou annuler votre rendez-vous?"
        else:
            msg = "Are you looking to change or cancel your appointment?"
        response = LlmResponse.from_parts([Part.from_text(msg)])
        response.partial = True
        return response

    # Pattern E: No-Input Handling & Escalation
    for part in callback_context.get_last_user_input():
        if part.text:
            text = part.text.lower()
            if "no user activity detected" in text or text.strip() == "":
                print("No-Input detected.")
                global_err = int(callback_context.variables.get("global_error_counter", 0)) + 1
                local_err = int(callback_context.variables.get("no_input_counter", 0)) + 1
                
                callback_context.variables["global_error_counter"] = global_err
                callback_context.variables["no_input_counter"] = local_err
                
                if global_err >= 3 or local_err >= 3:
                    print("Max errors reached, transferring to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                
                print("Sending local no-input reprompt.")
                lang = str(callback_context.variables.get("language", "English")).lower()
                if "fr" in lang or "french" in lang:
                    msg = "Désolé(e), je n'ai pas compris. Souhaitez-vous modifier ou annuler votre rendez-vous ?"
                else:
                    msg = "Sorry, I didn't get that. Are you looking to change or cancel your appointment?"
                return LlmResponse.from_parts(parts=[Part.from_text(msg)])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            print("Executing Tool Failure detected, initiating transfer (No Input).")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("No Input threshold reached, transferring to bell_No_Input_3.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text("Hi, are you still there?")]
            )

    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('modify_acut_contact_preference') and 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating transfer to bell_ticket_mgmt_webhook_failure.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent="AppointmentManagementAgent")
                ])
            if part.has_function_response('check_wfas_availability') and 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating transfer to bell_ticket_mgmt_webhook_failure.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent="AppointmentManagementAgent")
                ])
            if part.has_function_response('book_and_assign_appointment') and 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating transfer to bell_ticket_mgmt_webhook_failure.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent="AppointmentManagementAgent")
                ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback checks")
    
    user_inputs = callback_context.get_last_user_input()
    for part in user_inputs:
        if part.text:
            text_lower = part.text.lower().strip()
            if "start over" in text_lower or "start again" in text_lower or "recommencer" in text_lower:
                print("Global start over requested. Overriding transition to Default Start Flow.")
                callback_context.variables["routing_val"] = "full start over"
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Okay, let me get you back to the beginning."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
            if "no user activity detected" in text_lower:
                local_noinput = callback_context.variables.get("no_input_counter", 0) + 1
                global_error = callback_context.variables.get("global_error_counter", 0) + 1
                callback_context.variables["no_input_counter"] = local_noinput
                callback_context.variables["global_error_counter"] = global_error
                
                print(f"No Input detected. Local: {local_noinput}, Global: {global_error}")
                if global_error >= 3:
                    print("Global error limit reached. Routing to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I am having trouble hearing you. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                if local_noinput >= 3:
                    print("Local no-input limit reached. Routing to bell_No_Input_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Since I haven't heard from you, I'll transfer you now."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                return LlmResponse.from_parts(parts=[Part.from_text("Are you still there?")])
                
    for part in llm_request.contents[-1].parts:
        if part.has_function_response("fetch_omf_order_details"):
            if "error" in part.function_response.response.get("result", {}):
                print("OMF Webhook Failure detected. Transferring to technical agent.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Let's get you over to our technical team to look into your connection."),
                    Part.from_agent_transfer(agent="TechSupportAndRepairAgent")
                ])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('update_acut_contact') and 'error' in part.function_response.response.get('result', {}):
                print('Executing Tool Failure detected in ACUT, initiating transfer.')
                callback_context.variables['error_code'] = 'acut'
                return LlmResponse.from_parts(parts=[
                    Part.from_text('I am sorry, we are experiencing technical difficulties. Let me transfer you.'),
                    Part.from_agent_transfer(agent='Target_Agent_bell_ticket_mgmt_webhook_failure')
                ])
            for tool_name in ['check_wfas_availability', 'reschedule_wfas_appointment_bundled', 'cancel_wfas_interaction']:
                if part.has_function_response(tool_name) and 'error' in part.function_response.response.get('result', {}):
                    print('Executing Tool Failure detected in WFAS, initiating transfer.')
                    callback_context.variables['error_code'] = 'wfas'
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('I am sorry, we are experiencing technical difficulties. Let me transfer you.'),
                        Part.from_agent_transfer(agent='Target_Agent_bell_ticket_mgmt_webhook_failure')
                    ])

    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No input detected. Count: {retry_count}')
            if retry_count >= 3:
                print('Max no input retries reached, transferring to aqd.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you. Let me transfer you to an agent.'),
                    Part.from_agent_transfer(agent='Target_Agent_bell_aqd')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text('Hi, are you still there?')])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    global_error_counter = callback_context.variables.get('global_error_counter', 0)
    if isinstance(global_error_counter, (int, float)) and global_error_counter >= 3:
        print("Global error counter exceeded, initiating transfer to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("I'm having trouble understanding. Let me transfer you to a human agent who can help."),
            Part.from_agent_transfer(agent='RootAgent')
        ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Handle No-Input and No-Match thresholds
    global_error = callback_context.variables.get("global_error_counter", 0)
    local_noinput = callback_context.variables.get("no_input_counter", 0)
    local_nomatch = callback_context.variables.get("no_match_counter", 0)

    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "no user activity detected" in text_lower:
                local_noinput += 1
                callback_context.variables["no_input_counter"] = local_noinput
                global_error += 1
                callback_context.variables["global_error_counter"] = global_error
                print(f"No-input detected. Local: {local_noinput}, Global: {global_error}")
            elif "no match" in text_lower or "sys.no-match" in text_lower:
                local_nomatch += 1
                callback_context.variables["no_match_counter"] = local_nomatch
                global_error += 1
                callback_context.variables["global_error_counter"] = global_error
                print(f"No-match detected. Local: {local_nomatch}, Global: {global_error}")

            if local_noinput >= 3 or local_nomatch >= 3 or global_error >= 3:
                print("Max errors reached, initiating transfer to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Let me transfer you to someone who can help."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])

    # Webhook Failure Detection & Routing
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response("get_omf_order_details"):
                response_data = part.function_response.response.get("result", {})
                if "error" in part.function_response.response or "error" in response_data:
                    print("Webhook execution failed, routing to bell_ticket_mgmt_webhook_failure.")
                    callback_context.variables["error_code"] = "omf"
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm sorry, I couldn't pull up your order details. Let me get someone to help."),
                        Part.from_agent_transfer(agent="AppointmentManagementAgent")
                    ])

    print("No overriding conditions met in before_model_callback.")
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('extract_mya_eligibility') and 'error' in part.function_response.response.get('result', {}):
                print('Executing Tool Failure detected, initiating transfer to bell_aqd.')
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    last_input = callback_context.get_last_user_input()
    if last_input:
        for part in last_input:
            if part.text:
                text_lower = part.text.lower()
                if 'no user activity detected' in text_lower or 'sys.no-input-default' in text_lower:
                    retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                    callback_context.variables['no_input_counter'] = retry_count
                    if retry_count >= 3:
                        print('Max no-input retries reached, ending session.')
                        return LlmResponse.from_parts(parts=[
                            Part.from_end_session(reason='Max no-input reached')
                        ])
                    print('No-input detected, reprompting.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I didn't get that. Can you say it again?")
                    ])
                elif 'sys.no-match-default' in text_lower:
                    print('No-match detected, reprompting.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I didn't get that. Can you say it again?")
                    ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback")
    
    if callback_context.variables.get("first_turn", True):
        print("First turn detected, checking auth status")
        callback_context.variables["first_turn"] = False
        auth_status = callback_context.variables.get("auth_status")
        if auth_status is None or str(auth_status).strip().lower() in ["null", "none", ""]:
            print("Auth status is null, terminating session.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("For security reasons, we need to verify your account first. Please try again later."),
                Part.from_end_session(reason="Unauthenticated User")
            ])
            
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            print("No-input detected")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max no-input retries reached, transferring to default failure agent.")
                callback_context.variables["route"] = "tech_change_appointment_mya_false"
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("Prompting user for input retry.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("I'm sorry, I didn't get that. Are you still there?")]
            )
            
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('update_tech_visit_context') and 'error' in part.function_response.response.get('result', {}):
            print("Executing Tool Failure detected, initiating session end.")
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong. Please call back later.'),
                Part.from_end_session(reason='Tool Failure')
            ])

    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if 'no user activity detected' in text_lower or 'sys.no-input' in text_lower:
                retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                callback_context.variables['no_input_counter'] = retry_count
                if retry_count >= 3:
                    print("Max no-input retries reached, transferring to agent.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We haven\'t heard from you. Let me transfer you to an agent.'),
                        Part.from_agent_transfer(agent='escalation_agent')
                    ])
                print("No input detected, prompting user again.")
                return LlmResponse.from_parts(parts=[Part.from_text('I didn\'t get that. Can you say it again?')])

            if 'unrecognized input' in text_lower or 'sys.no-match' in text_lower:
                nm_retry = callback_context.variables.get('global_error_counter', 0) + 1
                callback_context.variables['global_error_counter'] = nm_retry
                if nm_retry >= 3:
                    print("Max no-match retries reached, transferring to agent.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, I\'m having trouble. Let me transfer you.'),
                        Part.from_agent_transfer(agent='escalation_agent')
                    ])
                print("No match detected, prompting user again.")
                return LlmResponse.from_parts(parts=[Part.from_text('I didn\'t get that. Can you say it again? / J\'ai du mal à comprendre cette question.')])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    user_inputs = callback_context.get_last_user_input()
    if user_inputs:
        for part in user_inputs:
            text = part.text.lower() if part.text else ''
            if 'no user activity detected' in text or 'no match' in text:
                retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                callback_context.variables['no_input_counter'] = retry_count
                if retry_count >= 3:
                    print('Max retries exceeded, routing to bell_aqd.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We are having trouble understanding you. Let me transfer you.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                print(f'No-input/No-match retry count: {retry_count}')
                return LlmResponse.from_parts(
                    parts=[Part.from_text("Sorry, I didn't get that. Can you say it again?")]
                )
    
    if llm_request.contents and llm_request.contents[-1].parts:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('evaluate_mya_eligibility'):
                response_dict = part.function_response.response.get('result', {})
                if 'error' in response_dict:
                    print('Executing Tool Failure detected, initiating transfer to bell_aqd.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    global_error_counter = int(callback_context.variables.get('global_error_counter', 0))
    if global_error_counter >= 3:
        print("Global error counter exceeded 3, escalating to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("We seem to be having trouble understanding each other. Let me transfer you to an agent."),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    if llm_request.contents and len(llm_request.contents) > 0:
        for part in llm_request.contents[-1].parts:
            if (part.has_function_response('acut_ticket_search_and_retrieve') or
                part.has_function_response('acut_content_lookup_wrapper')):
                response_dict = part.function_response.response.get('result', {})
                if 'error' in response_dict:
                    print("Executing Tool Failure detected, initiating transfer.")
                    error_route = 'bell_tech_service_outage_&_Tech_connection_issue'
                    if callback_context.variables.get('from_flow') == 'bell_vr_kickout':
                        error_route = 'bell_aqd'
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                        Part.from_agent_transfer(agent=error_route)
                    ])
    return None