def select_calendar_interval(day: str = "", calendar_identifier: str = "", interval: str = "", estimated_start_time: str = "") -> dict:
    """Webhook Wrapper for selected-interval API."""
    import json
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            print("Mock mode active for select_calendar_interval")
            mock_selections_obj = {
                "day": day.strip() if day else "2023-10-25",
                "calendarIdentifier": calendar_identifier.strip() if calendar_identifier else "CAL-987654321",
                "interval": interval.strip() if interval else "08:00:00-12:00:00",
                "estimatedStartTime": estimated_start_time.strip() if estimated_start_time else "08:30:00"
            }
            set_variable("interval_val", [mock_selections_obj])
            return {
                "status": "success",
                "data": "Interval selected and formatted into session state successfully.",
                "result": {
                    "omf_selections": mock_selections_obj,
                    "webhook_success": True
                }
            }

        payload = {
            "day": day.strip(),
            "calendarIdentifier": calendar_identifier.strip(),
            "interval": interval.strip(),
            "estimatedStartTime": estimated_start_time.strip()
        }
        api_response = tools.omf_calendar_selected_interval_api_post_omf_calendar_selected_interval_api(payload).json()

        omf_selections_obj = api_response.get("omf_selections", {})
        set_variable("interval_val", [omf_selections_obj])

        print("Business logic success - Interval selected")
        return {"status": "success", "data": "Interval selected and formatted into session state successfully."}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties saving their selection and offer to transfer them to a representative."}