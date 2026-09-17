def clear_infobot_flag() -> dict:
    '''State Manipulator. Sets the 'infobot_flag' variable to None/Null within the active session state.'''
    if get_variable("mock_mode"):
        return {"status": "success", "message": "infobot_flag has been cleared."}

    try:
        set_variable('infobot_flag', None)
        print("Business logic success: infobot_flag cleared.")
        return {"status": "success", "message": "infobot_flag has been cleared."}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}