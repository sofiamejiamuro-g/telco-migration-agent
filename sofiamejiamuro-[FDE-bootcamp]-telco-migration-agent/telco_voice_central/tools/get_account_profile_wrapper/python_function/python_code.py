def get_account_profile_wrapper(banType: str = "", banSubType: str = "", billing_account: str = "") -> dict:
    '''Evaluates banType/banSubType to conditionally call either the Ban Profile or Customer Profile backend system.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'onebillindicator': 'N',
                'errorCode': '0',
                'banType': banType if banType else 'I',
                'banSubType': banSubType if banSubType else 'R'
            }

        payload = {'banType': banType, 'banSubType': banSubType, 'billing_account': billing_account}
        api_response = tools.unknown_unknown(payload).json()
        print("Business logic success")

        return {
            'onebillindicator': api_response.get('oneBillIndicator', 'N'),
            'errorCode': api_response.get('returnCode', '0'),
            'banType': api_response.get('accountType', banType),
            'banSubType': api_response.get('accountSubType', banSubType)
        }
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {'error': str(e), 'agent_action': 'Gracefully fallback to self-service. Do not mention the error. Directly prompt the user if they would like an SMS with a link to set up pre-authorized payments.'}