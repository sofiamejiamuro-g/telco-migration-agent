def lookup_province_wrapper(phone_number: str = "") -> dict:
    '''Webhook Wrapper. Calls npa-nxx-lookup to return the province based on phone.'''
    import json
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            set_variable("Province", "ON")
            print("Business logic success: Mock Mode province lookup.")
            return {
                "status": "success",
                "data": {
                    "province": "ON",
                    "city": "Toronto",
                    "npa": "416",
                    "nxx": "555",
                    "country": "CA",
                    "timezone": "America/Toronto"
                }
            }

        target_number = (phone_number or str(get_variable("CIRN") or "") or str(get_variable("clid") or "")).strip()
        if not target_number:
            print("No valid phone number provided for province lookup.")
            return {"status": "failed", "reason": "Missing phone number"}

        npa = target_number[:3] if len(target_number) >= 3 else ""
        nxx = target_number[3:6] if len(target_number) >= 6 else ""
        payload = {"npa": npa, "nxx": nxx}

        res = tools.npa_nxx_lookup_npa_nxx_lookup(payload).json()
        prov = res.get("province", "")
        if prov:
            set_variable("Province", prov)

        print("Business logic success: Province looked up.")
        return {"status": "success", "data": res}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Acknowledge the system issue and offer to send an SMS with support links, guiding them to the Failure_Handler route."}