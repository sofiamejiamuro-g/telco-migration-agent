def execute_ivr_handover_preparation(tfn: str = '', clid: int = 0, cirn: int = 0, route: str = '') -> dict:
    '''Webhook Wrapper to prepare IVR handover configurations.'''
    import json

    if get_variable('mock_mode'):
        final_cirn = cirn if cirn else clid
        final_route = route if route else 'other_speak_to_agent'

        set_variable('domain', 'Consumer')
        set_variable('menu_id', 'default_menu_id')
        set_variable('department_id', 955)
        set_variable('agent_id', 'BBM')
        set_variable('tag', 'dam-transfer')
        set_variable('brand', 'Bell Residential Services')
        set_variable('account_type', 'B')
        set_variable('cti_at', 'BUSMENU')
        set_variable('cti_rt', final_route)
        set_variable('cti_sd', tfn)
        set_variable('cirn', final_cirn)
        set_variable('webhook_success', True)

        print('Business logic success - Mock Mode')
        return {
            'status': 'success',
            'message': 'Mocked IVR handover configs applied.',
            'result': {
                'webhook_success': True,
                'configuration': {
                    'domain': 'Consumer',
                    'department_id': 955,
                    'menu_id': 'default_menu_id',
                    'agent_id': 'BBM',
                    'tag': 'dam-transfer',
                    'brand': 'Bell Residential Services',
                    'account_type': 'B',
                    'cti_at': 'BUSMENU',
                    'cti_rt': final_route,
                    'cti_sd': tfn,
                    'cirn': final_cirn
                }
            }
        }
    else:
        try:
            mock_mode = get_variable('mock_mode')

            domain = 'Consumer'
            department = 955
            menu_id = 'default_menu_id'

            final_cirn = cirn if cirn else clid
            final_route = route if route else 'other_speak_to_agent'

            set_variable('domain', domain)
            set_variable('menu_id', menu_id)
            set_variable('department_id', department)
            set_variable('agent_id', 'BBM')
            set_variable('tag', 'dam-transfer')
            set_variable('brand', 'Bell Residential Services')
            set_variable('account_type', 'B')
            set_variable('cti_at', 'BUSMENU')
            set_variable('cti_rt', final_route)
            set_variable('cti_sd', tfn)
            set_variable('cirn', final_cirn)
            set_variable('webhook_success', True)

            if mock_mode:
                print('Business logic success - Mock Mode')
                return {'status': 'success', 'message': 'Mocked IVR handover configs applied.'}

            print('Business logic success')
            return {'status': 'success', 'message': 'IVR handover configs applied.'}
        except Exception as e:
            set_variable('webhook_success', False)
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}