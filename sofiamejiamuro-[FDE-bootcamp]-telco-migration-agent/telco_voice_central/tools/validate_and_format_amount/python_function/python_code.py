def validate_and_format_amount(raw_amount_input: str) -> dict:
    '''Validates payment amount is between $1 and $10,000 and updates amount_paid.'''
    if get_variable("mock_mode"):
        import re
        sanitized = re.sub(r'[^\d\.]', '', str(raw_amount_input))
        mock_amount = round(float(sanitized), 2) if sanitized else 150.00
        mock_amount = mock_amount if 1.0 <= mock_amount <= 10000.0 else 150.00
        set_variable("payment_amount", mock_amount)
        return {"is_valid": True, "formatted_amount": mock_amount}

    import re
    try:
        sanitized = re.sub(r'[^\d\.]', '', str(raw_amount_input))
        if not sanitized:
            bad_amount = get_variable("cc_invalid_counter")
            bad_amount = int(bad_amount) if bad_amount else 0
            set_variable("cc_invalid_counter", bad_amount + 1)
            return {"is_valid": False, "reason": "No numeric amount found"}

        amount = float(sanitized)
        amount = round(amount, 2)

        if 1.0 <= amount <= 10000.0:
            set_variable("payment_amount", amount)
            print("Business logic success")
            return {"is_valid": True, "formatted_amount": amount}
        else:
            bad_amount = get_variable("cc_invalid_counter")
            bad_amount = int(bad_amount) if bad_amount else 0
            set_variable("cc_invalid_counter", bad_amount + 1)
            return {"is_valid": False, "reason": "Amount must be between 1 and 10000"}
    except Exception as e:
        logger.error(f"Crash: {e}")
        bad_amount = get_variable("cc_invalid_counter")
        bad_amount = int(bad_amount) if bad_amount else 0
        set_variable("cc_invalid_counter", bad_amount + 1)
        return {
            "error": str(e),
            "agent_action": "Inform the user the amount was not understood and politely ask them to repeat it."
        }