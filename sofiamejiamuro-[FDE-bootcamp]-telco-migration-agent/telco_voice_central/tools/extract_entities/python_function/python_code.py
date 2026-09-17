def extract_entities(utterance: str, route: str, language: str) -> str:
    if get_variable("mock_mode"):
        return {
            '__cxas_system_directives__': [
                {
                    'action': 'add_override',
                    'target': 'RootAgent',
                    'parameters': {
                        'route': route,
                        'language': language,
                        'utterance': utterance,
                        'lob': 'Mobility',
                        'intent_identified': True
                    }
                }
            ]
        }

    __cxas_system_directives__ = []
    try:
        parameters = {}
        matches = flows.bell_Query_Rewriter.match_intent(get_variable('utterance')).matches
        if matches and matches[0].parameters:
            for entity, value in matches[0].parameters.items():
                if value:
                    parameters[entity] = value
        parameters['route'] = get_variable('route')
        parameters['language'] = get_variable('language')
        parameters['utterance'] = get_variable('utterance')
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'RootAgent', 'parameters': parameters})
    except Exception as e:
        print(f'[extract_entities] Error: {e}')
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'RootAgent', 'parameters': {'route': get_variable('route'), 'language': get_variable('language'), 'utterance': get_variable('utterance')}})
    return {'__cxas_system_directives__': __cxas_system_directives__}