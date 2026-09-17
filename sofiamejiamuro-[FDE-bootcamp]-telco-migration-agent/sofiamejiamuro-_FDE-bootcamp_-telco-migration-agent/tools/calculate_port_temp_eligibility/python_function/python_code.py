def calculate_port_temp_eligibility() -> dict:
    '''State/Variable Manipulator. Evaluates porting temp number eligibility window.'''
    if get_variable('mock_mode'):
        set_variable('port_temp_eligible', True)
        return {'status': 'success', 'port_temp_eligible': True}

    import datetime
    try:
        eff_date_str = get_variable('date_formatted')
        port_temp_eligible = False
        if eff_date_str:
            eff_date = datetime.datetime.fromisoformat(eff_date_str.replace('Z', '+00:00'))
            time_diff = datetime.datetime.now(datetime.timezone.utc) - eff_date
            if time_diff.days <= 7:
                port_temp_eligible = True
        set_variable('port_temp_eligible', port_temp_eligible)
        print('Business logic success')
        return {'status': 'success', 'port_temp_eligible': port_temp_eligible}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Silently skip the port temporary number check and proceed to the next verification state.'}