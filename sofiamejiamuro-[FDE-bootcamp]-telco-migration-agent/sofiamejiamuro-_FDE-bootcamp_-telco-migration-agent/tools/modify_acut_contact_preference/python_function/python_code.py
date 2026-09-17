def modify_acut_contact_preference(ticket_number: str = "", contact_phone: str = "", contact_preference: str = "") -> dict:
    '''Webhook Wrapper. Updates the contact preferences in ACUT.'''
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print("Business logic success")
            return {
                "success": True,
                "data": {
                    "ticket_number": ticket_number if ticket_number else "INC123456789",
                    "contact_phone": contact_phone if contact_phone else "416-555-1234",
                    "contact_preference": contact_preference if contact_preference else "SMS",
                    "status": "SUCCESS",
                    "message": "Contact preferences successfully updated in ACUT.",
                    "webhook_success": True
                }
            }

        t_num = ticket_number.strip()
        c_phone = contact_phone.strip()
        c_pref = contact_preference.strip()
        payload = {"ticket_number": t_num, "contact_phone": c_phone, "contact_preference": c_pref}

        result = tools.modify_modify(payload).json()
        print("Business logic success")
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties updating their preferences and offer to transfer them to a representative."}