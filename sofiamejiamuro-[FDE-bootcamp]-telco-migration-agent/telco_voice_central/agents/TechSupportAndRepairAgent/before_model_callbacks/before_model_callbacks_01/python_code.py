NATIVE_TRANSFER_TARGETS = {"RootAgent", "TechSupportAndRepairAgent"}

NATIVE_TRANSFER_TARGETS = {"RootAgent", "TechSupportAndRepairAgent"}

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
                for t in ["extract_entities", "routing"]
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
                for t in ["extract_entities", "routing"]
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

    language = str(callback_context.variables.get("language", "en")).lower()
    
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            
            if "no user activity detected" in text_lower or "sys.no-input" in text_lower:
                print("Executing No-Input detected logic.")
                retry_count = int(callback_context.variables.get("no_input_counter", 0)) + 1
                callback_context.variables["no_input_counter"] = retry_count
                
                if retry_count >= 3:
                    print("No-input threshold exceeded, executing fallback routing.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you to an agent." if "en" in language else "Nous n'avons pas de reponse. Laissez-moi vous transferer a un agent."),
                        Part.from_agent_transfer(agent="escalation_agent")
                    ])
                
                print("Playing localized silence reprompt.")
                reprompt = "I didn't get that. Can you say it again?" if "en" in language else "J'ai du mal à comprendre cette question."
                return LlmResponse.from_parts(parts=[Part.from_text(reprompt)])
            
            if "sys.no-match" in text_lower or "sys.no-match-default" in text_lower:
                print("Executing No-Match detected logic.")
                error_count = int(callback_context.variables.get("global_error_counter", 0)) + 1
                callback_context.variables["global_error_counter"] = error_count
                
                if error_count >= 3:
                    print("No-match threshold exceeded, executing fallback routing.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm having trouble understanding. Let me transfer you to an agent." if "en" in language else "J'ai des difficultes a comprendre. Laissez-moi vous transferer a un agent."),
                        Part.from_agent_transfer(agent="escalation_agent")
                    ])
                
                print("Playing localized comprehension reprompt.")
                reprompt = "I missed what you said. What was that?" if "en" in language else "Je n'ai pas saisi ce que vous avez dit."
                return LlmResponse.from_parts(parts=[Part.from_text(reprompt)])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print('Executing before_model_callback logic gates.')
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('execute_comprehensive_outage_check') and 'error' in part.function_response.response.get('result', {}):
            print('Executing Tool Failure detected, initiating transfer.')
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, due to an unexpected system issue, I was unable to verify if there is an active outage in your area. Let me transfer you so we can sort this out.'),
                Part.from_agent_transfer(agent='bell_SMS_Trigger')
            ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback")
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            print("No-input detected in before_model_callback")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            print(f"No-input retry count is now {retry_count}")
            if retry_count >= 3:
                print("Max no-input retries reached, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent. / Nous n'avons rien entendu. Je vous transfère à un agent."),
                    Part.from_agent_transfer(agent="escalation_agent")
                ])
            print("Playing bilingual reprompt for no-input.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre. Pouvez-vous répéter?")
            ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        user_input_text = ""
        for part in callback_context.get_last_user_input():
            if part.text:
                user_input_text += part.text.lower()
        
        if "no user activity detected" in user_input_text or "sys.no-match-default" in user_input_text:
            retry_count = callback_context.variables.get("global_error_counter", 0) + 1
            callback_context.variables["global_error_counter"] = retry_count
            print(f"Error detected (no-match/no-input). Retry count: {retry_count}")
            
            if retry_count >= 3:
                print("Max retries reached, initiating Live_Agent_Transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I'm sorry, I'm still having trouble. Let me transfer you to an agent. / Je suis désolé, je vais vous transférer à un agent."),
                    Part.from_agent_transfer(agent="Live_Agent_Transfer")
                ])
            
            return LlmResponse.from_parts(parts=[
                Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
            ])

        for part in llm_request.contents[-1].parts:
            if part.has_function_response("evaluate_and_set_apb_routing") and "error" in part.function_response.response.get("result", {}):
                print("Executing Tool Failure detected, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong with the system. Let me transfer you."),
                    Part.from_agent_transfer(agent="Live_Agent_Transfer")
                ])
                
        return None
    except Exception as e:
        print(f"Callback error: {e}")
        return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Evaluating before_model_callback for bell_vr_api_failure_handler")
    
    # State Machine: ROUTE_TO_AQD on Agent initialization
    if callback_context.variables.get('first_turn', True):
        print("Agent initialization detected, routing immediately to bell_aqd.")
        callback_context.variables['first_turn'] = False
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])

    # Handle sys.no-input-default and sys.no-match-default fallbacks
    last_input = callback_context.get_last_user_input()
    for part in last_input:
        if part.text:
            if 'no user activity detected' in part.text.lower():
                print("sys.no-input-default triggered. Playing bilingual error and transferring to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't get that... / J'ai du mal à comprendre..."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            else:
                print("sys.no-match-default / invalid input triggered. Playing bilingual error and transferring to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't get that... / J'ai du mal à comprendre..."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('prepare_route_parameters') and 'error' in part.function_response.response.get('result', {}):
            print("Executing Tool Failure detected, initiating transfer.")
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                Part.from_agent_transfer(agent='RootAgent')
            ])
            
    if callback_context.get_last_user_input():
        for part in callback_context.get_last_user_input():
            if part.text:
                text = part.text.lower()
                if "no user activity detected" in text or "sys.no-input-default" in text:
                    print("No-input detected, playing reprompt and incrementing counter.")
                    retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                    callback_context.variables["no_input_counter"] = retry_count
                    if retry_count >= 3:
                        print("Max no-input retries reached, routing to agent.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                            Part.from_agent_transfer(agent="RootAgent")
                        ])
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
                    ])
                elif "sys.no-match-default" in text:
                    print("No-match detected, playing reprompt and incrementing global error counter.")
                    err_count = callback_context.variables.get("global_error_counter", 0) + 1
                    callback_context.variables["global_error_counter"] = err_count
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Handle no-input / silence overrides globally
    for part in callback_context.get_last_user_input():
        if part.text and ("no user activity detected" in part.text.lower() or "no-match" in part.text.lower()):
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max no-input retries reached, routing to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("Prompting user for no-input/no-match.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("Sorry, I didn't get that. Can you please repeat?")]
            )
    
    # Enforce API Failure thresholds and transfers for task fetches
    if llm_request.contents and len(llm_request.contents) > 0:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('fetch_vr_next_task_wrapper'):
                result = part.function_response.response.get('result', {})
                if 'error' in result:
                    counter = callback_context.variables.get('loop_counter', 0) + 1
                    callback_context.variables['loop_counter'] = counter
                    if counter >= 3:
                        print("Executing Tool Failure detected 3 times, initiating transfer to bell_vr_api_failure_handler.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_text("I need to connect you to an agent."),
                            Part.from_agent_transfer(agent='TechSupportAndRepairAgent')
                        ])
                    else:
                        print(f"Executing Tool Failure detected (Attempt {counter}), injecting retry instruction.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_text("Oops! Something went wrong on my end. Let me try that again for you.")
                        ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            print("Executing No-Input logic.")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max no-input retries reached, transferring to agent.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I need to connect you to an agent. / J'ai besoin que vous vous connectiez à un agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("Playing retry prompt.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question. Pouvez-vous répéter?")]
            )
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('vr_post_answer_wrapper'):
                res = part.function_response.response.get('result', {})
                if 'error' in res:
                    print("Executing Tool Failure detected, initiating API error routing.")
                    counter = callback_context.variables.get('counter_post_task', 0) + 1
                    callback_context.variables['counter_post_task'] = counter
                    if counter >= 3:
                        print("Max API failures reached, routing to api failure handler.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_text("I need to connect you to an agent. / J'ai besoin que vous vous connectiez à un agent."),
                            Part.from_agent_transfer(agent="TechSupportAndRepairAgent")
                        ])
                    print("API failure retry logic executed.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Oops! Something went wrong on my end. Let me try that again for you. / Oups ! Une erreur s'est produite de mon côté. Permettez-moi de réessayer pour vous.")
                    ])
                elif res.get('webhook_success') is False:
                    print("Webhook success false detected, routing to AQD.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Oops! Something went wrong on my end. I need to connect you to an agent. / Oups! Une erreur est survenue de mon côté. Je vais vous mettre en relation avec un agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if callback_context.variables.get("first_turn", True):
        print("Executing deterministic greeting based on first_turn check.")
        callback_context.variables["first_turn"] = False
        lang = str(callback_context.variables.get("language", "en")).lower()
        if "fr" in lang:
            msg = "Un instant, je récupère les détails pour vous."
        else:
            msg = "Just a moment while I fetch some details for you."
        
        response = LlmResponse.from_parts([Part.from_text(msg)])
        response.partial = True
        return response

    for part in llm_request.contents[-1].parts:
        if part.has_function_response('extract_service_details'):
            response_data = part.function_response.response
            if 'error' in response_data:
                print("Tool Failure detected in extract_service_details, initiating transfer to bell_aqd.")
                callback_context.variables['hardstop'] = True
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        text = (part.text or '').lower()
        if 'no user activity detected' in text or 'no match' in text or 'unrecognized' in text:
            print('Executing No-Input fallback logic.')
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            if retry_count >= 3:
                return LlmResponse.from_parts(parts=[
                    Part.from_text('I am having trouble. Let me transfer you. / J\'éprouve des difficultés. Je vais vous transférer.'),
                    Part.from_agent_transfer(agent='escalation_agent')
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text('I didn\'t get that. Can you say it again? / J\'ai du mal à comprendre cette question. Pouvez-vous répéter?')]
            )

    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('start_vr_process_wrapper'):
                response_data = part.function_response.response.get('result', {})
                if 'error' in response_data or response_data.get('status') == 'failure':
                    print('Executing Tool Failure detected, evaluating retry logic.')
                    counter = callback_context.variables.get('loop_counter', 0) + 1
                    callback_context.variables['loop_counter'] = counter
                    
                    if counter <= 2:
                        svc_id = callback_context.variables.get('service_id', '')
                        retry_call = Part.from_function_call(
                            name='start_vr_process_wrapper',
                            args={'service_id': svc_id}
                        )
                        return LlmResponse.from_parts(parts=[
                            Part.from_text('Oops! Something went wrong on my end. Let me try that again for you. <speak><break time="5s"/></speak> Oups ! Une erreur s\'est produite de mon côté. Permettez-moi de réessayer pour vous.'),
                            retry_call
                        ])
                    elif counter == 3:
                        return LlmResponse.from_parts(parts=[
                            Part.from_text('I need to connect you to an agent. / J\'ai besoin que vous vous connectiez à un agent.'),
                            Part.from_agent_transfer(agent='TechSupportAndRepairAgent')
                        ])
                    else:
                        callback_context.variables['hardstop'] = True
                        return LlmResponse.from_parts(parts=[
                            Part.from_agent_transfer(agent='RootAgent')
                        ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if callback_context.variables.get('first_turn', True):
        callback_context.variables['first_turn'] = False
        callback_context.variables['apb_location_id'] = 70012
        callback_context.variables['context_source'] = 'bell_rehit'
        print('First turn initialized static routing variables.')
        
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text.lower():
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No-input detected, retry count: {retry_count}')
            
            if retry_count == 1:
                print('Triggering reprompt message 1')
                response = LlmResponse.from_parts(parts=[Part.from_text("I didn't quite get that. Can you try again?")])
                response.partial = True
                return response
            elif retry_count == 2:
                print('Triggering reprompt message 2')
                response = LlmResponse.from_parts(parts=[Part.from_text("I still didn't get that")])
                response.partial = True
                return response
            elif retry_count >= 3:
                print('Max No-Input Reached, forcing END_SESSION transition')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I am still having trouble getting your response."),
                    Part.from_end_session(reason='Max No-Input Reached')
                ])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        last_inputs = callback_context.get_last_user_input()
        is_no_input = False
        is_no_match = False
        
        if last_inputs:
            for part in last_inputs:
                if part.text:
                    text_lower = part.text.lower()
                    if "no user activity detected" in text_lower or "sys.no-input" in text_lower:
                        is_no_input = True
                    elif "sys.no-match" in text_lower:
                        is_no_match = True
                        
        if is_no_input or is_no_match:
            global_err = int(callback_context.variables.get("global_error_counter") or 0) + 1
            callback_context.variables["global_error_counter"] = global_err
            print(f"Global error counter incremented: {global_err}")
            
            if global_err >= 3:
                print("Global error limit reached, initiating transfer to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
            if is_no_input:
                local_noinput = int(callback_context.variables.get("no_input_counter") or 0) + 1
                callback_context.variables["no_input_counter"] = local_noinput
                print(f"Local no-input counter: {local_noinput}")
                if local_noinput >= 3:
                    print("No-input limit reached, routing to bell_No_Input_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                return LlmResponse.from_parts(parts=[Part.from_text("Hi, are you still there?")])
                
            if is_no_match:
                local_nomatch = int(callback_context.variables.get("no_match_counter") or 0) + 1
                callback_context.variables["no_match_counter"] = local_nomatch
                print(f"Local no-match counter: {local_nomatch}")
                if local_nomatch >= 3:
                    print("No-match limit reached, routing to bell_No_Match_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm having trouble understanding. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                return LlmResponse.from_parts(parts=[Part.from_text("I didn't quite catch that. Could you repeat?")])
                
        for part in llm_request.contents[-1].parts:
            if part.has_function_response("prepare_troubleshooting_sms") and "error" in part.function_response.response.get("result", {}):
                print("Executing Tool Failure detected, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
    except Exception as e:
        print(f"Callback execution failed: {e}")
        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback checks for bell_rehit_Check_Subscription")
    
    # Initialize tracking variables on first turn
    if callback_context.variables.get("first_turn", True):
        print("First turn detected, initializing local counters")
        callback_context.variables["first_turn"] = False
        callback_context.variables["no_input_counter"] = 0
        callback_context.variables["no_match_counter"] = 0

    global_error_counter = callback_context.variables.get("global_error_counter", 0)
    
    # Enforce Global Error Thresholds
    if global_error_counter >= 3:
        print("Global error limit exceeded (>=3), routing to bell_aqd")
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])

    # Detect No-Input (Silence/Timeout) scenarios
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            local_noinput = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = local_noinput
            
            global_error_counter += 1
            callback_context.variables["global_error_counter"] = global_error_counter
            
            print(f"No-input detected. Local counter: {local_noinput}, Global counter: {global_error_counter}")

            # Escalation: Global Counter Reached during no-input
            if global_error_counter >= 3:
                print("Global error limit exceeded via no-input, routing to bell_aqd")
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])

            # Escalation: Local No-Input Threshold Reached
            if local_noinput >= 3:
                print("Local no-input limit exceeded, routing to bell_No_Input_3")
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])

            # Provide localized contextual retry prompt
            lang = callback_context.variables.get("language", "English")
            if str(lang).lower() == "french":
                msg = "J'ai mal compris votre demande. Pouvez-vous voir si les chaînes manquantes sont incluses dans votre abonnement?"
            else:
                msg = "I'm having trouble understanding. Can you see if the missing channels are included in your subscription?"
            
            response = LlmResponse.from_parts(parts=[Part.from_text(msg)])
            # Allow the agent to continue processing after reprompting
            response.partial = True
            return response

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print('Executing before_model_callback')
    
    # Enforce Hardstop parameter on entry
    if callback_context.variables.get('first_turn', True):
        print('First turn detected, setting hardstop parameter to True')
        callback_context.variables['first_turn'] = False
        callback_context.variables['hardstop'] = True

    # Handle sys.no-input or sys.no-match events
    for part in callback_context.get_last_user_input():
        text = (part.text or '').lower()
        if 'no user activity detected' in text or 'sys.no-input' in text or 'sys.no-match' in text:
            print('Executing Error Handling: No-input or no-match detected')
            current_errors = callback_context.variables.get('global_error_counter', 0)
            callback_context.variables['global_error_counter'] = current_errors + 1
            return LlmResponse.from_parts(parts=[
                Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
            ])

    # Intercept execute_tv_rehit_wrapper tool failures and route to bell_rehit_SMS (Pattern A override)
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if (part.has_function_response('execute_tv_rehit_wrapper') and 'error' in part.function_response.response.get('result', {})):
                print('Executing Tool Failure detected, initiating transfer to bell_rehit_SMS')
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='TechSupportAndRepairAgent')
                ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # 1. Tool Failures (Fallback to bell_aqd)
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if (part.has_function_response('configure_tv_sync_sms_payload') and 
                'error' in part.function_response.response.get('result', {})):
                print("Tool failure detected in configure_tv_sync_sms_payload, routing to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='RootAgent')
                ])
    
    # 2. Extract User Input Text
    user_text = ""
    for part in callback_context.get_last_user_input():
        if part.text:
            user_text += part.text.lower()

    # 3. No-Input / Silence Check
    if "no user activity detected" in user_text or "sys.no-input" in user_text:
        print("No input / silence detected.")
        no_input_count = callback_context.variables.get('no_input_counter', 0) + 1
        global_err_count = callback_context.variables.get('global_error_counter', 0) + 1
        
        callback_context.variables['no_input_counter'] = no_input_count
        callback_context.variables['global_error_counter'] = global_err_count
        
        if global_err_count >= 3 or no_input_count >= 1:
            print("No-input threshold or global error threshold met, transferring to bell_aqd.")
            return LlmResponse.from_parts(parts=[
                Part.from_agent_transfer(agent='RootAgent')
            ])

    # 4. No-Match Check
    if "sys.no-match" in user_text:
        print("No match detected.")
        nm_count = callback_context.variables.get('no_match_counter', 0) + 1
        global_err_count = callback_context.variables.get('global_error_counter', 0) + 1
        
        callback_context.variables['no_match_counter'] = nm_count
        callback_context.variables['global_error_counter'] = global_err_count
        
        if nm_count >= 3:
            print("3 Consecutive No-Matches detected, transferring to bell_No_Match_3.")
            return LlmResponse.from_parts(parts=[
                Part.from_agent_transfer(agent='RootAgent')
            ])
        if global_err_count >= 3:
            print("Global error threshold met on no-match, transferring to bell_aqd.")
            return LlmResponse.from_parts(parts=[
                Part.from_agent_transfer(agent='RootAgent')
            ])
            
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            local_noinput_counter = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = local_noinput_counter
            print(f"No-input detected. Count: {local_noinput_counter}")
            if local_noinput_counter >= 3:
                print("local_noinput_counter >= 3, transferring to bell_No_Input_3")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text("Hi, are you still there?")]
            )

    local_nomatch_counter = callback_context.variables.get("no_match_counter", 0)
    if local_nomatch_counter >= 3:
        print("local_nomatch_counter >= 3, transferring to bell_No_Match_3")
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent="RootAgent")
        ])

    global_error_counter = callback_context.variables.get("global_error_counter", 0)
    if global_error_counter >= 3:
        print("global_error_counter >= 3, transferring to bell_aqd")
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent="RootAgent")
        ])

    for part in llm_request.contents[-1].parts:
        if part.has_function_response("sat_rehit_wrapper"):
            response_data = part.function_response.response.get("result", {})
            if "error" in response_data:
                print("Tool Failure detected in sat_rehit_wrapper, routing to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            if not response_data.get("webhook_success", True):
                print("Webhook returned false, routing to bell_rehit_SMS.")
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent="TechSupportAndRepairAgent")
                ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    nomatch_count = int(callback_context.variables.get('no_match_counter', 0))
    noinput_count = int(callback_context.variables.get('no_input_counter', 0))
    
    if nomatch_count >= 3:
        print('Executing Too Many No-Matches detected, initiating transfer to bell_No_Match_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    if noinput_count >= 3:
        print('Executing Too Many No-Inputs detected, initiating transfer to bell_No_Input_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('acut_search_find_wrapper') or part.has_function_response('omf_order_summary_wrapper'):
            response_dict = part.function_response.response.get('result', {})
            if 'error' in response_dict:
                print('Executing Tool Failure detected, initiating transfer to webhook failure flow.')
                callback_context.variables['error_code'] = 'tech_intent'
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='AppointmentManagementAgent')
                ])
                
    return None