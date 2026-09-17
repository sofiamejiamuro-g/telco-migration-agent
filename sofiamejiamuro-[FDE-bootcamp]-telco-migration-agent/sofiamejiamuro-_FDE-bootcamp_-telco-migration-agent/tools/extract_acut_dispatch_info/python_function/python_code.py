def extract_acut_dispatch_info() -> dict:
    '''State Manipulator. Extracts dispatch information from ACUT response.'''
    if get_variable('mock_mode'):
        set_variable('target_date', '2023-11-25T14:00:00Z')
        set_variable('contact_number', '555-123-4567')
        set_variable('contact_number', 'MOBILE')
        set_variable('dispatch_status', 'SCHEDULED')
        print('Business logic success (mock)')
        return {
            'status': 'success',
            'target_date': '2023-11-25T14:00:00Z',
            'contact_number': '555-123-4567',
            'contact_type': 'MOBILE',
            'dispatch_status': 'SCHEDULED'
        }

    try:
        acut_resp = get_variable('api_response')
        if not isinstance(acut_resp, dict):
            acut_resp = {}
        appt = acut_resp.get('appointments', {}).get('latestAppointment', {})
        pc = acut_resp.get('primaryContact', {})
        set_variable('target_date', appt.get('appointmentStartDate', ''))
        set_variable('contact_number', pc.get('number', ''))
        set_variable('contact_number', pc.get('type', ''))
        set_variable('dispatch_status', acut_resp.get('dispatch_status', ''))
        print('Business logic success')
        return {'status': 'success'}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them.'}