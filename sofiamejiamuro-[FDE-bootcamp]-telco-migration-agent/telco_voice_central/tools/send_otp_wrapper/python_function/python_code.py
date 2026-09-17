def send_otp_wrapper(brand: str = "", callKey: str = "", target_number: str = "") -> dict:
    '''Webhook Wrapper for customer-authentication#send-otp.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                "status": "success",
                "result": {
                    "status": "success",
                    "message": "OTP sent successfully"
                },
                "data": {
                    "delivery_status": "sent",
                    "target_number": target_number or "9999999999",
                    "expires_in": 300,
                    "message": "6-digit OTP code dispatched successfully to the requested mobile number."
                }
            }

        payload = {
            "brand": brand,
            "callKey": callKey,
            "target_number": target_number
        }
        api_response = tools.send_otp_send_otp(payload).json()
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the OTP could not be sent due to a technical error and offer to fallback to postal code authentication or transfer."}