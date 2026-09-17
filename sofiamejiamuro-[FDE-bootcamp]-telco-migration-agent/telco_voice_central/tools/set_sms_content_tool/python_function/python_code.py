def set_sms_content_tool(language: str = "en", accepted: bool = False, different_number: bool = False, is_outage: bool = False) -> dict:
    '''Sets SMS variables based on user response.'''
    if get_variable("mock_mode"):
        lang = str(language).lower().strip()
        if accepted or different_number:
            set_variable('sms_type', 'Public')
            if 'fr' in lang:
                set_variable('sms_content', "Vous pouvez visiter https://m.bell.ca/chatmanagepaymentf pour annuler les paiements préautorisés dans l'appli MonBell. ( bell.ca/apropos )")
            else:
                set_variable('sms_content', "You can visit https://m.bell.ca/chatmanagepaymente to cancel pre-authorized payments in the MyBell app. ( bell.ca/about-us )")
            if different_number:
                set_variable('different_number', True)
            return {
                "status": "success",
                "action": "SMS_CONFIGURED",
                "mock_mode": True
            }
        else:
            set_variable('sms_send_status', 'Declined')
            return {
                "status": "success",
                "action": "SMS_DECLINED",
                "mock_mode": True
            }
    else:
        try:
            lang = str(language).lower().strip()
            if accepted or different_number:
                set_variable('sms_type', 'Public')
                if 'fr' in lang:
                    sms_text = "Vous pouvez visiter https://m.bell.ca/chatmanagepaymentf pour annuler les paiements préautorisés dans l'appli MonBell. ( bell.ca/apropos )"
                else:
                    sms_text = "You can visit https://m.bell.ca/chatmanagepaymente to cancel pre-authorized payments in the MyBell app. ( bell.ca/about-us )"
                set_variable('sms_content', sms_text)
                if different_number:
                    set_variable('different_number', True)
                print("Business logic success: SMS content set.")
                return {"status": "success", "action": "SMS_CONFIGURED"}
            else:
                set_variable('sms_send_status', 'Declined')
                print("Business logic success: SMS declined.")
                return {"status": "success", "action": "SMS_DECLINED"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Inform the user of a technical error and offer an alternative."}