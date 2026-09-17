def extract_vr_routing_context(vr_next_task_payload: dict) -> dict:
    '''Safely parses the nested JSON task payload and flattens it into standard session variables.'''
    if get_variable("mock_mode"):
        set_variable("vr_type", "CDA")
        set_variable("is_expecting_answer", "true")
        set_variable("is_finished", "false")
        set_variable("status_changed", "true")
        set_variable("dcx_action_code", "RESTART_MODEM")
        set_variable("sms_content", "https://bell.ca/mock-sms-link")
        return {"status": "success", "message": "Context variables updated successfully."}
    else:
        try:
            if not isinstance(vr_next_task_payload, dict):
                return {"error": "Invalid payload format", "agent_action": "Retry fetching the task."}

            vr_context = vr_next_task_payload.get("vr_context", {})
            vr_type = str(vr_context.get("type", ""))
            is_expecting_answer = str(vr_context.get("is_expecting_answer", "")).lower()
            is_finished = str(vr_context.get("is_finished", "")).lower()
            status_changed = str(vr_context.get("status_changed", "")).lower()
            dcx_action_code = str(vr_context.get("dcx_action_code", ""))

            acceptable_answers = vr_next_task_payload.get("acceptable_answers", [])
            sms_content = ""
            if isinstance(acceptable_answers, list) and len(acceptable_answers) > 0:
                sms_content = str(acceptable_answers[0].get("deep_link", ""))

            set_variable("vr_type", vr_type)
            set_variable("is_expecting_answer", is_expecting_answer)
            set_variable("is_finished", is_finished)
            set_variable("status_changed", status_changed)
            set_variable("dcx_action_code", dcx_action_code)
            set_variable("sms_content", sms_content)

            print("Successfully extracted and set routing context variables")
            return {"status": "success", "message": "Context variables updated successfully."}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Inform the user that data extraction failed and transition to fallback logic."}