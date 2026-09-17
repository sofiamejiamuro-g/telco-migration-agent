def evaluate_profile_and_extract_bans() -> dict:
    '''STATE MANIPULATOR: Reads customer_id_search_response natively from session. Performs array extractions and sets subset arrays.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print('Executing evaluate_profile_and_extract_bans in mock mode')

            mock_bans = ['1234567890']
            set_variable('billing_account_number_list', mock_bans)
            set_variable('smb_ban', '')
            set_variable('account_identifier', '5551234567')
            set_variable('n_billing_accounts', len(mock_bans))
            set_variable('is_business', False)

            return {
                'status': 'success',
                'ban_count': len(mock_bans),
                'message': 'Profile successfully evaluated. Single BAN isolated for happy path.',
                'data': 'mocked_extraction'
            }

        customer_response = get_variable('customer_id_search_response')
        if not customer_response:
            return {'status': 'error', 'message': 'No customer response found in session variables.'}

        if isinstance(customer_response, str):
            customer_response = json.loads(customer_response)

        accounts = customer_response.get('billing_accounts', [])
        ban_list = []
        for acc in accounts:
            ban = str(acc.get('billing_account_number', ''))
            if ban:
                ban_list.append(ban)

        set_variable('billing_account_number_list', ban_list)

        print('Business logic success: extracted multi-ban lists')
        return {'status': 'success', 'ban_count': len(ban_list)}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}