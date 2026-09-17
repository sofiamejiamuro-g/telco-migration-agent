def fetch_clp_details() -> dict:
    '''Webhook Wrapper. Calls backend to retrieve Credit Limit Program (CLP) details. Extracts curSpendingLimitBal and sets state variables.'''
    if get_variable('mock_mode'):
        print('Mock mode enabled for fetch_clp_details')
        set_variable('clp_balance', 150.00)
        set_variable('clp_program', 200.00)
        set_variable('clp_aul_limit', 100.00)
        set_variable('special_status', 'bell_clp_aul')
        set_variable('is_prepaid', False)
        set_variable('webhook_success', True)
        return {
            'status': 'success',
            'clp_balance': 150.00,
            'clp_program': 200.00,
            'clp_aul_limit': 100.00,
            'special_status': 'bell_clp_aul',
            'is_prepaid': False,
            'webhook_success': True
        }

    try:
        payload = {}
        api_response = tools.get_clp_details_get_clp_details(payload).json()
        data = api_response

        balance = float(data.get('curSpendingLimitBal', 0.0))
        set_variable('clp_balance', balance)
        set_variable('is_prepaid', False)
        set_variable('webhook_success', True)
        print('Business logic success: fetched CLP details')
        return {'status': 'success', 'clp_balance': balance, 'webhook_success': True}
    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'webhook_success': False, 'agent_action': 'Inform the user that we are experiencing technical difficulties confirming the Credit Limit Balance and gracefully transition.'}