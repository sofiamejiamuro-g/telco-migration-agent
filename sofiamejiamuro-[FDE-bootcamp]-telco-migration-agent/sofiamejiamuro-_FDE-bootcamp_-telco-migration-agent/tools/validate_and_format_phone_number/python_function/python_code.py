def validate_and_format_phone_number(raw_phone_number: str = "") -> dict:
    '''State Manipulator. Takes a raw spoken phone number string. Strips non-numeric characters, strips a leading 1 if the length is 11, and checks if the resulting string is exactly 10 digits and not a repeating sequence. Sets Contact_Number and Contact_Number_flag variables.'''
    if get_variable("mock_mode"):
        set_variable('phone_number_val', '4165551234')
        set_variable('boolean_flag', True)
        return {
            "status": "success",
            "is_valid": True,
            "formatted_number": "4165551234"
        }

    try:
        sanitized_input = str(raw_phone_number).strip()
        clean_num = ''.join(filter(str.isdigit, sanitized_input))
        if len(clean_num) == 11 and clean_num.startswith('1'):
            clean_num = clean_num[1:]
        invalid_sequences = [str(i)*10 for i in range(10)]
        is_valid = len(clean_num) == 10 and clean_num not in invalid_sequences

        set_variable('phone_number_val', clean_num if is_valid else '')
        set_variable('boolean_flag', is_valid)

        print("validate_and_format_phone_number success")
        return {"status": "success", "is_valid": is_valid, "formatted_number": clean_num if is_valid else ""}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the user that we are experiencing technical difficulties validating the number and ask them to repeat it."}