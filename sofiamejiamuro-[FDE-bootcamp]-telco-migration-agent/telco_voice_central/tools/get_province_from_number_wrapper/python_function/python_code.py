def get_province_from_number_wrapper(phone_number: str = "") -> dict:
    '''Takes the user phone number, extracts NPA/NXX, and calls the lookup API to return the province.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'province': 'ON',
                'npa': '416',
                'nxx': '555',
                'status': 'Success',
                'description': 'Province successfully resolved from NPA-NXX lookup.',
                'api_success': True
            }

        sanitized = phone_number.replace('-', '').replace(' ', '').replace('+1', '').strip()
        npa = sanitized[0:3] if len(sanitized) >= 3 else '000'
        nxx = sanitized[3:6] if len(sanitized) >= 6 else '000'

        payload = {'npa': npa, 'nxx': nxx}
        api_response = tools.unknown_unknown(payload).json()
        print("Business logic success")

        return {'province': api_response.get('province', 'ON')}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {'error': str(e), 'agent_action': 'Province lookup failed. Bypass complex logic and transition directly to PAD_SMS_OFFER to gracefully fallback to self-service by prompting for SMS.'}