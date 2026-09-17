def validate_otp_wrapper(brand: str = "", callKey: str = "", otp_code: str = "") -> dict:
    '''Webhook Wrapper for customer-authentication#validate-otp.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                "status": "success",
                "is_authenticated": True,
                "result": {
                    "is_authenticated": True,
                    "status": "success"
                },
                "data": {
                    "is_authenticated": True,
                    "verification_status": "MATCHED",
                    "message": "OTP successfully validated.",
                    "brand": brand,
                    "callKey": callKey
                }
            }

        payload = {
            "brand": brand,
            "callKey": callKey,
            "otp_code": otp_code
        }
        api_response = tools.validate_otp_validate_otp(payload).json()
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the OTP validation service is unavailable and fallback to postal code authentication or an agent."}