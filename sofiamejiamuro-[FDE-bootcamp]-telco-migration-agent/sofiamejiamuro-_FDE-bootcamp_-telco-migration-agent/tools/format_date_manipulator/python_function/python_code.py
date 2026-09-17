def format_date_manipulator(raw_date_string: str = "") -> dict:
    '''State Manipulator for formatting the due date by stripping the timestamp.'''
    if get_variable("mock_mode"):
        mock_date = "2023-11-15"
        set_variable("date_formatted", mock_date)
        return {'status': 'success', 'dueDate': mock_date}

    try:
        if not raw_date_string:
            raw_date_string = get_variable('date_formatted')
            if not raw_date_string:
                raw_date_string = get_variable('date_formatted')
                if not raw_date_string:
                    raw_date_string = ""

        sanitized = str(raw_date_string).strip()
        if "T" in sanitized:
            formatted = sanitized.split("T")[0]
        else:
            formatted = sanitized

        set_variable('date_formatted', formatted)
        print('Business logic success')
        return {'status': 'success', 'dueDate': formatted}

    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Proceed without strict date formatting, using whatever date string is available.'}