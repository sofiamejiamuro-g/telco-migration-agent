def evaluate_collection_status(account_balance: float = 0.0, past_due_amount: float = 0.0, special_status: str = '') -> dict:
    """State Manipulator. Evaluates collection logic and returns routing directive."""
    if get_variable("mock_mode"):
        return {
            'directive': 'NO_CHANGE_REMAINING',
            'updated_account_balance': 150.00
        }
    else:
        import logging
        logger = logging.getLogger(__name__)
        try:
            outcome = 'DEFAULT'
            updated_balance = account_balance
            sanitized_status = str(special_status).strip().lower()
            target_statuses = ['bell_col_sus', 'bell_col_aul', 'bell_col_delinquent']
            if sanitized_status not in target_statuses:
                if account_balance == 0:
                    outcome = 'NO_CHANGE_PAID_UP'
                elif account_balance > 0:
                    outcome = 'NO_CHANGE_REMAINING'
                elif account_balance < 0:
                    outcome = 'NO_CHANGE_CREDIT'
                    updated_balance = abs(account_balance)
                    set_variable('accountBalance', updated_balance)
            else:
                if past_due_amount > 0:
                    outcome = 'PITCH_PACC'
                else:
                    if sanitized_status in target_statuses:
                        outcome = 'PITCH_PACC'
                    else:
                        outcome = 'DEFAULT'
            print('Business logic success')
            return {'directive': outcome, 'updated_account_balance': updated_balance}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Inform user that status evaluation failed.'}