def extract_acut_ticket_details(acut_retrieve_response: dict) -> dict:
    '''State/Variable Manipulator. Parses session.params.acut_retrieve_response. Extracts 'dispatch_status', 'appointments.latestAppointment.appointmentStartDate/EndDate', 'primaryContact.number', and flattens them into top-level session parameters.'''
    if get_variable("mock_mode"):
        set_variable("dispatch_status", "OPEN")
        set_variable("target_date", "2024-11-20T17:00:00Z")
        set_variable("contact_number", "4165551234")
        return {
            "status": "success",
            "dispatch_status": "OPEN",
            "contact_number": "4165551234"
        }

    try:
        acut = acut_retrieve_response if isinstance(acut_retrieve_response, dict) else {}
        dispatch_status = acut.get("dispatch_status", "")
        appointments = acut.get("appointments", {}).get("latestAppointment", {})
        start_date = appointments.get("appointmentStartDate", "")
        end_date = appointments.get("appointmentEndDate", "")
        primary_contact = acut.get("primaryContact", {})
        contact_number = primary_contact.get("number", "")

        set_variable("dispatch_status", dispatch_status)
        set_variable("target_date", start_date)
        set_variable("target_date", end_date)
        set_variable("contact_number", contact_number)

        print("Successfully extracted ACUT ticket details.")
        return {"status": "success", "dispatch_status": dispatch_status, "contact_number": contact_number}
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the user that their ticket details could not be loaded and transfer them to a representative."}