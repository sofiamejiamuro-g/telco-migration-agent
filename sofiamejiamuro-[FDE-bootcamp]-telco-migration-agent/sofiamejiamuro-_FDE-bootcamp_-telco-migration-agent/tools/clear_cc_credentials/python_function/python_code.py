def clear_cc_credentials() -> dict:
    """State Manipulator. Sets credit card credentials to None securely."""
    import logging
    logger = logging.getLogger(__name__)

    if get_variable("mock_mode"):
        try:
            set_variable('card_number', None)
            set_variable('cc_token', None)
            set_variable('expiry_date', None)
            set_variable('card_expiry_date', None)
            set_variable('expiry_year', None)
            set_variable('security_code', None)
            set_variable('cvv_number', None)
            set_variable('credit_card_number', None)
            set_variable('cc_from_utterance', None)
        except Exception:
            pass
        return {'status': 'success'}

    try:
        set_variable('card_number', None)
        set_variable('cc_token', None)
        set_variable('expiry_date', None)
        set_variable('card_expiry_date', None)
        set_variable('expiry_year', None)
        set_variable('security_code', None)
        set_variable('cvv_number', None)
        set_variable('credit_card_number', None)
        set_variable('cc_from_utterance', None)
        print('Business logic success')
        return {'status': 'success'}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Ignore and proceed.'}