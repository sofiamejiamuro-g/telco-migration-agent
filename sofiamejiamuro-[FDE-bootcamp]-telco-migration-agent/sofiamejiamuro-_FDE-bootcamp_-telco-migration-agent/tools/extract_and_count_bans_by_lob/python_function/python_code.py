def extract_and_count_bans_by_lob(customer_id_search_response: dict = {}, lob: str = '') -> dict:
    '''Extracts billing accounts matching the LOB and sets n_ban_with_lob variable.'''
    if get_variable("mock_mode"):
        mock_count = 1
        set_variable('n_ban_with_lob', mock_count)
        print(f"Mock mode active: Counted {mock_count} BAN(s) for LOB {lob}")
        return {'status': 'success', 'n_ban_with_lob': mock_count}

    try:
        sanitized_lob = str(lob).lower().strip()
        count = 0
        if isinstance(customer_id_search_response, dict):
            users = customer_id_search_response.get('users', [])
            for user in users:
                billing_accounts = user.get('billing_accounts', [])
                for ban in billing_accounts:
                    services = ban.get('services', [])
                    for service in services:
                        s_type = str(service.get('service_type', '')).lower().strip()
                        if sanitized_lob in s_type or s_type in sanitized_lob:
                            count += 1
        set_variable('n_ban_with_lob', count)
        print(f'Business logic success: Counted {count} BANs for LOB {sanitized_lob}')
        return {'status': 'success', 'n_ban_with_lob': count}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Inform the customer we are experiencing technical difficulties checking their accounts, and transfer them to a representative.'}