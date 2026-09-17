def check_payment_arrangement_eligibility(billing_account_number: str) -> dict:
    '''Webhook Wrapper. Checks payment arrangement eligibility for a BAN.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'data': {
                    'eligible': True,
                    'showPaymentArrangementLink': True,
                    'due_amount': 145.50,
                    'past_due_balance': 145.50
                },
                'result': {
                    'eligible': True,
                    'due_amount': 145.50,
                    '__cxas_system_directives__': [
                        {
                            'action': 'add_override',
                            'parameters': {
                                'due_amount': '145.50'
                            }
                        }
                    ]
                }
            }
        else:
            payload = {'billing_account_number': billing_account_number}
            result = tools.payment_arrangement_get_eligibility_criteria(payload).json()
            print('Business logic success')
            return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties validating payment arrangements and offer an agent transfer.'}