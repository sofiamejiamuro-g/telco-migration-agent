def get_sms_link_for_intent(intent_route: str) -> dict:
    '''Webhook Wrapper. Retrieves a dynamic URL for SMS based on the current session route.'''
    try:
        mock_mode = get_variable('mock_mode')
        sanitized_route = str(intent_route).lower().strip()

        if mock_mode:
            print("Business logic success: Mock mode enabled for get_sms_link_for_intent")

            # Default to payment link
            mock_url = "https://m.bell.ca/ecmanagepayment"

            # Route matching based on BillingAndPaymentsAgent taskflow expectations
            if "autopay" in sanitized_route or "preauth" in sanitized_route:
                mock_url = "https://m.bell.ca/chatpreauthorizedbanke"
            elif "bill" in sanitized_route or "inquiry" in sanitized_route or "profile" in sanitized_route:
                mock_url = "https://m.bell.ca/ecviewmybill"
            elif "contract" in sanitized_route or "agreement" in sanitized_route:
                mock_url = "https://m.bell.ca/ecmyagreement"

            return {
                "status": "success",
                "url": mock_url,
                "intent_route": sanitized_route,
                "data": {
                    "mapped_url": mock_url,
                    "is_active": True
                }
            }

        payload = {"intent_route": sanitized_route}
        api_response = tools.intent_sdl_mapping_post_intent_sdl_mapping(payload).json()
        print("Business logic success")
        return {"status": "success", "data": api_response}

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the user that we cannot send the SMS right now and transfer them to an agent."}