def fetch_omf_order_details(lob: str) -> dict:
    '''Webhook Wrapper to fetch OMF order details based on LOB.'''
    try:
        mock_mode = get_variable("mock_mode")
        if mock_mode:
            dummy_data = {
                "requestState": {
                    "orderStatus": "Pending",
                    "statusDate": "2023-10-20T10:00:00Z"
                },
                "bceOrderList": [
                    {
                        "orderId": "BCE123456789",
                        "customerAccountRequests": [{"accountAction": "Create"}],
                        "stateRestrictionList": {"stateRestriction": "null"},
                        "shippingChangesRestricted": "Y",
                        "orderType": "Provide"
                    }
                ],
                "isSiahcc": "Y",
                "fieldWorkFlag": True,
                "customerWorkFlag": False,
                "calendar_context": [
                    {
                        "startTime": "2023-11-01T08:00:00Z",
                        "endTime": "2023-11-01T12:00:00Z",
                        "cutoffTime": "2023-10-31T18:00:00Z",
                        "date": "2023-11-01",
                        "lineOfBusiness": lob,
                        "dispatchStatus": "SCHEDULED"
                    }
                ],
                "OneBoxShippingRequired": "N",
                "earlyTerminationPenalty": False,
                "contains_coded_orders": False,
                "contactInfo": {
                    "primaryPhone": "5551234567",
                    "contactName": "John Doe"
                }
            }
            set_variable("order_detail_response", dummy_data)
            set_variable("webhook_success", True)
            print("Mock order detail data loaded successfully for happy-path execution.")
            return {"status": "success", "data": dummy_data}

        payload = {"lob": lob}
        sanitized_lob = lob.lower().strip() if isinstance(lob, str) else ""

        if sanitized_lob == "homephone":
            api_response = tools.omf_order_detail_api_order_detail_Homephone(payload).json()
        else:
            api_response = tools.omf_order_detail_api_order_detail(payload).json()

        print("Business logic success")
        set_variable("order_detail_response", api_response)
        set_variable("webhook_success", True)
        return {"status": "success", "data": api_response}
    except Exception as e:
        logger.error(f"Crash: {e}")
        set_variable("webhook_success", False)
        return {"error": str(e), "agent_action": "Explain the technical error to the user and transfer them to the technical troubleshooting team."}