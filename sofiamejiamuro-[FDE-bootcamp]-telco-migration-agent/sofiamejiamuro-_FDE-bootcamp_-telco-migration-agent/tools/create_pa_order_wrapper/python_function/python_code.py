def create_pa_order_wrapper(billing_account_number: str, brand: str, menu_type: str) -> dict:
    '''Webhook Wrapper. Invokes the payment-arrangement#create-order endpoint to finalize the arrangement.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            print("Business logic success")
            return {
                "webhook_success": True,
                "pa_days": 14,
                "calculated_date_raw": "2024-11-15T23:59:59Z",
                "status": "APPROVED",
                "order_id": "PA-1049285093",
                "confirmation_code": "PA-SUCCESS-001"
            }

        payload = {"billing_account_number": billing_account_number.strip(), "brand": brand.strip(), "menu_type": menu_type.strip()}
        api_response = tools.payment_arrangement_create_order(payload).json()
        print("Business logic success")
        return {"webhook_success": True, "pa_days": api_response.get("paDays", 0), "calculated_date_raw": api_response.get("calculated_payment_date", "")}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the system is unable to proceed and offer to send a text message with a MyBell setup link to their device."}