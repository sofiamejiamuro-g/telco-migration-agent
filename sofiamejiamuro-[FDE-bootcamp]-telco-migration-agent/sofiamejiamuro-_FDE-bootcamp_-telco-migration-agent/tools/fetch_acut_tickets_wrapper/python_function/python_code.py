def fetch_acut_tickets_wrapper(lob: str, account_identifier: str, ticket_state: str, language: str) -> dict:
    '''Webhook Wrapper. Fetches ACUT tickets and formats dates natively. Mock mode enabled.'''
    import datetime
    try:
        mock_mode = get_variable("mock_mode")
        sanitized_lob = lob.lower().strip()
        safe_state = ticket_state.lower().strip()
        safe_lang = language.lower().strip() if language else "en"

        if mock_mode:
            dummy_creation_date = datetime.datetime.now().strftime("%Y-%m-%d")
            dummy_appointment_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
            fmt_date_mock = datetime.datetime.strptime(dummy_creation_date, "%Y-%m-%d").strftime("%A, %B %d")

            dummy_tickets = [
                {
                    "acut_trouble_ticket_number": "ACT987654321",
                    "ticket_state_category": "OPEN",
                    "dispatch_status": "SCHEDULED",
                    "ticket_creation_time": dummy_creation_date,
                    "appointment_date": dummy_appointment_date,
                    "appointment_time_slot": "08:00 AM - 12:00 PM",
                    "service_type": "Repair"
                }
            ]
            set_variable('n_acut_tickets', len(dummy_tickets))
            formatted_tickets = [f"Ticket ACT987654321 created on {fmt_date_mock}"]

            print("Business logic success (Mock Mode)")
            return {
                "status": "success",
                "ticket_summaries": dummy_tickets,
                "formatted_tickets": formatted_tickets
            }

        payload = {"lob": sanitized_lob, "account_identifier": account_identifier, "ticket_state": safe_state}
        api_response = tools.ACUT_Ticket_Search_find(payload).json()

        ticket_summaries = api_response.get("ticket_summaries", [])
        set_variable('n_acut_tickets', len(ticket_summaries))

        formatted_tickets = []
        for ticket in ticket_summaries:
            raw_date = ticket.get("ticket_creation_time", "")
            tkt_num = ticket.get("acut_trouble_ticket_number", "Unknown")
            try:
                if len(raw_date) >= 10:
                    dt = datetime.datetime.strptime(raw_date[:10], "%Y-%m-%d")
                    fmt_date = dt.strftime("%A, %B %d")
                else:
                    fmt_date = raw_date
            except Exception:
                fmt_date = raw_date

            formatted_tickets.append(f"Ticket {tkt_num} created on {fmt_date}")

        print("Business logic success")
        return {"status": "success", "ticket_summaries": ticket_summaries, "formatted_tickets": formatted_tickets}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Inform the user that ticket retrieval failed due to technical issues and offer to transfer them to a representative."}