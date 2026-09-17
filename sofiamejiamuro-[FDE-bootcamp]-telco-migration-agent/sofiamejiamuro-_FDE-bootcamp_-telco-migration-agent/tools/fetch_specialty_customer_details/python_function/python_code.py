def fetch_specialty_customer_details(telephone_number: str) -> dict:
    '''Webhook Wrapper. Fetches customer profile and SOC info based on TN.'''
    import json
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                'status': 'success',
                'data': {
                    'customer_profile': {
                        'firstName': 'Jane',
                        'lastName': 'Doe',
                        'ban': '314159265',
                        'banStatus': 'O',
                        'statActvRsnCode': 'ACTV',
                        'siOwner': 'COM1',
                        'arBalance': '0.00',
                        'accountType': 'I',
                        'subType': 'R'
                    },
                    'soc_info': [
                        {
                            'soc': 'AULDATA',
                            'description': 'Unlimited Data',
                            'effDate': '2023-01-01T00:00:00Z'
                        },
                        {
                            'soc': 'ITP_SOC',
                            'description': 'International Travel Pass',
                            'effDate': '2024-01-01T00:00:00Z'
                        }
                    ],
                    'billing_accounts': [
                        {
                            'billing_account_number': '314159265',
                            'services': [
                                {
                                    'service_type': 'MOBILITY',
                                    'is_prepaid': False,
                                    'status': 'A'
                                }
                            ]
                        }
                    ],
                    'delinquent_flag': False
                }
            }

        payload = {'telephone_number': telephone_number}
        result = tools.customer_identification_search_by_tn(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative.'}