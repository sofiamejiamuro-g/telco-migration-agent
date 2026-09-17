def configure_payment_sms_payload() -> dict:
    '''State Manipulator. Configures the SMS payload variables based on the language.'''
    if get_variable('mock_mode'):
        lang = get_variable('language')
        if not isinstance(lang, str):
            lang = 'en'
        sanitized_lang = lang.lower().strip()
        if sanitized_lang == 'fr-ca':
            content = "Mess. de Bell: Vous pouvez visiter https://m.bell.ca/ecgererpaiement pour effectuer un paiement dans l'application MonBell. ( bell.ca/apropos )"
        else:
            content = "Bell msg: You can visit https://m.bell.ca/ecmanagepayment to make a payment in the MyBell app. ( bell.ca/about-us )"

        set_variable('sms_type', 'Public')
        set_variable('sms_content', content)

        return {
            'status': 'success',
            'sms_type': 'Public',
            'language': sanitized_lang,
            'mock_mode': True
        }

    try:
        lang = get_variable('language')
        if not isinstance(lang, str):
            lang = 'en'

        sanitized_lang = lang.lower().strip()

        if sanitized_lang == 'fr-ca':
            content = "Mess. de Bell: Vous pouvez visiter https://m.bell.ca/ecgererpaiement pour effectuer un paiement dans l'application MonBell. ( bell.ca/apropos )"
        else:
            content = "Bell msg: You can visit https://m.bell.ca/ecmanagepayment to make a payment in the MyBell app. ( bell.ca/about-us )"

        set_variable('sms_type', 'Public')
        set_variable('sms_content', content)
        print('Business logic success: SMS payload configured')
        return {'status': 'success', 'sms_type': 'Public', 'language': sanitized_lang}

    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the user that the SMS configuration failed.'}