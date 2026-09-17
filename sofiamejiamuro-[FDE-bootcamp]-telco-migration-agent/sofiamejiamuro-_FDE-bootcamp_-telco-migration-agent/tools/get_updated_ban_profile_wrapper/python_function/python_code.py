def get_updated_ban_profile_wrapper(ban_number: str = '') -> dict:
    '''Webhook Wrapper: Fetches the BAN profile to retrieve updated balances and limits.'''
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            clp_bal = 100.0
            clp_aul = 150.0
            clp_sus = 300.0
            past_due = 0.0

            set_variable('clp_balance', clp_bal)
            set_variable('clp_limit', clp_aul)
            set_variable('clp_limit', clp_sus)
            set_variable('past_due_amount', past_due)

            mock_data = {
                'curSpendingLimitBal': clp_bal,
                'aul_threshold': clp_aul,
                'sus_threshold': clp_sus,
                'pastDueAmount': past_due,
                'accountStatus': 'Open',
                'clpProgram': True
            }
            print('get_updated_ban_profile_wrapper success (mock mode)')
            return {'status': 'SUCCESS', 'data': mock_data}

        payload = {'ban_number': ban_number}
        api_response = tools.ban_profile_get_ban_profile(payload).json()
        clp_bal = api_response.get('curSpendingLimitBal', 0.0)
        clp_aul = api_response.get('aul_threshold', 0.0)
        clp_sus = api_response.get('sus_threshold', 0.0)
        past_due = api_response.get('pastDueAmount', 0.0)
        set_variable('clp_balance', clp_bal)
        set_variable('clp_limit', clp_aul)
        set_variable('clp_limit', clp_sus)
        set_variable('past_due_amount', past_due)
        print('get_updated_ban_profile_wrapper success')
        return {'status': 'SUCCESS', 'data': api_response}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'result': {'error': str(e)}, 'agent_action': 'Explain the technical difficulty and guide the conversational path to feedback.'}