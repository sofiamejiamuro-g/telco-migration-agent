def execute_dam_transfer(call_id: str = '', clid: int = 0, cirn: int = 0) -> dict:
    '''Webhook Wrapper & State Manipulator for dam-transfer logic.'''
    if get_variable('mock_mode'):
        final_cirn = cirn if cirn else clid

        set_variable('agent_id', 'BBM')
        set_variable('account_type', 'B')
        set_variable('cti_at', 'BUSMENU')
        set_variable('cti_rt', 'business_account')
        set_variable('cti_sd', '8000212355')
        set_variable('department_id', '955')
        set_variable('va_ibm_id', 'BCE_Entry')
        set_variable('agent_id', '0f67e50b-0b7d-4e9c-9ebe-50557aff3f4e')
        set_variable('call_id', call_id if call_id else 'f12ca3-5a4-a2b-987-463832885')
        set_variable('brand', 'Bell Residential Services')
        set_variable('cirn', final_cirn)

        print('Business logic success (mock)')
        return {
            'status': 'success',
            'data': {
                'transfer_status': 'mocked_success',
                'call_id': call_id if call_id else 'f12ca3-5a4-a2b-987-463832885',
                'cirn': final_cirn
            },
            'message': 'Legacy dam-transfer executed successfully in mock mode'
        }
    else:
        try:
            mock_mode = get_variable('mock_mode')
            final_cirn = cirn if cirn else clid

            set_variable('agent_id', 'BBM')
            set_variable('account_type', 'B')
            set_variable('cti_at', 'BUSMENU')
            set_variable('cti_rt', 'business_account')
            set_variable('cti_sd', '8000212355')
            set_variable('department_id', '955')
            set_variable('va_ibm_id', 'BCE_Entry')
            set_variable('agent_id', '0f67e50b-0b7d-4e9c-9ebe-50557aff3f4e')
            set_variable('call_id', 'f12ca3-5a4-a2b-987-463832885')
            set_variable('brand', 'Bell Residential Services')
            set_variable('cirn', final_cirn)

            if mock_mode:
                print('Business logic success (mock)')
                return {'status': 'success', 'data': {'transfer_status': 'mocked_success'}}

            print('Business logic success')
            return {'status': 'success', 'message': 'Legacy dam-transfer executed'}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}