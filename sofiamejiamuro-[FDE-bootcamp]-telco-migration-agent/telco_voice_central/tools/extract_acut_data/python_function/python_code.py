def extract_acut_data(acut_retrieve_response: dict = {}) -> dict:
    '''State Manipulator. Parses acut_retrieve_response to extract contact info and dates.'''
    if get_variable("mock_mode"):
        set_variable('contact_number', '4165551234')
        return {
            "status": "success",
            "primaryContact": {
                "number": "4165551234",
                "type": "MOBILE"
            }
        }

    import logging
    logger = logging.getLogger(__name__)
    try:
        if not isinstance(acut_retrieve_response, dict):
            acut_retrieve_response = {}
        primary_contact = acut_retrieve_response.get('primaryContact', {})
        contact_number = primary_contact.get('number', '')
        contact_type = primary_contact.get('type', '')

        set_variable('contact_number', contact_number)
        set_variable('contact_number', contact_type)

        print("Business logic success: ACUT data extracted")
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties parsing their ticket details and offer to transfer them to a representative."}