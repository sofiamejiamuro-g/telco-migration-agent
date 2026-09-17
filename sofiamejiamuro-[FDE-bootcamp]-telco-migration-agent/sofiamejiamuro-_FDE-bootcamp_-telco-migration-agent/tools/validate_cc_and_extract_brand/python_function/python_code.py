def validate_cc_and_extract_brand(raw_card_input: str) -> dict:
    '''State Manipulator. Validates credit card number length and extracts brand.'''
    if get_variable("mock_mode"):
        set_variable('card_number', '4111222233334444')
        set_variable('card_brand', 'Visa')
        return {
            "status": "success",
            "card_brand": "Visa",
            "card_number_length": 16
        }
    else:
        import re
        try:
            sanitized_cc = re.sub(r'\D', '', str(raw_card_input))
            if not sanitized_cc:
                return {"error": "No valid digits found in input.", "agent_action": "Politely ask the user to provide their credit card number again."}
            length = len(sanitized_cc)
            if length not in [15, 16]:
                return {"error": "Invalid length.", "agent_action": "Inform the user that the card number seems invalid (must be 15 or 16 digits) and ask them to try again."}
            brand = "Unknown"
            if sanitized_cc.startswith('4') and length == 16:
                brand = "Visa"
            elif (51 <= int(sanitized_cc[:2]) <= 55 or 2221 <= int(sanitized_cc[:4]) <= 2720) and length == 16:
                brand = "MasterCard"
            elif sanitized_cc[:2] in ['34', '37'] and length == 15:
                brand = "Amex"
            else:
                return {"error": "Unsupported or unrecognized card brand.", "agent_action": "Inform the user that the card brand is not recognized (we accept Visa, MasterCard, Amex) and ask them to try again."}
            set_variable('card_number', sanitized_cc)
            set_variable('card_brand', brand)
            print("Business logic success: CC validation and brand extraction successful")
            return {"status": "success", "card_brand": brand, "card_number_length": length}
        except Exception as e:
            return {"error": str(e), "agent_action": "Politely ask the user to repeat their credit card number."}