def set_sms_payload_variables(language: str = '', is_different_number: bool = False) -> dict:
    '''Evaluates language and is_different_number to set SMS payload variables.'''
    if get_variable("mock_mode"):
        set_variable('different_number', is_different_number)
        set_variable('sms_type', 'Public')
        set_variable('sms_content', 'You can visit https://m.bell.ca/arrangepayment to set up your payment arrangement in MyBell. ( bell.ca/about-us )')
        return {'status': 'success', 'language_supported': True}
    else:
        try:
            lang = language.lower().strip()
            set_variable('different_number', is_different_number)
            if lang in ['en', 'english']:
                set_variable('sms_type', 'Public')
                set_variable('sms_content', 'You can visit https://m.bell.ca/arrangepayment to set up your payment arrangement in MyBell. ( bell.ca/about-us )')
                print('SMS payload set for English.')
                return {'status': 'success', 'language_supported': True}
            elif lang in ['fr-ca', 'fr', 'french']:
                set_variable('sms_type', 'Public')
                set_variable('sms_content', 'Vous pouvez visiter https://m.bell.ca/arrangepayment pour établir votre entente de paiement dans MonBell. ( bell.ca/apropos )')
                print('SMS payload set for French.')
                return {'status': 'success', 'language_supported': True}
            else:
                set_variable('hardstop', 'True')
                set_variable('page_id', '8c4640e2-6d5b-4bbe-b3ba-fcd0a51c99de')
                set_variable('flow_id', 'ff757595-86c5-4c23-9d2d-85005f329ace')
                set_variable('page_name', 'LangBased SMS')
                print('Unsupported language detected, fallback variables set.')
                return {'status': 'unsupported_language', 'language_supported': False}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}