def process_dts_token_wrapper(card_number: str) -> dict:
    '''Webhook Wrapper for DTS tokenization. Calls backend or uses mock_mode.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print('Executing mock mode for DTS tokenization.')
            return {
                'webhook_success': True,
                'cc_token': 'dts_tkn_mock_9876543210123456',
                'data': {
                    'token': 'dts_tkn_mock_9876543210123456',
                    'status': 'SUCCESS',
                    'message': 'Tokenization successful',
                    'card_brand': 'VISA',
                    'expiration_date': '12/29'
                }
            }

        payload = {'card_number': card_number}
        api_response = tools.ugyt_dss_dts_get_dts_token_details(payload).json()
        print('Business logic success')
        return {'webhook_success': True, 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'webhook_success': False, 'error': str(e), 'agent_action': 'Inform the user that the system is having trouble completing the next step. Offer to send a text message to their device to proceed with the payment in the My Account App.'}