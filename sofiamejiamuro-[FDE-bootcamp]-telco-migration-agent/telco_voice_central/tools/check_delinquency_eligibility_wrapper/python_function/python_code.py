def check_delinquency_eligibility_wrapper(billing_account_number: str) -> dict:
    '''Webhook Wrapper & State Manipulator. Bundles legacy delinquency and eligibility criteria. Calculates and sets 'is_delinquent', 'is_eligible', and 'installment_count'.'''
    import json
    try:
        if get_variable("mock_mode"):
            set_variable("special_status", True)
            set_variable("is_eligible", True)
            set_variable("count_entities", 0)
            print("Business logic success")
            return {
                "is_delinquent": True,
                "is_eligible": True,
                "installment_count": 0,
                "api_success": True,
                "webhook_success": True
            }
        else:
            sanitized_ban = billing_account_number.strip()
            is_delinquent = False
            is_eligible = False
            installment_count = 0

            payload = {"billing_account_number": sanitized_ban}
            delinq_res = tools.payment_arrangement_get_delinquency_details(payload).json()
            records = delinq_res if isinstance(delinq_res, list) else delinq_res.get("data", [])
            for rec in records:
                if rec.get("accountNumber") == sanitized_ban:
                    is_delinquent = rec.get("delinquentStatus", False)
                    break

            if is_delinquent:
                elig_res = tools.payment_arrangement_get_eligibility_criteria(payload).json()
                is_eligible = elig_res.get("showPaymentArrangementLink", False)
                installment_count = len(elig_res.get("installmentDetails", []))

            set_variable("special_status", is_delinquent)
            set_variable("is_eligible", is_eligible)
            set_variable("count_entities", installment_count)
            print("Business logic success")
            return {"is_delinquent": is_delinquent, "is_eligible": is_eligible, "installment_count": installment_count}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that the system is unable to proceed and offer to send a text message with a MyBell setup link to their device."}