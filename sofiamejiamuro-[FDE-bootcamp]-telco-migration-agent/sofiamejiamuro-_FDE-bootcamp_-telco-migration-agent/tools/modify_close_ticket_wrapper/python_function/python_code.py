def modify_close_ticket_wrapper(task_type: str = "") -> dict:
    '''Submits the request to modify or close an eligible ticket without a dispatch.'''
    try:
        sanitized_task = task_type.lower().strip().replace(' ', '_')
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("webhook_success", True)
            return {
                "status": "success",
                "result": {
                    "webhook_success": True,
                    "ticket_state": "CLOSED",
                    "confirmation_number": "CNF-9988776655",
                    "message": "Ticket successfully modified and closed.",
                    "task_type_processed": sanitized_task
                }
            }
        payload = {"task_type": sanitized_task}
        api_response = tools.modify_close_ticket_modify_close_ticket(payload).json()
        set_variable("webhook_success", True)
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties closing the ticket and offer to transfer them to a representative."}