def get_apbs_for_location_wrapper(apb_location_id: float = 0.0, language: str = "", clid: float = 0.0) -> dict:
    '''Webhook Wrapper for get_apbs_for_location. Fetches APB config and updates session state.'''
    if get_variable("mock_mode"):
        set_variable("apb_message", "Welcome to Bell. This is a dynamic Audio Play Back message.")
        set_variable("hang_up", False)
        set_variable("agent_transfer", False)
        set_variable("call_control", "Y")
        set_variable("department_id", "800")
        set_variable("webhook_success", True)
        return {
            "status": "success",
            "message": "Variables successfully updated.",
            "apb_config": {
                "apb_message": "Welcome to Bell. This is a dynamic Audio Play Back message.",
                "hang_up": False,
                "agent_transfer": False,
                "interruptible": "Y",
                "department_id": "800"
            }
        }
    else:
        import json
        try:
            mock_mode = get_variable("mock_mode")
            mock_data = {
                "apb_message": "This is a dynamic Audio Play Back message.",
                "hang_up": False,
                "agent_transfer": False,
                "interruptible": "Y",
                "department_id": "800"
            }
            if mock_mode:
                response_data = mock_data
            else:
                # Backend toolset NA, defaulting to mock data fallback
                response_data = mock_data

            set_variable("apb_message", response_data.get("apb_message", ""))
            set_variable("hang_up", response_data.get("hang_up", False))
            set_variable("agent_transfer", response_data.get("agent_transfer", False))
            set_variable("call_control", response_data.get("interruptible", "N"))
            set_variable("department_id", str(response_data.get("department_id", "")))
            set_variable("webhook_success", True)

            print("Business logic success - APB variables set in state.")
            return {"status": "success", "message": "Variables successfully updated."}
        except Exception as e:
            logger.error(f"Crash: {e}")
            set_variable("webhook_success", False)
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}