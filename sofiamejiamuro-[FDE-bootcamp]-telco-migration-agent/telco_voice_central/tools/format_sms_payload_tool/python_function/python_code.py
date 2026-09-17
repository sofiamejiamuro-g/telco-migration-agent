def format_sms_payload_tool(language_code: str = "") -> dict:
    '''State/Variable Manipulator. Reads language and outputs rigid SMS content string and sms_type.'''
    import json

    if get_variable("mock_mode"):
        mock_content = "You can visit https://m.bell.ca/chatmanagepaymente to cancel pre-authorized payments in the MyBell app. ( bell.ca/about-us )"
        set_variable("sms_content", mock_content)
        set_variable("sms_type", "Public")
        return {
            "status": "success",
            "sms_content": mock_content,
            "sms_type": "Public"
        }

    try:
        lang = (language_code or get_variable("language") or "en").lower().strip()

        if "fr" in lang:
            content = "Vous pouvez visiter https://m.bell.ca/chatmanagepaymentf pour annuler les paiements préautorisés dans l'appli MonBell. ( bell.ca/apropos )"
        else:
            content = "You can visit https://m.bell.ca/chatmanagepaymente to cancel pre-authorized payments in the MyBell app. ( bell.ca/about-us )"

        set_variable("sms_content", content)
        set_variable("sms_type", "Public")
        print("Business logic success: SMS payload formatted based on language.")
        return {"status": "success", "sms_content": content, "sms_type": "Public"}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Explain to the user that the SMS could not be generated and offer to route them directly to feedback or read them the support link instead."}