def set_comcentric_routing(identified_brand: str, si_owner_code: str) -> dict:
    '''State/Variable Manipulator for setting comcentric routing target.'''
    if get_variable("mock_mode"):
        mock_brand = identified_brand.lower().strip().replace(' ', '_') if identified_brand else "bell_mobility"
        mock_queue = "COM1"
        set_variable('special_queue', mock_queue)
        set_variable('customer_data_val', mock_brand)
        return {
            'status': 'success',
            'special_queue': mock_queue
        }
    else:
        try:
            sanitized_brand = identified_brand.lower().strip().replace(' ', '_')
            sanitized_si_owner = si_owner_code.upper().strip()
            brand_mapping = {'COM1': 'COM1', 'COM2': 'COM2', 'COM3': 'COM3', 'COM4': 'COM4', 'COM5': 'COM5', 'COM6': 'COM6', 'COM7': 'COM7', 'COM9': 'COM9', 'COMA': 'COMA', 'COMB': 'COMB'}
            target_queue = brand_mapping.get(sanitized_si_owner, 'bell_aqd')
            set_variable('special_queue', target_queue)
            set_variable('customer_data_val', sanitized_brand)
            print('Business logic success')
            return {'status': 'success', 'special_queue': target_queue}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Acknowledge the routing error and proceed with standard live agent transfer.'}