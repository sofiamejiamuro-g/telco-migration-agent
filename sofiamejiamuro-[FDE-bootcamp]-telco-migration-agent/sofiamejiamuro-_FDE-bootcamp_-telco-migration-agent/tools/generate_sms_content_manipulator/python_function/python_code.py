def generate_sms_content_manipulator(intent_route: str = "", lang: str = "") -> dict:
    '''State Manipulator generating the appropriate localized SMS content string.'''
    if get_variable("mock_mode"):
        mock_sms = "You can visit https://m.bell.ca/ecviewmybill to view your account details and Monthly Rate Charges in the MyBell app. ( bell.ca/about-us )"
        set_variable('sms_content', mock_sms)
        set_variable('sms_type', 'Public')
        return {
            'status': 'success',
            'sms_content': mock_sms
        }
    else:
        try:
            if not intent_route:
                intent_route = get_variable('route')
            if not lang:
                lang = get_variable('language')

            r = str(intent_route).lower().strip()
            l = str(lang).lower().strip()

            sms = ""
            if r == "bill_contract_terms":
                sms = "Vous pouvez visiter https://m.bell.ca/ecmesententes pour consulter les modalités de votre contrat dans l'application MonBell. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/ecmyagreement to view the terms and conditions of your contract in the MyBell app. ( bell.ca/about-us )"
            elif r == "bill_view_bill":
                sms = "Vous pouvez visiter https://m.bell.ca/ecvoirmafacture pour voir les détails de votre compte et les frais du tarif mensuel dans l'application MonBell. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/ecviewmybill to view your account details and Monthly Rate Charges in the MyBell app. ( bell.ca/about-us )"
            elif r == "bill_device_balance":
                sms = "Vous pouvez visiter https://m.bell.ca/ecvoirmafacture pour vérifier le solde de votre appareil dans l'application MonBell. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/ecviewmybill to check your device balance in the MyBell app. ( bell.ca/about-us )"
            elif r == "bill_switch_format":
                sms = "Vous pouvez visiter https://m.bell.ca/ecmonmodedefacturation pour mettre à jour vos préférences de facturation dans l'application MonBelll. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/ecmybillformat to update your billing preferences in the MyBell app. ( bell.ca/about-us )"
            elif r == "bill_reduce_plan":
                sms = "Vous pouvez visiter m.bell.ca/changemyplan pour modifier votre forfait dans l'application MonBell. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/changemyplan  to change your plan in the MyBell app. ( bell.ca/about-us )"
            elif r == "bill_dispute":
                sms = "Vous pouvez visiter https://m.bell.ca/ecutilisation pour voir vos frais mensuels et votre utilisation dans l'application MonBell. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/eccheckusage to view your monthly charges and usage in the MyBell app. ( bell.ca/about-us )"
            elif r == "bill_confirm_due_date":
                sms = "Vous pouvez visiter https://m.bell.ca/ecmaconnexion pour voir votre date de facturation mensuelle dans l'application MonBell. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/ecmylogin to view your Monthly Charge Date in the MyBell app. ( bell.ca/about-us )"
            elif r in ["bill_add_promo", "bill_inquire_promo"]:
                sms = "Vous pouvez visiter https://m.bell.ca/ecchangermonforfait our en savoir plus sur nos forfaits et offres dans l'application MonBell. (bell.ca/apropos)" if "fr" in l else "You can visit https://m.bell.ca/ecchangemyplan to learn more about our to learn more about our plans and offers in the MyBell app. ( bell.ca/about-us )"
            elif r in ["bill_missing_promos", "bill_missing_promo"]:
                sms = "Vous pouvez visiter https://m.bell.ca/ecchangermonforfait pour passer en revue vos promotions dans l'application MonBell. ( bell.ca/apropos )" if "fr" in l else "You can visit https://m.bell.ca/ecchangemyplan to review your promotions in the MyBell app. ( bell.ca/about-us )"
            else:
                sms = "Please visit the MyBell app for more details."

            set_variable('sms_content', sms)
            set_variable('sms_type', 'Public')
            print('Business logic success')
            return {'status': 'success', 'sms_content': sms}

        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Inform the user that the SMS content could not be generated at this time.'}