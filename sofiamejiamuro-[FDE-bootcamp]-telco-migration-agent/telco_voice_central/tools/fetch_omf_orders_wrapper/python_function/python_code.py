def fetch_omf_orders_wrapper(lob: str, account_identifier: str) -> dict:
    '''Webhook Wrapper. Fetches OMF order summaries based on LOB. Mock mode enabled natively.'''
    try:
        mock_mode = get_variable("mock_mode")
        sanitized_lob = lob.lower().strip()

        if mock_mode:
            dummy_orders = [
                {
                    "orderIdentifier": "OMF-987654321",
                    "status": "OPEN",
                    "dispatchStatus": "SCHEDULED",
                    "appointmentDate": "2024-05-20",
                    "appointmentTimeWindow": "08:00 AM - 12:00 PM",
                    "serviceAttributes": [
                        {
                            "lineOfBusiness": sanitized_lob,
                            "serviceType": "INTERNET",
                            "action": "INSTALL"
                        }
                    ]
                }
            ]
            set_variable('count_entities', len(dummy_orders))
            print("Business logic success")
            return {"status": "success", "order_summaries": dummy_orders, "n_omf_tickets": len(dummy_orders)}

        payload = {"lob": sanitized_lob, "account_identifier": account_identifier}
        api_response = tools.OMF_Order_Summary_fetch(payload).json()

        order_summaries = api_response.get("order_summaries", [])
        n_omf_tickets = len(order_summaries)
        set_variable('count_entities', n_omf_tickets)

        print("Business logic success")
        return {"status": "success", "order_summaries": order_summaries, "n_omf_tickets": n_omf_tickets}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the user that we cannot retrieve their orders right now and offer to transfer them to a representative."}