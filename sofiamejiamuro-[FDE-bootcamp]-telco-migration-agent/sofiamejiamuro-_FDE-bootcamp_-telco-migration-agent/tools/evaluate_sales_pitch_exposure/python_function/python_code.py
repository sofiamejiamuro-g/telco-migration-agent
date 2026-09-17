def evaluate_sales_pitch_exposure() -> dict:
    '''State/Variable Manipulator. Triggers upfront sales pitch randomly if queue is open.'''
    if get_variable("mock_mode"):
        set_variable('boolean_flag', True)
        return {'status': 'success', 'trigger_sales_pitch': True}
    else:
        import datetime
        import random
        try:
            now = datetime.datetime.now()
            is_weekday = now.weekday() < 5
            current_hour = now.hour
            sales_queue_open = False
            if current_hour >= 9:
                if (is_weekday and current_hour < 19) or (not is_weekday and current_hour < 18):
                    sales_queue_open = True
            trigger_sales_pitch = False
            if sales_queue_open:
                wml_eligible = get_variable('wml_eligible')
                exposure_roll = random.randint(1, 100)
                pitch_exposure_rate = 100
                if exposure_roll <= pitch_exposure_rate and wml_eligible:
                    trigger_sales_pitch = True
            set_variable('boolean_flag', trigger_sales_pitch)
            print('Business logic success')
            return {'status': 'success', 'trigger_sales_pitch': trigger_sales_pitch}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Skip the sales pitch and proceed to general routing.'}