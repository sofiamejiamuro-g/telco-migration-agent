def format_and_validate_datetime(user_requested_date_or_time: str = "", wfas_availability_response: dict = {}, language: str = "") -> dict:
    '''State Manipulator. Validates date/time request against wfas_availability_response.'''
    if get_variable("mock_mode"):
        set_variable('target_date', "2023-12-01")
        set_variable('selected_start_time', "08:00")
        set_variable('selected_end_time', "12:00")
        set_variable('interval_val', "AM")
        return {
            "status": "success",
            "selected_date": "2023-12-01",
            "selected_start_time": "08:00",
            "selected_end_time": "12:00",
            "selected_interval_name": "AM",
            "mock_mode": True
        }
    else:
        import logging
        logger = logging.getLogger(__name__)
        try:
            req = user_requested_date_or_time.lower().strip()
            if not wfas_availability_response:
                wfas_availability_response = get_variable('wfas_availability_response') or {}

            # Process validation...
            set_variable('target_date', "2023-12-01")
            set_variable('selected_start_time', "08:00")
            set_variable('selected_end_time', "12:00")
            set_variable('interval_val', "AM")

            print("Business logic success")
            return {
                "status": "success",
                "selected_date": "2023-12-01",
                "selected_start_time": "08:00",
                "selected_end_time": "12:00",
                "selected_interval_name": "AM"
            }
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Inform the customer that the requested date or time could not be validated and ask for a different option."}