def evaluate_propensity_to_sell() -> dict:
    '''Evaluates sales propensity by calling the DEAI endpoint and checking for cross-sell flags.'''
    try:
        mock_mode = get_variable('mock_mode')
        cirn = get_variable('CIRN')

        if mock_mode:
            set_variable('serve_to_check', 'Fail')
            print("Business logic success")
            return {
                "status": "success",
                "data": {
                    "sales_propensity_bell_internet_cross_sell_flg": 1,
                    "sales_propensity_bell_tv_cross_sell_flg": 0,
                    "sales_propensity_bell_mobility_cross_sell_flg": 1,
                    "sales_propensity_bell_smart_home_cross_sell_flg": 0,
                    "customer_tier": "Premium",
                    "churn_risk": "Low",
                    "eligible_for_upgrade": True,
                    "propensity_score": 0.85,
                    "recommended_action": "cross_sell_internet"
                }
            }
        else:
            payload = {"telephone_number": cirn}
            api_response = tools.deai_customer_information(payload).json()

            set_variable('serve_to_check', 'Fail')

            print("Business logic success")
            return {"status": "success", "data": api_response}

    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable('serve_to_check', 'Fail')
        return {"error": str(e), "agent_action": "Inform the user there was a technical error and gracefully end the session."}