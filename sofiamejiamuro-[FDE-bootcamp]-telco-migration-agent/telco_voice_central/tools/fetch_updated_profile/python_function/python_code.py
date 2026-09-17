def fetch_updated_profile(ban_type: str = '', ban_sub_type: str = '') -> dict:
    """Webhook Wrapper. Retrieves updated account balances."""
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'accountBalance': 125.50,
                'pastDueAmount': 0.0,
                'oneBillIndicator': 'Y',
                'accountType': ban_type if ban_type else 'I',
                'accountSubType': ban_sub_type if ban_sub_type else 'R'
            }

        payload = {'ban_type': ban_type, 'ban_sub_type': ban_sub_type}
        result = tools.fetch_profile_composite_fetch_updated_profile(payload).json()
        print('Business logic success')
        return {
            'accountBalance': result.get('accountBalance', 0.0),
            'pastDueAmount': result.get('pastDueAmount', 0.0),
            'oneBillIndicator': result.get('oneBillIndicator', '')
        }
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {
            'error': str(e),
            'status': 'system_unavailable',
            'agent_action': 'Politely apologize for the technical issue and ask if they would like an SMS with a link to the MyBell app.'
        }