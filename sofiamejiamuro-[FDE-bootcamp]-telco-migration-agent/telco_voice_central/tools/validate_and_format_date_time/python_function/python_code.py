def validate_and_format_date_time(requested_date: str = '', requested_time_slot: str = '') -> dict:
    '''State Manipulator. Validates the requested date and time.'''
    if get_variable("mock_mode"):
        mock_date = str(requested_date).lower().strip() if requested_date else "2024-12-01"
        mock_slot = str(requested_time_slot).lower().strip() if requested_time_slot else "morning"
        set_variable('target_date', mock_date)
        set_variable('interval_val', mock_slot)
        return {
            'status': 'success',
            'is_valid': True,
            'mock_details': {
                'requested_date': mock_date,
                'requested_time_slot': mock_slot
            }
        }
    else:
        try:
            sanitized_date = str(requested_date).lower().strip()
            sanitized_slot = str(requested_time_slot).lower().strip()
            set_variable('target_date', sanitized_date)
            set_variable('interval_val', sanitized_slot)
            print('Business logic success')
            return {'status': 'success', 'is_valid': True}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them.'}