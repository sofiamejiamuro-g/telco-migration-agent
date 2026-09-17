def format_balance_and_date_presentation(raw_last_payment_date: str = '', raw_last_payment_amount: str = '', raw_account_balance: str = '') -> dict:
    '''State Manipulator. Formats dates, checks balance logic, sets state routing flags.'''
    import json

    if get_variable("mock_mode"):
        return {
            'fr_date': '15-08',
            'en_date': '08-15',
            'is_balance_zero': False,
            'has_payment': True,
            'recommended_next_route': 'bell_payment_pitch_one_time_CC_payment_2'
        }
    else:
        try:
            date_str = str(raw_last_payment_date).strip()
            amt_str = str(raw_last_payment_amount).strip()
            bal_str = str(raw_account_balance).strip()

            amount = float(amt_str) if amt_str and amt_str.replace('.', '', 1).replace('-', '', 1).isdigit() else 0.0
            balance = float(bal_str) if bal_str and bal_str.replace('.', '', 1).replace('-', '', 1).isdigit() else 0.0

            is_balance_zero = balance <= 0.0
            has_payment = amount > 0.0

            fr_date = ''
            en_date = ''
            if date_str and len(date_str) >= 10:
                parts = date_str[:10].split('-')
                if len(parts) == 3:
                    en_date = f'{parts[1]}-{parts[2]}'
                    fr_date = f'{parts[2]}-{parts[1]}'

            set_variable('date_formatted', fr_date)
            set_variable('date_formatted', en_date)
            set_variable('boolean_flag', is_balance_zero)
            set_variable('boolean_flag', has_payment)

            route = 'bell_Feedback' if is_balance_zero else 'bell_payment_pitch_one_time_CC_payment_2'

            print('Business logic success: formatted dates and calculated route')
            return {'fr_date': fr_date, 'en_date': en_date, 'is_balance_zero': is_balance_zero, 'has_payment': has_payment, 'recommended_next_route': route}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Fall back to general routing and politely offer to text the customer their details.'}