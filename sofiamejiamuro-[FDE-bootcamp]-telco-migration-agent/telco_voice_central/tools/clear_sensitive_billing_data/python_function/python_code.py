def clear_sensitive_billing_data() -> dict:
    '''State Manipulator Tool. Hardcodes PCI data to None in the session context state.'''
    if get_variable("mock_mode"):
        return {
            'status': 'success',
            'message': 'Sensitive PCI data has been successfully purged.'
        }
    else:
        try:
            set_variable('credit_card_number', None)
            set_variable('cvv_number', None)
            set_variable('card_expiry_date', None)
            set_variable('card_number', None)
            set_variable('security_code', None)
            set_variable('expiry_year', None)
            set_variable('card_expiry_date', None)
            print('Sensitive billing data cleared.')
            return {'status': 'success', 'message': 'Sensitive PCI data has been successfully purged.'}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the user that a technical error occurred and the session will be closed immediately for security reasons.'}