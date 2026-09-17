def format_handoff_context() -> dict:
    '''Evaluates 'va_to_ccaip'. If true, extracts user_name and sanitizes null context variables to 'None'. If false, establishes routing SIP headers.'''
    if get_variable('mock_mode') is True:
        return {
            'status': 'success',
            'message': 'Handoff variables have been prepared.',
            'mock_data': {
                'customer_profile_type': 'mock_user_name',
                'cx_cornerstone': 'false',
                'X_DNIS': '18005551234',
                'X_G2Mkey': 'mock_call_id_12345',
                'url_link': 'sip:mock_routing_uri@bell.ca'
            }
        }
    else:
        try:
            va_to_ccaip = get_variable('context_source')

            if va_to_ccaip is True:
                first_user_account = get_variable('account_identifier')
                if isinstance(first_user_account, dict):
                    set_variable('customer_profile_type', first_user_account.get('user_name', 'None'))
                else:
                    set_variable('customer_profile_type', 'None')

                vars_list = ['language', 'brand', 'call_id', 'menu_type', 'clid', 'tfn', 'cirn', 'customer_name', 'customer_authentication', 'billing_account_number', 'account_type', 'intent', 'aqd_lob']
                for v in vars_list:
                    val = get_variable(v)
                    if val is None:
                        set_variable(v, 'None')

                cx = get_variable('cx_cornerstone')
                if cx is None:
                    set_variable('cx_cornerstone', 'false')
            else:
                tfn = get_variable('phone_number_val') or ''
                set_variable('X_DNIS', f'1{tfn}')

                call_id = get_variable('call_id') or ''
                set_variable('X_G2Mkey', call_id)

                config = get_variable('config')
                if isinstance(config, dict):
                    set_variable('url_link', config.get('sip_uri', ''))
                else:
                    set_variable('url_link', '')

            print('Business logic success: Handoff context formatted successfully.')
            return {'status': 'success', 'message': 'Handoff variables have been prepared.'}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Inform the user that a technical error occurred while preparing the live agent transfer and route them to bell_End the Conversation.'}