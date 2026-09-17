def check_customer_payment_eligibility_wrapper(billing_account_number: str = "", phone_number: str = "") -> dict:
    '''Webhook Wrapper tool. Bundles customer profile, BAN profile, province lookup, and payment eligibility into a single execution to return eligibility and account attributes.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('eligInd', 'Y')
            set_variable('accountType', 'I')
            set_variable('province', 'ON')
            return {
                "status": "success",
                "eligInd": "Y",
                "accountType": "I",
                "province": "ON",
                "api_success": True,
                "customer_profile": {
                    "firstName": "John",
                    "lastName": "Doe"
                },
                "ban_profile": {
                    "ban": billing_account_number if billing_account_number else "234567891",
                    "status": "Open",
                    "accountType": "I"
                },
                "data": {
                    "eligInd": "Y",
                    "reasonCode": "0",
                    "message": "Customer is eligible for payment"
                },
                "result": {
                    "eligInd": "Y",
                    "accountType": "I"
                }
            }

        payload = {
            "billing_account_number": billing_account_number,
            "phone_number": phone_number
        }
        api_response = tools.Multiple_check_customer_payment_eligibility(payload).json()
        print("Business logic success")
        elig_ind = api_response.get("eligInd", "N")
        set_variable('eligInd', elig_ind)
        return {"status": "success", "eligInd": elig_ind, "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the system is unable to process the credit card payment at this time. Offer to send a text message to make a payment in the MyBell app."}