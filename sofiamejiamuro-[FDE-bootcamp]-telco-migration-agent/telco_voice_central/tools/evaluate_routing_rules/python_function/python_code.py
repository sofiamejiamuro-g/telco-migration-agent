def evaluate_routing_rules(route: str = "", force_ss_exception: str = "") -> dict:
    '''State Manipulator: Evaluates legacy conditional logic to determine routing eligibility.'''
    if get_variable("mock_mode"):
        return {
            'is_ssr_eligible': True,
            'is_billing_intent': False
        }

    try:
        sanitized_route = str(route).lower().strip()
        sanitized_exception = str(force_ss_exception).lower().strip()

        ssr_routes = {
            'account_link_accounts', 'account_restore_service', 'account_suspend_service',
            'account_update_details', 'bill_contract_terms', 'bill_view_bill',
            'equipment_order_status', 'equipment_report_lost_device', 'equipment_upgrade_device',
            'payment_auto_payment_status', 'payment_cancel_autopay', 'payment_confirm_made',
            'payment_make_payment', 'payment_report_made', 'payment_restore_service',
            'payment_setup_autopay', 'payment_setup_payment_arrangements', 'payment_update_autopay',
            'service_add_feature', 'service_change_plan', 'service_remove_feature',
            'tech_change_appointment', 'tech_field_tech_visit_cancel', 'tech_field_tech_visits',
            'tech_voicemail_password_reset'
        }

        billing_intents = {
            'bill_amount_due', 'bill_confirm_due_date', 'bill_view_bill', 'bill_missing_bill',
            'bill_account_balance', 'bill_credit_report_inquiry', 'bill_deposit_inquiry',
            'bill_switch_format', 'payment_auto_payment_status', 'payment_cancel_autopay',
            'payment_confirm_made', 'payment_make_payment', 'payment_not_processing',
            'payment_report_made', 'payment_restore_service', 'payment_setup_autopay',
            'payment_setup_payment_arrangements', 'payment_update_autopay',
            'payment_update_payment_arrangements', 'payment_vague'
        }

        is_ssr_eligible = sanitized_route in ssr_routes
        if sanitized_route in ['tech_service_outage', 'tech_connection_issue'] and sanitized_exception == 'yes':
            is_ssr_eligible = True

        is_billing_intent = sanitized_route in billing_intents

        print('evaluate_routing_rules success')
        return {
            'is_ssr_eligible': is_ssr_eligible,
            'is_billing_intent': is_billing_intent
        }
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {'error': str(e), 'agent_action': 'Politely inform the user that routing evaluation failed and transfer them to an agent.'}