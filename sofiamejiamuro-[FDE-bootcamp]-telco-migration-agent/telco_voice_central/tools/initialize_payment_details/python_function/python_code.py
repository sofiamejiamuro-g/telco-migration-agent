def initialize_payment_details(billing_account_number: str) -> dict:
    '''Executes CLP details check and generates a one-time-payment order.'''
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("webhook_success", True)
            return {
                "spendingLimit": 500.0,
                "balances": {
                    "current": 150.75,
                    "past_due": 0.0,
                    "total_owing": 150.75,
                    "last_payment_amount": 75.00
                },
                "transaction_id": "ORD-987654321-MOCK",
                "webhook_success": True,
                "status": "SUCCESS",
                "eligibility": True,
                "message": "Payment initialization successful. Account is eligible for one-time payment."
            }

        payload = {"billing_account_number": billing_account_number}
        # Using placeholder display name and operation id due to no toolset mapped
        api_response = tools.PaymentAPI_createOrder(payload).json()

        set_variable("webhook_success", True)
        print("Business logic success")
        return {
            "spendingLimit": api_response.get("spendingLimit", 0.0),
            "balances": api_response.get("balances", {}),
            "transaction_id": api_response.get("transaction_id", ""),
            "webhook_success": True
        }
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {
            "error": str(e),
            "agent_action": "Politely explain that the payment system is temporarily unavailable and route to API_ERROR_HANDLING to offer an SMS payment link."
        }