def validate_otp(callKey: str, otp: str) -> dict:
    '''Webhook Wrapper to validate the 6-digit OTP.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'is_authenticated': True,
                'auth_status': 'Success',
                'message': 'OTP validated successfully.',
                'status_code': 200
            }

        payload = {'callKey': callKey, 'otp': otp}
        api_response = tools.customer_authentication_validate_otp(payload).json()
        print('Business logic success')
        return api_response
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that validation failed due to a system error and transfer them to an agent.'}