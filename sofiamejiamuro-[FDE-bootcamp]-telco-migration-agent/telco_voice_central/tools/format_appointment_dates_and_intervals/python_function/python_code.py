def format_appointment_dates_and_intervals(raw_user_date: str, raw_user_time_slot: str) -> dict:
    '''State/Variable Manipulator. Validates user dates against range, flattens intervals, mutates session states.'''
    if get_variable("mock_mode"):
        mock_date = "2023-10-25"
        mock_slot = "afternoon"
        set_variable("target_date", mock_date)
        set_variable("selected_start_time", mock_slot)
        return {
            "status": "success",
            "formatted_date": mock_date,
            "formatted_slot": mock_slot
        }
    else:
        try:
            sanitized_date = raw_user_date.lower().strip() if raw_user_date else ""
            sanitized_slot = raw_user_time_slot.lower().strip().replace(' ', '_') if raw_user_time_slot else ""

            set_variable("target_date", sanitized_date)
            set_variable("selected_start_time", sanitized_slot)

            print("Successfully formatted dates and intervals.")
            return {"status": "success", "formatted_date": sanitized_date, "formatted_slot": sanitized_slot}
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Inform the user that the date or time slot could not be processed and ask them to repeat it clearly."}