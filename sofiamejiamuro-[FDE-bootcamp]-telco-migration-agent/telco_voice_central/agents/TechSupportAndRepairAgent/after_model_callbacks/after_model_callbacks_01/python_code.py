NATIVE_TRANSFER_TARGETS = {"RootAgent", "TechSupportAndRepairAgent"}

NATIVE_TRANSFER_TARGETS = {"RootAgent", "TechSupportAndRepairAgent"}

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

    # No specific after_model_callback logic required by blueprint
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print('Executing after_model_callback logic gates.')
    global_error_counter = callback_context.variables.get('global_error_counter', 0)
    try:
        error_count = int(global_error_counter)
    except (ValueError, TypeError):
        error_count = 0
        
    if error_count >= 3:
        print('Max errors reached, forcing transition to bell_aqd.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('It seems we are having trouble understanding each other. Let me transfer you to an agent who can help.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback")
    is_no_match = False
    if llm_response.content and llm_response.content.parts:
        for part in llm_response.content.parts:
            text_content = (part.text or "").lower()
            if "didn't get that" in text_content or "missed what you said" in text_content or "mal à comprendre" in text_content or "pas saisi" in text_content:
                is_no_match = True
                break
    
    if is_no_match:
        print("No-match / unhandled utterance detected.")
        error_count = callback_context.variables.get("global_error_counter", 0) + 1
        callback_context.variables["global_error_counter"] = error_count
        print(f"Global error counter is now {error_count}")
        
        if error_count >= 3:
            print("Max errors reached, triggering default escalation.")
            return LlmResponse.from_parts(parts=[
                Part.from_text("I'm having trouble understanding. Let me transfer you to a representative. / Je vais vous transférer à un représentant."),
                Part.from_agent_transfer(agent="escalation_agent")
            ])
        
        print("Playing bilingual reprompt for no-match.")
        return LlmResponse.from_parts(parts=[
            Part.from_text("I didn't get that. Can you say it again? / J'ai du mal à comprendre cette question. Pouvez-vous répéter?")
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
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Enforce strict wait loop timeout limits based on variables evaluated in routing context
    vr_type = str(callback_context.variables.get("vr_type", ""))
    status_changed = str(callback_context.variables.get("status_changed", "")).lower()
    is_expecting_answer = str(callback_context.variables.get("is_expecting_answer", "")).lower()
    
    # If the system remains in a backend polling wait loop
    if is_expecting_answer == "false" and status_changed == "false":
        if vr_type == "sharpStarting":
            counter = callback_context.variables.get("loop_counter", 0) + 1
            callback_context.variables["loop_counter"] = counter
            print(f"Incremented counter_sharp: {counter}")
            if counter >= 24:
                print("Max wait time reached for sharpStarting, routing to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("The Virtual Repair tool is taking a bit longer than usual to start. I'll connect you with an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
        elif vr_type == "Microservice":
            counter = callback_context.variables.get("loop_counter", 0) + 1
            aqd_counter = callback_context.variables.get("loop_counter", 0)
            callback_context.variables["loop_counter"] = counter
            print(f"Incremented microservice_counter: {counter}")
            if counter >= 24 or aqd_counter >= 8:
                print("Max wait time reached for Microservice, routing to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("This step is taking longer than usual, so I need to put you in contact with an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
                ])
        elif vr_type != "":
            counter = callback_context.variables.get("loop_counter", 0) + 1
            callback_context.variables["loop_counter"] = counter
            print(f"Incremented vr_counter: {counter}")
            if counter >= 24:
                print("Max wait time reached for general VR task, routing to bell_aqd.")
                return LlmResponse.from_parts(parts=[
                    Part.from_text("The backend process is taking too long. Connecting you to an agent."),
                    Part.from_agent_transfer(agent="RootAgent")
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
    # Passthrough: tool execution validation and deterministic retry routing is safely managed in before_model_callback
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    for part in llm_response.content.parts:
        if (part.has_function_response('fetch_and_parse_tv_profile') and
            'error' in part.function_response.response.get('result', {})):
            print('Executing Tool Failure detected, initiating transfer to bell_rehit_SMS.')
            return LlmResponse.from_parts(parts=[
                Part.from_text('Sorry, something went wrong retrieving your profile. Let me transition you to an SMS agent.'),
                Part.from_agent_transfer(agent='TechSupportAndRepairAgent')
            ])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Generative validation or strict exit constraints can be captured here if needed.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print('Executing after_model_callback')
    # Architectural requirement for tool error routing is handled in before_model_callback (Pattern A)
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No post-generation deterministic overrides needed for this agent
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Webhook failures are handled structurally in before_model_callback per Pattern A.
    return None