def extract_postal_code_data() -> dict:
    '''State Manipulator tool to extract the last 3 characters of the postal code.'''
    if get_variable("mock_mode"):
        set_variable("postal_code_three_backend", "2h1")
        return {"status": "success", "extracted_postal_code": "2h1"}

    try:
        billing_list = get_variable('billing_account_info_list')
        if not billing_list or not isinstance(billing_list, list):
            return {"status": "failed", "reason": "No billing list found."}

        postal_code = ""
        for info in billing_list:
            if isinstance(info, dict):
                addr = info.get('billing_address', {})
                if isinstance(addr, dict) and addr.get('postcode'):
                    postal_code = addr.get('postcode', "")
                    break
                services = info.get('services', [])
                if isinstance(services, list) and len(services) > 0:
                    srv = services[0]
                    if isinstance(srv, dict):
                        srv_addr = srv.get('service_address', {})
                        if isinstance(srv_addr, dict) and srv_addr.get('postcode'):
                            postal_code = srv_addr.get('postcode', "")
                            break

        sanitized = postal_code.lower().strip().replace(' ', '')
        last_three = sanitized[-3:] if len(sanitized) >= 3 else sanitized
        set_variable('postal_code_three_backend', last_three)
        print("Business logic success")
        return {"status": "success", "extracted_postal_code": last_three}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the system encountered an error reading the postal code and offer to transfer."}