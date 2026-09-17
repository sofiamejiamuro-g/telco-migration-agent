def extract_lob_services(lob: str, billing_account_info_list_stringified: str) -> dict:
    '''State Manipulator. Filters account list to count matching services. Sets lob_count and extracts target account numbers.'''
    import json
    if get_variable("mock_mode"):
        set_variable('lob_count', 1)
        sanitized_lob = lob.lower().strip() if lob else 'tv'
        extracted = {}
        if sanitized_lob == 'tv':
            set_variable('account_identifier', 'TV123456789')
            extracted['tv_account_number'] = 'TV123456789'
        elif sanitized_lob == 'internet':
            set_variable('internet_account_number', 'INT123456789')
            extracted['internet_account_number'] = 'INT123456789'
        elif sanitized_lob in ('homephone', 'wireline'):
            set_variable('wireline_telephone_number', '4165551234')
            extracted['wireline_telephone_number'] = '4165551234'
        else:
            set_variable('account_identifier', 'GEN123456789')
            extracted['account_number'] = 'GEN123456789'

        return {
            "status": "success",
            "lob_count": 1,
            "extracted_accounts": extracted
        }
    else:
        try:
            sanitized_lob = lob.lower().strip()
            billing_list = []
            if billing_account_info_list_stringified:
                try:
                    billing_list = json.loads(billing_account_info_list_stringified)
                except Exception:
                    pass

            if not isinstance(billing_list, list):
                billing_list = []

            lob_mapping = {
                'tv': ['tv'],
                'internet': ['internet'],
                'homephone': ['homephone', 'wireline'],
                'wireline': ['homephone', 'wireline']
            }
            target_types = lob_mapping.get(sanitized_lob, [sanitized_lob])

            matched_services = []
            for account in billing_list:
                services = account.get('services', [])
                for srv in services:
                    srv_type = str(srv.get('service_type', '')).lower().strip()
                    if srv_type in target_types:
                        matched_services.append(srv)

            lob_count = len(matched_services)
            set_variable('lob_count', lob_count)

            extracted = {}
            if lob_count > 0:
                first_srv = matched_services[0]
                srv_id = first_srv.get('service_id', '')
                if 'tv' in target_types:
                    set_variable('account_identifier', srv_id)
                    extracted['tv_account_number'] = srv_id
                elif 'internet' in target_types:
                    set_variable('internet_account_number', srv_id)
                    extracted['internet_account_number'] = srv_id
                elif 'homephone' in target_types or 'wireline' in target_types:
                    set_variable('wireline_telephone_number', srv_id)
                    extracted['wireline_telephone_number'] = srv_id

            print("Business logic success")
            return {"status": "success", "lob_count": lob_count, "extracted_accounts": extracted}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Inform the user that we are experiencing technical difficulties validating the account services and offer to transfer them to a representative."}