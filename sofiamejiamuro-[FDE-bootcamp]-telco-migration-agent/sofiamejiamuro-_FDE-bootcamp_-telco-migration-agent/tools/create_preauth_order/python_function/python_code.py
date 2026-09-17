def create_preauth_order() -> dict:
    '''Calls the API to create the pre-authorized payment order.
    Returns OrderFormId and success_flag.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('transaction_id', 'ORD-PREAUTH-987654321')
            return {
                'status': 'success',
                'result': {
                    'OrderFormId': 'ORD-PREAUTH-987654321',
                    'success_flag': True,
                    'message': 'Pre-authorized payment order created successfully.'
                }
            }
        else:
            payload = {}
            api_response = tools.PreAuth_create_order(payload).json()
            print('Business logic success')
            order_id = api_response.get('OrderFormId', 'UNKNOWN')
            set_variable('transaction_id', order_id)
            return {'status': 'success', 'result': {'OrderFormId': order_id, 'success_flag': True}}
    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'agent_action': 'Explain the technical error to the user and route to FAILURE_HUB.'}