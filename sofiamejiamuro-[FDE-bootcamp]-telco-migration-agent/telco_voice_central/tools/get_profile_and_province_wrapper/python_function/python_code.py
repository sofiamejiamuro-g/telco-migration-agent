def get_profile_and_province_wrapper(billing_account_number: str) -> dict:
    '''Webhook Wrapper. Bundles legacy calls to ban-profile, customer-profile, and npa-nxx-lookup. Evaluates 'accountType', 'accountSubType', and 'oneBillIndicator' to compute rules.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        sanitized_ban = billing_account_number.strip()

        if mock_mode:
            print("Business logic success - Mock Mode")
            return {
                "profile_not_found": False,
                "is_valid_account": True,
                "handoff_to_ivr": False,
                "api_success": True
            }
        else:
            payload = {"billing_account_number": sanitized_ban}
            ban_res = tools.nm1_get_ban_profile(payload).json()
            npa_res = tools.npa_nxx_lookup(payload).json()

            profile_not_found = (ban_res.get("returnCode") == 0)
            acc_type = ban_res.get("accountType", "")
            acc_sub = ban_res.get("accountSubType", "")
            one_bill = ban_res.get("oneBillIndicator", "")
            prov = npa_res.get("province", "")

            is_valid_account = False
            if (acc_type == "I" and acc_sub in ["R", "P", "N", "B", "5", "E"]) or (acc_type == "C" and acc_sub in ["P", "V", "T"]):
                is_valid_account = True

            handoff_to_ivr = False
            if one_bill == "M" or (one_bill == "Y" and prov in ["PE", "NS", "NL", "NB"]):
                handoff_to_ivr = True

            print("Business logic success")
            return {
                "profile_not_found": profile_not_found,
                "is_valid_account": is_valid_account,
                "handoff_to_ivr": handoff_to_ivr
            }
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the system is unable to proceed and offer to send a text message with a MyBell setup link to their device."}