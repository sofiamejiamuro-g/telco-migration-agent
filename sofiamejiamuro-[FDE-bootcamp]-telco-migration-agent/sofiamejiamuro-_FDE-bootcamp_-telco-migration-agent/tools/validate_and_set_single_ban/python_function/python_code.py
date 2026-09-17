def validate_and_set_single_ban(isolated_account_number: str) -> dict:
    '''STATE MANIPULATOR: Validates the narrowed down or user-provided account_number against customer_id_search_response.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print('Executing validate_and_set_single_ban in mock mode')
            sanitized_mock_ban = str(isolated_account_number).lower().strip().replace(' ', '') if isolated_account_number else '1234567890'
            set_variable('is_prepaid', False)
            set_variable('identification_status', 'Pass')
            set_variable('billing_account_info_list', {
                'billing_account_number': sanitized_mock_ban,
                'account_status': 'OPEN',
                'services': [{'is_prepaid': False, 'service_type': 'Mobility'}],
                'service_account_number': '5551234567'
            })
            set_variable('subscriber_number', '5551234567')
            return {
                'status': 'success',
                'message': 'BAN validated and variables set.'
            }

        sanitized_ban = str(isolated_account_number).lower().strip().replace(' ', '')
        customer_response = get_variable('customer_id_search_response')

        if not customer_response:
            return {'status': 'error', 'message': 'Missing customer data for validation.'}

        if isinstance(customer_response, str):
            customer_response = json.loads(customer_response)

        accounts = customer_response.get('billing_accounts', [])
        matched = False

        for acc in accounts:
            acc_num = str(acc.get('billing_account_number', '')).lower().strip()
            if acc_num == sanitized_ban:
                matched = True
                services = acc.get('services', [])
                is_prepaid = False
                if len(services) > 0:
                    is_prepaid = services[0].get('is_prepaid', False)

                set_variable('is_prepaid', is_prepaid)
                set_variable('identification_status', 'Pass')
                set_variable('billing_account_info_list', acc)
                set_variable('subscriber_number', acc.get('service_account_number', ''))
                break

        if matched:
            print('Business logic success: validated BAN')
            return {'status': 'success', 'message': 'BAN validated and variables set.'}
        else:
            print('Validation failed: BAN not found')
            set_variable('identification_status', 'Fail')
            return {'status': 'failed', 'message': 'The account number provided does not match our records.'}

    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}