def fetch_account_balance_details_wrapper() -> dict:
    '''Webhook Wrapper for fetching account balance details.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('account_balance', 85.50)
            set_variable('last_payment_amount', 150.00)
            set_variable('last_payment_date', 'October 15, 2023')
            set_variable('webhook_success', True)
            print('Business logic success - Mock Mode')
            return {
                'status': 'success',
                'account_balance': 85.50,
                'last_payment_amount': 150.00,
                'last_payment_date': 'October 15, 2023'
            }

        payload = {}
        api_response = tools.get_account_balance_details_get(payload).json()

        details = api_response.get('balance_payment_details_response', {}).get('brs_postpaid_details', {})
        last_payment = details.get('last_payment_amount', 0.0)

        set_variable('last_payment_amount', last_payment)
        set_variable('webhook_success', True)
        print('Business logic success')
        return {'status': 'success', 'last_payment_amount': last_payment}

    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'agent_action': 'Politely inform the user that their account balance details could not be retrieved at this moment and transfer them to a representative.'}