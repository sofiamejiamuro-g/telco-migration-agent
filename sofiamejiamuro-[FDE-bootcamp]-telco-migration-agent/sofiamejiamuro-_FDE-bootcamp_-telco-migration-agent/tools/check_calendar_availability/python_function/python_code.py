def check_calendar_availability(start_date_utc: str = "", end_date_utc: str = "", billing_account_number: str = "") -> dict:
    """Webhook Wrapper for calendar availability API."""
    import json
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            print("Mock mode active for check_calendar_availability")
            set_variable("boolean_flag", True)
            set_variable("count_entities", 2)
            return {
                "status": "success",
                "data": {
                    "consistent_calendars": True,
                    "installationDetailList": {
                        "installationDetail": [
                            {
                                "date": "2024-11-20",
                                "availableIntervals": [
                                    {
                                        "intervalName": "Morning",
                                        "startTime": "08:00:00",
                                        "endTime": "12:00:00"
                                    },
                                    {
                                        "intervalName": "Afternoon",
                                        "startTime": "12:00:00",
                                        "endTime": "17:00:00"
                                    }
                                ],
                                "status": "AVAILABLE"
                            },
                            {
                                "date": "2024-11-21",
                                "availableIntervals": [
                                    {
                                        "intervalName": "Morning",
                                        "startTime": "08:00:00",
                                        "endTime": "12:00:00"
                                    }
                                ],
                                "status": "AVAILABLE"
                            }
                        ]
                    },
                    "message": "Availability checked successfully."
                }
            }

        payload = {
            "startDate": start_date_utc.strip(),
            "endDate": end_date_utc.strip(),
            "accountNumber": billing_account_number.strip(),
            "intervals": ["AllDay"]
        }
        api_response = tools.calendar_availability_api_post_calendar_availability_api(payload).json()

        consistent = api_response.get("consistent_calendars", False)
        set_variable("boolean_flag", consistent)

        details = api_response.get("installationDetailList", {}).get("installationDetail", [])
        set_variable("count_entities", len(details))

        print("Business logic success - Calendar availability verified")
        return {"status": "success", "data": "Availability checked and session variables updated securely."}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the customer that we are experiencing technical difficulties checking the calendar and seamlessly offer to transfer them to a representative."}