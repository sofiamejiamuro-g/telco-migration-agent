def get_ban_profile_wrapper(billing_account: str = "", ibm_application_id: str = "") -> dict:
    '''Webhook Wrapper. Calls the API to fetch customer profile details, updates pastDueAmount and currentBalance.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("pastDueAmount", 0.0)
            set_variable("currentBalance", 125.50)
            set_variable("account_balance", 125.50)
            set_variable("last_payment_amount", 75.00)
            set_variable("last_payment_date", "October 12th")
            set_variable("webhook_success", True)
            return {
                "status": "success",
                "pastDueAmount": 0.0,
                "currentBalance": 125.50,
                "account_balance": 125.50,
                "last_payment_amount": 75.00,
                "last_payment_date": "October 12th",
                "webhook_success": True,
                "billing_account": billing_account or "123456789",
                "ibm_application_id": ibm_application_id,
                "customer_status": "ACTIVE",
                "special_status": "regular"
            }

        payload = {
            "billing_account": billing_account,
            "ibm_application_id": ibm_application_id
        }
        api_response = tools.nm1_get_ban_profile(payload).json()

        past_due = float(api_response.get("pastDueAmount", 0.0))
        current_bal = float(api_response.get("currentBalance", 0.0))

        set_variable("pastDueAmount", past_due)
        set_variable("currentBalance", current_bal)
        set_variable("webhook_success", True)

        print("Business logic success")
        return {"status": "success", "pastDueAmount": past_due, "currentBalance": current_bal, "webhook_success": True}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Inform the user that system maintenance prevents setup and ask if it is alright to send an SMS link to complete it via MyBell."}