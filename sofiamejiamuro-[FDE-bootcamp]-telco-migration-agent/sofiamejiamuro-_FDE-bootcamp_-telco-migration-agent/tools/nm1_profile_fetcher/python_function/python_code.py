def nm1_profile_fetcher(lookup_type: str) -> dict:
    '''Webhook Wrapper for NM1 Profiles'''
    import json

    if get_variable('mock_mode'):
        lookup_type_sanitized = lookup_type.lower().strip()
        if lookup_type_sanitized == 'customer':
            set_variable('one_bill_indicator', 'Y')
            set_variable('accountType', 'C')
            set_variable('accountSubType', 'P')
            set_variable('pastDueAmount', 0)
            set_variable('accountBalance', 150.00)
            return {
                'status': 'success',
                'data': {
                    'oneBill': 'Y',
                    'banType': 'C',
                    'banSubType': 'P',
                    'pastDueAmount': 0,
                    'arBalance': 150.00,
                    'returnCode': 1
                }
            }
        else:
            set_variable('one_bill_indicator', 'Y')
            set_variable('accountType', 'I')
            set_variable('accountSubType', 'R')
            set_variable('pastDueAmount', 0)
            set_variable('accountBalance', 100.00)
            return {
                'status': 'success',
                'data': {
                    'oneBillIndicator': 'Y',
                    'accountType': 'I',
                    'accountSubType': 'R',
                    'pastDueAmount': 0,
                    'accountBalance': 100.00,
                    'returnCode': 1
                }
            }
    else:
        try:
            mock_mode = get_variable('mock_mode')
            lookup_type_sanitized = lookup_type.lower().strip()
            if mock_mode:
                if lookup_type_sanitized == 'customer':
                    data = {'oneBill': 'Y', 'banType': 'C', 'banSubType': 'P', 'pastDueAmount': 0, 'arBalance': 150.00, 'returnCode': 1}
                else:
                    data = {'oneBillIndicator': 'Y', 'accountType': 'I', 'accountSubType': 'R', 'pastDueAmount': 0, 'accountBalance': 100.00, 'returnCode': 1}
            else:
                payload = {'lookup_type': lookup_type_sanitized}
                if lookup_type_sanitized == 'customer':
                    data = tools.nm1_get_customer_profile(payload).json()
                else:
                    data = tools.nm1_get_ban_profile(payload).json()

            if lookup_type_sanitized == 'customer':
                set_variable('one_bill_indicator', data.get('oneBill', ''))
                set_variable('accountType', data.get('banType', ''))
                set_variable('accountSubType', data.get('banSubType', ''))
                set_variable('pastDueAmount', data.get('pastDueAmount', 0))
                set_variable('accountBalance', data.get('arBalance', 0))
            else:
                set_variable('one_bill_indicator', data.get('oneBillIndicator', ''))
                set_variable('accountType', data.get('accountType', ''))
                set_variable('accountSubType', data.get('accountSubType', ''))
                set_variable('pastDueAmount', data.get('pastDueAmount', 0))
                set_variable('accountBalance', data.get('accountBalance', 0))

            if data.get('returnCode') == 0:
                set_variable('billing_status', 'Outage')
                return {'status': 'Fail', 'reason': 'Outage', 'agent_action': 'Inform the user that the system is currently experiencing an outage and end the session.'}
            print('Business logic success')
            return {'status': 'success', 'data': data}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}