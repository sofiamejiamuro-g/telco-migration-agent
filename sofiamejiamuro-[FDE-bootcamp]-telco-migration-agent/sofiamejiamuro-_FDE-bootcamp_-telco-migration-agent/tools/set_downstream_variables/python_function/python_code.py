def set_downstream_variables(target_flow: str, sms_topic: str = "", utterance_context: str = "") -> dict:
    """State Manipulator to set session variables before routing."""
    if get_variable("mock_mode"):
        return {"status": "success", "message": f"Variables updated for {target_flow}"}
    else:
        try:
            target_sanitized = target_flow.lower().strip().replace(' ', '_')
            topic_sanitized = sms_topic.lower().strip()
            language = get_variable('language') or 'en-ca'

            if 'sms_trigger' in target_sanitized:
                set_variable('sms_type', 'Public')
                if 'hoop' in topic_sanitized:
                    if 'fr' in language.lower():
                        set_variable('sms_content', 'Bell : Vous pouvez visiter soutien.bell.ca/contactez-nous pour consulter nos heures d’ouverture. ( bell.ca/apropos )')
                    else:
                        set_variable('sms_content', 'Bell: You can visit support.bell.ca/contact-us to find our hours of operation. ( bell.ca/about-us )')
                elif 'store' in topic_sanitized or 'locator' in topic_sanitized:
                    if 'fr' in language.lower():
                        set_variable('sms_content', 'Bell : Vous pouvez visiter bell.ca/localisation_de_magasins pour trouver un magasin près de chez vous. ( bell.ca/apropos )')
                    else:
                        set_variable('sms_content', 'Bell msg: You can visit https://www.bell.ca/Store Locator to find the nearest store. (bell.ca/about-us)')

            if 'bell_aqd' in target_sanitized:
                set_variable('hardstop', True)
                set_variable('page_id', 'c5008440-e669-4b8f-bbb6-8569d5d1cdd1')
                set_variable('flow_id', '5cdd2f01-b83d-470c-86c5-368354a50ccb')
                set_variable('page_name', 'Price Comparison')

            if 'bell_feedback' in target_sanitized:
                set_variable('utterance', utterance_context)

            print('Business logic success: Downstream variables set')
            return {"status": "success", "message": f"Variables updated for {target_flow}"}
        except Exception as e:
            return {"error": str(e), "agent_action": "Politely inform the customer that a system error occurred and offer to transfer them."}