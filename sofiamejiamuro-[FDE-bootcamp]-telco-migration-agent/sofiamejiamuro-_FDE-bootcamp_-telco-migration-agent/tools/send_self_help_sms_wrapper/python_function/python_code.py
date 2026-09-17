def send_self_help_sms_wrapper(telephone_number: str = "", message_text: str = "", brand: str = "", tag: str = "") -> dict:
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            print("Mock mode enabled for send_self_help_sms_wrapper")
            set_variable("webhook_success", True)
            return {
                "status": "success",
                "data": {
                    "message_id": "msg_9876543210_mock_id",
                    "delivery_status": "queued",
                    "telephone_number": telephone_number,
                    "brand": brand,
                    "tag": tag,
                    "timestamp": "2023-10-27T10:00:00Z",
                    "result": "SMS sent successfully via mock"
                }
            }

        payload = {"telephone_number": telephone_number, "message_text": message_text, "brand": brand, "tag": tag}
        api_response = tools.self_help_messaging_post_self_help_messaging(payload).json()
        print("Business logic success for self_help_messaging")
        set_variable("webhook_success", True)
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Politely inform the user that we are experiencing technical difficulties sending the SMS and provide the fallback web link verbally."}