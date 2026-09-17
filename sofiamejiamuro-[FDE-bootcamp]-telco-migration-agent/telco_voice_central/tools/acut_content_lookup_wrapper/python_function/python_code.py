def acut_content_lookup_wrapper(lookup_type: str = "", code: str = "", sub_code: str = "") -> dict:
    '''Webhook Wrapper. Bundles multiple legacy content lookups to retrieve formatted messaging.'''
    if get_variable("mock_mode"):
        sanitized_type = lookup_type.lower().strip() if lookup_type else ""
        print(f"Executing acut_content_lookup_wrapper mock for {sanitized_type}")
        messages = {
            "acut-trouble-types": {
                "trouble_type_message": "You reported a connection issue.",
                "code": code
            },
            "dispatch-task": {
                "dispatch_task_status_message": "A technician is on the way.",
                "status": "ENROUTE"
            },
            "main-task": {
                "main_task_status_message": "The main task is in progress.",
                "status": "SCHEDULED"
            },
            "disposition-code": {
                "disposition_code_message": "The issue has been resolved.",
                "code": code
            }
        }
        return {
            "status": "success",
            "webhook_success": True,
            "data": messages.get(sanitized_type, {
                "message": "Details not found.",
                "trouble_type_message": "Service issue",
                "status": "OPEN"
            })
        }
    else:
        try:
            sanitized_type = lookup_type.lower().strip()
            payload = {"lookup_type": lookup_type, "code": code, "sub_code": sub_code}
            api_response = tools.AcutContent_lookup_wrapper(payload).json()
            print("Business logic success: Content retrieved.")
            return {"status": "success", "data": api_response}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties looking up their task details and offer to transfer them to a representative."}