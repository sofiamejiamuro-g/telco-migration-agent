def process_one_time_payment(payment_amount: float = 0.0) -> dict:
    """Webhook Wrapper. Bundles cc-payment-details and submit-order logic."""
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'isValid': True,
                'auth_status': 'Success',
                'confirmationNo': 'BCA-1029384756',
                'errorCodeID': '',
                'status': 'success',
                'transactionId': 'TXN987654321',
                'payment_amount': payment_amount,
                'message': 'Payment processed successfully.'
            }
        else:
            payload = {'payment_amount': payment_amount}
            result = tools.process_payment_composite_process_one_time_payment(payload).json()
            print('Business logic success')
            return {'isValid': result.get('isValid', True), 'auth_status': result.get('auth_status', 'Success'), 'confirmationNo': result.get('confirmationNo', ''), 'errorCodeID': result.get('errorCodeID', '')}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'status': 'system_unavailable', 'agent_action': 'Politely apologize for the technical issue and ask if they would like an SMS with a link to the MyBell app.'}