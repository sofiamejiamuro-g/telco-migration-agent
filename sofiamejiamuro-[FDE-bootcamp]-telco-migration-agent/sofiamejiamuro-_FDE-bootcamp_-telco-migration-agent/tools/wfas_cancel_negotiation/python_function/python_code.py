def wfas_cancel_negotiation(released_preferred: str) -> dict:
    '''Webhook Wrapper. Cancels the active hold or interaction context in WFAS.'''
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            print("Business logic success")
            return {
                "status": "success",
                "webhook_success": True,
                "data": {
                    "cancelled": True,
                    "released_preferred": released_preferred,
                    "interaction_status": "RELEASED",
                    "message": "The active hold and interaction context in WFAS have been successfully cancelled."
                }
            }

        payload = {"released_preferred": released_preferred}
        result = tools.cancel_cancel(payload).json()
        print("Business logic success")
        return {"status": "success", "data": result}
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Apologize to the user that we encountered a small issue but we will transfer them to complete the process."}