def update_acut_contact(contact_preference: str = '') -> dict:
    '''Webhook Wrapper. Calls the ACUT modify endpoint to update the user contact preferences.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print('Executing update_acut_contact in MOCK MODE')
            return {
                'status': 'success',
                'webhook_success': True,
                'result': {
                    'update_status': 'CONFIRMED',
                    'ticket_id': 'ACUT987654321',
                    'contact_preference': contact_preference if contact_preference else '555-019-8372',
                    'message': 'Contact preference successfully updated in ACUT.'
                }
            }

        payload = {'contact_preference': str(contact_preference)}
        api_response = tools.modify_modify(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them.'}