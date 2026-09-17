NATIVE_TRANSFER_TARGETS = {"AccountManagementAgent", "RootAgent"}

NATIVE_TRANSFER_TARGETS = {"AccountManagementAgent", "RootAgent"}

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

    global_errors = callback_context.variables.get('global_error_counter', 0)
    local_nomatch = callback_context.variables.get('no_match_counter', 0)
    
    if global_errors >= 3:
        print('Global error limit reached. Transferring to bell_aqd.')
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    if local_nomatch >= 3:
        print('No-match limit reached. Transferring to bell_No_Match_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text.lower():
            no_input_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = no_input_count
            if no_input_count >= 3:
                print('No-input limit reached. Transferring to bell_No_Input_3.')
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            print('No-input detected. Prompting user.')
            return LlmResponse.from_parts(parts=[
                Part.from_text('Are you still there? / Êtes-vous toujours là?')
            ])
            
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('set_downstream_variables') and 'error' in part.function_response.response.get('result', part.function_response.response):
            print('Executing Tool Failure detected, incrementing global error counter.')
            new_errors = global_errors + 1
            callback_context.variables['global_error_counter'] = new_errors
            if new_errors >= 3:
                print('Executing Tool Failure limit reached, initiating transfer.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print('Executing before_model_callback checks.')
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if 'wrapup' in text_lower:
                print('Wrapup event triggered. Routing to END_SESSION.')
                return LlmResponse.from_parts(parts=[
                    Part.from_end_session(reason='wrapup')
                ])
            if 'no user activity detected' in text_lower or 'sys.no-input' in text_lower or 'sys.no-match' in text_lower:
                retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                callback_context.variables['no_input_counter'] = retry_count
                print(f'Silence/No-match detected. Current retry count: {retry_count}')
                language = callback_context.variables.get('language', 'en').lower()
                if retry_count >= 3:
                    print('Threshold exceeded. Terminating session.')
                    end_msg = 'Au revoir.' if 'fr' in language else 'Goodbye.'
                    return LlmResponse.from_parts(parts=[
                        Part.from_text(end_msg),
                        Part.from_end_session(reason='Max errors')
                    ])
                print('Threshold not met. Sending standard reprompt.')
                reprompt = 'Pouvez-vous repeter?' if 'fr' in language else 'I did not get that. Can you say it again?'
                return LlmResponse.from_parts(parts=[
                    Part.from_text(reprompt)
                ])
    print('No overrides triggered. Proceeding to generative model.')
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Deterministic Greeting / Exit Route: Immediate Under-Development Notification
    if callback_context.variables.get("first_turn", True):
        callback_context.variables["first_turn"] = False
        print("First turn detected. Executing INFORM_UNDER_DEVELOPMENT logic.")
        language = callback_context.variables.get("language", "english")
        msg = "Vous êtes dans le flux PPV qui est actuellement en cours de développement." if language and language.lower() == "french" else "You are in the PPV Flow which is currently under development."
        print("First turn wrap up complete, triggering END_SESSION.")
        return LlmResponse.from_parts(parts=[
            Part.from_text(msg),
            Part.from_end_session(reason="PPV Under Development Informational Wrap-up")
        ])

    # Handle DFCX System Events for No-Input and No-Match
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            
            # Trigger: sys.no-input / silence timeout
            if "no user activity detected" in text_lower or "sys.no-input" in text_lower:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                print(f"sys.no-input event detected. Current no_input_retry_count: {retry_count}")
                
                if retry_count >= 3:
                    print("Max consecutive no-input events reached. Terminating session.")
                    lang = callback_context.variables.get("language", "english")
                    end_msg = "Nous n'avons pas reçu de réponse. Au revoir." if lang and lang.lower() == "french" else "We haven't heard from you. Goodbye."
                    return LlmResponse.from_parts(parts=[
                        Part.from_text(end_msg),
                        Part.from_end_session(reason="Max no-input limit reached")
                    ])
                
                print("Appending explicit fallback instructions for LLM to reprompt user on no-input.")
                llm_request.contents[-1].parts.append(
                    Part.from_text("SYSTEM DIRECTIVE: The user did not provide input. Please explicitly reprompt them to respond.")
                )
                
            # Trigger: Max consecutive sys.no-match-default events reached
            elif "sys.no-match" in text_lower:
                error_count = callback_context.variables.get("global_error_counter", 0) + 1
                callback_context.variables["global_error_counter"] = error_count
                print(f"sys.no-match event detected. Current global_error_counter: {error_count}")
                
                if error_count >= 3:
                    print("Max consecutive sys.no-match events reached. Playing standard failure message and terminating session.")
                    lang = callback_context.variables.get("language", "english")
                    end_msg = "Désolé, j'ai du mal à comprendre votre demande. Au revoir." if lang and lang.lower() == "french" else "Sorry, I am having trouble understanding your request. Goodbye."
                    return LlmResponse.from_parts(parts=[
                        Part.from_text(end_msg),
                        Part.from_end_session(reason="Max no-match limit reached")
                    ])
                
                print("Appending explicit fallback instructions for LLM to reprompt user on no-match.")
                llm_request.contents[-1].parts.append(
                    Part.from_text("SYSTEM DIRECTIVE: The user input was not understood. Please explicitly ask them to rephrase their request.")
                )
                
    return None