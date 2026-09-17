def initialize_payment_notification_wrapper(billing_account: str = "", brand: str = "") -> dict:
    '''Webhook Wrapper. Calls BAN profile, Customer Profile, NPA NXX, eligibility criteria, and creates a payment notification order.'''
    if get_variable("mock_mode"):
        return {
            "result": {
                "status": "Success",
                "api_success": True,
                "account_balance": 150.75,
                "last_payment_date": "November 28, 2023",
                "last_payment_amount": 75.00,
                "due_date": "2023-12-15",
                "transaction_id": "TXN987654321",
                "past_due_amount": 50.25,
                "showNotifyLink": True,
                "showPaymentArrangementLink": True,
                "eligibility_status": "Eligible"
            },
            "account_balance": 150.75,
            "last_payment_date": "November 28, 2023",
            "last_payment_amount": 75.00
        }
    else:
        try:
            payload = {"billing_account": billing_account, "brand": brand}
            api_response = tools.PaymentNotification_initializeOrder(payload).json()
            print("Business logic success")
            return api_response
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {
                "error": str(e),
                "agent_action": "Inform the customer that we are experiencing technical difficulties and offer to send them an SMS with a link to the MyBell app to review their payment notification."
            }