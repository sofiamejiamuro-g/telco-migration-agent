def get_intent_sdl_mapping(intent: str = '', language: str = '') -> dict:
    '''Retrieves vanity URLs for fallback messaging when SMS is declined.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print('Business logic success (mock)')
            is_french = str(language).lower() in ['fr', 'french', 'fr-ca']
            return {
                'vanity_url': 'bell.ca/soutien' if is_french else 'bell.ca/support',
                'status': 'success',
                'errorCode': '1',
                'intent_mapped': intent or 'default',
                'language_mapped': language or 'en'
            }

        payload = {'intent': intent, 'language': language}
        api_response = tools.intent_sdl_mapping_default(payload).json()
        url = api_response.get('url', 'bell.ca/support')
        print('Business logic success')
        return {'vanity_url': url}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the customer that we are experiencing technical difficulties and offer an SMS link.'}