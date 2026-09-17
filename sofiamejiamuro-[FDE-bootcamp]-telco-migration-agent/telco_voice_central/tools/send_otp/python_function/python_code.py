def send_otp(callKey: str, telephone_number: str) -> dict:
    '''Webhook Wrapper to trigger the SMS.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'result': {
                    'status': 'SUCCESS',
                    'message': 'OTP successfully sent to the provided mobile number.',
                    'delivery_method': 'SMS',
                    'code_length': 6
                },
                'success': True
            }

        payload = {'callKey': callKey, 'telephone_number': telephone_number}
        api_response = tools.customer_authentication_send_otp(payload).json()
        print('Business logic success')
        return api_response
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that we could not send the OTP and transfer them to an agent.'}