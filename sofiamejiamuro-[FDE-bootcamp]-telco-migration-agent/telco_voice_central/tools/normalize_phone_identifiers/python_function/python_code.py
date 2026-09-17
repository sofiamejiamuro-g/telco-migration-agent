def normalize_phone_identifiers() -> dict:
    '''Evaluates CLID and TFN session variables and normalizes formats.'''
    if get_variable('mock_mode'):
        set_variable('clid', '4165551234')
        set_variable('phone_number_val', '8005551234')
        set_variable('cirn', '4165551234')
        set_variable('intent', 'billing_and_payments')
        set_variable('route', 'billing_and_payments')
        return {"status": "success"}
    else:
        try:
            clid = str(get_variable('clid') or '')
            tfn = str(get_variable('phone_number_val') or '')
            cirn = str(get_variable('cirn') or '')
            intent = str(get_variable('intent') or '')

            if len(clid) in [11, 12]:
                clid = clid[-10:]
            if len(tfn) in [11, 12]:
                tfn = tfn[-10:]
            if not cirn or cirn == '0' or cirn == '0000000000':
                cirn = clid if clid else '0'

            sanitized_intent = intent.lower().strip()
            if not sanitized_intent or sanitized_intent in ['default', 'infobot', 'agent', 'none']:
                intent = 'other_speak_to_agent'

            set_variable('clid', clid)
            set_variable('phone_number_val', tfn)
            set_variable('cirn', cirn)
            set_variable('intent', intent)
            set_variable('route', intent)

            print("Business logic success - identifiers normalized")
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}