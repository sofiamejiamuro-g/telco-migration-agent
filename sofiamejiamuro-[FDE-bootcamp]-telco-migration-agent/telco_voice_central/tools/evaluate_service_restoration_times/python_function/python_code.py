def evaluate_service_restoration_times() -> dict:
    '''State Manipulator. Parses billing_account_info_list array and sets service restoration boolean flags.'''
    if get_variable("mock_mode"):
        set_variable("boolean_flag", True)
        set_variable("contains_tv", False)
        return {"status": "success", "message": "Service variables evaluated successfully"}

    try:
        billing_info = get_variable("billing_account_info_list")
        if not isinstance(billing_info, list):
            billing_info = []

        contains_mobility = False
        contains_tv = False
        contains_internet = False

        for account in billing_info:
            if isinstance(account, dict):
                services = account.get("services", [])
                if isinstance(services, list):
                    for service in services:
                        if isinstance(service, dict):
                            service_type = str(service.get("service_type", "")).upper()
                            if "MOBILITY" in service_type:
                                contains_mobility = True
                            if "TV" in service_type:
                                contains_tv = True
                            if "INTERNET" in service_type:
                                contains_internet = True

        set_variable("boolean_flag", contains_mobility)
        set_variable("contains_tv", contains_tv)
        set_variable("boolean_flag", contains_internet)

        print("Business logic success")
        return {"status": "success", "message": "Service variables evaluated successfully"}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {
            "error": str(e),
            "agent_action": "Proceed with standard flow but apologize that specific restoration times cannot be calculated right now."
        }