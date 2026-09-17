def validate_pin(callKey: str, pin: str) -> dict:
    '''Webhook Wrapper for PIN validation.'''
    try:
        if get_variable('mock_mode'):
            return {
                'is_authenticated': True,
                'is_locked': False,
                'status': 'SUCCESS',
                'message': 'PIN successfully validated.',
                'auth_method_used': 'PIN',
                'attempts_remaining': 3
            }

        payload = {'callKey': callKey, 'pin': pin}
        api_response = tools.customer_authentication_validate_pin(payload).json()
        print('Business logic success')
        return api_response
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that PIN validation failed due to a system error and transfer them to an agent.'}