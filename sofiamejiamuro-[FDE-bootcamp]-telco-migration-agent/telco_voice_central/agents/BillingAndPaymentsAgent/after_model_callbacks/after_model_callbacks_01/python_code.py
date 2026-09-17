NATIVE_TRANSFER_TARGETS = {"BillingAndPaymentsAgent", "RootAgent"}

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

    # Webhook failure evaluation for due date is deterministically handled in before_model_callback per Pattern A.
    # Additional validation logic can be placed here if model override is necessary post-generation.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Handled Tool Error and other transitions inside before_model_callback for proper conversational flow.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    for part in llm_response.content.parts:
        if part.text:
            sanitized_text = part.text.lower()
            if "minimum amount required" in sanitized_text or "maximum amount" in sanitized_text or "montant minimum requis" in sanitized_text:
                attempt = callback_context.variables.get("loop_counter", 0) + 1
                callback_context.variables["loop_counter"] = attempt
                print(f"Invalid payment attempt pushback. Count: {attempt}")
                if attempt >= 3:
                    print("Max invalid payment attempts reached, transferring to bell_aqd.")
                    return LlmResponse.from_parts(parts=[
                        Part.from_text("I'm unable to process this payment arrangement. Let me transfer you."),
                        Part.from_agent_transfer(agent="RootAgent")
                    ])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # No strict post-processing requirements for this flow based on architectural constraints.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Note: Unhandled webhook errors specified in the agent blueprint architecture
    # are trapped at the Python Tool Wrapper level and converted to natural language 
    # 'agent_action' directives instructing the generative agent to handle the failure.
    # This enforces the required Transition to Failure_Handler gracefully.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Standard pass-through. Webhook logic and threshold boundaries are caught in before_model_callback.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback for bell_payment_clp_payment_amount")
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    sys_err = callback_context.variables.get('global_error_counter', 0)
    if sys_err >= 3:
        print('System error limits breached, forcing exit to bell_Feedback.')
        return LlmResponse.from_parts(parts=[
            Part.from_text('We are experiencing technical difficulties and will transfer you now.'),
            Part.from_agent_transfer(agent='RootAgent')
        ])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    retry_count = callback_context.variables.get('no_input_counter', 0)
    if retry_count >= 3:
        print('Enforcing transition to bell_aqd after max retries in after_model_callback.')
        lang = str(callback_context.variables.get('language', 'en')).lower()
        if 'fr' in lang:
            msg = 'Si vous souhaitez toujours effectuer une demande de paiements pré-autorisés, vous pouvez le faire dans l’appli Mon compte. Veuillez visiter https://vpc.ca/soutien pour en savoir plus.'
        else:
            msg = 'If you\'d still like to complete your Pre-Authorized payment request, you can do so in the My Account app. Please visit  vpc.ca/support for more information.'
        return LlmResponse.from_parts(parts=[
            Part.from_text(msg),
            Part.from_agent_transfer(agent='RootAgent')
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
    # Validation or end-session logic fallback
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Validation or custom end-session logic
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    retry_count = callback_context.variables.get('no_input_counter', 0)
    if retry_count >= 3:
        print('Executing logic gate: Max retries reached after model execution, transferring to bell_determine_handover.')
        return LlmResponse.from_parts(parts=[
            Part.from_agent_transfer(agent='RootAgent')
        ])
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Fallback state override validation logic if needed
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    try:
        for index, part in enumerate(llm_response.content.parts):
            if part.has_function_call('end_session'):
                print('End session function call detected.')
    except Exception as e:
        print(f'Error in after_model_callback: {e}')
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback logic")
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Validation and custom end-session triggers can be placed here if needed.
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    print("Executing after_model_callback pass-through.")
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    return None

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Webhook tool error transitions are seamlessly handled directly by the agent_action natural language system prompt returned upon tool crash, avoiding abrupt and ungraceful message interruptions to the user here.
    return None