def extract_and_format_tickets(raw_omf_response: dict, raw_acut_response: dict, language: str = "") -> dict:
    '''State Manipulator to extract ticket counts, state, and format dates, setting them in session state variables.'''
    if get_variable("mock_mode"):
        set_variable('count_entities', 1)
        set_variable('n_acut_tickets', 1)
        set_variable('order_identifier', 'OMF-99887766')
        set_variable('ticket_number1', 'INC-11223344')
        set_variable('ticket_state', 'SCHEDULED')
        set_variable('date_formatted', '2024-05-20T14:30:00Z')
        print('Business logic success: Tickets formatted. (MOCK)')
        return {'status': 'success', 'data': {'n_omf_tickets': 1, 'n_acut_tickets': 1}}

    try:
        if not isinstance(raw_omf_response, dict):
            raw_omf_response = {}
        if not isinstance(raw_acut_response, dict):
            raw_acut_response = {}

        omf_tickets = raw_omf_response.get('order_summaries', [])
        acut_tickets = raw_acut_response.get('ticket_summaries', [])

        n_omf = len(omf_tickets) if isinstance(omf_tickets, list) else 0
        n_acut = len(acut_tickets) if isinstance(acut_tickets, list) else 0

        set_variable('count_entities', n_omf)
        set_variable('n_acut_tickets', n_acut)

        if n_omf > 0:
            set_variable('order_identifier', omf_tickets[0].get('orderIdentifier', ''))
            if n_omf > 1:
                set_variable('order_identifier2', omf_tickets[1].get('orderIdentifier', ''))

        if n_acut > 0:
            set_variable('ticket_number1', acut_tickets[0].get('acut_trouble_ticket_number', ''))
            set_variable('ticket_state', acut_tickets[0].get('ticket_state_category', ''))
            set_variable('date_formatted', acut_tickets[0].get('ticket_creation_time', ''))
            if n_acut > 1:
                set_variable('ticket_number2', acut_tickets[1].get('acut_trouble_ticket_number', ''))
                set_variable('ticket_state', acut_tickets[1].get('ticket_state_category', ''))
                set_variable('date_formatted', acut_tickets[1].get('ticket_creation_time', ''))

        print('Business logic success: Tickets formatted.')
        return {'status': 'success', 'data': {'n_omf_tickets': n_omf, 'n_acut_tickets': n_acut}}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Proceed with default intent determination as ticket parsing failed.'}