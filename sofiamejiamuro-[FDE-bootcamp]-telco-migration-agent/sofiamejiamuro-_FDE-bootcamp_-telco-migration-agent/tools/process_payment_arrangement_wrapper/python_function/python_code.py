def process_payment_arrangement_wrapper(billing_account: str = "", amount: float = 0.0, payment_type: str = "", payment_method: str = "") -> dict:
    '''Webhook Wrapper. Bundles the sequence of updating the order and submitting it. Returns confirmationNumber and webhook_success.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            mock_conf_num = "BCA-PA-987654321"
            set_variable("confirmationNumber", mock_conf_num)
            set_variable("webhook_success", True)
            return {
                "status": "success",
                "confirmationNumber": mock_conf_num,
                "webhook_success": True,
                "mock_execution_details": {
                    "billing_account": billing_account or "109823746",
                    "amount_arranged": amount or 150.00,
                    "payment_type": payment_type or "Arrangement",
                    "payment_method": payment_method or "CreditCard",
                    "transaction_timestamp": "2023-10-25T14:32:01Z",
                    "message": "Payment arrangement processed successfully in mock mode."
                }
            }
        else:
            payload = {
                "billing_account": billing_account,
                "amount": amount,
                "payment_type": payment_type,
                "payment_method": payment_method
            }
            api_response = tools.payment_arrangement_bundled(payload).json()

            conf_num = str(api_response.get("confirmationNumber", ""))
            set_variable("confirmationNumber", conf_num)
            set_variable("webhook_success", True)

            print("Business logic success")
            return {"status": "success", "confirmationNumber": conf_num, "webhook_success": True}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Inform the user that system maintenance prevents setup and ask if it is alright to send an SMS link to complete it via MyBell."}