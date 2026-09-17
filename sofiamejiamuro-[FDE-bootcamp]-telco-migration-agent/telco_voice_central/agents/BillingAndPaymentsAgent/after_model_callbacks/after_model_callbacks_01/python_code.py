NATIVE_TRANSFER_TARGETS = {"BillingAndPaymentsAgent", "RootAgent"}

VERBATIM_STRINGS = [
    "Hello! How can I help you today?",
    "Bonjour ! Comment puis-je vous aider aujourd’hui ?",
    "Okay, I’ll transfer you now. There may be a moment of silence while I do so.",
    "D'accord, je vous transfère maintenant. Il se peut qu'il y ait un moment de silence.",
    "Great! Just a quick question before you leave. Did you find the interaction easy?",
    "Parfait ! Une dernière question avant de vous quitter. Avez-vous trouvé cet appel facile ?",
    "That's Perfect! I'm really happy to hear that. Thanks for calling Bell. Goodbye!",
    "C'est parfait ! Je suis ravi(e) de l'entendre. Merci d'avoir appelé Bell. Au revoir !",
    "I appreciate your feedback. Thanks for calling Bell. Goodbye!",
    "J'apprécie vos commentaires. Merci d'avoir appelé Bell. Au revoir !",
    "Before we proceed, please note that by cancelling your service or porting out your number, any remaining contract balance or unreturned equipment fees will be billed on your final statement.",
    "Avant de procéder, veuillez noter qu'en annulant votre service ou en transférant votre numéro, tout solde de contrat restant ou frais d'équipement non retourné sera facturé sur votre dernière facture.",
    "I am transferring you immediately to our Fraud Prevention team. Please stay on the line.",
    "Je vous transfère immédiatement à notre équipe de prévention de la fraude. Veuillez rester en ligne.",
    "Multi-Factor Authentication is an essential safeguard that helps protect your account. I will send a text to the device you're calling from with a link to learn more. Is that alright?",
    "L'authentification multifacteur est une protection essentielle qui protège votre compte. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez avec un lien pour en savoir plus. Est-ce que cela vous convient ?",
    "Great news! You can easily update your MyBell profile online. I'll send a text to the device you're calling from so that you can easily make the changes. Is that alright?",
    "Excellente nouvelle ! Vous pouvez facilement mettre à jour votre profil MonBell en ligne. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez afin que vous puissiez apporter les modifications. Est-ce que cela vous convient ?",
    "Sure, I can help with that. You can easily suspend or restore your services in MyBell. I will send a text to the device you're calling from with a link to do it yourself. Is that alright?",
    "Bien sûr, je peux vous aider. Vous pouvez facilement suspendre ou rétablir vos services dans MonBell. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez avec un lien pour le faire vous-même. Est-ce que cela vous convient ?",
    "A credit of $12.50 will appear on your next billing statement.",
    "Un crédit de 12,50 $ apparaîtra sur votre prochaine facture.",
    "Your request requires specialist approval. I am transferring you to a billing specialist now.",
    "Votre demande nécessite l'approbation d'un spécialiste. Je vous transfère à un spécialiste de la facturation.",
    "Thank you for your payment. A confirmation has been processed using your card ending in 4321.",
    "Merci pour votre paiement. Une confirmation a été traitée avec votre carte se terminant par 4321.",
    "Your card payment was declined. Please provide an alternative payment card to complete your transaction.",
    "Votre paiement par carte a été refusé. Veuillez fournir une autre carte de paiement pour effectuer votre transaction.",
    "Pre-Authorized Payments (Auto-pay) have been successfully enabled for your account.",
    "Les paiements préautorisés (prélèvement automatique) ont été activés avec succès pour votre compte.",
    "We are currently experiencing a service outage in your area. Our technicians are actively working to resolve it. I can send a text to your phone with live updates. Is that okay?",
    "Nous subissons actuellement une panne de service dans votre région. Nos techniciens s'affairent à la résoudre. Je peux envoyer un texto à votre téléphone contenant des mises à jour en direct. Est-ce que cela vous convient ?",
    "Good news! There are no active service outages reported in your area. I can send a text to your phone with troubleshooting steps for your service. Is that okay?",
    "Bonne nouvelle ! Aucune panne de service active n'est signalée dans votre région. Je peux envoyer un texto à votre téléphone contenant des étapes de dépannage pour votre service. Est-ce que cela vous convient ?",
    "I can help you reset your password. I will send a text to the device you're calling from with a secure link to complete the reset. Is that alright?",
    "Je peux vous aider à réinitialiser votre mot de passe. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez avec un lien sécurisé pour effectuer la réinitialisation. Est-ce que cela vous convient ?",
    "This service is dedicated to residential accounts. For assistance with a business account, please call 1-800-667-0123 or visit bell.ca/business.",
    "Ce service est réservé aux comptes résidentiels. Pour de l'aide avec un compte d'entreprise, veuillez composer le 1 800 667-0123 ou visiter bell.ca/affaires."
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
