def set_fallback_3_status(is_triggered: bool = False) -> dict:
    '''State Manipulator. Sets the session variable 'fallback_3_triggered' to the provided boolean value.'''
    if get_variable("mock_mode"):
        return {"status": "success", "fallback_3_triggered": bool(is_triggered)}

    try:
        set_variable('fallback_3_triggered', bool(is_triggered))
        print("Business logic success: fallback_3_triggered has been set")
        return {"status": "success", "fallback_3_triggered": bool(is_triggered)}
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}