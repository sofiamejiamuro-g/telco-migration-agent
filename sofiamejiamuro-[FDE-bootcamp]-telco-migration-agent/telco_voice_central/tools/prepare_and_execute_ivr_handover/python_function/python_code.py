def prepare_and_execute_ivr_handover(route: str = '', tfn: str = '', clid: int = 0, cirn: int = 0, domain: str = '') -> dict:
    '''Executes IVR handover by mapping CTI parameters and sending transfer data.'''
    if get_variable('mock_mode'):
        print('Business logic success (mocked)')
        return {
            'webhook_success': True,
            'department_id': '2005',
            'message': 'Handover prepared successfully',
            'data': {
                'status': 'SUCCESS',
                'transaction_id': 'TXN-987654321',
                'route_mapped': route if route else 'default_route',
                'tfn_used': tfn,
                'mapped_parameters': {
                    'dam_id': 'BMCPPD',
                    'account_type': 'R',
                    'department': 2005,
                    'cti_at': 'VPRMMO',
                    'brand': 'MOB',
                    'clid': clid,
                    'cirn': cirn if cirn else clid,
                    'domain': domain
                }
            }
        }

    try:
        payload = {
            'route': route,
            'tfn': tfn,
            'clid': clid,
            'cirn': cirn if cirn else clid,
            'domain': domain,
            'dam_id': 'BMCPPD',
            'account_type': 'R',
            'department': 2005,
            'cti_at': 'VPRMMO',
            'brand': 'MOB'
        }

        api_response = tools.DAM_Transfer_send_transfer_data(payload).json()
        print('Business logic success')
        return {'webhook_success': True, 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'webhook_success': False, 'agent_action': 'Inform the user that the transfer failed, provide the fallback callback number 1-888-537-9999, and transfer to bell_wrapup.'}