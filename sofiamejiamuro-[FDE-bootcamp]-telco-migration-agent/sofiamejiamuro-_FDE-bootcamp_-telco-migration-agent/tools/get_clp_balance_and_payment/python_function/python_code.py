def get_clp_balance_and_payment(billing_account: str = '') -> dict:
    '''Webhook Wrapper. Fetches consolidated balance, limits, and last payment details.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        sanitized_account = str(billing_account).strip()

        if mock_mode:
            return {
                'webhook_success': True,
                'special_status': 'bell_clp_aul',
                'clp_program': '500.00',
                'clp_aul_limit': '450.00',
                'clp_balance': '475.50',
                'account_balance': '475.50',
                'last_payment_amount': '75.00',
                'last_payment_date': 'October 15th',
                'spendingLimit': '500.00'
            }

        payload = {'billing_account': sanitized_account}
        api_response = tools.get_account_balance_details_get_clp_balance_and_payment(payload).json()
        print('Business logic success: fetched clp and balance data')
        return api_response
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that balance details could not be retrieved and offer an SMS fallback link to the MyBell app.'}