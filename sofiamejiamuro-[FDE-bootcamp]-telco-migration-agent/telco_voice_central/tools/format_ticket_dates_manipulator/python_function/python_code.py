def format_ticket_dates_manipulator(raw_date_string: str) -> dict:
    '''Parses raw timestamp strings into flattened properties for TTS playback.'''
    if get_variable("mock_mode"):
        return {
            'day': '15',
            'month': 'October',
            'year': '2024',
            'day_fr': '15',
            'month_fr': 'octobre',
            'date': '2024-10-15'
        }
    else:
        try:
            from datetime import datetime
            if not raw_date_string:
                return {'day': '', 'month': '', 'year': '', 'day_fr': '', 'month_fr': '', 'date': ''}
            clean_date = str(raw_date_string).replace('Z', '')
            if '.' in clean_date:
                clean_date = clean_date.split('.')[0]
            dt = datetime.fromisoformat(clean_date)
            months_en = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            months_fr = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
            day = str(dt.day)
            year = str(dt.year)
            month_en = months_en[dt.month - 1]
            month_fr = months_fr[dt.month - 1]
            print('Business logic success')
            return {'day': day, 'month': month_en, 'year': year, 'day_fr': day, 'month_fr': month_fr, 'date': f'{dt.year}-{dt.month:02d}-{dt.day:02d}'}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Explain technical difficulty parsing date.'}