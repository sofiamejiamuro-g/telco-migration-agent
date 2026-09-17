def update_tech_visit_context(route: str = "", lob: str = "") -> dict:
    '''State/Variable Manipulator. Explicitly sets the CX session variable 'route' to the provided value and updates the 'lob' session variable.'''
    if get_variable("mock_mode"):
        return {
            'status': 'success',
            'route': route.lower().strip().replace(' ', '_') if route else 'tech_connection_issue',
            'lob': lob.lower().strip() if lob else 'internet'
        }
    else:
        try:
            sanitized_route = route.lower().strip().replace(' ', '_') if route else 'tech_connection_issue'
            sanitized_lob = lob.lower().strip() if lob else get_variable('lob')
            set_variable('route', sanitized_route)
            if sanitized_lob:
                set_variable('lob', sanitized_lob)
            print('Business logic success')
            return {'status': 'success', 'route': sanitized_route, 'lob': sanitized_lob}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}