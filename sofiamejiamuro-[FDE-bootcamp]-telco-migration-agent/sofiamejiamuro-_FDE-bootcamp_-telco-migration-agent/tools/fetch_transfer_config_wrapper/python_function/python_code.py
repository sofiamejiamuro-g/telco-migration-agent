def fetch_transfer_config_wrapper(domain: str = "", onebillindicator: str = "") -> dict:
    """Retrieves the DEFAULT_MENU_ID and department config for consolidated billing or regional routing."""
    import json
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('menu_id', 'DEFAULT_100')
            return {
                'status': 'success',
                'menu_id': 'DEFAULT_100',
                'department_id': '7020',
                'message': 'Mock mode enabled. Config retrieved successfully.'
            }

        sanitized_indicator = onebillindicator.strip().upper()
        menu_id = 'DEFAULT_100'
        if sanitized_indicator == 'Y':
            menu_id = 'CONS_BILL_ATL'
        elif sanitized_indicator == 'M':
            menu_id = 'CONS_BILL_MTS'

        set_variable('menu_id', menu_id)
        print("Business logic success - Config retrieved")
        return {'status': 'success', 'menu_id': menu_id}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {'error': str(e), 'agent_action': 'Politely inform the user that the configuration failed and default routing will be used.'}