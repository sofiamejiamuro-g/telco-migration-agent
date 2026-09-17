def start_auth_session_wrapper(billing_account: float = 0.0, calling_number: float = 0.0, brand: str = "") -> dict:
    '''Webhook Wrapper for customer-authentication#start-auth-session.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                "status": "success",
                "result": {
                    "session_id": "auth_sess_987654321",
                    "callKey": "mock_key_999",
                    "pin_available": True,
                    "has_pin": True,
                    "otp_tns": ["4165551234"],
                    "mobile_numbers": ["4165551234"],
                    "postal_code_available": True,
                    "is_authenticated": False
                },
                "data": {
                    "session_id": "auth_sess_987654321",
                    "callKey": "mock_key_999",
                    "pin_available": True,
                    "has_pin": True,
                    "otp_tns": ["4165551234"],
                    "mobile_numbers": ["4165551234"],
                    "postal_code_available": True,
                    "is_authenticated": False
                }
            }
        payload = {
            "billing_account": billing_account,
            "calling_number": calling_number,
            "brand": brand
        }
        api_response = tools.start_auth_session_start_auth_session(payload).json()
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties starting the authentication session and offer to transfer them to a representative."}