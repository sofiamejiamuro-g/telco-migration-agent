def initialize_auth_session(billing_account: str, calling_number: str) -> dict:
    '''Webhook Wrapper. Initializes auth session and retrieves customer profile.'''
    import json

    mock_mode = get_variable('mock_mode')
    if mock_mode:
        return {
            'result': {
                'session_id': 'auth-session-mock-12345',
                'callKey': 'mock-call-key-123',
                'pin_available': True,
                'otp_tns': ['4165551234', '4165559876'],
                'postal_code_available': True,
                'is_business': False,
                'status': 'SUCCESS'
            },
            'callKey': 'mock-call-key-123',
            'pin_available': True,
            'otp_tns': ['4165551234', '4165559876']
        }

    try:
        payload = {'billing_account': billing_account, 'calling_number': calling_number}
        api_response = tools.customer_authentication_start_auth_session(payload).json()
        print('Business logic success')
        return api_response
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that the authentication system is currently unavailable and offer to transfer them to an agent.'}