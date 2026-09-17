def increment_retry_counter() -> dict:
    '''State/Variable Manipulator. Increments the no_match_counter session variable by 1.'''
    if get_variable('mock_mode'):
        return {'status': 'success', 'new_counter': 1}
    try:
        mock_mode = get_variable('mock_mode')
        current = get_variable('no_match_counter')
        if current is None or current == '':
            current = 0
        else:
            current = int(current)
        new_counter = current + 1
        set_variable('no_match_counter', new_counter)
        print(f'Counter incremented to {new_counter}')
        return {'status': 'success', 'new_counter': new_counter}
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and gracefully end the session.'}