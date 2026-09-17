def extract_postal_code(services_payload: dict) -> dict:
    '''Extracts a flattened array of unique postal codes from the customer services payload.'''
    if get_variable("mock_mode"):
        set_variable('postal_code', 'M5V3L9')
        return {'status': 'success', 'postal_codes': ['M5V3L9']}
    else:
        import logging
        logger = logging.getLogger(__name__)
        try:
            postcodes = []
            services = services_payload.get('service_type', [])
            for svc in services:
                address = svc.get('service_address', {})
                pc = address.get('postcode')
                if pc:
                    sanitized_pc = pc.strip().replace(' ', '').upper()
                    if sanitized_pc not in postcodes:
                        postcodes.append(sanitized_pc)
            if len(postcodes) == 1:
                set_variable('postal_code', postcodes[0])
            print('Business logic success')
            return {'status': 'success', 'postal_codes': postcodes}
        except Exception as e:
            logger.error(f'Crash: {e}')
            return {'error': str(e), 'agent_action': 'Inform the customer that we could not extract the postal code and ask them to manually provide it.'}