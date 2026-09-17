def format_phone_number_manipulator(raw_number: str = "") -> dict:
    """
    State Manipulator. Extracts exactly 10 digits from incoming CLID/TFN variables.
    Sets session variables for clid and tfn.
    """
    if get_variable("mock_mode"):
        return {
            "status": "success",
            "formatted_number": "4165551234",
            "tfn": "8005559999",
            "clid": "4165551234"
        }

    try:
        def extract_ten_digits(num_str: str) -> str:
            if not num_str:
                return ""
            sanitized = str(num_str).strip().replace("+", "").replace("-", "").replace(" ", "")
            if len(sanitized) > 10:
                return sanitized[-10:]
            return sanitized

        current_tfn = get_variable("phone_number_val")
        current_clid = get_variable("clid")

        new_tfn = extract_ten_digits(current_tfn)
        new_clid = extract_ten_digits(current_clid)
        new_raw = extract_ten_digits(raw_number)

        if new_tfn:
            set_variable("phone_number_val", new_tfn)
        if new_clid:
            set_variable("clid", new_clid)

        print("Business logic success")
        return {
            "status": "success",
            "formatted_number": new_raw,
            "tfn": new_tfn,
            "clid": new_clid
        }
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {
            "error": str(e),
            "agent_action": "Inform the user that there was an error processing the phone number and ask them to repeat it."
        }