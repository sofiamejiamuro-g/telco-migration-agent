def format_payment_sms_payload(language: str, route: str) -> dict:
    '''Formats payment SMS payload by setting sms_type and sms_content based on language and route.'''
    if str(get_variable('mock_mode')).strip().lower() == 'true':
        set_variable('sms_type', 'Public')
        set_variable('sms_content', 'Bell msg: You can visit https://m.bell.ca/ecmanagepayment to make a payment in the MyBell app. ( bell.ca/about-us )')
        return {
            'status': 'success',
            'message': 'Variables sms_type and sms_content have been set. Proceed to route bell_SMS_Trigger.'
        }
    else:
        try:
            sanitized_lang = str(language).lower().strip() if language else 'en'
            sanitized_route = str(route).lower().strip() if route else ''
            sms_type = 'Public'
            sms_content = ''
            success = False
            if sanitized_lang == 'en':
                if sanitized_route in ['payment_update_autopay', 'payment_setup_autopay']:
                    sms_content = 'You can visit https://m.bell.ca/chatpreauthorizedbanke to complete setting up Pre Authorized payment in MyBell. (bell.ca/about-us )'
                    success = True
                elif sanitized_route == 'payment_make_payment':
                    sms_content = 'Bell msg: You can visit https://m.bell.ca/ecmanagepayment to make a payment in the MyBell app. ( bell.ca/about-us )'
                    success = True
            elif sanitized_lang == 'fr-ca':
                if sanitized_route in ['payment_update_autopay', 'payment_setup_autopay']:
                    sms_content = 'Vous pouvez visiter le https://m.bell.ca/chatpreauthorizedbankf pour terminer la configuration du prélèvement automatique dans MonBell. ( bell.ca/apropos )'
                    success = True
                elif sanitized_route == 'payment_make_payment':
                    sms_content = 'Mess. de Bell: Vous pouvez visiter https://m.bell.ca/ecgererpaiement pour effectuer un paiement dans l\'application MonBell. ( bell.ca/apropos )'
                    success = True
            if success:
                set_variable('sms_type', sms_type)
                set_variable('sms_content', sms_content)
                print('SMS content generated successfully')
                return {'status': 'success', 'message': 'Variables sms_type and sms_content have been set. Proceed to route bell_SMS_Trigger.'}
            else:
                print('No matching SMS conditions found. Proceeding to fallback.')
                return {'status': 'fallback', 'message': 'No specific mapping found. Proceed to route bell_aqd.'}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Inform the user that the SMS could not be formatted and route to bell_aqd.'}