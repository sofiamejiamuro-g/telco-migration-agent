def match_intent(revised_user_query: str, second_intent_true: bool, language: str) -> str:
    if get_variable("mock_mode"):
        lang_val = get_variable("language") if get_variable("language") is not None else language
        sit_val = get_variable("second_intent_true") if get_variable("second_intent_true") is not None else second_intent_true
        return {
            "__cxas_system_directives__": [
                {
                    "action": "add_override",
                    "target": "RootAgent",
                    "parameters": {
                        "route": "billing_and_payments",
                        "language": lang_val,
                        "utterance": revised_user_query,
                        "second_intent_true": sit_val,
                        "no_match_1": "",
                        "no_match_2": "",
                        "lob": "Mobility"
                    }
                }
            ]
        }
    else:
        __cxas_system_directives__ = []
        try:
            matches = flows.bell_Query_Rewriter.match_intent(revised_user_query).matches
            print(matches[0])
            if matches[0].intent:
                detected_intent = str(matches[0].intent.display_name)
                driver = detected_intent.split('_')[0]
                detected_intent = matches[0].intent.display_name
                confidence = matches[0].confidence
                print('confidence :', confidence)
                if get_variable('second_intent_true') == True:
                    if 'en' in get_variable('language').lower():
                        __cxas_system_directives__.append({'action': 'respond', 'text': f"Ok let's address one question first"})
                    elif 'fr' in get_variable('language').lower():
                        __cxas_system_directives__.append({'action': 'respond', 'text': f"D'accord, allons-y une question à la fois"})
                parameters = {}
                entities = matches[0].parameters
                if entities:
                    for entity in entities:
                        parameters[entity] = entities[entity]
                parameters['route'] = detected_intent
                parameters['language'] = get_variable('language')
                parameters['utterance'] = revised_user_query
                parameters['second_intent_true'] = get_variable('second_intent_true')
                parameters['no_match_1'] = ''
                parameters['no_match_2'] = ''
                __cxas_system_directives__.append({'action': 'add_override', 'target': 'RootAgent', 'parameters': parameters})
            else:
                parameters = {}
                parameters['route'] = 'no_intent'
                parameters['language'] = get_variable('language')
                parameters['utterance'] = revised_user_query
                parameters['second_intent_true'] = get_variable('second_intent_true')
                ds_output = {}
                ds_output['answer'] = ''
                if len(revised_user_query.split()) < 6 and 'page' in revised_user_query:
                    pass
                elif 'en' in get_variable('language').lower():
                    ds_output = tools.en_generic_datastore.EN_Generic_Datastore({'query': revised_user_query})
                elif 'fr' in get_variable('language').lower():
                    ds_output = tools.fr_generic_datastore.FR_Generic_Datastore({'query': revised_user_query})
                if ds_output['answer']:
                    __cxas_system_directives__.append({'action': 'respond', 'text': ds_output['answer']})
                    parameters['route'] = 'infobot'
                    __cxas_system_directives__.append({'action': 'add_override', 'target': 'RootAgent', 'parameters': parameters})
                else:
                    __cxas_system_directives__.append({'action': 'add_override', 'target': 'RootAgent', 'parameters': parameters})
        except Exception as e:
            print(f'Error during intent matching: {e}')
            if 'en' in get_variable('language').lower():
                __cxas_system_directives__.append({'action': 'respond', 'text': f'An error occurred while processing your request, please try again'})
            elif 'fr' in get_variable('language').lower():
                __cxas_system_directives__.append({'action': 'respond', 'text': f'Une erreur est survenue, pouvez-vous réessayer'})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def no_intent(revised_user_query: str, second_intent_true: bool, language: str) -> str:
    if get_variable("mock_mode"):
        lang_val = get_variable("language") if get_variable("language") is not None else language
        sit_val = get_variable("second_intent_true") if get_variable("second_intent_true") is not None else second_intent_true
        return {
            "__cxas_system_directives__": [
                {
                    "action": "respond",
                    "text": "This is a simulated infobot response from the datastore."
                },
                {
                    "action": "add_override",
                    "target": "RootAgent",
                    "parameters": {
                        "route": "infobot",
                        "language": lang_val,
                        "utterance": revised_user_query,
                        "second_intent_true": sit_val
                    }
                }
            ]
        }
    else:
        __cxas_system_directives__ = []
        print('In No Intent Tool')
        parameters = {}
        parameters['route'] = 'no_intent'
        parameters['language'] = get_variable('language')
        parameters['utterance'] = revised_user_query
        parameters['second_intent_true'] = get_variable('second_intent_true')
        ds_output = {}
        ds_output['answer'] = ''
        if len(revised_user_query.split()) < 6 and 'page' in revised_user_query:
            pass
        elif 'en' in get_variable('language').lower():
            ds_output = tools.en_generic_datastore.EN_Generic_Datastore({'query': revised_user_query})
        elif 'fr' in get_variable('language').lower():
            ds_output = tools.fr_generic_datastore.FR_Generic_Datastore({'query': revised_user_query})
        if ds_output['answer']:
            __cxas_system_directives__.append({'action': 'respond', 'text': ds_output['answer']})
            parameters['route'] = 'infobot'
            __cxas_system_directives__.append({'action': 'add_override', 'target': 'RootAgent', 'parameters': parameters})
        else:
            __cxas_system_directives__.append({'action': 'add_override', 'target': 'RootAgent', 'parameters': parameters})
        return {'__cxas_system_directives__': __cxas_system_directives__}