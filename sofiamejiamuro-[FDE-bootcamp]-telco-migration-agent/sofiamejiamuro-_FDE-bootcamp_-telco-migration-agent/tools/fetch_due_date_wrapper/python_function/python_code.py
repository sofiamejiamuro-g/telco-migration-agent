def fetch_due_date_wrapper() -> dict:
    '''Webhook Wrapper for fetching the user due date using the create-order endpoint.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('date_formatted', '2024-11-30T00:00:00Z')
            set_variable('webhook_success', True)
            print('Business logic success - Mock Mode')
            return {
                'status': 'success',
                'dueDateFull': '2024-11-30T00:00:00Z',
                'result': {
                    'status': 'success',
                    'dueDateFull': '2024-11-30T00:00:00Z'
                }
            }
        else:
            payload = {}
            api_response = tools.one_time_payment_create_order_post(payload).json()

            bill = api_response.get('start_one_time_pmt_response', {}).get('accountBill', {})
            due_date_full = bill.get('dueDate', '')

            set_variable('date_formatted', due_date_full)
            set_variable('webhook_success', True)
            print('Business logic success')
            return {'status': 'success', 'dueDateFull': due_date_full}

    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'agent_action': 'Silently acknowledge the error internally and rely on the conversational callbacks to route to the self-serve SMS.'}