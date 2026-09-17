def get_and_evaluate_customer_profile() -> dict:
    '''Fetches customer profile, evaluates CC expiry date and payment method, and sets relevant session variables.'''
    import datetime
    try:
        mock_mode = get_variable('mock_mode')
        cirn = get_variable('CIRN')

        if mock_mode:
            set_variable('Expired_credit_card_check', True)
            set_variable('cc_status', False)
            set_variable('cc_status', 'valid')
            print("Business logic success")
            return {
                "status": "success",
                "data": {
                    "ban": "123456789",
                    "paymentMethod": "C",
                    "ccExpiryDate": "1235",
                    "accountStatus": "O",
                    "language": "en",
                    "firstName": "Jane",
                    "lastName": "Doe",
                    "province": "ON",
                    "account_balance": 150.00
                }
            }

        payload = {"phone": cirn}
        api_response = tools.nm1_get_customer_profile(payload).json()

        set_variable('Expired_credit_card_check', True)

        payment_method = api_response.get('paymentMethod', '')
        expiry_date = str(api_response.get('ccExpiryDate', ''))

        cc_requires_update = False
        cc_expiry_status_message = 'valid'

        if payment_method == 'C' and len(expiry_date) in [3, 4]:
            if len(expiry_date) == 3:
                exp_month = int(expiry_date[0])
                exp_year = int(expiry_date[1:3])
            else:
                exp_month = int(expiry_date[0:2])
                exp_year = int(expiry_date[2:4])

            now = datetime.datetime.now()
            curr_month = now.month
            curr_year = now.year % 100

            if exp_year < curr_year:
                cc_requires_update = True
                cc_expiry_status_message = 'expired'
            elif exp_year == curr_year and exp_month < curr_month:
                cc_requires_update = True
                cc_expiry_status_message = 'expired'
            elif exp_year == curr_year and exp_month == curr_month:
                cc_requires_update = True
                cc_expiry_status_message = 'about to expire'

        set_variable('cc_status', cc_requires_update)
        set_variable('cc_status', cc_expiry_status_message)

        print("Business logic success")
        return {"status": "success", "data": api_response}

    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "The customer profile webhook failed. Immediately bypass the credit card update check and transition directly to EVALUATE_PROPENSITY by calling the evaluate_propensity_to_sell tool."}