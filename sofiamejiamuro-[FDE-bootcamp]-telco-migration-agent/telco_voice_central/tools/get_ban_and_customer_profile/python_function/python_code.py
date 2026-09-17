def get_ban_and_customer_profile(billing_account: str = '') -> dict:
    '''Webhook Wrapper. Bundles Ban Profile and Customer Profile lookups.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        sanitized_account = str(billing_account).strip()

        if mock_mode:
            return {
                'result': {
                    'accountBalance': '150.00',
                    'accountType': 'I',
                    'accountSubType': 'R',
                    'pastDueAmount': '0.00',
                    'oneBillIndicator': 'N',
                    'status': 'Pass',
                    'webhook_success': True
                },
                'accountBalance': '150.00',
                'accountType': 'I',
                'accountSubType': 'R',
                'pastDueAmount': '0.00',
                'oneBillIndicator': 'N',
                'status': 'Pass',
                'webhook_success': True
            }

        payload = {'billing_account': sanitized_account}
        api_response = tools.nm1_get_get_ban_and_customer_profile(payload).json()
        print('Business logic success: fetched ban and customer profile')
        return api_response
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that we cannot fetch their profile right now and offer to send an SMS link to the MyBell app.'}