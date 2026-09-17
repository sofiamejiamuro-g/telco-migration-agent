def set_event_type_variable(event_type_value: str = '') -> dict:
    '''Sets the event_type session variable when a user requests a full or partial start over.'''
    if get_variable("mock_mode"):
        safe_val = event_type_value.strip().lower() if event_type_value else 'full start over'
        return {'status': 'success', 'event_type_set': safe_val}

    try:
        safe_val = event_type_value.strip().lower()
        set_variable('routing_val', safe_val)
        print(f'event_type set to {safe_val}')
        return {'status': 'success', 'event_type_set': safe_val}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and proceed with the standard flow.'}