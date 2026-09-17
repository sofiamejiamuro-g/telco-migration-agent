def clear_credit_card_parameters() -> dict:
    '''Automatically sets credit card parameters to None within the session variables.'''
    if get_variable("mock_mode"):
        return {'status': 'success', 'message': 'Credit card parameters cleared.'}

    try:
        set_variable('card_number', None)
        set_variable('cc_token', None)
        set_variable('expiry_date', None)
        set_variable('card_expiry_date', None)
        set_variable('expiry_year', None)
        set_variable('security_code', None)
        set_variable('cvv_number', None)
        set_variable('cc_from_utterance', None)

        print('Business logic success - Cleared CC parameters')
        return {'status': 'success', 'message': 'Credit card parameters cleared.'}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Continue with flow routing without referencing credit card details.'}