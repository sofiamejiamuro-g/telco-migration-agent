def configure_tv_sync_sms_payload(language: str = "") -> dict:
    '''STATE MANIPULATOR: Sets sms_type and sms_content based on user language. No backend API calls.'''
    if get_variable("mock_mode"):
        set_variable("sms_type", "Public")
        mock_lang = str(language).lower().strip() if language else str(get_variable("language", "en")).lower().strip()
        if "fr" in mock_lang:
            set_variable("sms_content", "Bell : Vous pouvez visiter https://m.bell.ca/supportsynchprogf et suivre les instructions pour synchroniser votre programmation télé. ( bell.ca/apropos )")
        else:
            set_variable("sms_content", "Bell: You can visit https://m.bell.ca/supportsynchproge and follow the prompts to synchronize your TV programming. ( bell.ca/about-us )")
        return {
            "status": "success",
            "mock_mode": True,
            "message": "Mock TV sync SMS payload configured successfully."
        }
    else:
        try:
            print("Executing configure_tv_sync_sms_payload")
            lang_safe = str(language).lower().strip() if language else str(get_variable("language", "")).lower().strip()
            if not lang_safe:
                return {"error": "Language is missing", "agent_action": "Transition immediately to bell_aqd."}

            sms_type = "Public"
            if "fr" in lang_safe:
                sms_content = "Bell : Vous pouvez visiter https://m.bell.ca/supportsynchprogf et suivre les instructions pour synchroniser votre programmation télé. ( bell.ca/apropos )"
            else:
                sms_content = "Bell: You can visit https://m.bell.ca/supportsynchproge and follow the prompts to synchronize your TV programming. ( bell.ca/about-us )"

            set_variable("sms_type", sms_type)
            set_variable("sms_content", sms_content)

            print("Business logic success. Payload configured.")
            return {"status": "success"}
        except Exception as e:
            print(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Tool failed to set SMS payload. Transition immediately to bell_aqd."}