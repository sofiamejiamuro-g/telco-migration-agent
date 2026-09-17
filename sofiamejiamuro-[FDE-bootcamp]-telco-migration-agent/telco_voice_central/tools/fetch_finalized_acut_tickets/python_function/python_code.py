def fetch_finalized_acut_tickets(lob: str = "", account_number: str = "") -> dict:
    '''Webhook Wrapper. Fetches finalized ACUT tickets based on LOB.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'webhook_success': True,
                'data': {
                    'ticket_summaries': [
                        {
                            'ticket_state_category': 'Finalized',
                            'acut_trouble_ticket_number': 'T987654321',
                            'ticket_creation_time': '2023-10-15T08:00:00Z',
                            'close_time': '2023-10-16T14:30:00Z',
                            'resolution_code': 'FIXED',
                            'dispatch_status': 'COMPLETED',
                            'lob': lob if lob else 'WIRELESS'
                        }
                    ]
                }
            }
        sanitized_lob = lob.lower().strip()
        sanitized_acc = account_number.strip()
        payload = {'lob': sanitized_lob, 'account_number': sanitized_acc}
        api_response = tools.ACUT_Finalized_Search_post_ACUT_Finalized_Search(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties retrieving historical tickets and offer to transfer them to a representative.'}