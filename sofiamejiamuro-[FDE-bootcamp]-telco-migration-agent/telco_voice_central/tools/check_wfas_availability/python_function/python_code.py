def check_wfas_availability(date_range_begin: str = '', date_range_end: str = '') -> dict:
    '''Webhook Wrapper. Queries the WFAS availability endpoint.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            mock_data = {
                'hasAvailableTimeslot': True,
                'earliestAvailableDate': '2024-05-20',
                'availability': [
                    {
                        'date': '2024-05-20',
                        'timeSlots': [
                            {'interval': 'Morning', 'startTime': '08:00:00', 'endTime': '12:00:00'},
                            {'interval': 'Afternoon', 'startTime': '12:00:00', 'endTime': '17:00:00'}
                        ]
                    },
                    {
                        'date': '2024-05-21',
                        'timeSlots': [
                            {'interval': 'Morning', 'startTime': '08:00:00', 'endTime': '12:00:00'},
                            {'interval': 'Evening', 'startTime': '17:00:00', 'endTime': '21:00:00'}
                        ]
                    }
                ]
            }
            set_variable('api_response', mock_data)
            print('Business logic success (mock mode)')
            return {'status': 'success', 'data': mock_data}

        payload = {'date_range_begin': str(date_range_begin), 'date_range_end': str(date_range_end)}
        api_response = tools.wfas_check_availability_wfas_check_availability(payload).json()
        set_variable('api_response', api_response)
        print('Business logic success')
        return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them.'}