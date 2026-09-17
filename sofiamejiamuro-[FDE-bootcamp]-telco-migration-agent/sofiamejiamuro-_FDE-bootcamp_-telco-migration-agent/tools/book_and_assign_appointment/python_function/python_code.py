def book_and_assign_appointment(ticket_number: str = "", selected_date: str = "", selected_start_time: str = "", selected_end_time: str = "", selected_interval_name: str = "") -> dict:
    '''Webhook Wrapper. Executes WFAS reservation, ACUT Modification, and Assignment.'''
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print("Business logic success - Mock Mode")
            return {
                "success": True,
                "data": {
                    "ticket_number": ticket_number or "INC12345678",
                    "reservation_id": "RES-987654321",
                    "appointment_status": "ASSIGNED",
                    "confirmation_code": "CONF-85739",
                    "selected_date": selected_date or "2023-11-15",
                    "selected_start_time": selected_start_time or "08:00:00",
                    "selected_end_time": selected_end_time or "12:00:00",
                    "selected_interval_name": selected_interval_name or "AM",
                    "wfas_update": "Success",
                    "acut_update": "Success",
                    "message": "Appointment successfully booked and assigned in WFAS and ACUT.",
                    "webhook_success": True
                }
            }

        payload = {
            "ticket_number": ticket_number.strip(),
            "selected_date": selected_date.strip(),
            "selected_start_time": selected_start_time.strip(),
            "selected_end_time": selected_end_time.strip(),
            "selected_interval_name": selected_interval_name.strip()
        }

        result = tools.orchestrated_book_and_assign_orchestrated_book_and_assign(payload).json()
        print("Business logic success")
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties booking the appointment and offer to transfer them to a representative."}