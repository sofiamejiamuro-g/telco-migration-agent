NATIVE_TRANSFER_TARGETS = {"AuthenticationAgent", "RootAgent"}

NATIVE_TRANSFER_TARGETS = {"AuthenticationAgent", "RootAgent"}

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

    def safe_int(val):
        try: return int(val)
        except: return 0

    try:
        user_input = callback_context.get_last_user_input()
        if user_input:
            for part in user_input:
                if part.text and "no user activity detected" in part.text.lower():
                    retry_count = safe_int(callback_context.variables.get("no_input_counter", 0)) + 1
                    callback_context.variables["no_input_counter"] = retry_count
                    if retry_count >= 3:
                        print("Max no-inputs reached, transferring to bell_aqd.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                            Part.from_agent_transfer(agent="RootAgent")
                        ])
                    print("Prompting for no-input retry.")
                    return LlmResponse.from_parts(parts=[Part.from_text("Hi, are you still there?")])
                elif part.text:
                    callback_context.variables["no_input_counter"] = 0
        
        global_errs = safe_int(callback_context.variables.get("global_error_counter", 0))
        semantic_voids = safe_int(callback_context.variables.get("semantic_void", 0))
        if global_errs >= 3 or semantic_voids >= 3:
            print("Global error limit or semantic void limit reached, transferring.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("Seems like you're having some difficulty today. Let's connect you with someone who can help."),
                Part.from_agent_transfer(agent="RootAgent")
            ])
    except Exception as e:
        print(f"Callback error: {e}")
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    ni_count = callback_context.variables.get('no_input_counter', 0)
    nm_count = callback_context.variables.get('no_match_counter', 0)
    pin_invalid = callback_context.variables.get('pin_invalid_counter', 0)
    wrong_pin = callback_context.variables.get('loop_counter', 0)
    
    if ni_count >= 3 or nm_count >= 3:
        print("Executing sys.no-input/no-match trigger, initiating transfer to bell_aqd.")
        callback_context.variables['auth_status'] = 'Fail'
        callback_context.variables['hardstop'] = True
        return LlmResponse.from_parts(parts=[
            Part.from_text("We seem to be having trouble. Let me transfer you to an agent."),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    if pin_invalid >= 2 or wrong_pin >= 2:
        print("Executing PIN error threshold override, initiating transfer to bell_aqd.")
        callback_context.variables['auth_status'] = 'Fail'
        return LlmResponse.from_parts(parts=[
            Part.from_text("Too many invalid PIN attempts. Let me transfer you to an agent for further assistance."),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    if len(llm_request.contents) > 0:
        for part in llm_request.contents[-1].parts:
            for tool_name in ['start_auth_session_wrapper', 'validate_pin_wrapper', 'get_customer_profile_wrapper', 'send_otp_wrapper', 'validate_otp_wrapper']:
                if part.has_function_response(tool_name) and 'error' in part.function_response.response.get('result', {}):
                    print(f"Executing Tool Failure detected for {tool_name}, initiating transfer.")
                    callback_context.variables['auth_status'] = 'Fail'
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, we are experiencing technical difficulties validating your information. Let me transfer you to a representative."),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text.lower():
            print('No input detected.')
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            if retry_count >= 3:
                print('Max no input limit reached, initiating transfer.')
                callback_context.variables['auth_status'] = 'Fail'
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We haven\'t heard from you. Let me transfer you to an agent.'),
                    Part.from_agent_transfer(agent='escalation_agent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text('Hi, are you still there?')])
            
    tool_names = ['initialize_auth_session', 'validate_pin', 'send_otp', 'validate_otp', 'finalize_auth_status']
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            for tool in tool_names:
                if part.has_function_response(tool):
                    res = part.function_response.response.get('result', {})
                    if 'error' in res:
                        print('Executing Tool Failure detected, initiating transfer.')
                        callback_context.variables['auth_status'] = 'Fail'
                        return LlmResponse.from_parts(parts=[
                            Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                            Part.from_agent_transfer(agent='escalation_agent')
                        ])
            
            if part.has_function_response('validate_pin') or part.has_function_response('validate_otp'):
                res = part.function_response.response.get('result', {})
                if res.get('is_authenticated') is False:
                    print('Incorrect authentication provided.')
                    retries = callback_context.variables.get('no_match_counter', 0) + 1
                    callback_context.variables['no_match_counter'] = retries
                    if retries >= 2:
                        print('Max incorrect authentication attempts reached, initiating transfer.')
                        callback_context.variables['auth_status'] = 'Fail'
                        return LlmResponse.from_parts(parts=[
                            Part.from_text('That still doesn\'t seem right. Let me transfer you to an agent.'),
                            Part.from_agent_transfer(agent='escalation_agent')
                        ])
                        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        for part in callback_context.get_last_user_input():
            if part.text and 'no user activity detected' in part.text.lower():
                print('No-input condition met in callback.')
                current_errors = int(callback_context.variables.get('global_error_counter', 0))
                callback_context.variables['global_error_counter'] = current_errors + 1
                
                if (current_errors + 1) >= 3:
                    print('global_error_counter limit reached, transferring to bell_aqd.')
                    callback_context.variables['identification_status'] = 'Fail'
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('I am having trouble receiving your input. Let me transfer you.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                print('Incremented global_error_counter, requesting retry.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Are you still there? I did not hear anything.')
                ])
                
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('validate_and_set_single_ban') and 'error' in part.function_response.response.get('result', {}):
                print('Executing Tool Failure detected, initiating transfer.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
                
        print('No callback overrides required, proceeding to model.')
        return None
    except Exception as e:
        print(f'Error in before_model_callback: {e}')
        return None