def set_language_based_sms_content(language: str = "") -> dict:
    '''State/Variable Manipulator. Evaluates the language variable natively to set sms_content and sms_type via the state manager.'''
    if get_variable("mock_mode"):
        return {"status": "success", "message": "SMS variables set."}
    else:
        import json
        try:
            if not language:
                language = str(get_variable("language") or "en")

            sanitized_language = language.lower().strip()

            if sanitized_language in ["en", "en-ca"]:
                sms_content = "Bell msg: You can visit https://m.bell.ca/ecmanagepayment to make a payment in the MyBell app. ( bell.ca/about-us )"
            else:
                sms_content = "Mess. de Bell: Vous pouvez visiter https://m.bell.ca/ecgererpaiement pour effectuer un paiement dans l'application MonBell. ( bell.ca/apropos )"

            set_variable("sms_content", sms_content)
            set_variable("sms_type", "Public")

            print("Business logic success: set_language_based_sms_content executed")
            return {"status": "success", "message": "SMS variables set."}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and proceed with standard handling."}