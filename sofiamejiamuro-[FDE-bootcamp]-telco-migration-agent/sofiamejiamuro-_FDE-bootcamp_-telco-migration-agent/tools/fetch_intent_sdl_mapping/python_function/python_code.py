def fetch_intent_sdl_mapping(intent: str = "") -> dict:
    '''Webhook Wrapper: Fetches the specialized SDL URL based on the user's intent/route.'''
    try:
        if get_variable('mock_mode'):
            sanitized_intent = intent.lower().strip() if intent else ""
            mock_urls = {
                'authentication': 'bell.ca/login',
                'billing_and_payments': 'bell.ca/mybills',
                'tech_support': 'bell.ca/support',
                'sales_and_equipment': 'bell.ca/shop',
                'appointment_management': 'bell.ca/appointments',
                'account_management': 'bell.ca/myaccount',
                'bill_view_bill': 'bell.ca/mybills',
                'payment_make_payment': 'bell.ca/pay',
                'service_change_plan': 'bell.ca/myplan'
            }
            url = mock_urls.get(sanitized_intent, 'bell.ca/support')
            print('fetch_intent_sdl_mapping mock success')
            return {
                'result': {
                    'status': 'success',
                    'url': url,
                    'intent_mapped': sanitized_intent,
                    'is_valid_route': True
                },
                'status': 'success',
                'url': url
            }

        mock_mode = get_variable('mock_mode')
        sanitized_intent = intent.lower().strip()

        # Fallback default since no backend toolset was provided
        url = 'bell.ca/support'
        print('fetch_intent_sdl_mapping success')
        return {'status': 'success', 'url': url}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that the system is currently unavailable and offer to transfer them to an agent.'}