NATIVE_TRANSFER_TARGETS = {"RootAgent"}

NATIVE_TRANSFER_TARGETS = {"RootAgent"}

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # --- MIGRATION AUTO-GENERATED: LLM TRANSFER --- 
    if (
        llm_response
        and llm_response.content
        and llm_response.content.parts
    ):
        modified = False
        new_parts = []
        for p in llm_response.content.parts:
            if getattr(p, "agent_transfer", None):
                t = getattr(p.agent_transfer, "agent", "")
                if t and t not in NATIVE_TRANSFER_TARGETS:
                    new_parts.append(
                        Part.from_agent_transfer(agent=t)
                    )
                    modified = True
                    continue
            new_parts.append(p)
        if modified:
            return LlmResponse.from_parts(parts=new_parts)

    # --- MIGRATION AUTO-GENERATED: LLM TRANSFER --- 
    if (
        llm_response
        and llm_response.content
        and llm_response.content.parts
    ):
        modified = False
        new_parts = []
        for p in llm_response.content.parts:
            if getattr(p, "agent_transfer", None):
                t = getattr(p.agent_transfer, "agent", "")
                if t and t not in NATIVE_TRANSFER_TARGETS:
                    new_parts.append(
                        Part.from_agent_transfer(agent=t)
                    )
                    modified = True
                    continue
            new_parts.append(p)
        if modified:
            return LlmResponse.from_parts(parts=new_parts)

    # Webhook error interception logic is handled dynamically in before_model_callback via tool responses.
    # No additional generation-time overrides required.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Enforce sys.no-match-3 override based on global error tracking
    error_count = callback_context.variables.get("global_error_counter", 0)
    if error_count >= 3:
        print("Max no-match threshold reached, enforcing route to bell_No_Match_3")
        return LlmResponse.from_parts(parts=[
            Part.from_text("I still didn't get that. You can check out our frequently asked questions at bell.ca/prepaid-support"),
            Part.from_agent_transfer(agent="RootAgent")
        ])

    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No specific after_model modifications required for this agent.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Validate Infinite Routing Loops
    loop_counter = int(callback_context.variables.get("loop_counter", 0))
    if loop_counter >= 2:
        print("Infinite routing loop detected (query_rewriter_looping_counter >= 2), forcing escalation to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent="RootAgent")
        ])
    
    # Validate Consecutive No Matches
    no_match_counter = int(callback_context.variables.get("no_match_counter", 0))
    if no_match_counter >= 3:
        print("Consecutive no-matches reached max limit (>=3), forcing escalation to bell_No_Match_3.")
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent="RootAgent")
        ])
        
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback for nga_handling")
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    try:
        for index, part in enumerate(llm_response.content.parts):
            if part.has_function_call('wrapup') or part.has_function_call('END_SESSION'):
                print("Executing wrapup event transition, forcing END_SESSION.")
                return LlmResponse.from_parts(
                    parts=[
                        Part.from_end_session(reason="Wrapup event triggered")
                    ]
                )
    except Exception as e:
        print(f"Error in after_model_callback: {e}")
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    for part in callback_context.get_last_user_input():
        if part.text:
            text = part.text.lower()
            if "sys.no-input-default" in text or "no user activity detected" in text:
                print("Executing sys.no-input-default detected, transitioning to bell_aqd.")
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
            if "sys.no-match-default" in text:
                print("Executing sys.no-match-default detected, transitioning to bell_aqd.")
                return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='RootAgent')])
            if "wrapup" in text:
                print("Executing wrapup detected, transitioning to END_SESSION.")
                return LlmResponse.from_parts(parts=[Part.from_end_session(reason='wrapup')])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No post-generation logic required for wrap-up phase
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    for index, part in enumerate(llm_response.content.parts):
        if part.has_agent_transfer() and part.agent_transfer.agent == 'TRANSFER_FAILURE':
            print("Transfer failure state intercepted, routing to bell_wrapup.")
            return LlmResponse.from_parts(parts=[
                Part.from_agent_transfer(agent='RootAgent')
            ])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Validation and error routing are preemptively handled in before_model_callback to strictly prevent LLM hallucinations
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No strict post-processing logic specified
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No specialized wrap-up logic required for this sub-agent's state machine
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print('Executing after_model_callback validation wrapper.')
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    tester_fail_count = callback_context.variables.get('loop_counter', 0)
    routing_fail_count = callback_context.variables.get('loop_counter', 0)
    
    if tester_fail_count > 2 or routing_fail_count > 2:
        print('Maximum backend failure threshold reached. Overriding response to trigger END_SESSION.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('Exiting test Wrapper.'),
            Part.from_end_session(reason='Max API Failures Reached')
        ])
        
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    global_error_counter = callback_context.variables.get('global_error_counter', 0)
    fallback_counter = callback_context.variables.get('no_input_counter', 0)
    
    if int(global_error_counter) >= 3:
        print("Global error counter reached threshold. Initiating transfer to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("I seem to be having trouble understanding. Let me transfer you to an agent who can assist you further."),
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    if int(fallback_counter) >= 3:
        print("Fallback SMS counter reached threshold. Initiating transfer to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("It seems we are having trouble sending the SMS. Let me transfer you to an agent."),
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    user_input = ""
    for part in callback_context.get_last_user_input():
        user_input += (part.text or "").lower()
    
    if "sys.no-match" in user_input or "no-match" in user_input or "unrecognized" in user_input:
        print("Unrecognized intent (sys.no-match) detected in after_model_callback.")
        err_count = callback_context.variables.get("global_error_counter", 0) + 1
        callback_context.variables["global_error_counter"] = err_count
        lang = callback_context.variables.get("language", "English").lower()
        
        if err_count <= 2:
            print("Handling no-match within limits.")
            if err_count == 1:
                msg = "Je suis désolé, je n'ai pas bien saisie. Qu'est-ce que vous avez dit?" if lang == "french" else "Sorry, I didn't understand. What was that?"
            else:
                msg = "J'ai du mal à comprendre. Pouvez-vous répéter s'il vous plaît?" if lang == "french" else "I’m having trouble understanding. Can you repeat please?"
            return LlmResponse.from_parts(parts=[Part.from_text(msg)])
        else:
            print("Max error count reached. Ending session.")
            msg = "J'ai du mal à comprendre cette question." if lang == "french" else "I didn't get that. Can you say it again?"
            return LlmResponse.from_parts(parts=[
                Part.from_text(msg),
                Part.from_end_session(reason="Max errors reached")
            ])
            
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No post-generation logic required for routing flow
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    webhook_success = callback_context.variables.get('webhook_success')
    if webhook_success is False:
        print("Executing Webhook failure condition checked via state, triggering END_FLOW.")
        return LlmResponse.from_parts(parts=[
            Part.from_end_session(reason='Webhook Failure')
        ])

    global_error_counter = callback_context.variables.get('global_error_counter', 0)
    if global_error_counter >= 3:
        print("Executing No Match 3 condition detected, routing to bell_No_Match_3.")
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])

    return None