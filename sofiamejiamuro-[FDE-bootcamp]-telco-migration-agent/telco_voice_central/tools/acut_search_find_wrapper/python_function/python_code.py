def acut_search_find_wrapper(lob: str, service_id: str) -> dict:
    '''Searches ACUT for tickets based on service ID. Overrides separate search blocks.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'ticket_summaries': [
                    {
                        'acut_trouble_ticket_number': 'TT-192837465',
                        'ticket_state_category': 'Active',
                        'ticket_status': 'In Progress',
                        'ticket_creation_time': '2023-10-24T10:00:00Z',
                        'service_id': service_id,
                        'lob': lob
                    }
                ],
                'data': {
                    'total_records': 1,
                    'tickets': [
                        {
                            'acut_trouble_ticket_number': 'TT-192837465',
                            'ticket_state_category': 'Active',
                            'ticket_status': 'In Progress',
                            'ticket_creation_time': '2023-10-24T10:00:00Z',
                            'estimated_resolution_time': '2023-10-25T14:30:00Z',
                            'service_id': service_id,
                            'lob': lob,
                            'issue_description': 'Intermittent connectivity issues reported by diagnostic tool.'
                        }
                    ]
                }
            }
        else:
            payload = {'lob': lob.strip(), 'service_id': service_id.strip()}
            api_response = tools.search_find(payload).json()
            print('Business logic success')
            return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer of a technical error.'}