def set_routing_variable(target_route: str = "") -> dict:
    '''State Manipulator. Sets the session variable route to the provided value.'''
    if get_variable("mock_mode"):
        sanitized_route = str(target_route).strip()
        if not sanitized_route:
            sanitized_route = "sales_order_device"
        return {
            "status": "success",
            "route": sanitized_route,
            "mock_mode_execution": True
        }

    try:
        sanitized_route = str(target_route).strip()
        if not sanitized_route:
            sanitized_route = "sales_order_device"
        set_variable('route', sanitized_route)
        print("Business logic success: Route variable updated.")
        return {"status": "success", "route": sanitized_route}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}