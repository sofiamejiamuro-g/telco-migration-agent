def trigger_sms_notification_wrapper(language: str = "en", offer_type: str = "") -> dict:
    '''State/Variable Manipulator tool. Formats the correct SMS body based on language and offer_type, updates session state variables (sms_type, sms_content), and prepares the environment for the external bell_SMS_Trigger flow.'''
    if get_variable("mock_mode"):
        return {"status": "success", "message": "SMS content formatted and variables set successfully."}
    else:
        try:
            lang_sanitized = language.lower().strip()
            offer_sanitized = offer_type.lower().strip().replace(' ', '_')
            sms_content = ""
            if lang_sanitized in ["fr-ca", "fr"]:
                if offer_sanitized == "preauthorized_payment":
                    sms_content = "Vous pouvez visiter https://m.bell.ca/eceffectuerautopaiement pour configurer des paiements préautorisés dans l'application MonBell. ( bell.ca/apropos )"
                else:
                    sms_content = "Vous pouvez visiter https://m.bell.ca/ecgererpaiement pour effectuer un paiement dans l'application MonBell.( bell.ca/apropos )"
            else:
                if offer_sanitized == "preauthorized_payment":
                    sms_content = "You can visit https://m.bell.ca/ecsetupautopayment to set up pre-authorized payments in the MyBell app. ( bell.ca/about-us )"
                else:
                    sms_content = "You can visit https://m.bell.ca/ecmanagepayment to make a payment in the MyBell app.( bell.ca/about-us )"
            set_variable('sms_type', 'Public')
            set_variable('sms_content', sms_content)
            print("Business logic success")
            return {"status": "success", "message": "SMS content formatted and variables set successfully."}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}