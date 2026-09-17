def extract_service_details(billing_account_info_list: list = [], lob: str = "", clid: str = "") -> dict:
    '''State/Variable Manipulator tool that implements complex JSONPath filtering and conditional logic to extract service IDs based on LOB and CLID, then routing to the appropriate agent.'''
    if get_variable("mock_mode"):
        set_variable("service_id", "SRV-987654321")
        set_variable("multiple_services", False)
        set_variable("is_home_phone", False)
        set_variable("hardstop", False)
        return {
            "service_id": "SRV-987654321",
            "multiple_services": False,
            "FTTH_home": True,
            "calling_from_landline": False,
            "hardstop": False,
            "target_agent": "bell_vr_consent"
        }

    try:
        multiple_services = False
        FTTH_home = False
        calling_from_landline = False
        hardstop = False
        service_id = ""
        target_agent = "bell_vr_consent"

        safe_lob = str(lob).strip().upper().replace(" ", "")
        safe_clid = str(clid).strip()

        payload_list = billing_account_info_list if isinstance(billing_account_info_list, list) else []
        account_details = payload_list[0] if payload_list else {}
        services = account_details.get("services", [])

        homephone_services = [s for s in services if str(s.get("service_type", "")).upper() in ["HOMEPHONE", "WIRELINE"]]
        tv_services = [s for s in services if str(s.get("service_type", "")).upper() == "TV"]
        internet_services = [s for s in services if str(s.get("service_type", "")).upper() == "INTERNET"]

        if safe_lob in ["HOMEPHONE", "WIRELINE"] and len(homephone_services) > 1:
            multiple_services = True
        elif safe_lob == "TV" and len(tv_services) > 1:
            multiple_services = True
        elif safe_lob == "INTERNET" and len(internet_services) > 1:
            multiple_services = True

        clid_matches = [s for s in homephone_services if str(s.get("service_id", "")) == safe_clid]
        if clid_matches:
            calling_from_landline = True
            if str(clid_matches[0].get("network_type", "")).upper() == "FTTH":
                FTTH_home = True

        hp_access = homephone_services[0].get("service_cfs", {}).get("access") if homephone_services else ""
        tv_access = tv_services[0].get("service_cfs", {}).get("access") if tv_services else ""

        int_hp_matches = [s.get("service_id", "") for s in internet_services if str(s.get("service_cfs", {}).get("access")) == str(hp_access) and hp_access]
        int_tv_matches = [s.get("service_id", "") for s in internet_services if str(s.get("service_cfs", {}).get("access")) == str(tv_access) and tv_access]
        hp_tv_matches = [s.get("service_id", "") for s in homephone_services if str(s.get("service_cfs", {}).get("access")) == str(tv_access) and tv_access]

        if safe_lob == "TV":
            if int_tv_matches:
                service_id = int_tv_matches[0]
            elif hp_tv_matches:
                service_id = hp_tv_matches[0]
            elif tv_services:
                service_id = tv_services[0].get("service_id", "")
            else:
                hardstop = True
                target_agent = "bell_aqd"
        elif safe_lob == "INTERNET":
            if internet_services:
                service_id = internet_services[0].get("service_id", "")
            else:
                hardstop = True
                target_agent = "bell_aqd"
        elif safe_lob in ["HOMEPHONE", "WIRELINE"]:
            if int_hp_matches:
                service_id = int_hp_matches[0]
            elif homephone_services:
                service_id = homephone_services[0].get("service_id", "")
            else:
                hardstop = True
                target_agent = "bell_aqd"
        else:
            hardstop = True
            target_agent = "bell_aqd"

        set_variable("service_id", service_id)
        set_variable("multiple_services", multiple_services)
        set_variable("is_home_phone", FTTH_home)
        set_variable("is_home_phone", calling_from_landline)
        set_variable("hardstop", hardstop)

        print("Business logic success: extract_service_details processed successfully.")

        return {
            "service_id": service_id,
            "multiple_services": multiple_services,
            "FTTH_home": FTTH_home,
            "calling_from_landline": calling_from_landline,
            "hardstop": hardstop,
            "target_agent": target_agent
        }
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {
            "error": str(e),
            "agent_action": "Apologize to the user and explain that there was an error processing the account details, then gracefully guide the conversation."
        }