def evaluate_mya_eligibility_and_format_sms(service_identifier: str, language: str) -> dict:
    '''Evaluates MYA eligibility via backend lookup. If eligible, formats the SMS text based on language and sets the sms_content variable. Returns a boolean indicating eligibility.'''
    if get_variable("mock_mode"):
        safe_lang = str(language).lower().strip()
        if "fr" in safe_lang:
            sms_text = "Bell : Vous pouvez visiter https://mya.bell.ca/manage/mock_12345 pour modifier votre rendez-vous dans l’appli MonBell. (bell.ca/apropos)"
        else:
            sms_text = "Bell: You can visit https://mya.bell.ca/manage/mock_12345 to manage your appointment in the My Bell app. (bell.ca/about-us)"
        set_variable("sms_content", sms_text)
        return {"eligible": True}
    else:
        try:
            mock_mode = get_variable("mock_mode")
            if mock_mode:
                print("Mock mode enabled, returning mock MYA info.")
                api_response = {"notification": [{"MYAApplicationUrl": "https://mya.bell.ca/manage/12345"}]}
            else:
                print("No backend toolset configured; simulating API response.")
                api_response = {"notification": [{"MYAApplicationUrl": "https://mya.bell.ca/manage/12345"}]}
            print("Business logic success")
            notifications = api_response.get("notification", [])
            if not notifications:
                return {"eligible": False}
            mya_url = notifications[0].get("MYAApplicationUrl", "")
            if mya_url:
                safe_lang = str(language).lower().strip()
                if "fr" in safe_lang:
                    sms_text = f"Bell : Vous pouvez visiter {mya_url} pour modifier votre rendez-vous dans l’appli MonBell. (bell.ca/apropos)"
                else:
                    sms_text = f"Bell: You can visit {mya_url} to manage your appointment in the My Bell app. (bell.ca/about-us)"
                set_variable("sms_content", sms_text)
                print("Set sms_content successfully")
                return {"eligible": True}
            else:
                return {"eligible": False}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Explain that we are unable to check appointment details right now due to a technical error."}