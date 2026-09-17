def npa_nxx_lookup_wrapper() -> dict:
    '''Webhook Wrapper for NPA NXX Lookup'''
    import json

    if get_variable('mock_mode'):
        set_variable('region_val', 'ON')
        return {
            'status': 'success',
            'province': 'ON'
        }
    else:
        try:
            mock_mode = get_variable('mock_mode')
            cirn = get_variable('CIRN')
            clid = get_variable('clid')
            temp_number = str(cirn) if cirn not in [None, '', 0] else str(clid)
            if not temp_number or len(temp_number) < 6:
                raise ValueError('Valid CIRN or CLID is required but not found.')
            npa = temp_number[0:3]
            nxx = temp_number[3:6]
            payload = {'npa': npa, 'nxx': nxx}
            if mock_mode:
                data = {'province': 'ON'}
            else:
                data = tools.npa_nxx_lookup_npa_nxx_lookup(payload).json()
            province = data.get('province', '')
            set_variable('region_val', province)
            print('Business logic success')
            return {'status': 'success', 'province': province}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}