from itertools import product
import random
import parse

def run_dfa(input, file_contents, log):   
    # get the sections
    section_list = parse.get_section_list(file_contents)
    sigma = parse.get_section_content(file_contents, "Sigma")
    states = parse.get_section_content(file_contents, "States")
    transitions = parse.get_section_content(file_contents, "Transitions")
    initial = parse.get_section_content(file_contents, "Initial")
    final = parse.get_section_content(file_contents, "Final")
    
    # skip empty transitions (makes it more readable)
    transitions = [x for x in transitions if x != ""]
    
    # this is for printing each transition
    debug = True if "Debug" in section_list else False
    debug = log or debug
    
    # get the initial state
    initial_state = initial[0]
    
    # if the input is empty, return start==final
    if input == "":
        if initial_state in final:
            return 1
        else:
            return 0
    
    # get the transitions
    # my syntax is "abc, symbol, def" per lines
    transition_dict = {}
    for transition in transitions:
        transition = transition.split(", ")
        
        # trim everything tho
        for i in range(3):
            transition[i] = transition[i].strip()

        # if the state is not in the dict, ret -1
        if transition[0] not in states or transition[2] not in states:
            return -1

        # if the symbol is not in the sigma, ret -1
        if transition[1] not in sigma:
            return -1

        if transition[0] not in transition_dict:
            transition_dict[transition[0]] = {}
        transition_dict[transition[0]][transition[1]] = transition[2]
    
    # print(transition_dict) # debug
    
    # start the simulation
    current_state = initial_state
    for symbol in input:
        try:
            if debug:
                print("{} --{}--> {}".format(current_state, symbol, transition_dict[current_state][symbol]))
            current_state = transition_dict[current_state][symbol]
        except KeyError:
            None # gen tranzactia nu exista pt simbolu asta
        
    # check if the final state is in the final states
    if current_state in final:
        return 1
    else:
        return 0

# NECESSARY FOR NFA
def epsilon_closure(states, transition_dict):
    closure = set(states)
    stack = list(states)
    
    while stack:
        state = stack.pop()
        if state in transition_dict and "*" in transition_dict[state]:
            for next_state in transition_dict[state]["*"]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return list(closure)

def run_nfa(input_string, file_contents, log=False):
    # sections
    sigma = parse.get_section_content(file_contents, "Sigma")
    states = parse.get_section_content(file_contents, "States")
    transitions = parse.get_section_content(file_contents, "Transitions")
    initial = parse.get_section_content(file_contents, "Initial")[0]
    final = parse.get_section_content(file_contents, "Final")
    
    # transitions
    transition_dict = {}
    for transition in transitions:
        src, symbol, dest = map(str.strip, transition.split(","))
        transition_dict.setdefault(src, {}).setdefault(symbol, []).append(dest)

    current_states = epsilon_closure([initial], transition_dict)

    # processing
    for symbol in input_string:
        next_states = []
        for state in current_states:
            if symbol in transition_dict.get(state, {}):
                next_states.extend(transition_dict[state][symbol])
        next_states = epsilon_closure(next_states, transition_dict) 
        
        if log:
            print(f"{current_states} --{symbol}--> {next_states}")
        
        current_states = next_states

    return any(state in final for state in current_states)

# bruteforce function finds all the
# accepted strings of a NFA
# made of a certain length
def bruteforce_nfa(length, file_content, log):
    symbols = parse.get_section_content(file_content, "Sigma")
    
    tests = []
    
    # generate all the possible strings
    for i in range(1, length+1):
        for test in product(symbols, repeat=i):
            tests.append("".join(test))
    
    # run the tests
    accepted = []
    
    for test in tests:
        if run_nfa(test, file_content):
            accepted.append(test)
            
            if log:
                print("Accepted: ", test)
    
    return accepted

def run_cfg(input, file_contents, log=False):
    # sections
    variables = parse.get_section_content(file_contents, "Variables")
    sigma = parse.get_section_content(file_contents, "Sigma")
    rules = parse.get_section_content(file_contents, "Rules")
    
    # input
    if input:
        initial_symbol = input
    else:
        initial_symbol = parse.get_section_content(file_contents, "Input")[0]

    # rules
    rule_dict = {}
    for rule in rules:
        left_side, right_sides = rule.split(" -> ")
        right_sides = [side.strip().split(" ") for side in right_sides.split('|')]
        rule_dict[left_side] = right_sides

    # text generation
    def generate(sentence, depth=0):
        if depth > 50:
            # recursion limit
            return "Expansion exceeded maximum depth, possibly due to recursive rules."

        if all(token in sigma for token in sentence):
            return " ".join(sentence)

        for i, token in enumerate(sentence):
            if token in rule_dict:
                possible_expansions = rule_dict[token]
                random_expansion = random.choice(possible_expansions)
                new_sentence = sentence[:i] + random_expansion + sentence[i+1:]
                result = generate(new_sentence, depth + 1)
                if result:
                    return result

        # if sentence has no more variables to expand, return it
        # only if it has terminal symbols
        if all(token in sigma for token in sentence):
            return " ".join(sentence)

        if log:
            print("At depth", depth, "no valid expansion found for", sentence)
        return "No valid expansion found."

    result = generate([initial_symbol])
    
    # if log:
        # print("Generated sentence:", result)

    return result

