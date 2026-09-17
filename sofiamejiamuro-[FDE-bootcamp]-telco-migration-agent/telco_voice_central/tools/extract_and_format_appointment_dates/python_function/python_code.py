def extract_and_format_appointment_dates(start_time_raw: str = "", end_time_raw: str = "") -> dict:
    '''State/Variable Manipulator. Parses nested timestamps and formats variables.'''
    if get_variable("mock_mode"):
        set_variable("date_part", "Monday")
        set_variable("date_part", "January")
        set_variable("date_part", "1")
        set_variable("date_part", "2024")
        set_variable("date_part", "lundi")
        set_variable("date_part", "janvier")
        set_variable("time_val", "8:00 AM")
        set_variable("time_val", "12:00 PM")
        set_variable("start_time_hours_fr", "08 h 00")
        set_variable("end_time_hours_fr", "12 h 00")
        return {
            "status": "success",
            "message": "Appointment variables successfully set."
        }
    else:
        try:
            from datetime import datetime
            start_time_clean = start_time_raw.strip() if start_time_raw else ""
            end_time_clean = end_time_raw.strip() if end_time_raw else ""
            if not start_time_clean:
                return {"status": "success", "message": "No start time provided"}

            try:
                start_dt = datetime.fromisoformat(start_time_clean.replace("Z", "+00:00"))
            except:
                start_dt = datetime.now()

            try:
                end_dt = datetime.fromisoformat(end_time_clean.replace("Z", "+00:00")) if end_time_clean else start_dt
            except:
                end_dt = start_dt

            en_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            fr_months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
            en_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            fr_days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

            wd = start_dt.weekday()
            mo = start_dt.month - 1

            set_variable("date_part", en_days[wd])
            set_variable("date_part", en_months[mo])
            set_variable("date_part", str(start_dt.day))
            set_variable("date_part", str(start_dt.year))

            set_variable("date_part", fr_days[wd])
            set_variable("date_part", fr_months[mo])
            set_variable("date_part", str(start_dt.day))
            set_variable("date_part", str(start_dt.year))

            set_variable("time_val", start_dt.strftime("%I:%M %p").lstrip("0"))
            set_variable("time_val", end_dt.strftime("%I:%M %p").lstrip("0"))
            set_variable("start_time_hours_fr", start_dt.strftime("%H h %M"))
            set_variable("end_time_hours_fr", end_dt.strftime("%H h %M"))

            print("Business logic success: Date extraction completed.")
            return {"status": "success", "message": "Appointment variables successfully set."}
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Crash: {e}")
            return {"error": str(e), "agent_action": "Politely inform the customer that we are experiencing technical difficulties parsing the appointment and offer to transfer them to a representative."}