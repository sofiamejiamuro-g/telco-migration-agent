def fetch_and_parse_tv_profile(caller_id: int = 0) -> dict:
    '''Webhook Wrapper + State Manipulator. Fetches the TN search profile, calculates IPTV and DTH counts, extracts service IDs and sets global routing variables.'''
    import logging
    logger = logging.getLogger(__name__)
    try:
        if get_variable('mock_mode'):
            set_variable('FIBE_COUNT', 1)
            set_variable('SAT_COUNT', 1)
            set_variable('account_identifier', 'FIBE456')
            set_variable('region_val', 'QC')
            return {
                'status': 'success',
                'FIBE_COUNT': 1,
                'SAT_COUNT': 1,
                'province': 'QC'
            }
        else:
            payload = {'caller_id': caller_id}
            response = tools.customer_identification_search_by_tn(payload).json()

            users = response.get('users', [])
            if not users:
                raise ValueError('No users found in profile')

            billing_accounts = users[0].get('billing_accounts', [])
            fibe_count = 0
            sat_count = 0
            first_fibe_id = ''
            first_sat_id = ''
            province = ''

            for account in billing_accounts:
                services = account.get('services', [])
                for service in services:
                    tech_type = service.get('technology_type', '')
                    if tech_type == 'IPTV':
                        fibe_count += 1
                        if not first_fibe_id:
                            first_fibe_id = service.get('service_id', '')
                            province = service.get('service_address', {}).get('stateOrProvince', province)
                    elif tech_type == 'DTH':
                        sat_count += 1
                        if not first_sat_id:
                            first_sat_id = service.get('service_id', '')
                            province = service.get('service_address', {}).get('stateOrProvince', province)

            tv_sub_type = get_variable('tv_sub_type') or ''
            sanitized_sub_type = str(tv_sub_type).lower().strip()

            tv_account_number = first_sat_id if sanitized_sub_type in ['sat', 'satellite', 'satellite tv', 'sat tv'] else first_fibe_id
            if not tv_account_number and first_fibe_id:
                tv_account_number = first_fibe_id

            set_variable('FIBE_COUNT', fibe_count)
            set_variable('SAT_COUNT', sat_count)
            set_variable('account_identifier', tv_account_number)
            set_variable('region_val', province)

            print('Business logic success: Profile fetched and parsed')
            return {'status': 'success', 'FIBE_COUNT': fibe_count, 'SAT_COUNT': sat_count, 'province': province}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties fetching the profile and route to the next flow.'}