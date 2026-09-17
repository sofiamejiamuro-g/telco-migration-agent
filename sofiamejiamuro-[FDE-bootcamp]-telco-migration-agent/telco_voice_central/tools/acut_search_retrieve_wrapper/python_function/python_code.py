def acut_search_retrieve_wrapper() -> dict:
    '''Webhook Wrapper for ACUT search#retrieve.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('street_number', '123')
            set_variable('street_name', 'Main St')
            set_variable('sub_unit', 'Apt 4B')
            set_variable('webhook_success', True)
            print('Business logic success (mock)')
            return {
                'status': 'success',
                'data': 'Address and ticket details retrieved successfully in mock mode.',
                'result': {
                    'dispatch_status': 'SCHEDULED',
                    'tickets': [
                        {
                            'ticket_id': 'INC123456789',
                            'dispatch_status': 'SCHEDULED',
                            'status': 'OPEN',
                            'appointment_date': '2023-12-01',
                            'appointment_window': '08:00 - 12:00',
                            'eligible_for_cancel': True,
                            'eligible_for_reschedule': True
                        }
                    ]
                }
            }

        payload = {}
        api_response = tools.search_retrieve(payload).json()

        acut_context = api_response.get('acutContext', {})
        geo_address = acut_context.get('geographicAddress', {})
        urban_address = geo_address.get('urbanPropertyAddress', {})

        street_number = urban_address.get('streetNrFirst', '')
        street_name = urban_address.get('streetName', '')
        sub_unit = urban_address.get('subUnitNr', '')

        set_variable('street_number', str(street_number))
        set_variable('street_name', str(street_name))
        set_variable('sub_unit', str(sub_unit) if sub_unit else '')
        set_variable('webhook_success', True)

        print('Business logic success')
        return {'status': 'success', 'data': 'Address retrieved and session variables set successfully.'}
    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties retrieving their address and guide them next.'}