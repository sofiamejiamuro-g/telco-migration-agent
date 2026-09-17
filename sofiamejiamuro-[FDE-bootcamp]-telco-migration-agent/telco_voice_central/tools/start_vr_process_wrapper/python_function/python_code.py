def start_vr_process_wrapper(service_id: str = "") -> dict:
    '''Webhook Wrapper & State Manipulator: Executes the VR start-process request natively.'''
    import json

    if get_variable('mock_mode'):
        set_variable('vr_context', {
            'session_id': 'VR-MOCK-12345',
            'status': 'started',
            'mocked_task': 'true',
            'vr_type': 'initialization'
        })
        set_variable('boolean_flag', True)
        set_variable('loop_counter', 0)
        set_variable('prev_ms_dcx_action_code', '')
        set_variable('dcx_action_code', '')
        set_variable('prev_cda_dcx_action_code', '')
        set_variable('faq_question_answer', '')
        set_variable('vr_no_input', False)
        set_variable('6590_customer_answer1_id', '')
        return {
            'status': 'success',
            'agent_action': 'Route to bell_vr_next_task',
            'mock_mode_execution': True,
            'service_id': service_id,
            'message': 'Virtual Repair process started successfully in mock mode.'
        }
    else:
        try:
            sanitized_service_id = str(service_id).strip()
            payload = {'service_id': sanitized_service_id}
            api_response = tools.bell_vr_start_process(payload).json()
            print('Business logic success')

            webhook_success = str(api_response.get('webhook_success', 'false')).lower()
            if webhook_success == 'true':
                set_variable('vr_context', api_response.get('vr_context', {}))
                set_variable('boolean_flag', True)
                set_variable('loop_counter', 0)
                set_variable('prev_ms_dcx_action_code', '')
                set_variable('dcx_action_code', '')
                set_variable('prev_cda_dcx_action_code', '')
                set_variable('faq_question_answer', '')
                set_variable('vr_no_input', False)
                set_variable('6590_customer_answer1_id', '')
                return {'status': 'success', 'agent_action': 'Route to bell_vr_next_task'}
            else:
                return {'status': 'failure', 'error': 'API returned webhook_success=false'}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'status': 'failure', 'agent_action': 'Inform the user about the error and escalate.'}