def extract_mobility_services(billing_account_info_list: list = []) -> dict:
    '''State/Variable Manipulator. Takes raw billing_account_info_list array, checks if MOBILITY exists in services, sets contains_mobility variable.'''
    if get_variable("mock_mode"):
        set_variable("boolean_flag", "Mobility")
        return {"status": "success", "contains_mobility": "Mobility"}

    import json
    try:
        contains_mobility = "None"
        if billing_account_info_list and isinstance(billing_account_info_list, list):
            for item in billing_account_info_list:
                if not isinstance(item, dict):
                    continue
                services = item.get("services", [])
                if isinstance(services, list):
                    for srv in services:
                        if not isinstance(srv, dict):
                            continue
                        srv_type = str(srv.get("service_type", "")).strip().upper()
                        if srv_type == "MOBILITY":
                            contains_mobility = "Mobility"
                            break
                if contains_mobility == "Mobility":
                    break

        set_variable("boolean_flag", contains_mobility)
        print("Business logic success")
        return {"status": "success", "contains_mobility": contains_mobility}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("boolean_flag", "None")
        return {"error": str(e), "agent_action": "Proceed with default non-mobility flow logic."}