def process_cc_payment_wrapper(payment_amount: float = 0.0) -> dict:
    '''Webhook Wrapper: Evaluates the secure session CC token and submits the payment transaction.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'SUCCESS',
                'errorCodeID': '',
                'ConfirmationNo': 'MOCK-123456',
                'data': {
                    'transaction_status': 'APPROVED',
                    'confirmation_number': 'MOCK-123456',
                    'payment_amount': payment_amount,
                    'auth_code': 'AUTH12345',
                    'transaction_date': '2023-11-01T14:22:11Z',
                    'message': 'Payment processed successfully'
                }
            }

        payload = {'payment_amount': payment_amount}
        api_response = tools.submit_order_post_submit_order(payload).json()
        print('process_cc_payment_wrapper success')
        return {'status': 'SUCCESS', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'result': {'error': str(e)}, 'agent_action': 'Inform the user of the technical difficulty without using jargon, let them know no charges were applied if applicable, and route to feedback.'}