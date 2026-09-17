NATIVE_TRANSFER_TARGETS = {"RootAgent"}

NATIVE_TRANSFER_TARGETS = {"RootAgent"}

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
                for t in ["extract_entities", "no_intent", "routing", "check_payment_arrangement_eligibility"]
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
                            if action == "respond":
                                text = directive.get("text", "")
                                parts_to_return.append(
                                    Part.from_text(text=text)
                                )
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
                for t in ["no_intent", "routing", "extract_entities"]
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
                            if action == "respond":
                                text = directive.get("text", "")
                                parts_to_return.append(
                                    Part.from_text(text=text)
                                )
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

    global_error = callback_context.variables.get("global_error_counter", 0)
    try:
        global_error = int(global_error)
    except (ValueError, TypeError):
        global_error = 0
        
    if global_error >= 3:
        print("Executing logic gate: global_error_counter limit reached, initiating transfer to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("Let me transfer you to an agent who can help."),
            Part.from_agent_transfer(agent="RootAgent")
        ])
        
    local_noinput = callback_context.variables.get("no_input_counter", 0)
    try:
        local_noinput = int(local_noinput)
    except (ValueError, TypeError):
        local_noinput = 0
        
    if local_noinput >= 3:
        print("Executing logic gate: local_noinput_counter limit reached, initiating transfer to bell_wrapup.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("We haven't heard from you. Let me transfer you."),
            Part.from_agent_transfer(agent="RootAgent")
        ])
        
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response("initialize_caller_context_wrapper") or part.has_function_response("submit_ivr_transfer_wrapper"):
                resp = part.function_response.response.get("result", {})
                if "error" in resp:
                    print("Executing logic gate: Tool Failure detected, playing standard apology and initiating transfer to bell_wrapup.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I apologize, but we are experiencing technical difficulties. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Wrapup Event Override
    if callback_context.variables.get("routing_val") == "wrapup":
        print("Wrapup event triggered, transitioning to END_SESSION")
        return LlmResponse.from_parts(parts=[
            Part.from_end_session(reason="wrapup")
        ])

    # Custom Response for No-Input / Silence Timeout (Pattern E)
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            print("Executing No-Input logic in before_model_callback")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            
            if retry_count >= 3:
                print("Max no-input threshold reached, strictly routing to bell_No_Input_3")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("You can check out our frequently asked questions at bell.ca/prepaid-support"),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text("Sorry, I didn't quite get that. Can you try again?")]
            )

    # Terminate Session on Tool Failures (Pattern B)
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if (part.has_function_response("set_routing_variables") and
                "error" in part.function_response.response.get("result", {})):
                print("Executing Tool Failure detected, initiating session end.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Please call back later."),
                    Part.from_end_session(reason="Tool Failure")
                ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # 1. Tool Failure handling
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('increment_retry_counter') and
            'error' in part.function_response.response.get('result', {})):
            print('Executing Tool Failure detected, initiating session end.')
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong. Please call back later.'),
                Part.from_end_session(reason='Tool Failure')
            ])

    # 2. Check Max Invalid Attempts
    no_match_counter = callback_context.variables.get('no_match_counter', 0)
    try:
        no_match_counter = int(no_match_counter)
    except (ValueError, TypeError):
        no_match_counter = 0

    if no_match_counter >= 2:
        print('Max invalid attempts reached. Terminating session.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am sorry, but I am still having trouble understanding. Please call us back later. Goodbye.'),
            Part.from_end_session(reason='Max retry limit reached')
        ])

    # 3. Handle Silence (sys.no-input natively)
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text:
            print('Silence detected. Handling natively.')
            no_match_counter += 1
            callback_context.variables['no_match_counter'] = no_match_counter
            
            if no_match_counter >= 2:
                print('Max silence retries reached. Terminating session.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you. Please call us back later. Goodbye.'),
                    Part.from_end_session(reason='Max silence timeouts')
                ])
            
            language = callback_context.variables.get('language', 'English')
            if language.lower() == 'french':
                prompt = 'Je n ai pas compris. Pouvez-vous répéter ?'
            elif language.lower() == 'chinese':
                prompt = '对不起，我没听懂。请再说一遍。'
            else:
                prompt = 'I didn t get that. Can you say it again?'
                
            return LlmResponse.from_parts(
                parts=[Part.from_text(prompt)]
            )
            
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Handle sys.no-input (Silence Timeout)
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            print("Silence detected (no user activity), evaluating no-input retry counter.")
            retry_count = int(callback_context.variables.get("no_input_counter", 0)) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max no-inputs reached (>=3). Terminating session gracefully.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you in a while. Please call back later when you are ready."),
                    Part.from_end_session(reason="Max No-Inputs")
                ])
            print("Reprompting for no-input.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("Sorry, I didn't get that. Can you say it again?")]
            )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback for nga_handling")
    user_inputs = callback_context.get_last_user_input()
    
    if user_inputs:
        user_text = ""
        for part in user_inputs:
            if part.text:
                user_text += part.text.lower()
                
        if "no user activity detected" in user_text or "sys.no-input" in user_text:
            print("No-input detected in before_model_callback")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            
            if retry_count >= 3:
                print("Max no-input retries reached, initiating transfer to POST_STEERING_ROUTING / bell_No_Input_3.")
                callback_context.variables["route"] = "nga_no_input"
                callback_context.variables["handoff_to"] = "post_steering"
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
            print("Playing standard bilingual no-input prompt")
            response = LlmResponse.from_parts(
                parts=[Part.from_text("I didn't get that... / J'ai du mal à comprendre...")]
            )
            response.partial = True
            return response
            
        if "sys.no-match" in user_text or "unrecognized utterance" in user_text:
            print("No-match detected in before_model_callback")
            error_count = callback_context.variables.get("global_error_counter", 0) + 1
            callback_context.variables["global_error_counter"] = error_count
            
            if error_count >= 3:
                print("Max no-match retries reached, initiating transfer to POST_STEERING_ROUTING / bell_No_Match_3.")
                callback_context.variables["route"] = "nga_no_match"
                callback_context.variables["handoff_to"] = "post_steering"
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I am having trouble understanding. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
            print("Playing standard bilingual no-match prompt")
            response = LlmResponse.from_parts(
                parts=[Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")]
            )
            response.partial = True
            return response

    for part in llm_request.contents[-1].parts:
        if part.has_function_response('set_routing_state_variables') and 'error' in part.function_response.response.get('result', {}):
            print("Executing Tool Failure detected, initiating transfer.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("Sorry, something went wrong with the system. Let me transfer you."),
                Part.from_agent_transfer(agent='RootAgent')
            ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        for part in callback_context.get_last_user_input():
            if part.text and ("no user activity detected" in part.text.lower() or "sys.no-match" in part.text.lower() or "sys.no-input" in part.text.lower()):
                print("Executing reprompt logic for no-input/no-match event.")
                counter = callback_context.variables.get("global_error_counter", 0) + 1
                callback_context.variables["global_error_counter"] = counter
                if counter >= 3:
                    print("Max error threshold reached, initiating session termination.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, we are experiencing technical difficulties. Please call back later."),
                        Part.from_end_session(reason="Max Errors")
                    ])
                print("Providing standard reprompt error message.")
                return LlmResponse.from_parts(
                    parts=[Part.from_text("I didn't get that. Can you say it again?")]
                )
    except Exception as e:
        print(f"Error in before_model_callback: {e}")
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('set_fallback_flag') and
            'error' in part.function_response.response.get('result', {})):
            print("Executing Tool Failure detected, initiating transfer to bell_aqd.")
            return LlmResponse.from_parts(parts=[
                Part.from_text(
                    'Sorry, something went wrong. Let me transfer you.'
                ),
                Part.from_agent_transfer(agent='RootAgent')
            ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    last_inputs = callback_context.get_last_user_input()
    if last_inputs:
        for part in last_inputs:
            if part.text:
                text_lower = part.text.lower()
                if "no user activity detected" in text_lower or "sys.no-input" in text_lower or "sys.no-match" in text_lower:
                    print("Executing logic: No-input/no-match condition detected.")
                    current_count = callback_context.variables.get("global_error_counter", 0)
                    try:
                        current_count = int(current_count)
                    except (ValueError, TypeError):
                        current_count = 0
                    new_count = current_count + 1
                    callback_context.variables["global_error_counter"] = new_count
                    print(f"Incremented global_error_counter to {new_count}")
                    if new_count >= 3:
                        print("Executing logic: Error threshold reached, initiating transfer to bell_aqd.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_agent_transfer(agent="RootAgent")
                        ])
                    else:
                        print("Executing logic: Error threshold not reached, playing bilingual reprompt.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
                        ])

    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response("increment_error_counter"):
                if "error" in part.function_response.response.get("result", {}):
                    print("Executing Tool Failure detected, initiating transfer.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, something went wrong. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                result_data = part.function_response.response.get("result", {})
                new_count = result_data.get("global_error_counter", 0)
                try:
                    new_count = int(new_count)
                except (ValueError, TypeError):
                    new_count = 0
                if new_count >= 3:
                    print("Executing logic: Tool response threshold reached, transferring to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing bell_wrapup before_model_callback")
    
    last_input = callback_context.get_last_user_input()
    is_no_input = False
    if last_input:
        for part in last_input:
            if part.text and "no user activity detected" in part.text.lower():
                is_no_input = True
                break
                
    if is_no_input:
        print("No-input detected, playing fallback and ending session")
        return LlmResponse.from_parts([
            Part.from_text("J'ai du mal à comprendre cette question. J'ai mal compris votre demande. Je n'ai pas saisi ce que vous avez dit. Je crois que je ne vous suis pas. Je ne comprends pas de quoi vous me parlez."),
            Part.from_end_session(reason="sys.no-input-default")
        ])
        
    if callback_context.variables.get("first_turn", True):
        print("First turn detected, executing unconditional wrapup")
        callback_context.variables["first_turn"] = False
        return LlmResponse.from_parts([
            Part.from_text("Merci d'avoir appelé. Au revoir!\nThanks for calling. Goodbye!"),
            Part.from_end_session(reason="bell_End the Conversation")
        ])
        
    print("No-match detected, playing fallback and ending session")
    return LlmResponse.from_parts([
        Part.from_text("J'ai du mal à comprendre cette question. J'ai mal compris votre demande. Je n'ai pas saisi ce que vous avez dit. Je crois que je ne vous suis pas. Je ne comprends pas de quoi vous me parlez."),
        Part.from_end_session(reason="sys.no-match-default")
    ])

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Check for no-input or no-match events during the wrap-up phase
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if 'no user activity detected' in text_lower or 'sys.no-input' in text_lower or 'sys.no-match' in text_lower:
                print('No-Input/No-Match detected in termination phase, forcing END_SESSION.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("J'ai du mal à comprendre cette question. Je n'ai pas saisi ce que vous avez dit."),
                    Part.from_end_session(reason='No-Input/No-Match Termination')
                ])
                
    # Terminate Session on Tool Failures (Pattern B)
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if (part.has_function_response('clear_sensitive_billing_data') and
                'error' in part.function_response.response.get('result', {})):
                print('Executing Tool Failure detected, initiating termination.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Désolé, une erreur technique est survenue. Nous devons mettre fin à la conversation."),
                    Part.from_end_session(reason='Tool Failure')
                ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('format_handoff_context') and 'error' in part.function_response.response.get('result', {}):
            print('Executing Tool Failure detected, initiating transfer to End Conversation agent.')
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong while preparing your transfer.'),
                Part.from_agent_transfer(agent='RootAgent')
            ])

    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text:
            print('No-input detected. Checking retry limits.')
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            if retry_count >= 3:
                print('Max no-input retries reached. Routing to bell_End the Conversation.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you in a while. Let me end this conversation.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            print('Prompting user for activity.')
            return LlmResponse.from_parts(parts=[Part.from_text('Hi, are you still there?')])
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Check for Tool Failures (determine_agent_queue, execute_agent_transfer) triggering System Unavailable Apology
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('determine_agent_queue') or part.has_function_response('execute_agent_transfer'):
                if 'error' in part.function_response.response.get('result', {}):
                    print("Executing Tool Failure detected, initiating session end.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, I'm unable to transfer you to an agent due to an unexpected system issue. Please try calling us back later."),
                        Part.from_end_session(reason='Tool Failure')
                    ])

    # Check No-Input and No-Match Retry Limits
    last_inputs = callback_context.get_last_user_input()
    if last_inputs:
        for part in last_inputs:
            if part.text:
                text_lower = part.text.lower()
                if "no user activity detected" in text_lower:
                    retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                    callback_context.variables['no_input_counter'] = retry_count
                    print(f"No Input detected. Count: {retry_count}")
                    if retry_count >= 3:
                        print("Max no-input reached, transferring to bell_No_Input_3 exit route.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_agent_transfer(agent='RootAgent')
                        ])
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I didn't get that. Can you say it again?")
                    ])
                
                if "sys.no-match" in text_lower or "unrecognized" in text_lower:
                    retry_count_nm = callback_context.variables.get('no_match_counter', 0) + 1
                    callback_context.variables['no_match_counter'] = retry_count_nm
                    print(f"No Match detected. Count: {retry_count_nm}")
                    if retry_count_nm >= 3:
                        print("Max no-match reached, transferring to bell_No_Match_3 exit route.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_agent_transfer(agent='RootAgent')
                        ])
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, could you say that again?")
                    ])
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('execute_dam_transfer_wrapper'):
            result = part.function_response.response.get('result', {})
            if 'error' in result:
                print("Executing Tool Failure detected, initiating transfer to bell_wrapup.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, I couldn't transfer you just now. Please try again later."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text.lower():
            print("No user activity detected.")
            no_input_counter = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = no_input_counter
            if no_input_counter >= 3:
                print("Max no-input reached, routing to bell_No_Input_3.")
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[
                Part.from_text("Je n'ai pas saisi ce que vous avez dit. Pouvez-vous répéter? / I didn't catch that, could you repeat?")
            ])

    if callback_context.variables.get('no_match_counter', 0) >= 3:
        print("Max no-match reached, routing to bell_No_Match_3.")
        callback_context.variables['no_match_counter'] = 0
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Handle Tool Failures (Intercepting function_response before the LLM processes it)
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('prepare_and_execute_ivr_handover'):
            response_dict = part.function_response.response.get('result', {})
            if 'error' in response_dict or response_dict.get('webhook_success') is False:
                print('Executing Tool Failure detected, initiating transfer to bell_wrapup.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, I couldn\'t transfer you just now. Please call 1-888-537-9999 for support.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    # Handle No-Input / Silence Timeouts
    user_inputs = callback_context.get_last_user_input()
    if user_inputs:
        for part in user_inputs:
            if part.text and ('no user activity detected' in part.text.lower() or part.text.strip() == ''):
                retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                callback_context.variables['no_input_counter'] = retry_count
                if retry_count >= 3:
                    print('Max no-input retries reached, initiating transfer to bell_aqd.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We haven\'t heard from you. Let me transfer you to an agent.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                print('No-input detected, reprompting user.')
                return LlmResponse.from_parts(parts=[Part.from_text('I didn\'t get that. Can you say it again?')])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # 1. Tool Error Validation and Handoff
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('execute_business_ivr_transfer_wrapper'):
                response_dict = part.function_response.response
                if 'error' in response_dict or 'error' in response_dict.get('result', {}):
                    print("Executing Tool Failure detected, initiating transfer to bell_wrapup.")
                    callback_context.variables['webhook_success'] = False
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, I couldn’t transfer you just now. Please call 1-888-788-2355 for support."),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])

    # 2. No-Input / No-Match Signals and Global Counter Handling
    user_inputs = callback_context.get_last_user_input()
    if user_inputs:
        for part in user_inputs:
            if part.text:
                text_lower = part.text.lower()
                is_no_input = "no user activity detected" in text_lower or "sys.no-input" in text_lower
                is_no_match = "sys.no-match" in text_lower
                
                if is_no_input or is_no_match:
                    global_err = callback_context.variables.get("global_error_counter", 0) + 1
                    callback_context.variables["global_error_counter"] = global_err
                    
                    if is_no_input:
                        retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                        callback_context.variables["no_input_counter"] = retry_count
                        print(f"No-input detected. Count: {retry_count}")
                        
                        if global_err >= 3:
                            print("Global error counter >= 3, routing to bell_aqd.")
                            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])
                        if retry_count >= 3:
                            print("Max no-input retries reached, routing to bell_No_Input_3.")
                            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])
                        return LlmResponse.from_parts(parts=[Part.from_text("J'ai du mal à comprendre cette question. J'ai mal compris votre demande. Je n'ai pas saisi ce que vous avez dit.")])
                    
                    if is_no_match:
                        retry_count = callback_context.variables.get("no_match_counter", 0) + 1
                        callback_context.variables["no_match_counter"] = retry_count
                        print(f"No-match detected. Count: {retry_count}")
                        
                        if global_err >= 3:
                            print("Global error counter >= 3, routing to bell_aqd.")
                            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])
                        if retry_count >= 3:
                            print("Max no-match retries reached, routing to bell_No_Match_3.")
                            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])
                        return LlmResponse.from_parts(parts=[Part.from_text("J'ai du mal à comprendre cette question. J'ai mal compris votre demande. Je n'ai pas saisi ce que vous avez dit.")])
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('execute_ivr_handover_preparation') and
            'error' in part.function_response.response.get('result', {})):
            print('Executing Tool Failure detected, initiating transfer.')
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, I couldn’t transfer you just now. Please connect with us by chat at bell.ca/business_contactus.'),
                Part.from_agent_transfer(agent='RootAgent')
            ])

    user_text = ''
    for part in callback_context.get_last_user_input():
        if part.text:
            user_text = part.text.lower()
            
    if 'no user activity detected' in user_text:
        ni_count = callback_context.variables.get('no_input_counter', 0) + 1
        callback_context.variables['no_input_counter'] = ni_count
        g_err = callback_context.variables.get('global_error_counter', 0) + 1
        callback_context.variables['global_error_counter'] = g_err
        
        print(f'No-input detected. Count: {ni_count}, Global Error: {g_err}')
        
        if g_err >= 3:
            print('Global error limit reached, transferring to bell_aqd.')
            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
            
        if ni_count >= 3:
            print('No-input limit reached, transferring to bell_No_Input_3.')
            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
            
        response = LlmResponse.from_parts([Part.from_text("J'ai du mal à comprendre cette question. J'ai mal compris votre demande.")])
        response.partial = True
        return response
        
    if 'start over' in user_text or 'recommencer' in user_text:
        print('Start over intent detected.')
        callback_context.variables['routing_val'] = 'full start over'
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text.lower():
            no_input_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = no_input_count
            print(f'Executing no_input check. Count: {no_input_count}')
            if no_input_count >= 3:
                print('Max no_input_retry_count reached. Routing to bell_No_Input_3.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            else:
                return LlmResponse.from_parts(parts=[
                    Part.from_text('I did not catch that. Are you still there?')
                ])

    global_error_counter = callback_context.variables.get('global_error_counter', 0)
    if global_error_counter >= 3:
        print('Max global_error_counter reached. Routing to bell_aqd.')
        callback_context.variables['hardstop'] = True
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am having trouble understanding. Let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    local_nomatch_counter = callback_context.variables.get('no_match_counter', 0)
    if local_nomatch_counter >= 3:
        print('Max local_nomatch_counter reached. Routing to bell_No_Match_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am having trouble understanding. Let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('fetch_did_and_initial_customer_profile') or part.has_function_response('search_customer_by_manual_phone'):
                response_dict = part.function_response.response if hasattr(part.function_response, 'response') else {}
                if 'error' in response_dict.get('result', {}):
                    print('Executing Tool Failure detected, initiating transfer.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        part_text = (part.text or "").lower()
        
        if "wrapup" in part_text:
            print("Wrapup event detected. Ending session.")
            return LlmResponse.from_parts(parts=[
                Part.from_end_session(reason="wrapup event triggered")
            ])
            
        if "no user activity detected" in part_text or "sys.no-match" in part_text or "sys.no-input" in part_text:
            error_count = int(callback_context.variables.get("global_error_counter", 0)) + 1
            callback_context.variables["global_error_counter"] = error_count
            print(f"Input Error detected. Counter updated to: {error_count}")
            
            if error_count >= 3:
                print("Max errors reached. Initiating fallback transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, we are having trouble understanding. Let me transfer you for further assistance."),
                    Part.from_agent_transfer(agent="escalation_agent")
                ])
                
            lang = str(callback_context.variables.get("language", "")).lower()
            reprompt = "J'ai du mal à comprendre. Pouvez-vous répéter?" if lang in ["french", "fr", "fr-ca"] else "I didn't get that. Can you say it again?"
            return LlmResponse.from_parts(
                parts=[Part.from_text(reprompt)]
            )
            
    if callback_context.variables.get("first_turn", True):
        callback_context.variables["first_turn"] = False
        language = str(callback_context.variables.get("language", "english")).lower()
        
        if language in ["french", "fr", "fr-ca"]:
            msg = "Veuillez noter qu'à compter du 1er octobre, Bell n'offre plus son services Bell Maison Intelligente ou Sécurité et Domotique Affaires. Pour toute question concernant votre service actuel, veuillez composer le 1-800-267-2001."
        else:
            msg = "Please be advised that effective October 1st, Bell is no longer offering the Bell Smart Home or Bell Business Security services. For any questions on your existing service, please call 1-800-267-2001."
            
        print("First turn detected. Playing deterministic announcement and transferring to feedback.")
        return LlmResponse.from_parts(parts=[
            Part.from_text(msg),
            Part.from_agent_transfer(agent="RootAgent")
        ])
        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # No-input handling logic
    for part in callback_context.get_last_user_input():
        if part.text and ('no user activity detected' in part.text.lower() or 'sys.no-input' in part.text.lower()):
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No-input detected. Retry count: {retry_count}')
            if retry_count > 2:
                print('Max no-input retries reached, triggering END_SESSION.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you. Ending the session.'),
                    Part.from_end_session(reason='Max no-input retries')
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text('I did not get that. Can you say it again?')]
            )

    # Webhook timeout or error handling
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('execute_dam_transfer'):
                result = part.function_response.response.get('result', {})
                if 'error' in result:
                    print('Executing Tool Failure detected, initiating transfer.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                        Part.from_agent_transfer(agent='escalation_agent')
                    ])
                    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if callback_context.variables.get("first_turn", True):
        print("First turn detected. Setting event_type and auto-routing to bell_Steering_Feedback.")
        callback_context.variables["first_turn"] = False
        callback_context.variables["routing_val"] = "anything_else_start_over"
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent="RootAgent")
        ])

    for part in callback_context.get_last_user_input():
        if part.text:
            text = part.text.lower()
            if "no user activity detected" in text or "sys.no-input" in text or "sys.no-match" in text:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                callback_context.variables["routing_val"] = "anything_else_start_over"
                if retry_count >= 3:
                    print("Max retries reached for no-input/no-match. Escalating.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("J'ai du mal à comprendre. Laissez-moi vous transférer à un agent."),
                        Part.from_agent_transfer(agent="escalation_agent")
                    ])
                print("No-input or no-match detected. Playing standard prompt.")
                return LlmResponse.from_parts(
                    parts=[Part.from_text("J'ai du mal à comprendre cette question. J'ai mal compris votre demande. Je n'ai pas saisi ce que vous avez dit. Je crois que je ne vous suis pas. Je ne comprends pas de quoi vous me parlez.")]
                )

    for part in llm_request.contents[-1].parts:
        if part.has_function_response("update_event_type") and "error" in part.function_response.response.get("result", {}):
            print("Executing Tool Failure detected, initiating transfer.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("Désolé, une erreur est survenue. Laissez-moi vous transférer."),
                Part.from_agent_transfer(agent="escalation_agent")
            ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    user_input_parts = callback_context.get_last_user_input()
    user_text = ""
    if user_input_parts:
        user_text = " ".join([part.text for part in user_input_parts if part.text]).lower().strip()

    language = callback_context.variables.get('language', 'english').lower()

    if "wrapup" in user_text:
        print("Wrapup event triggered, transitioning to END_SESSION.")
        return LlmResponse.from_parts(parts=[
            Part.from_end_session(reason='wrapup event')
        ])

    if not user_text or "no user activity detected" in user_text or "sys.no-input" in user_text:
        retry_count = callback_context.variables.get("no_input_counter", 0) + 1
        callback_context.variables["no_input_counter"] = retry_count
        if retry_count >= 3:
            print("No-input counter reaches 3, routing to bell_IVR_Options.")
            msg_en = "<speak>You can check out our frequently asked questions at <say-as interpret-as=\"url\">bell.ca/prepaid-support</say-as></speak>"
            msg_fr = "<speak>Vous pouvez consulter notre foire aux questions sur  <say-as interpret-as=\"url\">bell.ca/soutien-prepaye</say-as></speak>"
            msg = msg_fr if "french" in language or "fr" in language else msg_en
            return LlmResponse.from_parts(parts=[
                Part.from_text(msg),
                Part.from_agent_transfer(agent='RootAgent')
            ])

    if "sys.no-match" in user_text:
        nm_retry = callback_context.variables.get("no_match_counter", 0) + 1
        callback_context.variables["no_match_counter"] = nm_retry
        if nm_retry >= 3:
            print("No-match counter reaches 3, routing to bell_IVR_Options.")
            msg_en = "<speak>I still didn’t get that. You can check out our frequently asked questions at <say-as interpret-as=\"url\">bell.ca/prepaid-support</say-as></speak>"
            msg_fr = "<speak>Excusez-moi, je n'ai toujours pas compris. Vous pouvez consulter notre foire aux questions sur <say-as interpret-as=\"url\">bell.ca/soutien-prepaye</say-as></speak>"
            msg = msg_fr if "french" in language or "fr" in language else msg_en
            return LlmResponse.from_parts(parts=[
                Part.from_text(msg),
                Part.from_agent_transfer(agent='RootAgent')
            ])

    if callback_context.variables.get("first_turn", True):
        print("First turn execution: Delivering survey placeholder and ending session.")
        callback_context.variables["first_turn"] = False
        return LlmResponse.from_parts(parts=[
            Part.from_text("VA Survey placeholder"),
            Part.from_end_session(reason='Survey Delivered')
        ])
        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Check for Tool Failure & Trigger Escalation Pattern A
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if (part.has_function_response('clear_infobot_flag') and
                'error' in part.function_response.response.get('result', {})):
                print("Executing Tool Failure detected, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                    Part.from_agent_transfer(agent='escalation_agent')
                ])

    # Evaluate Event Triggers (No-Input and No-Match)
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "no user activity detected" in text_lower or "sys.no-input-default" in text_lower:
                print("No-input condition detected, validating retry counts.")
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                if retry_count >= 3:
                    print("Max no-input retries reached, transferring to agent.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="escalation_agent")
                    ])
                print("Playing standard multilingual no-input reprompts.")
                return LlmResponse.from_parts(
                    parts=[Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")]
                )
            elif "sys.no-match-default" in text_lower or "unrecognized input" in text_lower:
                print("No-match condition detected, returning standard reprompts.")
                return LlmResponse.from_parts(
                    parts=[Part.from_text("I didn't get that. Can you say it again? / J'ai mal compris votre demande.")]
                )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        # Pattern A: Check for tool failures and route to AQD
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('fetch_intent_sdl_mapping') and 'error' in part.function_response.response.get('result', {}):
                print('Tool Failure detected in fetch_intent_sdl_mapping, initiating transfer.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('I am sorry, something went wrong retrieving that information. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            if part.has_function_response('evaluate_routing_rules') and 'error' in part.function_response.response.get('result', {}):
                print('Tool Failure detected in evaluate_routing_rules, initiating transfer.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('I am sorry, something went wrong validating your account. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
        
        # Pattern E: Check for No Input Timeout
        for part in callback_context.get_last_user_input():
            if part.text and 'no user activity detected' in part.text.lower():
                print('No input detected.')
                local_counter = callback_context.variables.get('no_input_counter', 0) + 1
                global_counter = callback_context.variables.get('global_error_counter', 0) + 1
                callback_context.variables['no_input_counter'] = local_counter
                callback_context.variables['global_error_counter'] = global_counter
                
                if local_counter >= 3:
                    print('Max no-input retries reached, routing to bell_No_Input_3')
                    return LlmResponse.from_parts(parts=[
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                
                print('Prompting user for input retry.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't quite catch that. Are you still there?")
                ])
    except Exception as e:
        print(f'Error in before_model_callback: {e}')
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text.lower():
            print('Executing No Input detected')
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            if retry_count >= 3:
                print('Max retries reached, transferring to bell_aqd.')
                callback_context.variables['special_queue'] = 'bell_aqd'
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We haven\'t heard from you. Let me transfer you to an agent.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text('Hi, are you still there?')])
    
    for part in llm_request.contents[-1].parts:
        tool_names = ['fetch_specialty_customer_details', 'check_deai_eligibility', 'check_payment_arrangement_eligibility']
        for tool in tool_names:
            if part.has_function_response(tool):
                resp = part.function_response.response.get('result', {})
                if 'error' in resp:
                    print(f'Executing Tool Failure detected in {tool}, initiating transfer.')
                    callback_context.variables['special_queue'] = 'bell_aqd'
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong. Let me transfer you to an agent who can help.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text.lower():
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No-input detected. Current retry count: {retry_count}')
            
            if retry_count >= 3:
                print('Max no-input retries reached. Triggering END_SESSION.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We have not heard from you. Exiting test Wrapper now.'),
                    Part.from_end_session(reason='Max No Input Retries')
                ])
            
            print('Prompting user for activity due to silence.')
            return LlmResponse.from_parts(
                parts=[Part.from_text('Are you still there? Please provide your input.')]
            )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            print("No user activity detected, initiating retry verification logic.")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max no_input retries reached. Transferring out to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you in a while. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text("Hi, are you still there? Did you receive the text message?")]
            )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('reset_counters_manipulator') and 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                    Part.from_agent_transfer(agent='escalation_agent')
                ])

    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower().strip()
            
            if text_lower == "wrapup":
                print("Wrapup event detected, transitioning to END_SESSION.")
                return LlmResponse.from_parts(parts=[
                    Part.from_end_session(reason="wrapup event")
                ])
                
            if text_lower in ["sys.no-match-default", "sys.no-input-default", "no user activity detected"]:
                fallback_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = fallback_count
                print(f"Silence or unrecognized input detected. Incremented fallback_counter to {fallback_count}. Playing bilingual error prompt.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Je n'ai pas compris. Pouvez-vous répéter, s'il vous plaît ? I didn't get that. Can you say it again?")
                ])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if callback_context.variables.get("first_turn", True):
        callback_context.variables["first_turn"] = False
        print("First turn detected. Playing placeholder and terminating session.")
        lang = callback_context.variables.get("language", "English").lower()
        msg = "Message d'espace réservé RVI Bell." if lang == "french" else "Bell IVR placeholder message."
        return LlmResponse.from_parts(parts=[
            Part.from_text(msg),
            Part.from_end_session(reason="Placeholder complete")
        ])

    for part in callback_context.get_last_user_input():
        text = (part.text or "").lower()
        
        if "wrapup" in text:
            print("Wrapup event detected. Transitioning to END_SESSION.")
            return LlmResponse.from_parts(parts=[Part.from_end_session(reason="wrapup")])
        
        if "sys.no-input" in text or "no user activity detected" in text:
            print("No input detected in before_model_callback.")
            retry = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry
            lang = callback_context.variables.get("language", "English").lower()
            
            if retry <= 2:
                print("Handling no-input within limits.")
                if retry == 1:
                    msg = "Désolé, je n'ai pas bien compris. Pourriez-vous réessayer?" if lang == "french" else "Sorry, I didn’t quite get that. Can you try again?"
                else:
                    msg = "Êtes-vous toujours là? Pouvez-vous répèter?" if lang == "french" else "Are you still there? Can you repeat please?"
                return LlmResponse.from_parts(parts=[Part.from_text(msg)])
            else:
                print("Max no-input retries reached. Ending session.")
                msg = "J'ai du mal à comprendre cette question." if lang == "french" else "I didn't get that. Can you say it again?"
                return LlmResponse.from_parts(parts=[
                    Part.from_text(msg),
                    Part.from_end_session(reason="Max no-input reached")
                ])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Immediate routing on session start as per routing state machine
    if callback_context.variables.get('first_turn', True):
        callback_context.variables['first_turn'] = False
        print('First turn detected. Routing immediately to bell_vr_pre_checks.')
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='TechSupportAndRepairAgent')
        ])

    # Handle user inputs and explicit events
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            
            # Wrapup routing
            if 'wrapup' in text_lower:
                print('Wrapup event detected. Routing to END_SESSION.')
                return LlmResponse.from_parts(parts=[
                    Part.from_end_session(reason='wrapup event')
                ])
            
            # Global error handling (sys.no-input / sys.no-match / silence)
            if 'no user activity detected' in text_lower or 'sys.no-input' in text_lower or 'sys.no-match' in text_lower:
                print('Global error event detected.')
                error_count = callback_context.variables.get('global_error_counter', 0) + 1
                callback_context.variables['global_error_counter'] = error_count
                
                if error_count >= 3:
                    print('Max consecutive errors reached. Routing to fallback / END_SESSION.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_end_session(reason='Max error attempts reached')
                    ])
                else:
                    print('Playing localized retry prompt.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")
                    ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if not llm_request.contents:
        return None
    
    for part in llm_request.contents[-1].parts:
        # Intercept tool response (both success and error) to transition immediately to PARENT_AGENT as per blueprint
        if part.has_function_response('fetch_sdl_mapping_url'):
            print("Tool fetch_sdl_mapping_url completed (success or error). Initiating transfer to PARENT_AGENT.")
            return LlmResponse.from_parts(parts=[
                Part.from_agent_transfer(agent='PARENT_AGENT')
            ])
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('get_apbs_for_location_wrapper') and 'error' in part.function_response.response.get('result', {}):
            print("Executing Tool Failure detected, terminating session for Webhook Failure.")
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong with the system. Please call back later.'),
                Part.from_end_session(reason='Tool Failure')
            ])

    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Executing No Input 3 detected, routing to bell_No_Input_3 agent.")
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("Executing No Input detected, prompting user again.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("Hi, are you still there?")]
            )
    return None