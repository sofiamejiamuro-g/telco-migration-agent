def get_vr_faq_override(action_code: str, language: str) -> dict:
    '''Queries internal FAQ mappings for Virtual Repair based on action code and sets session variable.'''
    if get_variable("mock_mode"):
        mock_answer = "To proceed, please ensure your modem's power cable is firmly plugged in and the lights are on. This is a standard troubleshooting step to establish a baseline connection."
        set_variable("faq_question_answer", mock_answer)
        return {"status": "success", "answer_found": True}

    try:
        sanitized_code = str(action_code).strip()
        sanitized_lang = str(language).strip().lower()

        # Simulated KB map overrides based on action code
        answer = ""
        if sanitized_code == "6590":
            answer = "Here is the information you requested about your service status."
        else:
            answer = "ANSWER_NOT_FOUND"

        set_variable("faq_question_answer", answer)
        print(f"FAQ override executed for code {sanitized_code}")

        return {"status": "success", "answer_found": answer != "ANSWER_NOT_FOUND"}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that FAQ retrieval failed and return to the routing prompt."}