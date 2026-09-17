def evaluate_phone_number_match(spoken_number: str = "") -> dict:
    '''Evaluates if the spoken number matches OTP eligible numbers or CIRN.'''
    if get_variable("mock_mode"):
        set_variable('boolean_flag', True)
        print("Business logic success")
        return {"status": "success", "is_match": True}

    try:
        sanitized = spoken_number.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if len(sanitized) == 11 and sanitized.startswith('1'):
            sanitized = sanitized[1:]

        otp_list = get_variable('otp_number_list')
        if not isinstance(otp_list, list):
            otp_list = []

        cirn = str(get_variable('CIRN') or "").strip()
        is_match = (sanitized == cirn) or (sanitized in otp_list)

        set_variable('boolean_flag', is_match)
        print("Business logic success")
        return {"status": "success", "is_match": is_match}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the phone number could not be validated due to a technical error."}