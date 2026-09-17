def validate_phone_in_account(customer_id_search_response: str = "", phone_number: str = "") -> dict:
    import json

    if get_variable("mock_mode"):
        print("Mock mode enabled: Simulating successful phone validation in account.")
        set_variable("is_in_account", True)
        return {
            "status": "success",
            "is_in_account": True
        }

    try:
        sanitized_phone = str(phone_number).replace("-", "").replace(" ", "").replace("(", "").replace(")", "").strip()
        data = json.loads(customer_id_search_response) if customer_id_search_response else []
        is_in_account = False
        if isinstance(data, list):
            for item in data:
                users = item.get("users", [])
                if isinstance(users, list):
                    for user in users:
                        contact = str(user.get("contact_number", ""))
                        if contact and contact.replace("-", "").replace(" ", "").strip() == sanitized_phone:
                            is_in_account = True
                            break
        print(f"Business logic success. is_in_account resolved to: {is_in_account}")
        set_variable("is_in_account", is_in_account)
        return {"status": "success", "is_in_account": is_in_account}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("is_in_account", False)
        return {"error": str(e), "agent_action": "Acknowledge the technical issue seamlessly and gently prompt the user to verbally confirm their 10-digit phone number."}