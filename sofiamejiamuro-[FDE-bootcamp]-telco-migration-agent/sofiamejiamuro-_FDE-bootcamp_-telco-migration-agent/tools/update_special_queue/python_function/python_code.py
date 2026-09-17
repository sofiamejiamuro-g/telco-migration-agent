def update_special_queue(queue_name: str = "") -> dict:
    '''
    Sets the 'special_queue' session variable to the provided string value.

    Args:
        queue_name (str): The name of the queue to route to (e.g., 'tech_to_care').

    Returns:
        dict: A dictionary containing the status of the operation.
    '''
    if get_variable("mock_mode"):
        sanitized_mock = queue_name.strip() if queue_name else "tech_to_care"
        return {"status": "success", "message": f"special_queue successfully updated to {sanitized_mock}"}
    else:
        try:
            sanitized_queue = queue_name.strip()
            set_variable('special_queue', sanitized_queue)

            print(f"Business logic success: special_queue set to {sanitized_queue}")
            return {"status": "success", "message": f"special_queue successfully updated to {sanitized_queue}"}
        except Exception as e:
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}