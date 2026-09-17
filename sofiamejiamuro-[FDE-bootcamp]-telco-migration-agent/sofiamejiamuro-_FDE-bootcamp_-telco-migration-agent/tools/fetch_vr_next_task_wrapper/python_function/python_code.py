def fetch_vr_next_task_wrapper() -> dict:
    '''Calls the Virtual Repair next-task API to retrieve the next task payload.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            print("Mock mode enabled, returning dummy VR task payload")
            return {
                "result": {
                    "vr_type": "CDA",
                    "vr_title_desc": "Please unplug your modem from the power outlet, wait 30 seconds, and then plug it back in.",
                    "status_changed": True,
                    "is_expecting_answer": True,
                    "is_finished": False,
                    "acceptable_answers": [],
                    "webhook_success": True
                },
                "vr_type": "CDA",
                "vr_title_desc": "Please unplug your modem from the power outlet, wait 30 seconds, and then plug it back in.",
                "status_changed": True,
                "is_expecting_answer": True,
                "is_finished": False,
                "acceptable_answers": [],
                "webhook_success": True,
                "vr_context": {
                    "type": "CDA",
                    "is_expecting_answer": "true",
                    "is_finished": "false",
                    "status_changed": "true",
                    "dcx_action_code": "RESTART_MODEM"
                },
                "step_verbiage": {
                    "title": "Restart Modem",
                    "description": "Please unplug your modem from the power outlet, wait 30 seconds, and then plug it back in."
                }
            }
        print("Executing real backend fetch")
        api_response = tools.bell_vr_next_task_next_task({}).json()
        print("Business logic success")
        return api_response
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties retrieving their diagnostic results and attempt a retry."}