NATIVE_TRANSFER_TARGETS = {"RootAgent", "SalesAndEquipmentAgent"}

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

    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "no user activity detected" in text_lower or "sys.no-input" in text_lower:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                if retry_count >= 3:
                    print("Max no-input retries reached, transferring to escalation_agent.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="escalation_agent")
                    ])
                print("No-input detected, reprompting user.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't get that. Can you say it again?")
                ])
            if "wrapup" in text_lower:
                print("Wrapup event detected, forcing transition to END_SESSION.")
                return LlmResponse.from_parts(parts=[
                    Part.from_end_session(reason="wrapup event")
                ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print('Checking before_model_callback error counters')
    
    global_err = int(callback_context.variables.get('global_error_counter', 0))
    if global_err >= 3:
        print('Global error limit reached, routing to bell_aqd')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am transferring you to an agent.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    local_nomatch = int(callback_context.variables.get('no_match_counter', 0))
    if local_nomatch >= 3:
        print('No match limit reached, routing to bell_No_Match_3')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am transferring you to an agent.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    local_noinput = int(callback_context.variables.get('no_input_counter', 0))
    if local_noinput >= 3:
        print('No input limit reached, routing to bell_No_Input_3')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am transferring you to an agent.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('search_customer_by_tn') or part.has_function_response('lookup_npa_nxx'):
                if 'error' in part.function_response.response.get('result', {}):
                    print('Tool failure detected, setting identification_status to Fail for silent routing')
                    callback_context.variables['identification_status'] = 'Fail'

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        for part in callback_context.get_last_user_input():
            if part.text and "no user activity detected" in part.text:
                print("Silence detected, triggering no-input logic.")
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                if retry_count >= 3:
                    print("Max silence retries reached. Transferring to agent.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We have not heard from you. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="escalation_agent")
                    ])
                print("Prompting user to repeat due to silence.")
                return LlmResponse.from_parts(parts=[Part.from_text("I did not get that. Can you say it again?")])

        if llm_request.contents:
            for part in llm_request.contents[-1].parts:
                if part.has_function_response("set_sales_routing_parameters") and "error" in part.function_response.response.get("result", {}):
                    print("Executing Tool Failure detected, initiating transfer.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, something went wrong. Let me transfer you."),
                        Part.from_agent_transfer(agent="escalation_agent")
                    ])
    except Exception as e:
        print(f"Callback Error: {e}")

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Check for Tool Failures
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('update_session_route') and 'error' in part.function_response.response.get('result', {})):
            print("Executing Tool Failure detected, initiating transfer.")
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                Part.from_agent_transfer(agent='RootAgent')
            ])

    # Check for consecutive sys.no-input or sys.no-match exceedances
    for part in callback_context.get_last_user_input():
        if part.text and ("no user activity detected" in part.text.lower() or "sys.no-input" in part.text.lower() or "sys.no-match" in part.text.lower()):
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f"No-input or no-match detected. Current retry count: {retry_count}")
            
            if retry_count >= 3:
                print("Max retries reached (3), transferring to bell_determine_handover.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Je n’ai toujours pas compris. / I still didn't get that. Let me transfer you."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
                
            print("Prompting user to retry due to no-match/no-input.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("Je n’ai pas tout à fait compris. Pouvez-vous réessayer? / I didn't quite get that. Can you try again?")]
            )
        elif part.text:
            if callback_context.variables.get('no_input_counter', 0) > 0:
                print("Valid user input received, resetting retry count.")
                callback_context.variables['no_input_counter'] = 0

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        user_inputs = callback_context.get_last_user_input()
        if not user_inputs:
            print("No user input to process in callback.")
            return None

        for part in user_inputs:
            text = part.text.lower() if part.text else ""
            
            if "wrapup" in text:
                print("Wrapup event detected. Triggering END_SESSION.")
                return LlmResponse.from_parts(parts=[
                    Part.from_end_session(reason="Wrapup event")
                ])

            if "no user activity detected" in text or "sys.no-input-default" in text or "sys.no-match-default" in text:
                print("No-input or no-match event triggered.")
                
                retry_count = int(callback_context.variables.get("no_input_counter", 0)) + 1
                callback_context.variables["no_input_counter"] = retry_count
                
                global_error = int(callback_context.variables.get("global_error_counter", 0)) + 1
                callback_context.variables["global_error_counter"] = global_error
                
                if retry_count >= 3:
                    print("Max retries exceeded. Ending session.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you or are having trouble understanding. Ending the session."),
                        Part.from_end_session(reason="Max retries reached")
                    ])
                
                print("Playing bilingual fallback message.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
                ])

        print("No override conditions met. Proceeding to LLM.")
        return None
    except Exception as e:
        print(f"Error in before_model_callback: {e}")
        return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('set_routing_variable'):
                result = part.function_response.response.get('result', {})
                if 'error' in result:
                    print("Executing Tool Failure detected, initiating end session.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong. Please call back later.'),
                        Part.from_end_session(reason='Tool Failure')
                    ])
    last_input = callback_context.get_last_user_input()
    if last_input:
        for part in last_input:
            if part.text and 'no user activity detected' in part.text.lower():
                retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                callback_context.variables['no_input_counter'] = retry_count
                if retry_count >= 3:
                    print("Max no-input retries reached, triggering END_SESSION.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We have not heard from you. Ending session.'),
                        Part.from_end_session(reason='Max No-Input')
                    ])
                print("No input detected, prompting user.")
                return LlmResponse.from_parts(
                    parts=[Part.from_text('Hi, are you still there?')]
                )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "wrapup" in text_lower:
                print("Wrapup event detected. Ending session.")
                return LlmResponse.from_parts(parts=[
                    Part.from_end_session(reason="wrapup")
                ])
            if "no user activity detected" in text_lower or "sys.no-input" in text_lower or "sys.no-match" in text_lower:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                print(f"No-input/No-match event detected. Retry count: {retry_count}")
                if retry_count >= 3:
                    print("Error limit reached, initiating transfer to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm having trouble understanding. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                print("Prompting user to repeat.")
                return LlmResponse.from_parts(
                    parts=[Part.from_text("I didn't get that. Can you say it again?")]
                )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    last_user_input = callback_context.get_last_user_input()
    for part in last_user_input:
        if part.text:
            text_lower = part.text.lower()
            if "wrapup" in text_lower:
                print("Wrapup event received, terminating session.")
                return LlmResponse.from_parts(parts=[
                    Part.from_end_session(reason="wrapup event received")
                ])
            
            if "no user activity detected" in text_lower or "sys.no-input" in text_lower or "silence" in text_lower:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                if retry_count >= 3:
                    print("Max no-input retries reached. Transferring to Live Agent.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="Live_Agent_Transfer")
                    ])
                print("No-input detected. Playing localized standard reprompt.")
                return LlmResponse.from_parts(
                    parts=[Part.from_text("I didn't get that. Can you say it again?")]
                )
    
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('set_route_variable') and 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent='escalation_agent')
                ])
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('set_session_route') and 'error' in part.function_response.response.get('result', {}):
            print("Executing Tool Failure detected, initiating transfer.")
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                Part.from_agent_transfer(agent='escalation_agent')
            ])
    
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if 'no user activity detected' in text_lower or 'sys.no-match' in text_lower or 'sys.no-input' in text_lower:
                print("No-input or no-match detected, playing bilingual reprompt.")
                error_counter = callback_context.variables.get('global_error_counter', 0) + 1
                callback_context.variables['global_error_counter'] = error_counter
                
                if error_counter >= 3:
                    print("Max errors reached. Transferring to agent.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We are having trouble understanding. Let me transfer you to an agent.'),
                        Part.from_agent_transfer(agent='escalation_agent')
                    ])
                    
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
                ])
                
    return None