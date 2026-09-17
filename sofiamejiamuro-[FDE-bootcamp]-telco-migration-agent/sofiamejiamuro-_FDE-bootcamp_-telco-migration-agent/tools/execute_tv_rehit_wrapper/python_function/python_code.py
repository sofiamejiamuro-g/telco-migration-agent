def execute_tv_rehit_wrapper() -> dict:
    '''Executes the TV rehit webhook. Determines real vs mock execution based on mock_mode state and updates webhook_success session variable based on outcome.'''
    if get_variable('mock_mode'):
        set_variable('webhook_success', True)
        print('Business logic success - Mock Mode')
        return {
            'status': 'success',
            'webhook_success': True,
            'message': 'TV rehit authorization signal sent successfully.',
            'details': {
                'estimated_restoration_time': 'Up to 2 hours',
                'instruction': 'Inform the customer that the signal has been sent, it may take up to 2 hours for channels to reappear, and ask if they need further assistance.'
            }
        }

    try:
        payload = {}
        api_response = tools.sat_rehit_post_sat_rehit(payload).json()

        # Safely determine success
        is_success = api_response.get('status', '') == 'success'
        set_variable('webhook_success', is_success)

        print('Business logic success')
        return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {
            'error': str(e),
            'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'
        }