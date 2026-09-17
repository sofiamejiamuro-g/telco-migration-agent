def update_event_type(event_type: str = "") -> dict:
    '''State Manipulator: Updates the 'event_type' session variable.'''
    if get_variable("mock_mode"):
        mock_event = event_type.strip().lower() if event_type.strip() else "anything_else_start_over"
        return {
            "status": "success",
            "event_type": mock_event,
            "message": "Mock mode enabled: Event type successfully registered."
        }
    else:
        try:
            sanitized_event = event_type.strip().lower()
            if not sanitized_event:
                sanitized_event = "anything_else_start_over"
            set_variable('routing_val', sanitized_event)
            print(f"Business logic success: event_type set to {sanitized_event}")
            return {"status": "success", "event_type": sanitized_event}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}