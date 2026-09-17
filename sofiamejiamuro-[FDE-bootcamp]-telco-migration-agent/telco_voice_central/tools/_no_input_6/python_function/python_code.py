def _no_input_1() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': 'Are you there?'}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Êtes-vous là ?'})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Are you there?'})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_1_extend() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."}, {'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': "Pour nous assurer d'avoir assez de temps pour terminer, je prolonge notre session. Un moment, s'il vous plaît."})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."})
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_2() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': 'I am not able to hear you. Are you speaking?'}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Je ne vous entends pas. Parlez-vous ?'})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': 'I am not able to hear you. Are you speaking?'})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_2_extend() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."}, {'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': "Pour nous assurer d'avoir assez de temps pour terminer, je prolonge notre session. Un moment, s'il vous plaît."})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."})
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_3() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': 'Are you still there?'}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Êtes-vous encore là ?'})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Are you still there?'})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_3_extend() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."}, {'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': "Pour nous assurer d'avoir assez de temps pour terminer, je prolonge notre session. Un moment, s'il vous plaît."})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."})
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_4() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': 'Hello, are you there?'}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Bonjour, êtes-vous ici?'})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Hello, are you there?'})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_4_extend() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."}, {'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': "Pour nous assurer d'avoir assez de temps pour terminer, je prolonge notre session. Un moment, s'il vous plaît."})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."})
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_5() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': 'Please let me know if you are still here. The session is about to timeout'}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Faites-moi savoir si vous êtes encore là. La session va bientôt expirer.'})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Please let me know if you are still here. The session is about to timeout'})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_5_extend() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."}, {'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': "Pour nous assurer d'avoir assez de temps pour terminer, je prolonge notre session. Un moment, s'il vous plaît."})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': "To ensure we have enough time to finish, I'm just extending our session. One moment, please."})
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-2'}})
        return {'__cxas_system_directives__': __cxas_system_directives__}

def _no_input_6() -> dict:
    if get_variable("mock_mode"):
        return {'__cxas_system_directives__': [{'action': 'respond', 'text': 'Sorry, the session has timed out.'}, {'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-1'}}]}
    else:
        __cxas_system_directives__ = []
        input_params = history.agent_input.action_parameters
        set_variable('language', input_params['language'])
        if get_variable('language') == 'fr-ca':
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Désolé, la session a expiré.'})
        else:
            __cxas_system_directives__.append({'action': 'respond', 'text': 'Sorry, the session has timed out.'})
        __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent', 'parameters': {'customer_answer1_id': '-1'}})
        return {'__cxas_system_directives__': __cxas_system_directives__}