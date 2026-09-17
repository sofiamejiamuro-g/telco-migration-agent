def execute_pacc_enrollment() -> dict:
    '''Bundles the create-order and cc-payment-details sequence into a single atomic operation.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            set_variable('webhook_success', True)
            set_variable('transaction_id', 'OFI-9876543210')
            set_variable('cc_token', 'TKN-5555-4444-3333-2222')
            print('Business logic success - Mock PACC Enrollment')
            return {
                'status': 'success',
                'transaction_id': 'OFI-9876543210',
                'cc_token': 'TKN-5555-4444-3333-2222',
                'message': 'Pre-authorized credit card enrollment processed successfully.'
            }

        expiry_date = str(get_variable('expiry_date', ''))
        expiry_month = expiry_date[:2] if len(expiry_date) >= 2 else ''
        expiry_year = expiry_date[2:4] if len(expiry_date) >= 4 else ''
        card_number = get_variable('card_number')
        cvv_number = get_variable('cvv_number')

        create_payload = {'card_number': card_number}
        create_response = tools.pre_auth_payment_create_order(create_payload).json()
        transaction_id = create_response.get('OrderFormId', 'UNKNOWN_ORDER')

        payment_payload = {
            'transaction_id': transaction_id,
            'expiry_month': expiry_month,
            'expiry_year': expiry_year,
            'security_code': cvv_number
        }
        payment_response = tools.pre_auth_payment_cc_payment_details(payment_payload).json()
        cc_token = payment_response.get('cc_token', 'UNKNOWN_TOKEN')

        set_variable('webhook_success', True)
        set_variable('transaction_id', transaction_id)
        set_variable('cc_token', cc_token)

        print('Business logic success')
        return {'status': 'success', 'transaction_id': transaction_id, 'cc_token': cc_token}
    except Exception as e:
        logger.error(f'Crash: {e}')
        set_variable('webhook_success', False)
        return {'error': str(e), 'agent_action': 'Inform the customer that the system is having trouble. Ask if they would like an SMS sent to their device to sign up for pre-authorized payments in the MyBell App.'}