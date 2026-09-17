def evaluate_order_routing_directive() -> dict:
    '''State Manipulator to evaluate order logic and calculate cutoff routing directives.'''
    if get_variable("mock_mode"):
        set_variable("routing_val", "TECH_VISIT")
        return {
            "status": "success",
            "directive": "TECH_VISIT",
            "mock_mode": True,
            "mock_message": "Order routing evaluated successfully in mock mode. Directive set to TECH_VISIT."
        }

    import datetime
    try:
        order_data = get_variable("order_detail_response")
        if not order_data or not isinstance(order_data, dict):
            return {"error": "No order data found", "agent_action": "Route to technical troubleshooting."}

        directive = "UNKNOWN_OR_TECH_ISSUE"
        request_state = order_data.get("requestState", {})
        order_status = request_state.get("ticket_state", "")

        bce_list = order_data.get("bceOrderList", [{}])
        first_bce = bce_list[0] if bce_list else {}
        acct_requests = first_bce.get("customerAccountRequests", [{}])
        account_action = acct_requests[0].get("accountAction", "") if acct_requests else ""

        is_siahcc = order_data.get("isSiahcc", "N")
        field_work = order_data.get("fieldWorkFlag", False)
        customer_work = order_data.get("customerWorkFlag", False)
        onebox_shipping = order_data.get("OneBoxShippingRequired", "N")

        cal_context = order_data.get("calendar_context", [{}])
        first_cal = cal_context[0] if cal_context else {}
        cutoff_time_str = first_cal.get("cutoffTime", "")
        date_str = first_cal.get("date", "")
        early_term = order_data.get("earlyTerminationPenalty", False)
        contains_coded = order_data.get("contains_coded_orders", False)

        if order_status == "HeldInOCS":
            directive = "HELD_ORDER"
        elif account_action == "Create" and is_siahcc == "N" and (field_work or customer_work):
            directive = "TECH_VISIT"
        elif account_action == "Create" and onebox_shipping == "Y":
            directive = "SELF_INSTALL_PENDING_SHIPPING"
        elif account_action == "Create" and is_siahcc == "Y":
            if date_str and cutoff_time_str:
                try:
                    cutoff_date = datetime.datetime.strptime(date_str[:10], "%Y-%m-%d").date()
                    now_utc = datetime.datetime.utcnow()
                    if now_utc.date() > cutoff_date:
                        directive = "AFTER_CUTOFF"
                    elif now_utc.date() < cutoff_date:
                        directive = "BEFORE_CUTOFF"
                    else:
                        now_time_str = now_utc.strftime("%H:%M:%S")
                        if now_time_str > str(cutoff_time_str):
                            directive = "AFTER_CUTOFF"
                        else:
                            directive = "BEFORE_CUTOFF"
                except Exception as e:
                    print(f"Date parsing error: {e}")
                    directive = "AFTER_CUTOFF"
            else:
                directive = "AFTER_CUTOFF"
        elif account_action == "Change":
            directive = "CHANGE_ORDER"
        elif account_action == "Move":
            directive = "MOVE_ORDER"
        elif account_action == "Remove":
            directive = "DISCONNECT_ORDER"
        elif early_term:
            directive = "EARLY_TERMINATION"
        elif contains_coded:
            directive = "CODED_ORDER"

        set_variable("routing_val", directive)
        print(f"Calculated Directive: {directive}")
        return {"status": "success", "directive": directive}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Route to technical troubleshooting due to error evaluating directive."}