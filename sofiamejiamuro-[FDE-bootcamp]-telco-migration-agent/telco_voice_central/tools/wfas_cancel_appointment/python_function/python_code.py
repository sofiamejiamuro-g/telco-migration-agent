def wfas_cancel_appointment(ticket_number: str = "") -> dict:
    '''Webhook Wrapper. Cancels the active WFAS transaction.'''
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            return {
                "success": True,
                "webhook_success": True,
                "result": {
                    "status": "SUCCESS",
                    "message": "WFAS appointment transaction cancelled successfully.",
                    "ticket_number": ticket_number,
                    "transaction_id": "WFAS-CANCEL-99882211",
                    "cancellation_timestamp": "2023-10-14T10:05:00Z"
                }
            }

        payload = {"ticket_number": ticket_number.strip()}
        result = tools.wfas_cancel_wfas_cancel(payload).json()
        print("Business logic success")
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties canceling the transaction and offer to transfer them to a representative."}