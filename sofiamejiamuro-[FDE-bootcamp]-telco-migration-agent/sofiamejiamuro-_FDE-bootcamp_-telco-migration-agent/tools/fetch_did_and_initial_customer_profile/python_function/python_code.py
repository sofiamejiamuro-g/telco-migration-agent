def fetch_did_and_initial_customer_profile(tfn: str) -> dict:
    '''Fetches DID data, translates LOB, and retrieves initial customer profile by CIRN.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('lob', 'mobility')
            set_variable('ivr_va_ban_count', 1)
            set_variable('CIRN', '5145550199')
            set_variable('identification_status', 'Success')
            return {
                'status': 'success',
                'lob': 'mobility',
                'ban_count': 1,
                'ban_list': ['100123456']
            }

        did_payload = {'tfn': str(tfn)}
        did_response = tools.get_did_data_get_did_data(did_payload).json()

        lob_from_ivr = did_response.get('lob', '')
        cirn = did_response.get('cirn', '')

        lob_mapping = {
            'BRS': None, 'BusFibeTV': 'tv', 'BusSBM': None, 'BusSec': 'smarthome',
            'Home Phone': 'homephone', 'Internet': 'internet', 'NA': None,
            'SmartHome': 'smarthome', 'TV': 'tv', 'Virgin': None, 'Wireless': 'mobility',
            'internet': 'internet', 'mobility': 'mobility', 'tv': 'tv'
        }
        mapped_lob = lob_mapping.get(lob_from_ivr, None)
        set_variable('lob', mapped_lob)

        if not cirn:
            set_variable('identification_status', 'Fail')
            return {'status': 'success', 'lob': mapped_lob, 'ban_count': 0, 'ban_list': []}

        set_variable('CIRN', cirn)

        tn_payload = {'telephone_number': cirn}
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
        return {'status': 'success', 'lob': mapped_lob, 'ban_count': ban_count, 'ban_list': ban_list}
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Crash: {e}')
        set_variable('identification_status', 'Fail')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and route them to the Default Start Flow.'}