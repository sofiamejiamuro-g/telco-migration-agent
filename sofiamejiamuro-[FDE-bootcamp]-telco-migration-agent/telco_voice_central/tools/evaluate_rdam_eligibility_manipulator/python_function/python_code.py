def evaluate_rdam_eligibility_manipulator(route_intent: str = "") -> dict:
    """Evaluates if the route is eligible for RDAM based on a hardcoded list of billing/payment intents."""
    import logging
    logger = logging.getLogger(__name__)

    if get_variable("mock_mode"):
        is_not_eligible = False
        set_variable('not_eligible_for_rdam', is_not_eligible)
        print(f"[MOCK MODE] RDAM Eligibility checked: not_eligible_for_rdam = {is_not_eligible}")
        return {
            'status': 'success',
            'not_eligible_for_rdam': is_not_eligible
        }

    try:
        non_eligible_intents = [
            'bill_charge_inquiry', 'payment_setup_autopay', 'payment_update_autopay',
            'payment_cancel_autopay', 'payment_auto_payment_status', 'payment_setup_payment_arrangements',
            'payment_update_payment_arrangements', 'payment_make_payment', 'bill_view_bill',
            'bill_add_promo', 'bill_inquire_promo', 'bill_change_bill_cycle',
            'bill_confirm_due_date', 'bill_missing_promo', 'bill_dispute_bill',
            'bill_switch_format', 'bill_missing_bill', 'bill_contract_terms',
            'bill_device_balance', 'bill_credit_report_inquiry', 'bill_remove_service_charge',
            'bill_unexpected_after_cancel', 'bill_unexpected_after_suspend', 'bill_promo_expired',
            'bill_deposit_inquiry', 'payment_restore_service', 'bill_reduce_plan',
            'payment_request_refund', 'payment_not_processing'
        ]
        sanitized_intent = route_intent.strip().lower()
        is_not_eligible = sanitized_intent in non_eligible_intents
        set_variable('not_eligible_for_rdam', is_not_eligible)
        print(f"RDAM Eligibility checked: not_eligible_for_rdam = {is_not_eligible}")
        return {'status': 'success', 'not_eligible_for_rdam': is_not_eligible}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {'error': str(e), 'agent_action': 'Route user normally as RDAM eligibility evaluation failed.'}