NATIVE_TRANSFER_TARGETS = {"BillingAndPaymentsAgent", "RootAgent"}

from typing import Optional

def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    if llm_request.contents and llm_request.contents[-1].parts:
        for p in llm_request.contents[-1].parts:
            if getattr(p, "function_response", None):
                rd = getattr(p.function_response, "response", None) or dict()
                rd = rd.get("result", rd) if isinstance(rd, dict) else dict()
                if isinstance(rd, dict):
                    t = rd.get("target") or rd.get("target_agent")
                    a = rd.get("action")
                    if a in ("agentTransfer", "Transfer") and t:
                        if t not in NATIVE_TRANSFER_TARGETS:
                            return LlmResponse.from_parts(
                                parts=[Part.from_agent_transfer(agent=t)]
                            )
    return None
