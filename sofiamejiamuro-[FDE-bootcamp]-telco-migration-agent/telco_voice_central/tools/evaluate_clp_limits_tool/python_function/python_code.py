def evaluate_clp_limits_tool(clp_balance: float = 0.0, amount_paid: float = 0.0, clp_aul_limit: float = 0.0, clp_sus_limit: float = 0.0, past_due_amount: float = 0.0, previous_special_status: str = '') -> dict:
    '''State Manipulator: Calculates limit evaluations (AUL vs SUS vs Past Due).'''
    if get_variable("mock_mode"):
        set_variable('current_special_status', 'bell_clp_under')
        return {
            'newSpendingLimitBal': 0.0,
            'current_special_status': 'bell_clp_under',
            'routing_instruction': 'ROUTE_TO_PACC',
            'agent_action': 'Follow the routing instruction exactly: ROUTE_TO_PACC'
        }

    try:
        new_spending_limit = float(clp_balance) - float(amount_paid)
        current_special_status = ''
        if new_spending_limit < clp_aul_limit:
            current_special_status = 'bell_clp_under'
        elif new_spending_limit >= clp_sus_limit:
            current_special_status = 'bell_clp_sus'
        else:
            current_special_status = 'bell_clp_aul'
        set_variable('current_special_status', current_special_status)
        routing = 'ROUTE_TO_AQD'
        if previous_special_status == 'bell_clp_under' and current_special_status == 'bell_clp_under':
            routing = 'ROUTE_TO_PACC'
        elif previous_special_status == 'bell_clp_sus' and current_special_status == 'bell_clp_under':
            routing = 'ROUTE_TO_PACC'
        elif previous_special_status == 'bell_clp_aul' and current_special_status == 'bell_clp_under':
            routing = 'ROUTE_TO_PACC'
        elif previous_special_status == 'bell_clp_sus' and current_special_status == 'bell_clp_sus':
            routing = 'ROUTE_TO_PACC'
        elif previous_special_status == 'bell_clp_aul' and current_special_status == 'bell_clp_aul':
            routing = 'ROUTE_TO_PACC'
        elif previous_special_status == 'bell_clp_sus' and current_special_status == 'bell_clp_aul':
            routing = 'ROUTE_TO_PACC'
        elif not previous_special_status or current_special_status == 'bell_clp_under':
            routing = 'ROUTE_TO_PACC'
        print(f'evaluate_clp_limits_tool calculated status: {current_special_status}, routing: {routing}')
        return {'newSpendingLimitBal': new_spending_limit, 'current_special_status': current_special_status, 'routing_instruction': routing, 'agent_action': f'Follow the routing instruction exactly: {routing}'}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'result': {'error': str(e)}, 'agent_action': 'Inform the user that the system encountered an error evaluating their account limits and offer to transfer to a representative.'}