def prepare_route_parameters(dcx_action_code: str, kickout_response: str) -> dict:
    '''State Manipulator Tool to evaluate dcx_action_code, configure session variables, and return the target agent.'''
    if get_variable("mock_mode"):
        return {
            "status": "success",
            "target_agent": "bell_vr_kickout_sms"
        }

    try:
        code = str(dcx_action_code).strip()
        target_agent = "bell_aqd"

        if code in ["7011", "7012", "7013", "7100", "7101"]:
            target_agent = "bell_aqd"
        elif code == "7004":
            target_agent = "bell_tech_service_outage_connection_issue_main"
            set_variable("vr_outcome", "dispatch")
            set_variable("from_flow", "bell_vr_kickout")
        elif code == "7000":
            target_agent = "bell_Feedback"
        elif code in ["7016", "7029", "7030", "7028"]:
            target_agent = "bell_vr_kickout_sms"
            set_variable("generative_utterance", str(kickout_response))
        elif code == "7015":
            target_agent = "bell_Feedback"
        else:
            target_agent = "bell_aqd"
            set_variable("hardstop", True)
            set_variable("page_id", "0c22e956-3a89-41eb-a48f-a23412ec5748")
            set_variable("flow_id", "e75403f7-98e1-4a47-9d85-4cc4dd354540")
            set_variable("page_name", "Routing")

        print(f"Evaluated action code {code}, routing to {target_agent}")
        return {"status": "success", "target_agent": target_agent}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the user that a routing error occurred and you will transfer them to a representative."}