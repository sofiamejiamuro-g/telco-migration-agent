def evaluate_mya_eligibility(service_identifier: str = "") -> dict:
    '''Retrieves service ID, calls MYA info backend, and sets routing variables based on eligibility.'''
    if get_variable("mock_mode"):
        set_variable("mya_eligible", True)
        set_variable("mya_link", "https://mybell.bell.ca/manage-appointment/mock_12345")
        set_variable("route", "tech_change_appointment_mya_true")
        return {
            "status": "success",
            "mya_eligible": True
        }
    else:
        try:
            if not service_identifier:
                billing_info = get_variable("billing_account_info_list") or {}
                services = billing_info.get("services", [])
                if services:
                    service_identifier = services[0].get("service_id", "")

            payload = {"service_identifier": service_identifier}
            api_response = tools.mya_information_mya_information(payload).json()
            print("Business logic success: MYA API called")

            notifications = api_response.get("notification", [])
            mya_links = [n.get("MYAApplicationUrl") for n in notifications if n.get("MYAApplicationUrl")]

            if len(mya_links) > 0:
                set_variable("mya_eligible", True)
                set_variable("mya_link", mya_links[0])
                set_variable("route", "tech_change_appointment_mya_true")
            else:
                set_variable("mya_eligible", False)
                set_variable("route", "tech_change_appointment_mya_false")

            return {"status": "success", "mya_eligible": len(mya_links) > 0}

        except Exception as e:
            logger.error(f"Crash: {e}")
            set_variable("route", "tech_change_appointment_mya_false")
            return {"error": str(e), "agent_action": "Inform the customer that we could not retrieve appointment details due to a system issue, and proceed with the fallback flow."}