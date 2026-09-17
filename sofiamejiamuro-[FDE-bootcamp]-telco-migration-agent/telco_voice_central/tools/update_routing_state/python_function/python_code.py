def update_routing_state(identified_route: str = "", is_no_match: bool = False, start_over_type: str = "") -> dict:
    """Updates routing state, looping counters, and handles no-match or start-over events."""
    if get_variable("mock_mode"):
        return {
            "status": "success",
            "route": identified_route.strip() if identified_route.strip() else "BillingAndPaymentsAgent",
            "previous_route": "",
            "query_rewriter_looping_counter": 0,
            "no_match_retry_count": 0,
            "message": "Mock mode: Routing state successfully updated."
        }

    try:
        # Handle Start Over Logic
        sanitized_start = start_over_type.lower().strip().replace('_', ' ')
        if "full" in sanitized_start:
            set_variable("routing_val", "full start over")
            print("State updated: event_type set to full start over")
        elif "partial" in sanitized_start or "start over" in sanitized_start:
            set_variable("routing_val", "partial start over")
            print("State updated: event_type set to partial start over")

        # Handle No Match Logic
        if is_no_match or identified_route.lower().strip() == "no_intent":
            current_no_match = int(get_variable("no_match_counter") or 0)
            new_no_match = current_no_match + 1
            set_variable("no_match_counter", new_no_match)
            print(f"State updated: no_match_retry_count incremented to {new_no_match}")
            return {"status": "success", "no_match_retry_count": new_no_match, "message": "No match logic applied."}

        # Handle Normal Route & Looping Logic
        sanitized_route = identified_route.strip()
        if sanitized_route:
            set_variable("route", sanitized_route)
            prev_route = get_variable("previous_route") or ""
            loop_count = int(get_variable("loop_counter") or 0)

            if prev_route == sanitized_route:
                loop_count += 1
            else:
                loop_count = 0
                set_variable("previous_route", sanitized_route)

            set_variable("loop_counter", loop_count)
            print(f"State updated: route set to {sanitized_route}, loop count is {loop_count}")
            return {
                "status": "success",
                "route": sanitized_route,
                "previous_route": get_variable("previous_route"),
                "query_rewriter_looping_counter": loop_count
            }

        return {"status": "success", "message": "No explicit changes made."}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the user that a technical error occurred while trying to route their request, and offer to transfer them to a human representative."}