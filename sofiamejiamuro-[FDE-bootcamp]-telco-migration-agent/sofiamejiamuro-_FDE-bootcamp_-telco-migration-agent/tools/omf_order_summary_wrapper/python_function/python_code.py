def omf_order_summary_wrapper(lob: str) -> dict:
    '''Searches OMF for order summaries based on LOB. Overrides separate summary blocks.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'result': {
                    'webhook_success': True,
                    'order_summaries': [
                        {
                            'orderIdentifier': 'ORD-98765-ABC',
                            'orderStatus': 'In Progress',
                            'orderDate': '2023-10-25T08:30:00Z',
                            'expectedCompletionDate': '2023-10-27T12:00:00Z',
                            'serviceAttributes': [
                                {
                                    'lineOfBusiness': lob,
                                    'serviceAction': 'INSTALL',
                                    'status': 'Scheduled'
                                }
                            ],
                            'appointmentDetails': {
                                'appointmentId': 'APT-12345',
                                'date': '2023-10-27',
                                'timeWindow': '08:00 - 12:00'
                            }
                        }
                    ]
                },
                'data': {
                    'order_summaries': [
                        {
                            'orderIdentifier': 'ORD-98765-ABC',
                            'orderStatus': 'In Progress',
                            'orderDate': '2023-10-25T08:30:00Z',
                            'expectedCompletionDate': '2023-10-27T12:00:00Z',
                            'serviceAttributes': [
                                {
                                    'lineOfBusiness': lob,
                                    'serviceAction': 'INSTALL',
                                    'status': 'Scheduled'
                                }
                            ],
                            'appointmentDetails': {
                                'appointmentId': 'APT-12345',
                                'date': '2023-10-27',
                                'timeWindow': '08:00 - 12:00'
                            }
                        }
                    ]
                }
            }

        payload = {'lob': lob.strip()}
        api_response = tools.order_summary(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer of a technical error.'}