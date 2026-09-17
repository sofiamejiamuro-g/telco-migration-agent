def validate_expiry_date_in_future(raw_expiry_input: str) -> dict:
    '''State Manipulator. Validates if expiry date is in the future.'''
    if get_variable("mock_mode"):
        set_variable('card_expiry_date', '12')
        set_variable('expiry_year', '35')
        print("Mock mode enabled: Expiry date validation bypassed")
        return {"status": "success", "expiry_month": "12", "expiry_year": "35"}

    import re
    from datetime import datetime
    try:
        sanitized_date = re.sub(r'\D', '', str(raw_expiry_input))
        if len(sanitized_date) != 4:
            return {"error": "Invalid length.", "agent_action": "Ask the user to provide the expiry date as a 4-digit number (MMYY)."}
        month_str = sanitized_date[:2]
        year_str = sanitized_date[2:]
        month = int(month_str)
        year = int(year_str)
        if not (1 <= month <= 12):
            return {"error": "Invalid month.", "agent_action": "Ask the user to provide a valid month for the expiry date."}
        now = datetime.now()
        current_month = now.month
        current_year = int(str(now.year)[-2:])
        if year < current_year or (year == current_year and month < current_month):
            return {"error": "Expiry date in the past.", "agent_action": "Inform the user that the expiry date cannot be in the past and ask for a valid date."}
        set_variable('card_expiry_date', month_str)
        set_variable('expiry_year', year_str)
        print("Business logic success: Expiry date validation successful")
        return {"status": "success", "expiry_month": month_str, "expiry_year": year_str}
    except Exception as e:
        return {"error": str(e), "agent_action": "Politely ask the user to repeat their expiry date."}