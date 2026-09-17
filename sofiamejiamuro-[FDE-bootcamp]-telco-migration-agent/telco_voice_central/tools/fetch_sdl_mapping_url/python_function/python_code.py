def fetch_sdl_mapping_url(brand: str = "bell", language: str = "", intent_route: str = "") -> dict:
    '''Retrieves a customized Self-Serve/FAQ URL based on intent route, brand, and language. Sets the baseline URL first natively, then attempts an API lookup to override it.'''
    import json

    if get_variable("mock_mode"):
        sanitized_lang = language.lower().strip()
        mock_url = "bell.ca/soutien/faq" if sanitized_lang in ["fr", "fr-ca", "fr_ca", "fr-fr"] else "bell.ca/support/faq"
        set_variable("url_link", mock_url)
        print("Mock mode: URL fetched successfully")
        return {
            "status": "success",
            "data": {
                "url": mock_url,
                "intent_route": intent_route,
                "brand": brand,
                "language": language,
                "status": "200 OK"
            }
        }
    else:
        try:
            sanitized_lang = language.lower().strip()
            baseline_url = "bell.ca/support"
            if sanitized_lang in ["fr", "fr-ca", "fr_ca", "fr-fr"]:
                baseline_url = "bell.ca/soutien"
            set_variable("url_link", baseline_url)

            payload = {
                "brand": brand.strip() if brand else "bell",
                "language": language.strip(),
                "intent_route": intent_route.strip()
            }
            api_response = tools.intent_sdl_mapping_post(payload).json()

            custom_url = api_response.get("url", "")
            if custom_url:
                set_variable("url_link", custom_url)

            print("Business logic success")
            return {"status": "success", "data": api_response}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Do not attempt to fix the link. Baseline link is already set. Transition to PARENT_AGENT."}