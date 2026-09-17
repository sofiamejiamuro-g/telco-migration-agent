def determine_agent_queue(domain: str = "", menu_type: str = "", customer_type: str = "", intent: str = "") -> dict:
    '''Calls AQD backend to derive final transfer destinations.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print("Business logic success - mock mode")
            return {
                "status": "success",
                "data": {
                    "queue_name": "General_Support",
                    "menu_id": "999",
                    "department_id": "2005",
                    "routing_destination": "live_agent_queue",
                    "estimated_wait_time_seconds": 120,
                    "is_open": True
                }
            }
        payload = {"domain": domain, "menu_type": menu_type, "customer_type": customer_type, "intent": intent}
        api_response = tools.agent_queue_determination_get_queue(payload).json()
        print("Business logic success - queue determined")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}