def validate_pin_wrapper(pin: str = "", callKey: str = "") -> dict:
    '''Webhook Wrapper for customer-authentication#validate-pin.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                "result": {
                    "is_authenticated": True,
                    "is_locked": False,
                    "status": "success",
                    "pin_match": True,
                    "attempts_remaining": 3,
                    "message": "PIN validated successfully."
                },
                "status": "success",
                "is_authenticated": True,
                "is_locked": False,
                "data": {
                    "is_authenticated": True,
                    "is_locked": False,
                    "message": "PIN validated successfully."
                }
            }

        payload = {
            "pin": pin,
            "callKey": callKey
        }
        api_response = tools.validate_pin_validate_pin(payload).json()
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the PIN validation service is currently unavailable and offer an alternative authentication method or agent transfer."}