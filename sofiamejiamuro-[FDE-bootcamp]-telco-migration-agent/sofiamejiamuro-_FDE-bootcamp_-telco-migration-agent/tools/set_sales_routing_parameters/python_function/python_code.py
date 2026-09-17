def set_sales_routing_parameters(line_type: str = "", route: str = "") -> dict:
    '''State Manipulator. Sets the session variables line_type and route in the session state.'''
    if get_variable("mock_mode"):
        safe_line_type_mock = str(line_type).strip()
        if safe_line_type_mock.lower() == "new":
            safe_line_type_mock = "New"

        safe_route_mock = str(route).strip().replace(" ", "_").lower()
        if not safe_route_mock:
            safe_route_mock = "sales_add_to_existing_account"

        return {
            "status": "success",
            "line_type": safe_line_type_mock,
            "route": safe_route_mock,
            "mock_mode": True
        }
    else:
        try:
            safe_line_type = str(line_type).strip()
            if safe_line_type.lower() == "new":
                safe_line_type = "New"

            safe_route = str(route).strip().replace(" ", "_").lower()
            if not safe_route:
                safe_route = "sales_add_to_existing_account"

            set_variable("line_type", safe_line_type)
            set_variable("route", safe_route)

            print("Business logic success: Variables line_type and route configured.")
            return {"status": "success", "line_type": safe_line_type, "route": safe_route}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}