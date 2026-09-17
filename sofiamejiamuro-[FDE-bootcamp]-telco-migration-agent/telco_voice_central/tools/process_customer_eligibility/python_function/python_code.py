def process_customer_eligibility(customer_profile_data: str, calling_number: str) -> dict:
    '''State/Variable Manipulator. Processes raw profile data to determine auth eligibility.'''
    if get_variable("mock_mode"):
        return {
            'is_pin_eligible': True,
            'is_otp_eligible': True,
            'requires_phone_prompt': False,
            'target_otp_phone': '4165551234'
        }

    import json
    try:
        sanitized_profile = customer_profile_data.strip() if customer_profile_data else '{}'
        profile = json.loads(sanitized_profile) if sanitized_profile.startswith('{') else {}
        otp_tns = profile.get('otp_tns', [])
        is_pin_eligible = profile.get('pin_available', False)
        is_otp_eligible = len(otp_tns) > 0
        requires_phone_prompt = len(otp_tns) > 1
        target_otp_phone = ''
        if len(otp_tns) == 1:
            target_otp_phone = otp_tns[0]
        elif calling_number in otp_tns:
            target_otp_phone = calling_number
            requires_phone_prompt = False
        print('Business logic success')
        return {'is_pin_eligible': is_pin_eligible, 'is_otp_eligible': is_otp_eligible, 'requires_phone_prompt': requires_phone_prompt, 'target_otp_phone': target_otp_phone}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Explain that we could not verify eligibility and transfer the user to an agent.'}