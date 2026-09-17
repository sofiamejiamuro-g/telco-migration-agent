def get_intent_sdl_mapping_wrapper(intent_route: str = "", brand: str = "", language: str = "") -> dict:
    '''Maps a routing intent to a specific vanity URL for user self-service.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'vanity_url': 'https://m.bell.ca/chatpreauthorizedbanke',
                'intent_route_mapped': intent_route if intent_route else 'autopay_setup',
                'brand': brand if brand else 'bell',
                'language': language if language else 'en',
                'status': 'success',
                'message': 'Successfully mapped intent to self-service vanity URL.'
            }

        payload = {'intent_route': intent_route, 'brand': brand, 'language': language}
        api_response = tools.unknown_unknown(payload).json()
        print("Business logic success")

        return {'vanity_url': api_response.get('url', 'bell.ca/support')}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {'error': str(e), 'agent_action': 'Tell the user they can set up pre-authorized debit on MyBell at bell.ca/support, then gracefully end the session or transition to feedback.'}