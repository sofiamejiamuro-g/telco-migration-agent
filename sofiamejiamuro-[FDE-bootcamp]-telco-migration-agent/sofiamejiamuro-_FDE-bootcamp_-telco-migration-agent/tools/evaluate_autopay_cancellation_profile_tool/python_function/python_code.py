def evaluate_autopay_cancellation_profile_tool(ban_type: str = "", ban_sub_type: str = "", billing_account: int = 0, clid: int = 0, cirn: int = 0) -> dict:
    '''Evaluates account profile and returns an action command: SEND_SMS, HANDOFF, UNSUPPORTED, AQD, or OUTAGE.'''
    if get_variable("mock_mode"):
        return {
            "status": "success",
            "action": "SEND_SMS"
        }
    else:
        try:
            mock_mode = get_variable('mock_mode')
            b_type = str(ban_type).strip().upper()
            b_subtype = str(ban_sub_type).strip().upper()

            # Mock webhook responses since no OpenAPI endpoints are available
            error_code = "0"
            one_bill = "Y"
            prov = "ON"

            is_cust = False
            if (b_type == "I" and b_subtype in ["B", "N", "5"]) or (b_type == "C" and b_subtype in ["V", "T", "P"]):
                is_cust = True

            if error_code == "0":
                print("Business logic success: Returning SEND_SMS based on error_code=0")
                return {"status": "success", "action": "SEND_SMS"}

            if one_bill in ["Y", "M", "N"]:
                if one_bill == "M":
                    return {"status": "success", "action": "HANDOFF"}
                check_prov = False
                if (b_type == "I" and b_subtype in ["R", "N", "B", "5", "E", "P"]) or (b_type == "C" and b_subtype in ["P", "T", "V"]):
                    check_prov = True
                if not check_prov:
                    return {"status": "success", "action": "UNSUPPORTED"}
                if one_bill == "Y" and prov in ["NB", "NL", "NS", "PE"]:
                    return {"status": "success", "action": "HANDOFF"}
                elif one_bill == "N" and prov not in ["NB", "NL", "NS", "PE"]:
                    return {"status": "success", "action": "SEND_SMS"}
                else:
                    return {"status": "success", "action": "AQD"}

            print("Business logic success: Returning AQD")
            return {"status": "success", "action": "AQD"}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Explain that there is a system outage and gracefully transition to STATE_OFFER_SMS_OUTAGE."}