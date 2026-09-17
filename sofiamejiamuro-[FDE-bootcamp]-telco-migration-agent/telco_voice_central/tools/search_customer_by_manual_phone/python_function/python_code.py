def search_customer_by_manual_phone(raw_phone_input: str) -> dict:
    '''Sanitizes user phone input, validates it, and searches for customer profile.'''
    import re
    try:
        if get_variable('mock_mode'):
            set_variable('ivr_va_ban_count', 1)
            set_variable('CIRN', '4165551234')
            set_variable('identification_status', 'Success')
            return {
                'status': 'success',
                'valid_phone': True,
                'ban_count': 1,
                'ban_list': ['987654321'],
                'message': 'Mock customer profile successfully retrieved.'
            }

        counter = get_variable('loop_counter')
        if not isinstance(counter, int):
            counter = 0
        set_variable('loop_counter', counter + 1)

        sanitized_arg = str(raw_phone_input).strip()
        sanitized = re.sub(r'[^0-9]', '', sanitized_arg)

        if len(sanitized) == 11 and sanitized.startswith('1'):
            sanitized = sanitized[1:]

        if len(sanitized) != 10:
            set_variable('identification_status', 'Fail')
            return {'status': 'failure', 'valid_phone': False, 'message': 'Invalid phone length.'}

        set_variable('CIRN', sanitized)

        tn_payload = {'telephone_number': sanitized}
        tn_response = tools.customer_identification_search_by_tn(tn_payload).json()

        ban_list = []
        if isinstance(tn_response, dict):
            accounts = tn_response.get('accounts', [])
            for acc in accounts:
                if 'billing_account_number' in acc:
                    ban_list.append(acc['billing_account_number'])

        ban_count = len(ban_list)
        set_variable('ivr_va_ban_count', ban_count)

        print('Business logic success')
        return {'status': 'success', 'valid_phone': True, 'ban_count': ban_count, 'ban_list': ban_list}
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Crash: {e}')
        set_variable('identification_status', 'Fail')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and route them to the Default Start Flow.'}