def format_and_validate_identifier(raw_identifier: str = "") -> dict:
    if get_variable("mock_mode"):
        return {
            "formatted_identifier": "4165551234",
            "identifier_type": "CIRN"
        }
    else:
        try:
            print("Formatting raw identifier")
            sanitized_id = str(raw_identifier).strip()
            clean_id = "".join(filter(str.isdigit, sanitized_id))
            id_length = len(clean_id)
            id_type = "INVALID"
            if id_length == 10:
                id_type = "CIRN"
            elif id_length == 9:
                id_type = "BAN"
            return {"formatted_identifier": clean_id, "identifier_type": id_type}
        except Exception as e:
            print(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Apologize and politely ask the user to provide their 10-digit phone number or 9-digit account number again."}