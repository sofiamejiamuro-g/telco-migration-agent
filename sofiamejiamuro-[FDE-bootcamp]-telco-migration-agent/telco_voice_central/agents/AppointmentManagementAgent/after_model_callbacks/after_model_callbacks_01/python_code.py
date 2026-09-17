NATIVE_TRANSFER_TARGETS = {"AppointmentManagementAgent", "RootAgent"}

NATIVE_TRANSFER_TARGETS = {"AppointmentManagementAgent", "RootAgent"}

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

    # No specific post-response overrides required by blueprint
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    variables = callback_context.variables

    webhook_success = variables.get('webhook_success')
    if webhook_success is False:
        print('Executing Tool Failure detected (webhook_success == False), initiating transfer to bell_aqd.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('Sorry, something went wrong retrieving your address. Let me transfer you to an agent.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    global_error_counter = variables.get('global_error_counter', 0)
    if isinstance(global_error_counter, (int, float)) and global_error_counter >= 3:
        print('Global error limit reached, initiating transfer to bell_aqd.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('Sorry, I am having trouble understanding. Let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    local_nomatch_counter = variables.get('no_match_counter', 0)
    if isinstance(local_nomatch_counter, (int, float)) and local_nomatch_counter >= 3:
        print('Local no match limit reached, initiating transfer to bell_No_Match_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am still having trouble understanding. Let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    local_noinput_counter = variables.get('no_input_counter', 0)
    if isinstance(local_noinput_counter, (int, float)) and local_noinput_counter >= 3:
        print('Local no input limit reached, initiating transfer to bell_No_Input_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('Since I have not heard from you, let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])

    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    if callback_context.variables.get("webhook_success") is False:
        print("Webhook failure flag detected during after_model_callback, routing to acut error handling.")
        callback_context.variables["error_code"] = "acut"
        callback_context.variables["webhook_success"] = None
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent="AppointmentManagementAgent")])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No specific after model overrides needed for this agent state.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    phone_invalid_counter = callback_context.variables.get('phone_invalid_counter', 0)
    if phone_invalid_counter > 2:
        print("phone_invalid_counter > 2, transferring to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("Let me transfer you for further assistance."),
            Part.from_agent_transfer(agent='RootAgent')
        ])
    
    refusal_counter = callback_context.variables.get('loop_counter', 0)
    if refusal_counter > 2:
        print("refusal_counter > 2, transferring to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("Let me transfer you for further assistance."),
            Part.from_agent_transfer(agent='RootAgent')
        ])
    
    is_home_phone = callback_context.variables.get('is_home_phone', False)
    if is_home_phone == True:
        print("is_home_phone is true, transferring to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("It looks like this is a home phone. Let me transfer you."),
            Part.from_agent_transfer(agent='RootAgent')
        ])
    
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print('Executing after_model_callback checks')
    
    no_input_count = callback_context.variables.get('no_input_counter', 0)
    if no_input_count >= 3:
        print('Executing Max no input reached, transferring to bell_No_Input_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('We have not heard from you. Let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    no_match_count = callback_context.variables.get('no_match_counter', 0)
    if no_match_count >= 3:
        print('Executing Max no match reached, transferring to bell_No_Match_3.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('I am having trouble understanding. Let me transfer you.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])
        
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Logic checks implemented in before_model_callback
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    webhook_success = callback_context.variables.get('webhook_success')
    if webhook_success is False or str(webhook_success).lower() == 'false':
        print('Webhook success is false. Overriding to route to webhook failure agent.')
        callback_context.variables['error_code'] = 'acut'
        return LlmResponse.from_parts(parts=[Part.from_agent_transfer(agent='AppointmentManagementAgent')])
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
    print("Executing after_model_callback checks")
    
    global_error = callback_context.variables.get("global_error_counter", 0)
    local_nomatch = callback_context.variables.get("no_match_counter", 0)
    
    if global_error >= 3:
        print("Global error limit reached in after_model_callback. Routing to bell_aqd.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("We seem to be having trouble. Let me transfer you."),
            Part.from_agent_transfer(agent="RootAgent")
        ])
    elif local_nomatch >= 3:
        print("Local no-match limit reached in after_model_callback. Routing to bell_No_Match_3.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("I didn't quite get that. Let me transfer you."),
            Part.from_agent_transfer(agent="RootAgent")
        ])
        
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    webhook_success = callback_context.variables.get('webhook_success')
    if webhook_success is False:
        print("Webhook failure detected, routing to bell_ticket_mgmt_webhook_failure.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("I'm sorry, I'm experiencing technical difficulties right now."),
            Part.from_agent_transfer(agent='AppointmentManagementAgent')
        ])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback validation.")
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No post-generation overrides required for this specific state machine flow
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback")
    
    for index, part in enumerate(llm_response.content.parts):
        if part.has_function_response("evaluate_mya_eligibility"):
            print("evaluate_mya_eligibility tool response detected")
            response_payload = part.function_response.response.get("result", {})
            if "error" in response_payload:
                print("Tool failure detected, setting fallback route and ending session.")
                callback_context.variables["route"] = "tech_change_appointment_mya_false"
                return LlmResponse.from_parts(parts=[
                    Part.from_text("I apologize, but we are currently unable to access the appointment system. Let me route you accordingly."),
                    Part.from_end_session(reason="System Error Tool Failure")
                ])
            
            print("MYA eligibility checked successfully, ending session for routing.")
            return LlmResponse.from_parts(parts=[
                Part.from_end_session(reason="Routing Transition")
            ])
            
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback validation pass.")
    return None