def check_deai_eligibility(telephone_number: str) -> dict:
    '''Webhook Wrapper. Checks DEAI service for customer eligibility flags.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'data': {
                    'telephone_number': telephone_number,
                    'atl_privilege': 0,
                    'has_pending_order': False,
                    'partner_network_eligibility': 1,
                    'deai_eligibility_status': 'Eligible',
                    'account_standing': 'Good',
                    'fraud_check_passed': True,
                    'special_handling_required': False
                }
            }

        payload = {'telephone_number': telephone_number}
        result = tools.deai_customer_information(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Explain that we cannot verify pending orders right now and offer alternative assistance or an agent transfer.'}