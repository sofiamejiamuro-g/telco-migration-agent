def execute_dam_transfer_wrapper(dam_id: str = "", route_intent: str = "") -> dict:
    """Executes the DAM transfer by mapping dam_id to API parameters."""
    import json
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'transfer_payload': {
                    'dam_id': dam_id.strip().upper() if dam_id else 'BBM',
                    'route': route_intent or 'BILLING_PAYMENT_INTENT',
                    'brand': 'Bell Mobility',
                    'department': '955',
                    'account_type': 'B',
                    'cti_at': 'BUSMENU'
                }
            }

        sanitized_id = dam_id.strip().upper()
        transfer_payload = {'dam_id': sanitized_id, 'route': route_intent}

        if sanitized_id == 'BBM':
            transfer_payload.update({'brand': 'Bell Mobility', 'department': '955', 'account_type': 'B', 'cti_at': 'BUSMENU'})
        elif sanitized_id == 'ATLMAIN':
            transfer_payload.update({'brand': 'Bell Aliant', 'department': '7020', 'account_type': 'R', 'cti_at': 'ALNTMMA'})
        elif sanitized_id == 'MTSMAIN':
            transfer_payload.update({'brand': 'Bell MTS', 'department': '6102', 'account_type': 'R', 'cti_at': 'A2AMM'})
        elif sanitized_id == 'ATLBILL':
            transfer_payload.update({'brand': 'Bell Aliant', 'department': '7020', 'account_type': 'R', 'cti_at': 'ALNTMMA'})
        elif sanitized_id == 'MTSBILL':
            transfer_payload.update({'brand': 'Bell MTS', 'department': '6102', 'account_type': 'R', 'cti_at': 'A2AMM'})

        print(f"Business logic success for dam_id: {sanitized_id}")
        return {'status': 'success', 'transfer_payload': transfer_payload}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {'error': str(e), 'agent_action': 'Apologize and inform the user the transfer failed, then provide the appropriate fallback phone number.'}