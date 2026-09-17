def reset_counters_manipulator() -> dict:
    '''State/Variable Manipulator. Initializes necessary conversational session variables to 0.'''
    if get_variable("mock_mode"):
        return {
            "status": "success",
            "agent_action": "Route to bell_SMS Trigger flow immediately without prompting the user."
        }
    else:
        try:
            set_variable('SMS_Counter', 0)
            set_variable('loop_counter', 0)
            set_variable('More_Time_Counter', 0)
            set_variable('Mistake_Counter', 0)
            set_variable('loop_counter', 0)
            set_variable('no_input_counter', 0)
            set_variable('repeat_counter', 0)
            print("Business logic success: Counters reset successfully")
            return {"status": "success", "agent_action": "Route to bell_SMS Trigger flow immediately without prompting the user."}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}