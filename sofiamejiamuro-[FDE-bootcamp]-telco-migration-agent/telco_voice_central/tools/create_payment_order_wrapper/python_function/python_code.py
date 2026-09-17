def create_payment_order_wrapper(billing_account_number: str = "") -> dict:
    '''Webhook Wrapper tool. Creates a one-time payment transaction order.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                "result": {
                    "status": "success",
                    "webhook_success": True,
                    "order_id": "MOCK_ORDER_12345",
                    "payment_status": "APPROVED",
                    "confirmation_number": "C-987654321"
                },
                "status": "success",
                "data": {
                    "order_id": "MOCK_ORDER_12345",
                    "payment_status": "APPROVED",
                    "confirmation_number": "C-987654321",
                    "billing_account_number": billing_account_number
                }
            }

        payload = {"billing_account_number": billing_account_number}
        api_response = tools.create_order_create_payment_order(payload).json()
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the system is unable to process the credit card payment at this time. Offer to send a text message to make a payment in the MyBell app."}