def calculate_payment_dates_manipulator(pa_days: int, calculated_date_raw: str, language: str) -> dict:
    '''State Manipulator. Performs date math and formats the resulting date string based on session language.'''
    if get_variable("mock_mode"):
        mock_actual_date = "November 15"
        mock_calc_date = "11-15"
        set_variable("actual_date", mock_actual_date)
        set_variable("date_formatted", mock_calc_date)
        return {
            "actual_date": mock_actual_date,
            "calculated_payment_date": mock_calc_date
        }

    import datetime
    try:
        days = int(pa_days)
        lang = language.strip().lower()
        target_date = datetime.date.today() + datetime.timedelta(days=days)

        if "fr" in lang:
            months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
            actual_date = f"{months[target_date.month - 1]} {target_date.day:02d}"
        else:
            actual_date = target_date.strftime("%B %d")

        calc_date = ""
        if calculated_date_raw and len(calculated_date_raw) >= 10:
            calc_date = calculated_date_raw[5:10]

        set_variable("actual_date", actual_date)
        set_variable("date_formatted", calc_date)
        print("Business logic success")
        return {"actual_date": actual_date, "calculated_payment_date": calc_date}
    except Exception as e:
        logger.error(f"Crash: {e}")
        return {"error": str(e), "agent_action": "Explain that there was an error calculating the processing dates."}