def set_routing_variables(route: str = "", event_type: str = "") -> dict:
    '''State Manipulator. Sets session variables 'route' and 'event_type'. Since Generative LLMs cannot reliably set session variables natively via plain text, this tool ensures state mutation is explicitly handled.'''
    if get_variable("mock_mode"):
        return {
            "status": "success",
            "message": "Routing variables successfully updated.",
            "mock_mode": True
        }

    try:
        if route:
            sanitized_route = route.lower().strip().replace(' ', '_')
            set_variable('route', sanitized_route)
        if event_type:
            sanitized_event = event_type.lower().strip()
            set_variable('routing_val', sanitized_event)
        print("Business logic success")
        return {"status": "success", "message": "Routing variables successfully updated."}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}