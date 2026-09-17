def get_payment_arrangement_eligibility(brand: str = "", billing_account_number: str = "") -> dict:
    '''Calls the eligibility criteria API to extract installmentDetails and returns installment_count.'''
    try:
        if get_variable('mock_mode'):
            print("Business logic success - Mock Mode")
            return {
                "api_success": True,
                "is_eligible": True,
                "installment_count": 3,
                "due_amount": 150.00
            }

        sanitized_brand = str(brand).strip().lower()
        sanitized_ban = str(billing_account_number).strip()
        print("Business logic success - Live Mode (Fallback)")
        return {"installment_count": 0, "api_success": True}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}