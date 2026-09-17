def submit_cc_payment_details(card_number: str, expiry_month: str, expiry_year: str, cvv_number: str) -> dict:
    '''Webhook Wrapper. Submits the collected credit card details for authorization.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print("Business logic success: Mock mode enabled for submit_cc_payment_details")
            set_variable('cc_token', 'MOCK_TOKEN_12345')
            return {
                "status": "success",
                "isValid": True,
                "errorCodeID": "",
                "data": {
                    "isValid": True,
                    "token": "MOCK_TOKEN_12345",
                    "responseCode": "00",
                    "responseMessage": "Approved",
                    "transactionId": "MOCK_TXN_987654321"
                }
            }

        payload = {
            "cardNumber": str(card_number),
            "expiryMonth": str(expiry_month),
            "expiryYear": str(expiry_year),
            "securityCode": str(cvv_number)
        }
        api_response = tools.cc_payment_details_post_cc_payment_details(payload).json()
        if api_response.get("isValid"):
            set_variable('cc_token', api_response.get("token", "TOKEN_GENERATED"))
        print("Business logic success")
        return {"status": "success", "data": api_response}
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer the SMS alternative."}