# bruteforce for the cfg
def run_all_cfg(input, file_contents, log=False):
    variables = parse.get_section_content(file_contents, "Variables")
    sigma = parse.get_section_content(file_contents, "Sigma")
    rules = parse.get_section_content(file_contents, "Rules")
    
    if input:
        initial_symbol = input
    else:
        initial_symbol = parse.get_section_content(file_contents, "Input")[0]

    rule_dict = {}
    for rule in rules:
        left_side, right_sides = rule.split(" -> ")
        right_sides = [side.strip().split(" ") for side in right_sides.split('|')]
        rule_dict[left_side] = right_sides

    results = []

    def generate(sentence, depth=0):
        if depth > 50:
            return ["Expansion exceeded maximum depth, possibly due to recursive rules."]

        if all(token in sigma for token in sentence):
            return [" ".join(sentence)]

        for i, token in enumerate(sentence):
            if token in rule_dict:
                possible_expansions = rule_dict[token]
                for expansion in possible_expansions:
                    new_sentence = sentence[:i] + expansion + sentence[i+1:]
                    result = generate(new_sentence, depth + 1)
                    if result:
                        if log:
                            print("Result:",result)
                        results.extend(result)

        # if sentence has no more variables to expand, return it
        # only if it has terminal symbols
        if all(token in sigma for token in sentence):
            return [" ".join(sentence)]

    generate([initial_symbol])
    
    # if log:
        # print("Generated sentences:", results)

    return results

def run_pda(input, file_contents, log=True):
    import parse

    # sections
    sigma = parse.get_section_content(file_contents, "Sigma")
    states = parse.get_section_content(file_contents, "States")
    raw_transitions = parse.get_section_content(file_contents, "Transitions")
    initial = parse.get_section_content(file_contents, "Initial")
    initial = initial[0] # pt ca returna lista
    final = [state.strip() for state in parse.get_section_content(file_contents, "Final")]
    stacksymbols = parse.get_section_content(file_contents, "StackSymbols")
    stackinitial = parse.get_section_content(file_contents, "StackInitial")
    stackinitial = stackinitial[0] # pt ca returna lista

    # process transitions from file content
    transitions = []
    for transition in raw_transitions:
        parts = transition.split(",")
        transitions.append([part.strip() for part in parts])
    
    # main processing
    current_state = initial
    current_stack = [stackinitial]  # Use list for easier stack manipulation

    for symbol in input:
        if log:
            print(f"Processing symbol: {symbol} | Current state: {current_state} | Stack: {current_stack}")
        transition_applied = False
        for transition in transitions:
            if transition[0] == current_state and (transition[1] == symbol or transition[1] == 'epsilon'):
                if log:
                    print(f"Attempting transition: {transition}", end=" | ")
                if transition[3].startswith("push "):
                    current_stack.append(transition[3][5:])
                    current_state = transition[4]
                    if log:
                        print(f"Action: Push | New stack: {current_stack}")
                elif transition[3].startswith("pop"):
                    if current_stack:
                        current_stack.pop()
                    current_state = transition[4]
                    if log:
                        print(f"Action: Pop | New stack: {current_stack}")
                elif transition[3].startswith("check "):
                    if current_stack and current_stack[-1] == transition[3][6:]:
                        current_state = transition[4]
                        if log:
                            print(f"Action: Check | New state: {current_state}")
                transition_applied = True
                break
            else:
                print(f"Ignoring transition: {transition} | ")
        if not transition_applied and log:
            print(f"No valid transition found for symbol: {symbol} | State: {current_state} | Stack: {current_stack}")

    # now checking if there are transitionz possbile
    # when the input doesnt matter (= epislon)
    for transition in transitions:
        if transition[0] == current_state and transition[1] == 'epsilon':
            if log:
                print(f"Attempting transition: {transition}", end=" | ")
            if transition[3].startswith("push "):
                current_stack.append(transition[3][5:])
                current_state = transition[4]
                if log:
                    print(f"Action: Push | New stack: {current_stack}")
            elif transition[3].startswith("pop"):
                if current_stack:
                    current_stack.pop()
                current_state = transition[4]
                if log:
                    print(f"Action: Pop | New stack: {current_stack}")
            elif transition[3].startswith("check "):
                if current_stack and current_stack[-1] == transition[3][6:]:
                    current_state = transition[4]
                    if log:
                        print(f"Action: Check | New state: {current_state}")
            transition_applied = True
            break
        else:
            print(f"Ignoring transition: {transition} | ")
    if not transition_applied and log:
        print(f"No valid transition found for symbol: {symbol} | State: {current_state} | Stack: {current_stack}")

    result_state = current_state in final and len(current_stack) == 1 and current_stack[0] == stackinitial
    if log:
        print(f"Final state: {current_state} | Final stack: {current_stack} | Accepted: {result_state}")
    return result_state
