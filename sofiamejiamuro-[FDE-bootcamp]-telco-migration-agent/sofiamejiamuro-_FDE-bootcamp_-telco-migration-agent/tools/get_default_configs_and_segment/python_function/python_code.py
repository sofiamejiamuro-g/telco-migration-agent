def get_default_configs_and_segment(menu_type: str = "", brand: str = "", route: str = "") -> dict:
    '''Fetches dialogflow config and aqd segment info.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print("Business logic success - mock mode")
            return {
                "status": "success",
                "data": {
                    "domain": "Consumer",
                    "DEFAULT_MENU_ID": "100",
                    "DEFAULT_DEPARTMENT_ID": "2005",
                    "segment": "Care",
                    "menu_type": menu_type if menu_type else "inbound_main",
                    "brand": brand if brand else "Bell",
                    "route": route if route else "default_routing",
                    "is_business_hours": True,
                    "supported_languages": ["en", "fr"]
                }
            }

        payload = {"menu_type": menu_type, "brand": brand, "route": route}
        api_response = tools.get_configs_for_dialogflow_get_configs(payload).json()
        print("Business logic success - configs fetched")
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}