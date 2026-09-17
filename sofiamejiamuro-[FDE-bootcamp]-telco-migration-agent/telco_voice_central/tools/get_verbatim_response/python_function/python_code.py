"""
Single Source of Truth tool for all verbatim expectations across Bell Canada CXAS Sub-Agents.
Supports both English ('en') and Canadian French ('fr-CA').
"""

VERBATIM_STORE = {
    "INITIAL_GREETING": {
        "en": "Hello! How can I help you today?",
        "fr-CA": "Bonjour ! Comment puis-je vous aider aujourd’hui ?"
    },
    "LIVE_AGENT_HANDOFF": {
        "en": "Okay, I’ll transfer you now. There may be a moment of silence while I do so.",
        "fr-CA": "D'accord, je vous transfère maintenant. Il se peut qu'il y ait un moment de silence."
    },
    "FEEDBACK_PROMPT": {
        "en": "Great! Just a quick question before you leave. Did you find the interaction easy?",
        "fr-CA": "Parfait ! Une dernière question avant de vous quitter. Avez-vous trouvé cet appel facile ?"
    },
    "FEEDBACK_POSITIVE": {
        "en": "That's Perfect! I'm really happy to hear that. Thanks for calling Bell. Goodbye!",
        "fr-CA": "C'est parfait ! Je suis ravi(e) de l'entendre. Merci d'avoir appelé Bell. Au revoir !"
    },
    "FEEDBACK_NEGATIVE": {
        "en": "I appreciate your feedback. Thanks for calling Bell. Goodbye!",
        "fr-CA": "J'apprécie vos commentaires. Merci d'avoir appelé Bell. Au revoir !"
    },
    "MANDATORY_CONTRACT_DISCLOSURE": {
        "en": "Before we proceed, please note that by cancelling your service or porting out your number, any remaining contract balance or unreturned equipment fees will be billed on your final statement.",
        "fr-CA": "Avant de procéder, veuillez noter qu'en annulant votre service ou en transférant votre numéro, tout solde de contrat restant ou frais d'équipement non retourné sera facturé sur votre dernière facture."
    },
    "FRAUD_IMMEDIATE_TRANSFER": {
        "en": "I am transferring you immediately to our Fraud Prevention team. Please stay on the line.",
        "fr-CA": "Je vous transfère immédiatement à notre équipe de prévention de la fraude. Veuillez rester en ligne."
    },
    "MFA_SMS_OFFER": {
        "en": "Multi-Factor Authentication is an essential safeguard that helps protect your account. I will send a text to the device you're calling from with a link to learn more. Is that alright?",
        "fr-CA": "L'authentification multifacteur est une protection essentielle qui protège votre compte. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez avec un lien pour en savoir plus. Est-ce que cela vous convient ?"
    },
    "PROFILE_UPDATE_SMS_OFFER": {
        "en": "Great news! You can easily update your MyBell profile online. I'll send a text to the device you're calling from so that you can easily make the changes. Is that alright?",
        "fr-CA": "Excellente nouvelle ! Vous pouvez facilement mettre à jour votre profil MonBell en ligne. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez afin que vous puissiez apporter les modifications. Est-ce que cela vous convient ?"
    },
    "SUSPEND_RESTORE_SMS_OFFER": {
        "en": "Sure, I can help with that. You can easily suspend or restore your services in MyBell. I will send a text to the device you're calling from with a link to do it yourself. Is that alright?",
        "fr-CA": "Bien sûr, je peux vous aider. Vous pouvez facilement suspendre ou rétablir vos services dans MonBell. Je vais envoyer un texto sur l'appareil au moyen duquel vous appelez avec un lien pour le faire vous-même. Est-ce que cela vous convient ?"
    },
    "CREDIT_CONFIRMATION": {
        "en": "A credit of $12.50 will appear on your next billing statement.",
        "fr-CA": "Un crédit de 12,50 $ apparaîtra sur votre prochaine facture."
    },
    "SPECIALIST_THRESHOLD_ESCALATION": {
        "en": "Your request requires specialist approval. I am transferring you to a billing specialist now.",
        "fr-CA": "Votre demande nécessite l'approbation d'un spécialiste. Je vous transfère à un spécialiste de la facturation."
    },
    "PAYMENT_SUCCESS_SECURE": {
        "en": "Thank you for your payment. A confirmation has been processed using your card ending in {last_4_digits}.",
        "fr-CA": "Merci pour votre paiement. Une confirmation a été traitée avec votre carte se terminant par {last_4_digits}."
    },
    "PAYMENT_DECLINED_RETRY": {
        "en": "Your card payment was declined. Please provide an alternative payment card to complete your transaction.",
        "fr-CA": "Votre carte de paiement a été refusée. Veuillez fournir une autre carte de paiement pour compléter votre transaction."
    },
    "AUTOPAY_CONFIRMATION": {
        "en": "Autopay has been successfully configured for your account.",
        "fr-CA": "Le paiement automatique a été configuré avec succès pour votre compte."
    },
    "AUTH_PROMPT_PIN": {
        "en": "To verify your account, please enter or say your 4-digit security PIN.",
        "fr-CA": "Pour vérifier votre compte, veuillez me donner ou saisir votre NIP de sécurité à 4 chiffres."
    },
    "AUTH_RETRY_STRIKE": {
        "en": "That information didn't match. Please try entering your PIN or security information again.",
        "fr-CA": "Ces renseignements ne correspondent pas. Veuillez réessayer de saisir votre NIP ou vos informations de sécurité."
    },
    "AUTH_SUCCESS": {
        "en": "Thank you, your identity has been verified.",
        "fr-CA": "Merci, votre identité a été vérifiée avec succès."
    },
    "OUTAGE_ACTIVE_CONFIRM": {
        "en": "There is an active service outage in your area. Technicians are currently working to resolve the issue.",
        "fr-CA": "Une panne de service est actuellement en cours dans votre secteur. Nos techniciens travaillent à la résoudre."
    },
    "SMS_TROUBLESHOOT_OFFER": {
        "en": "No active outage was found. I can send an SMS link with a step-by-step troubleshooting guide to your phone. Would you like that?",
        "fr-CA": "Aucune panne n'a été détectée. Je peux envoyer un lien SMS avec un guide de dépannage étape par étape sur votre téléphone. Souhaitez-vous le recevoir ?"
    },
    "BUSINESS_ACCOUNT_DEFLECTION": {
        "en": "To get you the best support for your business account, I'll transfer you to an agent. You'll need to use your phone keypad instead of talking to the virtual assistant.",
        "fr-CA": "Pour obtenir le meilleur soutien pour votre compte d'entreprise, je vais vous transférer à un agent. Vous devrez utiliser le clavier de votre téléphone."
    },
    "SHIPMENT_TRACKING_SMS_OFFER": {
        "en": "Got it, you can view and check the status of your device order in MyBell. I'll send a text to the device you are calling from, so that you can track your shipment. Is that alright?",
        "fr-CA": "J'ai compris, vous pouvez consulter l'état de votre commande sur MonBell. Je vais vous envoyer un texto pour suivre votre livraison. Est-ce que cela vous convient ?"
    },
    "WARRANTY_CLAIM_SUBMITTED": {
        "en": "Your warranty replacement request for your device has been submitted. You will receive an email with instructions on returning your unit.",
        "fr-CA": "Votre demande de remplacement sous garantie pour votre appareil a été soumise. Vous recevrez un courriel avec les instructions de retour."
    },
    "TECH_EN_ROUTE_NO_CANCEL": {
        "en": "Unfortunately you can not cancel your appointment as the technician is already on their way. You can advise the technician upon arrival with your concerns.",
        "fr-CA": "Malheureusement, vous ne pouvez pas annuler votre rendez-vous, car le ou la technicien(ne) est déjà en route. Vous pouvez faire part de vos préoccupations au ou à la technicien(ne) dès son arrivée."
    },
    "MANAGE_APP_SMS_OFFER": {
        "en": "Are you aware of our Manage Your Appointment App? I'll send you a text to the device you're calling from so that you can view, reschedule, or cancel your appointment.",
        "fr-CA": "Connaissez-vous notre appli Gérez votre rendez-vous? Je vais vous envoyer un texto afin que vous puissiez consulter, replanifier ou annuler votre rendez-vous."
    }
}


def get_verbatim_response(response_key: str, language: str = "en", **kwargs) -> dict:
    """
    Returns the exact verbatim string from the single source of truth dictionary.
    
    Args:
        response_key (str): The unique identifier for the verbatim message.
        language (str): Language code ('en', 'fr-CA', etc.).
        **kwargs: Optional string formatting parameters (e.g. last_4_digits).
        
    Returns:
        dict: {'status': 'success', 'verbatim_text': str}
    """
    lang_code = "fr-CA" if "fr" in str(language).lower() else "en"
    messages = VERBATIM_STORE.get(response_key, {})
    raw_text = messages.get(lang_code, messages.get("en", f"Message for '{response_key}' not found."))
    
    # Safely format string if kwargs provided
    try:
        formatted_text = raw_text.format(**kwargs) if kwargs else raw_text
    except KeyError:
        formatted_text = raw_text
        
    return {
        "status": "success",
        "response_key": response_key,
        "language": lang_code,
        "verbatim_text": formatted_text
    }
