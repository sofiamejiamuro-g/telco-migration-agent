def execute_comprehensive_outage_check(postcode: str, lob: str) -> dict:
    '''Bundles the complex DFCX polling sequence into a single synchronous tool call to check for outages.'''
    import json
    import logging
    logger = logging.getLogger(__name__)
    try:
        mock_mode = get_variable('mock_mode')
        if mock_mode:
            print('Executing in mock mode')
            return {
                'status': 'success',
                'has_outage': True,
                'active_outage_found': True,
                'service_lob': lob,
                'postcode': postcode,
                'outage_details': {
                    'incident_id': 'INC-9988776655',
                    'cause': 'Network infrastructure repair',
                    'status': 'In Progress'
                },
                'formatted_etr': {
                    'fromTime': '10:00 AM',
                    'toTime': '2:00 PM',
                    'fromTime_fr': '10h00',
                    'toTime_fr': '14h00',
                    'month_date': 'October 12',
                    'month_date_fr': '12 Octobre',
                    'estimated_restoration_message_en': 'between 10:00 AM and 2:00 PM on October 12',
                    'estimated_restoration_message_fr': 'entre 10h00 et 14h00 le 12 Octobre'
                }
            }

        sanitized_postcode = postcode.strip().replace(' ', '').upper()
        sanitized_lob = lob.lower().strip()
        payload = {'postcode': sanitized_postcode, 'lob': sanitized_lob}
        result = tools.outage_check_orchestrator_post_outage_check_orchestrator(payload).json()
        print('Business logic success')
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f'Crash: {e}')
        return {
            'error': str(e),
            'agent_action': 'Apologize to the customer stating that due to an unexpected system issue, the outage status could not be verified. Execute HANDLE_FAILED_OUTAGE_CHECK routing.'
        }