def reschedule_wfas_appointment_bundled(selected_date: str = '', selected_start_time: str = '', selected_end_time: str = '', selected_interval_name: str = '') -> dict:
    '''Webhook Wrapper. Books the appointment in WFAS and updates ACUT.'''
    try:
        if get_variable('mock_mode'):
            print('Business logic success - Mock Mode')
            return {
                'status': 'success',
                'data': {
                    'rescheduled': True,
                    'confirmation_number': 'WFAS-9988776655',
                    'appointment_details': {
                        'date': selected_date if selected_date else '2023-11-20',
                        'start_time': selected_start_time if selected_start_time else '08:00',
                        'end_time': selected_end_time if selected_end_time else '12:00',
                        'interval_name': selected_interval_name if selected_interval_name else 'MORNING',
                        'status': 'SCHEDULED'
                    },
                    'message': 'Appointment successfully rescheduled in WFAS and ACUT updated.'
                }
            }

        payload = {'selected_date': str(selected_date), 'selected_start_time': str(selected_start_time), 'selected_end_time': str(selected_end_time), 'selected_interval_name': str(selected_interval_name)}
        api_response = tools.appointment_appointment(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them.'}