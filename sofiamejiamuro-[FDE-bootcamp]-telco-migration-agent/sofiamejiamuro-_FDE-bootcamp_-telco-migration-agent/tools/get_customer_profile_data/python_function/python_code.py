def get_customer_profile_data(billing_account_number: str = "", telephone_number: str = "") -> dict:
    '''Fetches escalation, collections, and building info.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print("Business logic success - mock mode")
            return {
                "status": "success",
                "data": {
                    "escalation_risk_flg": "0",
                    "preferred_building_internet_flg": "1",
                    "colAgencyContactNo": "",
                    "collections_status": "in_good_standing",
                    "building_type": "residential_mdu",
                    "account_status": "active",
                    "billing_account_number": billing_account_number or "293847561",
                    "telephone_number": telephone_number or "4165551234"
                }
            }

        payload = {"billing_account_number": billing_account_number, "telephone_number": telephone_number}
        api_response = tools.nm11_get_auto_col_agncy_info(payload).json()
        print("Business logic success - profile data fetched")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}