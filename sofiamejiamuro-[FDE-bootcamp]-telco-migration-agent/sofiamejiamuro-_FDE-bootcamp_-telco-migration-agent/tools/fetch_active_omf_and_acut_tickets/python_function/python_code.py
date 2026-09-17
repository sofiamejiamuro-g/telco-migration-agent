def fetch_active_omf_and_acut_tickets(lob: str = "", account_number: str = "") -> dict:
    '''Webhook Wrapper. Bundles the DFCX order summary and active ticket searches.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'webhook_success': True,
                'data': {
                    'order_summaries': [],
                    'ticket_summaries': [
                        {
                            'ticket_state_category': 'Active',
                            'acut_trouble_ticket_number': 'T987654321',
                            'ticket_creation_time': '2023-11-01T08:30:00Z',
                            'dispatch_status': 'SCHEDULED',
                            'appointment_date': '2023-11-15',
                            'appointment_time_slot': '08:00 AM - 12:00 PM',
                            'contact_number': '555-123-4567',
                            'lob': lob if lob else 'internet'
                        }
                    ]
                }
            }

        sanitized_lob = lob.lower().strip()
        sanitized_acc = account_number.strip()
        payload = {'lob': sanitized_lob, 'account_number': sanitized_acc}
        api_response = tools.OMF_and_ACUT_Active_Search_Combined_post_OMF_and_ACUT_Active_Search_Combined(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties retrieving active tickets and offer to transfer them to a representative.'}