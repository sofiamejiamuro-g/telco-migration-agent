def extract_mya_eligibility(mya_information_response: dict) -> dict:
    '''Extracts MYA eligibility and application URL from the payload.'''
    if get_variable("mock_mode"):
        set_variable('mya_eligible', True)
        set_variable('mya_link', 'https://mybell.bell.ca/AppT/mock123456789')
        print('Mock mode success: MYA Eligible')
        return {
            'status': 'success',
            'mya_eligible': True,
            'mya_link': 'https://mybell.bell.ca/AppT/mock123456789'
        }

    try:
        if not mya_information_response:
            mya_information_response = get_variable('mya_information_response')
            if not mya_information_response:
                mya_information_response = {}

        notifications = mya_information_response.get('notification', [])
        if not isinstance(notifications, list):
            notifications = [notifications]

        mya_links = []
        for n in notifications:
            if isinstance(n, dict) and 'MYAApplicationUrl' in n:
                mya_links.append(n['MYAApplicationUrl'])

        if len(mya_links) > 0:
            set_variable('mya_eligible', True)
            set_variable('mya_link', mya_links[0])
            print('Business logic success: MYA Eligible')
            return {'status': 'success', 'mya_eligible': True, 'mya_link': mya_links[0]}
        else:
            set_variable('mya_eligible', False)
            print('Business logic success: Not MYA Eligible')
            return {'status': 'success', 'mya_eligible': False}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Explain the technical error and immediately transfer the user to bell_aqd.'}