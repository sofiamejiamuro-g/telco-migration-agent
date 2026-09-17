def extract_lob_services_manipulator(billing_account_info_list: list, lob: str) -> dict:
    '''Extracts service IDs for a given LOB and sets lob_service_ids and lob_count.'''
    if get_variable('mock_mode'):
        mock_service_ids = ["SVC-987654321"]
        set_variable('service_type', mock_service_ids)
        set_variable('lob_count', len(mock_service_ids))
        print('Business logic success (mock)')
        return {
            'status': 'success',
            'lob_service_ids': mock_service_ids,
            'lob_count': len(mock_service_ids)
        }

    try:
        if not isinstance(billing_account_info_list, list):
            billing_account_info_list = []
        sanitized_lob = lob.lower().strip()
        lob_aliases = [sanitized_lob]
        if sanitized_lob in ['homephone', 'wireline']:
            lob_aliases.extend(['homephone', 'wireline'])
        service_ids = []
        for account in billing_account_info_list:
            services = account.get('services', [])
            for service in services:
                svc_type = str(service.get('service_type', '')).lower().strip()
                if svc_type in lob_aliases:
                    svc_id = service.get('service_id')
                    if svc_id:
                        service_ids.append(svc_id)
        set_variable('service_type', service_ids)
        set_variable('lob_count', len(service_ids))
        print('Business logic success')
        return {'status': 'success', 'lob_service_ids': service_ids, 'lob_count': len(service_ids)}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties.'}