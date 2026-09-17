def prepare_troubleshooting_sms(tv_sub_type: str = "", language: str = "") -> dict:
    """Reads 'language' and 'tv_sub_type', then sets sms_content and sms_type."""
    if get_variable("mock_mode"):
        set_variable("sms_content", "Bell: You can visit bell.ca/fibetvtroubleshooting for more information on troubleshooting your Fibe TV service. ( bell.ca/about-us )")
        set_variable("sms_type", "Public")
        return {
            "status": "success",
            "message": "Variables sms_content and sms_type successfully set.",
            "mock_mode": True
        }

    try:
        sanitized_tv = str(tv_sub_type).lower().strip()
        sanitized_lang = str(language).lower().strip()

        if not sanitized_tv:
            tv_val = get_variable("tv_sub_type")
            sanitized_tv = str(tv_val).lower().strip() if tv_val else ""
        if not sanitized_lang:
            lang_val = get_variable("language")
            sanitized_lang = str(lang_val).lower().strip() if lang_val else ""

        sms_content = ""
        if "fibe" in sanitized_tv:
            if "fr" in sanitized_lang:
                sms_content = "Bell : Vous pouvez visiter bell.ca/telefibedepannage pour obtenir plus d'information sur le dépannage de votre service Télé Fibe. ( bell.ca/apropos )"
            else:
                sms_content = "Bell: You can visit bell.ca/fibetvtroubleshooting for more information on troubleshooting your Fibe TV service. ( bell.ca/about-us )"
        elif "sat" in sanitized_tv:
            if "fr" in sanitized_lang:
                sms_content = "Bell : Vous pouvez visiter bell.ca/telesatdepannage pour obtenir plus d'information sur le dépannage de votre service Télé Satellite."
            else:
                sms_content = "Bell: You can visit bell.ca/sattvtroubleshooting for more information on troubleshooting your Satellite TV service. ( bell.ca/about-us )"
        else:
            sms_content = "Bell: You can visit bell.ca/fibetvtroubleshooting for more information on troubleshooting your Fibe TV service. ( bell.ca/about-us )"

        set_variable("sms_content", sms_content)
        set_variable("sms_type", "Public")

        print("Business logic success")
        return {"status": "success", "message": "Variables sms_content and sms_type successfully set."}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties and offer to transfer them to a representative."}