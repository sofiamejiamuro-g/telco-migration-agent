def validate_and_set_payment_amount(raw_amount: str) -> dict:
    '''State Manipulator. Validates if the payment amount is between $1 and $10,000.'''
    if get_variable("mock_mode"):
        mock_amount = 150.0
        try:
            sanitized = str(raw_amount).replace('$', '').replace(',', '').strip()
            parsed = float(sanitized)
            if 1 <= parsed <= 10000:
                mock_amount = parsed
        except ValueError:
            pass
        set_variable('clp_amount_paid', mock_amount)
        set_variable('cc_invalid_counter', 0)
        return {'valid': True, 'clp_bad_amount': 0, 'amount': mock_amount}
    else:
        try:
            sanitized_arg = str(raw_amount).replace('$', '').replace(',', '').strip()
            try:
                amount = float(sanitized_arg)
            except ValueError:
                amount = -1.0

            if 1 <= amount <= 10000:
                set_variable('clp_amount_paid', amount)
                set_variable('cc_invalid_counter', 0)
                print('Business logic success: Valid payment amount')
                return {'valid': True, 'clp_bad_amount': 0, 'amount': amount}
            else:
                bad_amount_count = get_variable('cc_invalid_counter')
                if not isinstance(bad_amount_count, (int, float)):
                    bad_amount_count = 0
                bad_amount_count += 1
                set_variable('cc_invalid_counter', bad_amount_count)
                print(f'Business logic success: Invalid payment amount. Failure count: {bad_amount_count}')
                return {'valid': False, 'clp_bad_amount': bad_amount_count}

        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Inform the user that there was a problem checking the amount, and ask them to repeat how much they would like to pay.'}