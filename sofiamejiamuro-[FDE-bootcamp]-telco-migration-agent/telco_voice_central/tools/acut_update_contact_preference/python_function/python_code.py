def acut_update_contact_preference(ticket_number: str, contact_preference: str, contact_phone: str) -> dict:
    '''Webhook Wrapper. Updates the user's contact preference in ACUT.'''
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("webhook_success", True)
            print("Business logic success")
            return {
                "status": "success",
                "data": {
                    "updated": True,
                    "ticket_number": ticket_number,
                    "contact_preference": contact_preference,
                    "contact_phone": contact_phone,
                    "confirmation_code": "ACUT-UPD-993821",
                    "message": "Contact preferences successfully updated in ACUT."
                }
            }

        payload = {"ticket_number": ticket_number, "contact_preference": contact_preference, "contact_phone": contact_phone}
        result = tools.modify_contact_preferences_modify_contact_preferences(payload).json()
        set_variable("webhook_success", True)
        print("Business logic success")
        return {"status": "success", "data": result}
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Inform the user that we are experiencing technical difficulties and offer to transfer them to a representative."}