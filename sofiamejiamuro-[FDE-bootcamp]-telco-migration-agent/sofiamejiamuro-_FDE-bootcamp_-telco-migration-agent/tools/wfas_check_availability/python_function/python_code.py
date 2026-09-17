def wfas_check_availability(date_range_begin: str, date_range_end: str, brand: str) -> dict:
    '''Webhook Wrapper. Checks availability for appointments.'''
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            mock_data = {
                "hasAvailableTimeslot": True,
                "earliest_date": date_range_begin if date_range_begin else "2023-11-25",
                "earliest_interval": "Morning",
                "earliest_slot": "08:00 AM",
                "available_dates": [
                    {
                        "date": date_range_begin if date_range_begin else "2023-11-25",
                        "intervals": [
                            {"name": "Morning", "start": "08:00", "end": "12:00"},
                            {"name": "Afternoon", "start": "12:00", "end": "17:00"}
                        ]
                    },
                    {
                        "date": date_range_end if date_range_end else "2023-11-26",
                        "intervals": [
                            {"name": "Morning", "start": "08:00", "end": "12:00"},
                            {"name": "Evening", "start": "17:00", "end": "21:00"}
                        ]
                    }
                ]
            }
            set_variable("availability_details", mock_data)
            print("Business logic success")
            return {"status": "success", "data": mock_data}

        payload = {"date_range_begin": date_range_begin, "date_range_end": date_range_end, "brand": brand}
        result = tools.availability_availability(payload).json()
        set_variable("availability_details", result)
        print("Business logic success")
        return {"status": "success", "data": result}
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the scheduling system is currently unavailable and transfer to an agent."}