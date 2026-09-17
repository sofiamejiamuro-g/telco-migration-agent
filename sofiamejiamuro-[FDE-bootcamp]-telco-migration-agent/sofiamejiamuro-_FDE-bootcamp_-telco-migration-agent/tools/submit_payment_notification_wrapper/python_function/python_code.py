def submit_payment_notification_wrapper(transaction_id: str = "", amount_paid: float = 0.0, payment_method: str = "") -> dict:
    '''Webhook Wrapper. Submits the payment notification order and re-fetches the past due amount.'''
    try:
        sanitized_method = payment_method.lower().strip().replace(' ', '_')

        if get_variable("mock_mode"):
            print("Mock mode: Returning dummy submission data.")
            return {
                "result": {
                    "status": "Success",
                    "webhook_success": True,
                    "confirmationNumber": "CONF12345678",
                    "past_due_amount": 0.0,
                    "amountPaid": amount_paid,
                    "payment_method": sanitized_method,
                    "transaction_id": transaction_id,
                    "message": "Payment notification order is created successfully."
                },
                "status": "Success",
                "webhook_success": True,
                "confirmationNumber": "CONF12345678",
                "past_due_amount": 0.0,
                "amountPaid": amount_paid
            }

        payload = {
            "transaction_id": transaction_id,
            "amount_paid": amount_paid,
            "payment_method": sanitized_method
        }
        api_response = tools.PaymentNotification_submitOrder(payload).json()
        print("Business logic success")
        return api_response
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {
            "error": str(e),
            "agent_action": "Inform the customer that we are experiencing technical difficulties and offer to send them an SMS with a link to the MyBell app to review their payment notification."
        }