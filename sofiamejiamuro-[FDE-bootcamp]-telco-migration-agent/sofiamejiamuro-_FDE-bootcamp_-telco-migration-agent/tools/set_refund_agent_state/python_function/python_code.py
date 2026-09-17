def set_refund_agent_state(outage_type: str = "", event_type: str = "") -> dict:
    '''State/Variable Manipulator. Updates 'outage_type' or 'event_type' based on user input.'''
    if get_variable("mock_mode"):
        if outage_type:
            set_variable('outage_type', str(outage_type).lower().strip())
        if event_type:
            set_variable('routing_val', str(event_type).lower().strip())
        return {
            "status": "success",
            "message": "Variables updated successfully.",
            "mock_mode": True,
            "simulated_updates": {
                "outage_type": str(outage_type).lower().strip() if outage_type else None,
                "event_type": str(event_type).lower().strip() if event_type else None
            }
        }

    try:
        if outage_type:
            sanitized_outage = str(outage_type).lower().strip()
            set_variable('outage_type', sanitized_outage)
            print(f"Business logic success: outage_type set to {sanitized_outage}")
        if event_type:
            sanitized_event = str(event_type).lower().strip()
            set_variable('routing_val', sanitized_event)
            print(f"Business logic success: event_type set to {sanitized_event}")
        return {"status": "success", "message": "Variables updated successfully."}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}