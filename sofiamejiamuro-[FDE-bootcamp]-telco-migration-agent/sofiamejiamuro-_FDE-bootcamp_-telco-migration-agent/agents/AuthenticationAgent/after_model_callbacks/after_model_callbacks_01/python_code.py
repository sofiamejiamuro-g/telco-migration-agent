NATIVE_TRANSFER_TARGETS = {"AuthenticationAgent", "RootAgent"}

NATIVE_TRANSFER_TARGETS = {"AuthenticationAgent", "RootAgent"}

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

    try:
        for index, part in enumerate(llm_response.content.parts):
            if part.has_function_response("execute_customer_identification_check"):
                result = part.function_response.response.get("result", {})
                if "error" in result:
                    print("Tool execution failed, setting identification_status to Fail and transferring.")
                    callback_context.variables["identification_status"] = "Fail"
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("Sorry, there was a problem on our side and I can't find your profile. Please hold while I connect you with an agent."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
    except Exception as e:
        print(f"Callback error: {e}")
    
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Any webhook timeout, bad-request, or unavailability events are handled preemptively in before_model_callback through tool result parsing.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Validation and error routing handled defensively in before_model_callback.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print('Executing after_model_callback verification.')
    return None