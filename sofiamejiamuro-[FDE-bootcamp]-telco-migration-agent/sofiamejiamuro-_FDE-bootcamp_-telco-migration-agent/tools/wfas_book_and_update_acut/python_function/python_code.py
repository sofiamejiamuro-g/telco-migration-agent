def wfas_book_and_update_acut(selected_date: str, selected_start_time: str, selected_end_time: str, selected_interval_name: str, ticket_number: str) -> dict:
    '''Webhook Wrapper. Bundles booking the WFAS appointment and subsequently updating the ACUT ticket.'''
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("webhook_success", True)
            print("Business logic success")
            mock_payload = {
                "booking_confirmed": True,
                "wfas_confirmation_id": "WFAS-847291054",
                "acut_ticket_updated": True,
                "ticket_number": ticket_number,
                "appointment_details": {
                    "scheduled_date": selected_date,
                    "start_time": selected_start_time,
                    "end_time": selected_end_time,
                    "interval_name": selected_interval_name,
                    "dispatch_status": "SCHEDULED"
                },
                "message": "Appointment successfully booked in WFAS and ACUT ticket updated."
            }
            return {"status": "success", "data": mock_payload, "result": mock_payload}

        payload = {"selected_date": selected_date, "selected_start_time": selected_start_time, "selected_end_time": selected_end_time, "selected_interval_name": selected_interval_name, "ticket_number": ticket_number}
        result = tools.appointment_and_modify_appointment_and_modify(payload).json()
        set_variable("webhook_success", True)
        print("Business logic success")
        return {"status": "success", "data": result}
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Inform the user that their appointment could not be booked due to a system error."}