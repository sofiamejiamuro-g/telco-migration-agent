def check_existing_payment_method() -> dict:
    '''Calls the pre-auth-payment API to get the user's existing payment method.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('payment_method', 'Regular')
            set_variable('webhook_success', True)
            print('Business logic success - Mock Check Existing Payment Method')
            return {
                'status': 'success',
                'paymentMethod': 'Regular',
                'result': {
                    'paymentMethod': 'Regular',
                    'isActive': False,
                    'isEligibleForSetup': True,
                    'message': 'Customer is not currently set up for pre-authorized payments.'
                }
            }
        else:
            payload = {}
            api_response = tools.pre_auth_payment_get_existing(payload).json()
            payment_method = api_response.get('paymentMethod', 'Regular')

            set_variable('payment_method', payment_method)
            set_variable('webhook_success', True)
            print('Business logic success')
            return {'status': 'success', 'paymentMethod': payment_method}
    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'agent_action': 'Inform the customer that the system is having trouble. Ask if they would like an SMS sent to their device to sign up for pre-authorized payments in the MyBell App.'}