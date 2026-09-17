NATIVE_TRANSFER_TARGETS = {"BillingAndPaymentsAgent", "RootAgent"}

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

    # Handle No-Input / No-Match retries across SMS Offers and AQD
    for part in callback_context.get_last_user_input():
        text = part.text.lower() if part.text else ""
        if "no user activity detected" in text or "no match" in text or "unrecognized" in text:
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            print(f"Tracking error/no-input. Count: {retry_count}")
            
            if retry_count >= 3:
                print("Max errors reached. Evaluating routing context...")
                route = callback_context.variables.get("route", "")
                
                # If user was in Pre AQD CX Response (Balance fetched)
                if callback_context.variables.get("webhook_success") and callback_context.variables.get("last_payment_amount"):
                    print("Max retries on Pre AQD, routing to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm having trouble understanding. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                    
                # If user was in Bill Dispute SMS Offer
                if route == "bill_dispute":
                    print("Max retries on Bill Dispute SMS Offer, routing to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm having trouble understanding. Let's get you to an agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                    
                # Default fallback for SMS offers (Vanity Info)
                print("Max retries on SMS offer, routing to Vanity Info / Feedback.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("It seems we're having connection issues. You can check our website for more details."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
    # Pattern A: Deterministic tool failure interception (webhook.error on Fetch Due Date)
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('fetch_due_date_wrapper'):
            response = part.function_response.response.get('result', {})
            if 'error' in response or callback_context.variables.get('webhook_success') is False:
                print("Error in fetch due date detected. Routing to SMS Trigger.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I couldn't fetch your due date right now, but I can send you a link to check it on the MyBell app."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        for part in callback_context.get_last_user_input():
            if part.text and ("no user activity detected" in part.text.lower() or "silence" in part.text.lower()):
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                print(f"No Input detected. Count: {retry_count}")
                if retry_count >= 3:
                    print("Max No Input reached, transferring to bell_No_Input_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
            
            if part.text and ("no-match" in part.text.lower() or "unrecognized" in part.text.lower()):
                nm_count = callback_context.variables.get("no_match_counter", 0) + 1
                callback_context.variables["no_match_counter"] = nm_count
                print(f"No Match detected. Count: {nm_count}")
                if nm_count >= 3:
                    print("Max No Match reached, transferring to bell_No_Match_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm still having trouble understanding. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])

        if llm_request.contents and len(llm_request.contents) > 0:
            for part in llm_request.contents[-1].parts:
                if part.has_function_response("fetch_and_calculate_clp_details"):
                    response = part.function_response.response
                    if "error" in response or callback_context.variables.get("webhook_success") is False:
                        print("Executing Tool Failure detected, initiating transfer to bell_Feedback.")
                        callback_context.variables["webhook_success"] = False
                        lang = str(callback_context.variables.get("language", "en")).lower()
                        if "fr" in lang:
                            msg = "Nous effectuons actuellement une maintenance sur nos systèmes, par conséquent, je ne peux malheureusement pas vous communiquer les détails de votre limite de crédit pour le moment. Veuillez rappeler demain."
                        else:
                            msg = "We are currently performing maintenance on our systems so unfortunately I am unable to proceed with providing your credit limit details at this moment. Please call again tomorrow."
                        return LlmResponse.from_parts(parts=[
                            Part.from_text(msg),
                            Part.from_agent_transfer(agent="RootAgent")
                        ])
    except Exception as e:
        print(f"Error in callback: {e}")
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        text_input = part.text.lower() if part.text else ''
        if 'no user activity detected' in text_input or 'no-match' in text_input or 'no input' in text_input:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print('Executing Logic Gate: No-input/No-match detected.')
            if retry_count >= 3:
                print('Executing Tool Failure detected, initiating transfer to bell_determine_handover.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('I am having trouble understanding. Let me transfer you to an agent.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text('Sorry, I didn\'t quite get that. Can you try again?')])
            
    integrated_tools = ['get_ban_and_customer_profile', 'get_npa_nxx_province', 'get_clp_balance_and_payment']
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            for tool in integrated_tools:
                if part.has_function_response(tool):
                    resp = part.function_response.response
                    if 'error' in resp or 'error' in resp.get('result', {}):
                        print(f'Executing Tool Failure detected for {tool}, initiating OFFER_SMS_FALLBACK state natively.')
                        return LlmResponse.from_parts(parts=[
                            Part.from_text('Sorry, it looks like I\'m having trouble completing the next step. There\'s nothing wrong on your end. I\'ll send a text to the device you\'re calling from so that you can view your account balance in the MyBell app. Is that alright?')
                        ])
                        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # 1. No-input/No-match handling (3 consecutive failures -> bell_determine_handover)
    for part in callback_context.get_last_user_input():
        text_lower = (part.text or "").lower()
        if "no user activity detected" in text_lower or not text_lower.strip():
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            print(f"No-input/No-match detected. Retry count: {retry_count}")
            if retry_count >= 3:
                print("Max retries reached, initiating transfer to bell_determine_handover.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            return LlmResponse.from_parts(parts=[Part.from_text("I didn't quite catch that. Can you please say it again?")])
    
    # Reset retry count on valid input
    callback_context.variables["no_input_counter"] = 0

    # 2. bad_amount > 2 -> Route to bell_Feedback
    bad_amount = callback_context.variables.get("cc_invalid_counter", 0)
    try:
        bad_amount = int(bad_amount)
    except:
        bad_amount = 0
        
    if bad_amount > 2:
        print("bad_amount exceeds 2, initiating transfer to bell_Feedback.")
        callback_context.variables["cc_invalid_counter"] = 0
        return LlmResponse.from_parts(parts=[
            Part.from_text("We can only take payments between $1 and $10,000."),
            Part.from_agent_transfer(agent="RootAgent")
        ])

    # 3. Tool error handling for initialize_payment_details -> API_ERROR_HANDLING state transfer
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('initialize_payment_details'):
            response = part.function_response.response.get('result', {})
            if 'error' in response or not response.get('webhook_success', True):
                print("Executing Tool Failure detected, transitioning to API_ERROR_HANDLING.")
                callback_context.variables["webhook_success"] = False
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, I'm unable to process your payment at this time. I'll send a text to the device you're calling from so that you can make a payment in the MyBell app. Is that alright?")
                ])
    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('set_sms_payload_variables') and 'error' in part.function_response.response.get('result', {}):
                print('Tool failure detected for set_sms_payload_variables, initiating transfer.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            if part.has_function_response('set_event_type_variable') and 'error' in part.function_response.response.get('result', {}):
                print('Tool failure detected for set_event_type_variable, initiating transfer.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong. Let me transfer you.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    user_input_parts = callback_context.get_last_user_input()
    if user_input_parts:
        for part in user_input_parts:
            if part.text:
                text_lower = part.text.lower()
                if 'wrapup' in text_lower:
                    print('Wrapup event detected, routing to END_SESSION.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_agent_transfer(agent='END_SESSION')
                    ])
                if 'no user activity detected' in text_lower or 'sys.no-input' in text_lower or 'sys.no-match' in text_lower:
                    retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                    callback_context.variables['no_input_counter'] = retry_count
                    print(f'No-input/no-match event detected. Retry count is now: {retry_count}')
                    if retry_count >= 3:
                        print('Max consecutive failures reached, transferring to bell_Feedback.')
                        lang = str(callback_context.variables.get('language', 'en')).lower()
                        if lang in ['fr-ca', 'fr', 'french']:
                            msg = 'Si vous souhaitez toujours prendre une entente de paiement, vous pouvez le faire dans MonBell. Veuillez consulter le site bell.ca/soutien pour plus d\'information.'
                        else:
                            msg = 'If you\'d still like to set up Payment Arrangement, you can do so in MyBell. Please visit bell.ca/support for more information.'
                        return LlmResponse.from_parts(parts=[
                            Part.from_text(msg),
                            Part.from_agent_transfer(agent='RootAgent')
                        ])
                    else:
                        print('Prompting user to rephrase due to input failure.')
                        lang = str(callback_context.variables.get('language', 'en')).lower()
                        if lang in ['fr-ca', 'fr', 'french']:
                            reprompt = 'Je suis désolé, je n\'ai toujours pas compris. Pouvez-vous reformuler votre réponse s\'il vous plait ?'
                        else:
                            reprompt = 'I\'m sorry, I still didn\'t catch that. Can you please rephrase your response?'
                        return LlmResponse.from_parts(parts=[
                            Part.from_text(reprompt)
                        ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text:
            sanitized_text = part.text.lower()
            if "no user activity detected" in sanitized_text or "no input" in sanitized_text:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                print(f"No input detected. Count: {retry_count}")
                if retry_count >= 3:
                    print("Max no-input reached. Transferring to bell_No_Input_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                print("Initiating no-input prompt.")
                return LlmResponse.from_parts(parts=[Part.from_text("Hi, are you still there?")])
            
            if "no match" in sanitized_text or "sys.no-match" in sanitized_text:
                nm_count = callback_context.variables.get("no_match_counter", 0) + 1
                callback_context.variables["no_match_counter"] = nm_count
                print(f"No match detected. Count: {nm_count}")
                if nm_count >= 3:
                    print("Max no-match reached. Transferring to bell_No_Match_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I am having trouble understanding. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            print("Silence detected, incrementing retry count.")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max silence retries reached, initiating handover.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you for further assistance."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text("I didn't quite get that. Can you try again?")]
            )

    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            for tool_name in ['get_profile_and_province_wrapper', 'check_delinquency_eligibility_wrapper', 'create_pa_order_wrapper']:
                if part.has_function_response(tool_name):
                    result = part.function_response.response.get('result', {})
                    if 'error' in result:
                        print(f"Executing Tool Failure detected for {tool_name}, transitioning to HANDLE_FAILURES via bell_SMS_Trigger.")
                        return LlmResponse.from_parts(parts=[
                            Part.from_text("I'm unable to proceed with your payment arrangement at this time. I'll send a text to the device you're calling from so that you can set it up in MyBell."),
                            Part.from_agent_transfer(agent='bell_SMS_Trigger')
                        ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback for bell_payment_autopay_cancel")
    
    # 1. No Input / No Match Retry Logic
    last_inputs = callback_context.get_last_user_input()
    if last_inputs:
        for part in last_inputs:
            text = part.text.lower() if part.text else ""
            if "no user activity detected" in text or "no_match" in text or "unrecognized" in text:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                print(f"Failed input detected, retry count: {retry_count}")
                if retry_count >= 3:
                    print("Max retries reached. Transferring to bell_Feedback.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("If you'd still like to cancel Pre-Authorized payment, you can do so in MyBell. Please visit bell.ca/support for more information."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                return LlmResponse.from_parts(parts=[Part.from_text("I didn't quite get that. Can you try again?")])
            elif text:
                callback_context.variables["no_input_counter"] = 0

    # 2. Tool Execution Timeout / Exception Logic
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('evaluate_autopay_cancellation_profile_tool') or part.has_function_response('set_sms_content_tool'):
                func_resp = part.function_response.response
                if 'error' in func_resp or 'error' in func_resp.get('result', {}):
                    print("Tool error detected. Forcing transition to STATE_OFFER_SMS_OUTAGE.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Due to a system failure, you MUST immediately transition to 'STATE_OFFER_SMS_OUTAGE'. Inform the user that we are performing maintenance and cannot cancel the payment directly, but can send a self-serve text message to the device they are calling from. Follow the Yes/No/Different Number logic.")
                    ])
                    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('fetch_customer_ban_profile') or part.has_function_response('evaluate_province_routing') or part.has_function_response('check_preauth_payment_status') or part.has_function_response('get_intent_sdl_mapping'):
            response_data = part.function_response.response.get('result', {})
            if 'error' in response_data or response_data.get('errorCode') == '0':
                print('Executing Tool Failure detected, initiating SMS fallback.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, it looks like I'm having trouble completing the next step. There's nothing wrong on your end. I'll send a text to the device you're calling from so that you can check your Pre-Authorized payments status in the MyBell app. Is that alright?")
                ])

    for part in callback_context.get_last_user_input():
        text = part.text.lower() if part.text else ''
        if 'no user activity detected' in text or 'sys.no-match' in text:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            if retry_count >= 3:
                print('Max no-input/no-match limit reached, transitioning to bell_Feedback.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("If you'd still like to check your Pre-Authorized payments status, you can do so in MyBell. Please visit bell.ca/support for more information"),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            print('Incrementing no-input/no-match retry count.')
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Enforce deterministic routing for 'no input' or 'no match' timeouts (Maximum 3 retries)
    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "no user activity detected" in text_lower or "unrecognized input" in text_lower:
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                
                if retry_count >= 3:
                    print("Max retries reached for No Input/No Match (3), routing to bell_Feedback.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("If you'd still like to update Pre-Authorized payments, you can do so in MyBell. Please visit bell.ca/support."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                print(f"Executing No Input/No Match retry. Current count: {retry_count}")
                return LlmResponse.from_parts(
                    parts=[Part.from_text("I didn't quite get that. Can you try again?")]
                )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Check for no-input/no-match conversational limits
    for part in callback_context.get_last_user_input():
        text_lower = part.text.lower() if part.text else ''
        if 'no user activity detected' in text_lower or 'sys.no-match' in text_lower or 'sys.no-input' in text_lower:
            print('No-input or no-match limit reached.')
            err_count = callback_context.variables.get('global_error_counter', 0) + 1
            callback_context.variables['global_error_counter'] = err_count
            if err_count >= 3:
                print('Error threshold exceeded, routing to bell_determine_handover.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We seem to be having trouble. Let me transfer you to an agent.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text('I did not quite catch that. Could you repeat it?')])

    # Terminate Session on Tool/Webhook Failures
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('nm1_profile_fetcher') or part.has_function_response('npa_nxx_lookup_wrapper'):
                func_resp = part.function_response.response.get('result', {})
                if 'error' in func_resp or func_resp.get('status') == 'Fail':
                    print('Webhook failure detected, ending session.')
                    callback_context.variables['billing_status'] = 'Fail'
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We are currently experiencing technical difficulties. Please try again later.'),
                        Part.from_end_session(reason='Webhook Failure')
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            print("Silence detected, executing timeout logic.")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max no-input retries reached, transferring agent.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Since I didn't get a response from you, I won't be able to proceed with your payment. Let me transfer you."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("Prompting user again due to silence.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("I didn't quite get that. Can you try again?")]
            )

    for part in llm_request.contents[-1].parts:
        if part.has_function_response('submit_cc_payment_details'):
            response_data = part.function_response.response.get('result', {})
            if 'error' in response_data:
                print("Executing Tool Failure detected, initiating SMS alternative.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Unfortunately there was a system error and I cannot process the payment right now. Would you like an SMS with a link to complete the payment via the MyBell App?")
                ])
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback for bell_payment_clp_payment_amount")
    
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('create_payment_order_wrapper') and 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong with our payment system. Let me transfer you."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    last_input = ""
    for part in callback_context.get_last_user_input():
        if part.text:
            last_input += part.text.lower()
            
    if "no user activity detected" in last_input or "sys.no-input" in last_input or "sys.no-match" in last_input:
        retry_count = callback_context.variables.get("no_input_counter", 0) + 1
        callback_context.variables["no_input_counter"] = retry_count
        print(f"Tracking no-input/no-match event. Count: {retry_count}")
        
        if retry_count >= 3:
            print("Max retries reached. Triggering transfer.")
            if callback_context.variables.get("clp_balance") is not None:
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            else:
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent="RootAgent")
                ])
    else:
        if callback_context.variables.get("no_input_counter", 0) > 0:
            callback_context.variables["no_input_counter"] = 0

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            for tool_name in ['process_cc_payment_wrapper', 'get_updated_ban_profile_wrapper', 'evaluate_clp_limits_tool']:
                if part.has_function_response(tool_name) and 'error' in part.function_response.response.get('result', {}):
                    print(f'Executing Tool Failure detected in {tool_name}, initiating transfer.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong. Let me transfer you to provide feedback.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])

    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text:
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No input detected. Retry count: {retry_count}')
            if retry_count >= 3:
                print('Max retries reached. Initiating transfer.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('We haven\'t heard from you. Let me transfer you to an agent.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text('I didn\'t quite get that. Can you try again?')]
            )
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('process_dts_token_wrapper'):
            result = part.function_response.response.get('result', {})
            if 'error' in result or result.get('webhook_success') is False:
                print('Webhook failure detected, initiating Webhook_Failure_DTS prompt.')
                lang = str(callback_context.variables.get('language', 'en')).lower()
                if 'fr' in lang:
                    text = 'Merci de votre patience. Il semble que j\'aie de la difficulté à effectuer la prochaine étape en ce moment. Il n\'y a rien de mal de votre côté. Je vais envoyer un texto à l\'appareil à partir duquel vous appelez, afin que vous puissiez effectuer votre paiement vous-même dans l\'Appli Mon Compte. Est-ce que cela vous convient?'
                else:
                    text = 'Thanks for your patience. It looks like I\'m having trouble completing the next step right now. There\'s nothing wrong on your end. I\'ll send a text to the device you\'re calling from, so that you can proceed with your payment yourself in the My Account App. Is that alright?'
                return LlmResponse.from_parts(parts=[Part.from_text(text)])

    user_inputs = callback_context.get_last_user_input()
    for part in user_inputs:
        if part.text and ('no user activity detected' in part.text.lower() or 'no match' in part.text.lower()):
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'No-input/No-match retry count: {retry_count}')
            if retry_count >= 3:
                print('Max attempts reached. Transitioning to bell_aqd.')
                lang = str(callback_context.variables.get('language', 'en')).lower()
                if 'fr' in lang:
                    msg = 'Si vous souhaitez toujours effectuer une demande de paiements pré-autorisés, vous pouvez le faire dans l’appli Mon compte. Veuillez visiter https://vpc.ca/soutien pour en savoir plus.'
                else:
                    msg = 'If you\'d still like to complete your Pre-Authorized payment request, you can do so in the My Account app. Please visit  vpc.ca/support for more information.'
                return LlmResponse.from_parts(parts=[
                    Part.from_text(msg),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            lang = str(callback_context.variables.get('language', 'en')).lower()
            retry_text = 'Je n’ai pas tout à fait compris. Pouvez-vous réessayer?' if 'fr' in lang else 'I didn\'t quite get that. Can you try again?'
            if retry_count == 2:
                retry_text = 'Je n’ai toujours pas compris.' if 'fr' in lang else 'I still didn\'t get that.'
            return LlmResponse.from_parts(parts=[Part.from_text(retry_text)])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('get_account_balance_details'):
                result = part.function_response.response.get('result', {})
                if 'error' in result or result.get('webhook_success') is False:
                    print('Executing Tool Failure detected, initiating transfer to bell_aqd.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Sorry, something went wrong retrieving your details. Let me transfer you.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                    
    last_input = callback_context.get_last_user_input()
    if last_input:
        for part in last_input:
            text_lower = part.text.lower() if part.text else ''
            if 'no user activity detected' in text_lower or 'sys.no-match' in text_lower:
                retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                callback_context.variables['no_input_counter'] = retry_count
                print(f'No-input or no-match logic gate executed. Current retry count: {retry_count}')
                if retry_count >= 3:
                    print('Max retry threshold reached. Transferring to bell_aqd.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We haven\'t heard from you or couldn\'t understand. Let me transfer you to an agent.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                print('Sending retry prompt for no-input/no-match.')
                return LlmResponse.from_parts(
                    parts=[Part.from_text('I didn\'t get that. Can you say it again?')]
                )
                
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Tool Failures routing based on Blueprint triggers
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('initialize_payment_notification_wrapper') or part.has_function_response('submit_payment_notification_wrapper'):
            if 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating transition to UNVERIFIED_ACCOUNT_SMS_OFFER.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong with our system. Let me check other options.'),
                    Part.from_agent_transfer(agent='UNVERIFIED_ACCOUNT_SMS_OFFER')
                ])

    # No-Input/No-Match Timeout Routing
    for part in callback_context.get_last_user_input():
        text_val = part.text.lower() if part.text else ""
        if "no user activity detected" in text_val or "no match" in text_val or not text_val.strip():
            print("No input or no match detected.")
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max retries reached, transferring to bell_determine_handover.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't been able to understand you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text("I didn't quite get that. Can you try again?")]
            )
        
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('check_customer_payment_eligibility_wrapper') and 'error' in part.function_response.response.get('result', {}):
            print("Executing Tool Failure detected for eligibility, transitioning to WEBHOOK_FAILURE_FALLBACK.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("Sorry, I'm unable to process your credit card payment at this time. I can send a text to the device you're calling from so that you can make a payment in the MyBell app. Is that alright?")
            ])
        if part.has_function_response('create_payment_order_wrapper') and 'error' in part.function_response.response.get('result', {}):
            print("Executing Tool Failure detected for order creation, transitioning to WEBHOOK_FAILURE_FALLBACK.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("Sorry, I'm unable to process your credit card payment at this time. I can send a text to the device you're calling from so that you can make a payment in the MyBell app. Is that alright?")
            ])

    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            if retry_count >= 3:
                print("Max no-input retries reached. Initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("No user input detected, prompting user.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("Hi, I didn't quite catch that. Are you still there?")]
            )
        
        if part.text and "no match" in part.text.lower():
            nm_retry = callback_context.variables.get("no_match_counter", 0) + 1
            callback_context.variables["no_match_counter"] = nm_retry
            if nm_retry >= 3:
                print("Max no-match retries reached. Initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I'm having trouble understanding. Let me transfer you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("No match detected, reprompting user.")
            return LlmResponse.from_parts(
                parts=[Part.from_text("I didn't quite understand that. Could you please rephrase?")]
            )

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('fetch_clp_details'):
                response_dict = part.function_response.response
                if 'error' in response_dict or 'error' in response_dict.get('result', {}):
                    print('Executing Tool Failure detected, initiating transfer to bell_Feedback.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('I am sorry, I cannot help you with confirming your Credit Limit Balance or account details at this time.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                    
    is_no_input = False
    is_no_match = False
    for part in callback_context.get_last_user_input():
        text = part.text.lower() if part.text else ''
        if 'no user activity detected' in text or 'sys.no-input' in text:
            is_no_input = True
        if 'sys.no-match' in text:
            is_no_match = True

    if is_no_input:
        ni_count = callback_context.variables.get('no_input_counter', 0) + 1
        callback_context.variables['no_input_counter'] = ni_count
        print(f'No-Input detected. Count: {ni_count}')
        if ni_count >= 3:
            webhook_success = callback_context.variables.get('webhook_success')
            if not webhook_success:
                print('Max No-Input on Start Page, transferring to bell_No_Input_3.')
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            else:
                print('Max No-Input on main prompt, transferring to bell_Feedback.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('You can pay down your credit limit balance on bell.ca, or call again to learn about credit limit details.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    if is_no_match:
        nm_count = callback_context.variables.get('no_match_counter', 0) + 1
        callback_context.variables['no_match_counter'] = nm_count
        print(f'No-Match detected. Count: {nm_count}')
        if nm_count >= 3:
            webhook_success = callback_context.variables.get('webhook_success')
            if not webhook_success:
                print('Max No-Match on Start Page, transferring to bell_No_Match_3.')
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            else:
                print('Max No-Match on main prompt, transferring to bell_Feedback.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('You can pay down your credit limit balance on bell.ca, or call again to learn about credit limit details.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    special_status = callback_context.variables.get("special_status", "")
    is_special = special_status in ["bell_finals", "bell_col_aul", "bell_col_sus"]
    
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            print(f"No input detected. Retry count: {retry_count}")
            
            if retry_count >= 3:
                if is_special:
                    print("Max no-input threshold reached on specialty flow. Transferring to bell_specialty_flow.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Okay."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                else:
                    print("Max no-input threshold reached. Transferring to bell_No_Input_3.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                    
            return LlmResponse.from_parts(
                parts=[Part.from_text("I didn't get that. Can you say it again?")]
            )
            
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    user_input = ''
    for part in callback_context.get_last_user_input():
        if part.text:
            user_input = part.text.lower().strip()

    if 'no user activity detected' in user_input:
        retry_count = callback_context.variables.get('no_input_counter', 0) + 1
        callback_context.variables['no_input_counter'] = retry_count
        print(f'Executing logic gate: No input detected. Retry count: {retry_count}')
        if retry_count >= 3:
            print('Executing logic gate: Max no-input retries reached, routing to bell_determine_handover')
            return LlmResponse.from_parts(parts=[
                Part.from_agent_transfer(agent='RootAgent')
            ])
        return LlmResponse.from_parts(
            parts=[Part.from_text("I didn't quite get that. Can you try again?")]
        )

    repeat_phrases = ['repeat', 'say that again', 'what was that', 'pardon']
    if any(phrase in user_input for phrase in repeat_phrases):
        print('Executing logic gate: Repeat intent detected, routing to bell_va_to_ivr_handoff')
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])

    startover_phrases = ['start over', 'restart', 'start again']
    if any(phrase in user_input for phrase in startover_phrases):
        print('Executing logic gate: Startover intent detected, routing to Default Start Flow')
        callback_context.variables['routing_val'] = 'full start over'
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # No-Input / No-Match Handling
    for part in callback_context.get_last_user_input():
        if part.text and ('no user activity detected' in part.text.lower() or 'no-match' in part.text.lower()):
            retry_count = callback_context.variables.get('no_input_counter', 0) + 1
            callback_context.variables['no_input_counter'] = retry_count
            print(f'Executing No-Input/No-Match detection. Retry count: {retry_count}')
            
            if retry_count >= 3:
                print('Max retries reached, transferring to bell_Feedback.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text('If you\'d still like to complete your Pre-Authorized payment request, you can do so in MyBell. Please visit bell.ca/support for more information.'),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text('I didn\'t quite get that. Can you try again?')]
            )
            
    # API Timeout / Webhook Failure Override (Pattern A Adaptation)
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('submit_pre_auth_order_wrapper') or part.has_function_response('get_clp_details_wrapper'):
                resp = part.function_response.response.get('result', {})
                if 'error' in resp or resp.get('webhook_success') is False:
                    print('Executing Tool Failure detected, initiating SMS fallback prompt transition.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('I\'m unable to set up your pre-authorized payment at this time. I\'ll send a text to the device you\'re calling from so that you can set it up in MyBell. Is that alright?')
                    ])
                    
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    try:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response('process_one_time_payment') or part.has_function_response('fetch_updated_profile'):
                response_data = part.function_response.response.get('result', {})
                if 'error' in response_data or response_data.get('status') in ['system_timeout', 'system_unavailable']:
                    print('Executing Tool Failure detected, initiating HANDLE_WEBHOOK_FAILURE flow via text intervention.')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('Thanks for your patience. It looks like I am having trouble with the system right now. I can send a text to the device you are calling from, so that you can view your account details yourself in the MyBell App. Is that alright?')
                    ])
        for part in callback_context.get_last_user_input():
            if part.text and 'no user activity detected' in part.text.lower():
                retry_count = callback_context.variables.get('no_input_counter', 0) + 1
                callback_context.variables['no_input_counter'] = retry_count
                if retry_count >= 3:
                    print('Max no-input retries reached, transitioning to bell_determine_handover')
                    return LlmResponse.from_parts(parts=[
                        Part.from_text('We haven\'t heard from you. Let me transfer you to an agent.'),
                        Part.from_agent_transfer(agent='RootAgent')
                    ])
                print('No-input retry logic executed')
                return LlmResponse.from_parts(
                    parts=[Part.from_text('I didn\'t quite catch that. Are you still there?')]
                )
    except Exception as e:
        print(f'Error in before_model_callback: {e}')
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print("Executing before_model_callback logic")
    
    if callback_context.variables.get("first_turn", True):
        print("Executing First turn deterministic routing based on consolidated_status")
        callback_context.variables["first_turn"] = False
        status = str(callback_context.variables.get("billing_status", "")).strip().lower()
        
        if status == "fail":
            print("Executing transfer to bell_aqd due to fail status")
            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])
        elif status == "outage":
            print("Executing transfer to bell_Feedback due to outage status")
            return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="RootAgent")])
        else:
            print("Executing prompt for Pass status to COLLECT_REFUND_REASON")
            lang = str(callback_context.variables.get("language", "en")).strip().lower()
            msg = "Quelle est la raison de votre demande ?" if "fr" in lang else "What is the reason for your request?"
            response = LlmResponse.from_parts(parts=[Part.from_text(msg)])
            response.partial = True
            return response
            
    for part in llm_request.contents[-1].parts:
        if part.has_function_response("set_refund_agent_state"):
            resp = part.function_response.response.get("result", {})
            if "error" in resp:
                print("Executing Tool Failure detected, initiating transfer.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Sorry, something went wrong. Let me transfer you."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text:
            print("Executing No-Input timeout logic")
            error_count = callback_context.variables.get("global_error_counter", 0) + 1
            callback_context.variables["global_error_counter"] = error_count
            
            if error_count >= 3:
                print("Executing Max consecutive errors reached, transferring to bell_Feedback.")
                callback_context.variables["global_error_counter"] = 0
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you in a while. Let me transfer you."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
                
            print("Executing retry prompt for No-Input")
            lang = str(callback_context.variables.get("language", "en")).strip().lower()
            retry_msg = "Désolé, je n'ai pas compris, pouvez-vous reformuler votre réponse s'il vous plaît ?" if "fr" in lang else "Sorry, I didn't catch that, can you please rephrase your response?"
            return LlmResponse.from_parts(parts=[Part.from_text(retry_msg)])
            
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    tool_names = ['evaluate_account_routing_profile', 'check_pacc_eligibility', 'create_preauth_order', 'get_intent_vanity_url']
    for part in llm_request.contents[-1].parts:
        for tool_name in tool_names:
            if (part.has_function_response(tool_name) and 'error' in part.function_response.response.get('result', {})):
                print(f'Webhook failure detected in {tool_name}, forcing FAILURE_HUB transition.')
                callback_context.variables['webhook_success'] = False
                return LlmResponse.from_parts(parts=[
                    Part.from_text('Sorry, something went wrong with our system. Let me check for alternative options.'),
                    Part.from_agent_transfer(agent='FAILURE_HUB')
                ])

    for part in callback_context.get_last_user_input():
        if part.text and ('no user activity detected' in part.text.lower() or 'no-match' in part.text.lower()):
            retry_count = callback_context.variables.get('global_error_counter', 0) + 1
            callback_context.variables['global_error_counter'] = retry_count
            print(f'Error/No-input detected, retry count: {retry_count}')
            if retry_count >= 3:
                print('Max retries reached, initiating transfer to bell_Feedback.')
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Okay. If you'd still like to set up Pre-Authorized payment, you can do so in MyBell. Please visit bell.ca/support for more information."),
                    Part.from_agent_transfer(agent='RootAgent')
                ])
            return LlmResponse.from_parts(parts=[Part.from_text('I did not quite get that. Can you try again?')])
            
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if part.has_function_response('get_account_profile_wrapper') or part.has_function_response('get_province_from_number_wrapper'):
            if 'error' in part.function_response.response.get('result', {}):
                print("Executing Tool Failure detected, initiating bypass to PAD_SMS_OFFER.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("Would you like me to send you a text message with a link to set up pre-authorized payments?")
                ])

    for part in callback_context.get_last_user_input():
        if part.text:
            text_lower = part.text.lower()
            if "no user activity detected" in text_lower or "sys.no-match" in text_lower:
                print("No input or no match detected.")
                retry_count = callback_context.variables.get("no_input_counter", 0) + 1
                callback_context.variables["no_input_counter"] = retry_count
                if retry_count >= 3:
                    print("Max retries reached, transferring to bell_Feedback.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Okay. If you'd still like to set up Pre-Authorized debit, you can do so in MyBell. Please visit bell.ca/support for more information."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
                print("Prompting retry.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I didn't quite get that. Can you try again?")
                ])

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            retry_count = callback_context.variables.get("no_input_counter", 0) + 1
            callback_context.variables["no_input_counter"] = retry_count
            print(f"No input detected. Retry count incremented to: {retry_count}")
            if retry_count >= 3:
                print("Max no-input retries reached, executing transfer to bell_No_Input_3.")
                return LlmResponse.from_parts(parts=[
                    Part.from_agent_transfer(agent="RootAgent")
                ])
            print("Prompting user for input again.")
            return LlmResponse.from_parts(parts=[Part.from_text("I didn't get that. Can you say it again?")])
    
    if llm_request.contents:
        for part in llm_request.contents[-1].parts:
            if part.has_function_response("evaluate_account_and_province_eligibility") or part.has_function_response("get_payment_arrangement_eligibility"):
                resp = part.function_response.response.get("result", {})
                if "error" in resp or resp.get("api_success") is False:
                    print("Executing Tool Failure detected, playing NM1 outage message and initiating transfer to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("We are currently performing maintenance on our systems so unfortunately I am unable to proceed with your request at this time. I'll send a text to the device you're calling from, so that you can view your account balance in the MyBell App. Is that alright?"),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    for part in llm_request.contents[-1].parts:
        if (part.has_function_response('set_routing_variables') and
            'error' in part.function_response.response.get('result', {})):
            print("Executing Tool Failure detected, initiating transfer.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("Sorry, something went wrong. Let me transfer you."),
                Part.from_agent_transfer(agent='escalation_agent')
            ])

    for part in callback_context.get_last_user_input():
        if part.text and "no user activity detected" in part.text.lower():
            print("No user input detected. Executing no-input reprompt.")
            error_count = callback_context.variables.get("global_error_counter", 0) + 1
            callback_context.variables["global_error_counter"] = error_count
            if error_count >= 3:
                print("Max no-input errors reached. Transferring to agent.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("We haven't heard from you. Let me transfer you to an agent. / Nous n'avons pas eu de vos nouvelles. Permettez-moi de vous transférer à un agent."),
                    Part.from_agent_transfer(agent="escalation_agent")
                ])
            return LlmResponse.from_parts(
                parts=[Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question.")]
            )

    return None

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    no_input_counter = callback_context.variables.get('no_input_counter', 0)
    no_match_counter = callback_context.variables.get('no_match_counter', 0)
    global_err_counter = callback_context.variables.get('global_error_counter', 0)

    for part in callback_context.get_last_user_input():
        if part.text and 'no user activity detected' in part.text:
            no_input_counter += 1
            callback_context.variables['no_input_counter'] = no_input_counter
            global_err_counter += 1
            callback_context.variables['global_error_counter'] = global_err_counter
            
            if global_err_counter >= 3:
                print("Global error counter reached 3, routing to bell_aqd")
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
            if no_input_counter >= 3:
                print("No input counter reached 3, routing to bell_No_Input_3")
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
                
            return LlmResponse.from_parts(parts=[Part.from_text("I didn't quite catch that. Are you still there?")])
            
    if global_err_counter >= 3:
        print("Global error counter reached 3, routing to bell_aqd")
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
        
    if no_match_counter >= 3:
        print("No match counter reached 3, routing to bell_No_Match_3")
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
        
    return None