def check_preauth_setup_wrapper() -> dict:
    '''Webhook Wrapper. Calls pre-auth-payment#get-existing and extracts paymentMethod.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("payment_method", "PreAuthCreditCard")
            print("Business logic success: Mock Mode pre-auth setup check.")
            return {
                "status": "success",
                "data": {
                    "paymentMethod": "PreAuthCreditCard",
                    "status": "Active",
                    "lastUpdated": "2023-10-01T12:00:00Z"
                }
            }

        payload = {}
        res = tools.pre_auth_payment_get_existing(payload).json()
        method = res.get("paymentMethod", "Regular")
        set_variable("payment_method", method)

        print("Business logic success: Pre-auth setup extracted.")
        return {"status": "success", "data": res}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Explain to the user that there was an error retrieving their payment details, and transition to the Failure_Handler by offering to send support links via SMS."}