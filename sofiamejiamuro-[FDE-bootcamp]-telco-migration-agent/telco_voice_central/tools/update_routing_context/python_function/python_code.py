def update_routing_context(identification_status: str = "", customer_type: str = "", route: str = "", hardstop: bool = False, page_id: str = "", flow_id: str = "", page_name: str = "") -> dict:
    """Updates the conversation routing variables natively for target routing."""
    if get_variable("mock_mode"):
        return {
            "status": "success",
            "message": "Variables updated."
        }
    else:
        try:
            if identification_status:
                set_variable("identification_status", identification_status)
            if customer_type:
                set_variable("customer_profile_type", customer_type)
            if route:
                set_variable("route", route)
            if hardstop:
                set_variable("hardstop", hardstop)
            if page_id:
                set_variable("page_id", page_id)
            if flow_id:
                set_variable("flow_id", flow_id)
            if page_name:
                set_variable("page_name", page_name)

            print("Routing context updated successfully.")
            return {"status": "success", "message": "Variables updated."}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Inform the user that routing encountered a technical issue and transfer them to a human representative."}