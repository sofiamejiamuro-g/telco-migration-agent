def evaluate_ticket_status_wrapper(language: str = "") -> dict:
    '''Retrieves and evaluates ticket status, returning scenario, formatted message, and special queue.'''
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("ticket_state", "SCHEDULED")
            set_variable("message_text", "Your ticket is currently active and a technician is scheduled.")
            set_variable("special_queue", "")
            set_variable("webhook_success", True)
            return {
                "status": "success",
                "result": {
                    "dispatch_status": "SCHEDULED",
                    "ticket_scenario": "ELIGIBLE_DISPATCH",
                    "formatted_status_message": "Your ticket is currently active and a technician is scheduled.",
                    "special_queue": "",
                    "webhook_success": True
                },
                "data": {
                    "ticket_id": "TKT987654321",
                    "dispatch_status": "SCHEDULED",
                    "appointment_date": "2023-12-01",
                    "appointment_window": "08:00 - 12:00",
                    "eligible_for_cancel": True,
                    "eligible_for_reschedule": True
                }
            }

        sanitized_language = language.lower().strip()
        payload = {"language": sanitized_language}
        api_response = tools.ticket_mgmt_evaluate_ticket(payload).json()
        set_variable("webhook_success", True)
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties checking the ticket status and offer to transfer them to a representative."}