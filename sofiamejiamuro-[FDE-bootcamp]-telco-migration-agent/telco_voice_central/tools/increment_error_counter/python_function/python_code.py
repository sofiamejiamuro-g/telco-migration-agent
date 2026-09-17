def increment_error_counter() -> dict:
    """State/Variable Manipulator. Retrieves the session variable 'global_error_counter' (defaults to 0 if null), increments it by 1, and writes it back to the session state natively. Returns the new integer value."""
    if get_variable("mock_mode"):
        return {"status": "success", "global_error_counter": 1}
    else:
        try:
            counter = get_variable("global_error_counter")
            if counter is None or counter == "":
                counter = 0
            else:
                counter = int(counter)
            counter += 1
            set_variable("global_error_counter", counter)
            print("Business logic success: Incremented global_error_counter")
            return {"status": "success", "global_error_counter": counter}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Inform the user that a technical error occurred and transfer them to a representative."}