def get_npa_nxx_province(phone_number: str = '') -> dict:
    '''Webhook Wrapper. Lookup for province based on phone number.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        sanitized_phone = str(phone_number).strip().replace('-', '').replace(' ', '')

        if mock_mode:
            npa = sanitized_phone[:3] if len(sanitized_phone) >= 3 else "416"
            nxx = sanitized_phone[3:6] if len(sanitized_phone) >= 6 else "555"
            return {
                "result": {
                    "status": "Success",
                    "province": "ON",
                    "region_name": "Ontario",
                    "npa": npa,
                    "nxx": nxx,
                    "country_code": "CA",
                    "message": "NPA-NXX lookup successful."
                },
                "province": "ON",
                "status": "Success"
            }

        payload = {'phone_number': sanitized_phone}
        api_response = tools.npa_nxx_lookup_get_npa_nxx_province(payload).json()
        print('Business logic success: retrieved province')
        return api_response
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Proceed with default flow logic, or if location is strictly required, offer an SMS fallback.'}