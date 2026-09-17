NATIVE_TRANSFER_TARGETS = {"TechSupportAndRepairAgent", "RootAgent"}

VERBATIM_STRINGS = [
    "Before we proceed, please note that by cancelling your service or porting out your number, any remaining contract balance or unreturned equipment fees will be billed on your final statement.",
    "Avant de procéder, veuillez noter qu'en annulant votre service ou en transférant votre numéro, tout solde de contrat restant ou frais d'équipement non retourné sera facturé sur votre dernière facture.",
    "Okay, I’ll transfer you now. There may be a moment of silence while I do so.",
    "D'accord, je vous transfère maintenant. Il se peut qu'il y ait un moment de silence.",
    "Hello! How can I help you today?",
    "Bonjour ! Comment puis-je vous aider aujourd’hui ?",
    "I am transferring you immediately to our Fraud Prevention team. Please stay on the line.",
    "Je vous transfère immédiatement à notre équipe de prévention de la fraude. Veuillez rester en ligne.",
    "A credit of $12.50 will appear on your next billing statement.",
    "Un crédit de 12,50 $ apparaîtra sur votre prochaine facture.",
    "Your request requires specialist approval. I am transferring you to a billing specialist now.",
    "Votre demande nécessite l'approbation d'un spécialiste. Je vous transfère à un spécialiste de la facturation."
]

from typing import Optional

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    if llm_response and llm_response.content and llm_response.content.parts:
        modified = False
        new_parts = []
        for p in llm_response.content.parts:
            if getattr(p, "agent_transfer", None):
                t = getattr(p.agent_transfer, "agent", "")
                if t and t not in NATIVE_TRANSFER_TARGETS:
                    new_parts.append(Part.from_agent_transfer(agent=t))
                    modified = True
                    continue
            
            # Sanitize verbatim response text if LLM attached intro/outro filler text
            if getattr(p, "text", None):
                txt = p.text
                for v_str in VERBATIM_STRINGS:
                    if v_str in txt and txt.strip() != v_str:
                        p = Part.from_text(text=v_str)
                        modified = True
                        break
            new_parts.append(p)

        if modified:
            return LlmResponse.from_parts(parts=new_parts)
    return None
