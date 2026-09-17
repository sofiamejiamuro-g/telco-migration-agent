def _no_input() -> dict:
    if get_variable("mock_mode"):
        return {
            '__cxas_system_directives__': [
                {'action': 'add_override', 'target': 'TechSupportAndRepairAgent'}
            ]
        }

    __cxas_system_directives__ = []
    input_params = history.agent_input.action_parameters
    set_variable('language', input_params['language'])
    __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent'})
    return {'__cxas_system_directives__': __cxas_system_directives__}

def routing(language: str) -> dict:
    if get_variable("mock_mode"):
        return {
            '__cxas_system_directives__': [
                {'action': 'add_override', 'target': 'TechSupportAndRepairAgent'}
            ]
        }

    __cxas_system_directives__ = []
    __cxas_system_directives__.append({'action': 'add_override', 'target': 'TechSupportAndRepairAgent'})
    return {'__cxas_system_directives__': __cxas_system_directives__}