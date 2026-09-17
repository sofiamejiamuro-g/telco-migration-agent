def get_intent_vanity_url(intent: str, language: str) -> dict:
    '''Retrieves the standard vanity URL for fallback scenarios based on intent and language.'''
    import json

    if get_variable('mock_mode'):
        sanitized_intent = str(intent).lower().strip()
        lang = str(language).lower().strip()

        if 'autopay' in sanitized_intent or 'preauth' in sanitized_intent:
            vanity_url = 'https://m.bell.ca/chatpreauthorizedbankf' if 'fr' in lang else 'https://m.bell.ca/chatpreauthorizedbanke'
        elif 'payment' in sanitized_intent:
            vanity_url = 'https://m.bell.ca/ecmanagepaymentf' if 'fr' in lang else 'https://m.bell.ca/ecmanagepayment'
        elif 'bill' in sanitized_intent or 'balance' in sanitized_intent:
            vanity_url = 'https://m.bell.ca/ecviewmybillf' if 'fr' in lang else 'https://m.bell.ca/ecviewmybill'
        elif 'contract' in sanitized_intent or 'agreement' in sanitized_intent:
            vanity_url = 'https://m.bell.ca/ecmyagreementf' if 'fr' in lang else 'https://m.bell.ca/ecmyagreement'
        else:
            vanity_url = 'https://bell.ca/soutien' if 'fr' in lang else 'https://bell.ca/support'

        set_variable('vanity_url', vanity_url)
        set_variable('webhook_success', True)

        return {
            'status': 'success',
            'result': {
                'url': vanity_url,
                'intent': intent,
                'language': language
            }
        }

    try:
        sanitized_intent = intent.lower().strip().replace(' ', '_')
        payload = {'intent': sanitized_intent, 'language': language}
        api_response = tools.Intent_sdl_mapping(payload).json()
        print('Business logic success')
        set_variable('vanity_url', api_response.get('url', 'https://bell.ca/support'))
        return {'status': 'success', 'result': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'agent_action': 'Explain the technical error to the user and route to FAILURE_HUB.'}