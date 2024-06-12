from parse import *

# hardcoded section names
name_sigma = "Sigma"
name_states = "States"
name_transitions = "Transitions"
name_initial = "Initial"
name_final = "Final"

name_stack_symbols = "StackSymbols"
name_stack_initial = "StackInitial"

def check_configuration(file_contents):
    section_list = get_section_list(file_contents)
    
    # check if the file has the required sections
    has_sigma = True if "Sigma" in section_list else False
    has_states = True if "States" in section_list else False
    has_transitions = True if "Transitions" in section_list else False
    has_initial = True if "Initial" in section_list else False
    has_final = True if "Final" in section_list else False
    
    if not has_sigma:
        return False, "Sigma section is missing"
    if not has_states:
        return False, "States section is missing"
    if not has_transitions:
        return False, "Transitions section is missing"
    if not has_initial:
        return False, "Initial section is missing"
    if not has_final:
        return False, "Final section is missing"

    # the initial section should have only one state
    initial_section = get_section_content(file_contents, name_initial)
    if len(initial_section) != 1:
        return False, "Initial section should have only one state"
    
    # the final section should have at least one state
    final_section = get_section_content(file_contents, name_final)
    if len(final_section) < 1:
        return False, "Final section should have at least one state"
    
    # if there is an input, it should be in the sigma section (if not *)
    has_input = True if "Input" in section_list else False
    if has_input:
        input_section = get_section_content(file_contents, "Input")
        sigma_section = get_section_content(file_contents, name_sigma)
        for symbol in input_section:
            if symbol != "*" and symbol not in sigma_section:
                return False, "Input symbol is not in the Sigma section (" + symbol + ")"
    
    # check if the transitions have existing states and symbols
    sigma_section = get_section_content(file_contents, name_sigma)
    states_section = get_section_content(file_contents, name_states)
    transitions_section = get_section_content(file_contents, name_transitions)
    for transition in transitions_section:
        transition = transition.split(", ")
        
        # trim everything tho
        for i in range(3):
            transition[i] = transition[i].strip()

        # if the state is not in the dict, ret false
        if transition[0] not in states_section or transition[2] not in states_section:
            return False, "Transition has a state that is not in the States section (" + transition[0] + ", " + transition[2] + ")"
        
        # if the symbol is not in the sigma, ret false
        if transition[1] not in sigma_section:
            if transition[1] != "*":
                return False, "Transition has a symbol that is not in the Sigma section (" + transition[1] + ")"
    
    return True, "Configuration is valid"

def check_cfg_configuration(file_contents):
    # check if valid
    section_list = get_section_list(file_contents)
    
    # check if the file has the required sections
    
    has_variables = True if "Variables" in section_list else False
    has_terminals = True if "Sigma" in section_list else False
    has_rules = True if "Rules" in section_list else False
    has_start = True if "Input" in section_list else False
    
    if not has_variables:
        return False, "Variables section is missing"
    if not has_terminals:
        return False, "Sigma section is missing"
    if not has_rules:
        return False, "Rules section is missing"
    if not has_start:
        return False, "Input section is missing"
    
    # the start section should have only one state
    start_section = get_section_content(file_contents, "Input")
    if len(start_section) != 1:
        return False, "Input section should have only one variable"
    
    # check if the rules have existing variables and symbols
    variables_section = get_section_content(file_contents, "Variables")
    sigma_section = get_section_content(file_contents, "Sigma")
    rules_section = get_section_content(file_contents, "Rules")
    for rule in rules_section:
        rule = rule.split(" -> ")
        
        # trim everything tho
        for i in range(2):
            rule[i] = rule[i].strip()

        # if the state is not in the dict, ret false
        if rule[0] not in variables_section:
            return False, "Rule has a variable that is not in the Variables section (" + rule[0] + ")"
    
    # check if input symbols are not in the variables section
    input_section = get_section_content(file_contents, "Input")
    for symbol in input_section:
        if symbol not in variables_section:
            return False, "Input symbol is not in the Variables section (" + symbol + ")"
    
    return True, "Configuration is valid"

def check_pda_configuration(file_contents):
    section_list = get_section_list(file_contents)
    
    has_sigma = True if "Sigma" in section_list else False
    has_states = True if "States" in section_list else False
    has_transitions = True if "Transitions" in section_list else False
    has_initial = True if "Initial" in section_list else False
    has_final = True if "Final" in section_list else False
    has_stack_symbols = True if "StackSymbols" in section_list else False
    has_stack_initial = True if "StackInitial" in section_list else False
    
    if not has_sigma:
        return False, "Sigma section is missing"
    if not has_states:
        return False, "States section is missing"
    if not has_transitions:
        return False, "Transitions section is missing"
    if not has_initial:
        return False, "Initial section is missing"
    if not has_final:
        return False, "Final section is missing"
    if not has_stack_symbols:
        return False, "StackSymbols section is missing"
    if not has_stack_initial:
        return False, "StackInitial section is missing"

    initial_section = get_section_content(file_contents, name_initial)
    if len(initial_section) != 1:
        return False, "Initial section should have only one state"
    
    final_section = get_section_content(file_contents, name_final)
    if len(final_section) < 1:
        return False, "Final section should have at least one state"

    stack_initial_section = get_section_content(file_contents, name_stack_initial)
    if len(stack_initial_section) != 1:
        return False, "StackInitial section should have only one symbol"

    sigma_section = get_section_content(file_contents, name_sigma)
    states_section = get_section_content(file_contents, name_states)
    stack_symbols_section = get_section_content(file_contents, name_stack_symbols)
    transitions_section = get_section_content(file_contents, name_transitions)
    
    for transition in transitions_section:
        transition = transition.split(",")
        for i in range(len(transition)):
            transition[i] = transition[i].strip()

        if transition[0] not in states_section or transition[4] not in states_section:
            return False, "Transition has a state that is not in the States section (" + transition[0] + ", " + transition[3] + ")"
        
        if transition[1] not in sigma_section and transition[1] != "epsilon":
            return False, "Transition has a symbol that is not in the Sigma section (" + transition[1] + ")"
        
        if transition[2] not in stack_symbols_section and transition[2]!="epsilon":
            return False, "Transition has a stack symbol that is not in the StackSymbols section (" + transition[2] + ")"
        
        # transition[3] = transition[2].replace("push ", "")
        # transition[3] = transition[2].replace("pop", "")
        # transition[3] = transition[2].replace("check ", "")
        # if transition[3] not in states_section:
        #     return False, "Transition has a state that is not in the States section (" + transition[3] + ")"
    
    return True, "Configuration is valid"
