def fetch_account_profile_wrapper(ban_type: str = "", ban_sub_type: str = "") -> dict:
    '''Webhook Wrapper. Bundles nm1_get#customer-profile and nm1_get#ban-profile logic.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("customer_data_val", "I")
            set_variable("banSubType", "B")
            set_variable("onebillindicator", "N")
            set_variable("error_code", "0")
            print("Business logic success: Mock Mode nm1_get account profile.")
            return {
                "status": "success",
                "data": {
                    "banType": "I",
                    "accountType": "I",
                    "banSubType": "B",
                    "accountSubType": "B",
                    "oneBill": "N",
                    "oneBillIndicator": "N",
                    "returnCode": "0",
                    "accountStatus": "OPEN",
                    "firstName": "John",
                    "lastName": "Doe",
                    "province": "ON",
                    "language": "EN"
                }
            }

        b_type = (ban_type or get_variable("customer_data_val") or "").upper().strip()
        b_sub = (ban_sub_type or get_variable("banSubType") or "").upper().strip()
        payload = {"banType": b_type, "banSubType": b_sub}

        is_customer = False
        if b_type == "I" and b_sub in ["B", "N", "5"]:
            is_customer = True
        if b_type == "C" and b_sub in ["V", "T", "P"]:
            is_customer = True

        if is_customer:
            res = tools.nm1_get_customer_profile(payload).json()
        else:
            res = tools.nm1_get_ban_profile(payload).json()

        set_variable("customer_data_val", res.get("banType", res.get("accountType", "I")))
        set_variable("banSubType", res.get("banSubType", res.get("accountSubType", "B")))
        set_variable("onebillindicator", res.get("oneBill", res.get("oneBillIndicator", "N")))
        set_variable("error_code", res.get("returnCode", "0"))

        print("Business logic success: Account profile fetched and parsed.")
        return {"status": "success", "data": res}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to send an SMS with support links. Transition conversational state to Failure_Handler."}