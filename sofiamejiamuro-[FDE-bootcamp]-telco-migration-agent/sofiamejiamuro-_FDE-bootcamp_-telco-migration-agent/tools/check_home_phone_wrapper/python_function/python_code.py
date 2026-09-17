def check_home_phone_wrapper(phone_number: str = "") -> dict:
    '''Webhook Wrapper. Checks the provided phone number against the customer billing account to determine if it is a registered home phone line. Sets session variable is_home_phone.'''
    if get_variable('mock_mode'):
        set_variable('is_home_phone', False)
        print("check_home_phone_wrapper mock success")
        return {
            "status": "success",
            "is_home_phone": False,
            "message": "Phone number successfully verified as a valid mobile line.",
            "result": {
                "webhook_success": True,
                "is_home_phone": False
            }
        }
    else:
        try:
            payload = {"phone_number": str(phone_number).strip()}
            api_response = tools.INTERNAL_PROFILE_API_cpm_profile_info(payload).json()

            is_home_phone = api_response.get('is_home_phone', False)
            set_variable('is_home_phone', is_home_phone)

            print("Business logic success")
            return {"status": "success", "is_home_phone": is_home_phone}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}