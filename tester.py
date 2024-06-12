from parse import *
import json
from checker import *
import emulator

if __name__ != "__main__":
    print("This file is meant to be run as a script")
    exit(1)

# load config.json
config = json.loads(open("config.json", "r", encoding="utf-8").read().strip())
file_name = config["file"]
debug_mode = config["debug"]

# load file content
content = load_file(file_name)

# checking the file is a valid DFA configuration
if config['type'] in ["DFA", "NFA", "both"]:
    result, message = check_configuration(content)
    if not result:
        if debug_mode:
            print("DFA/NFA Configuration error: ", message)
        exit(1)

# checking the file is a valid CFG configuration
if config['type'] == "CFG":
    result, message = check_cfg_configuration(content)
    if not result:
        if debug_mode:
            print("CFG Configuration error: ", message)
        exit(1)

# checking the file is a valid PDA configuration
if config['type'] == "PDA":
    result, message = check_pda_configuration(content)
    if not result:
        if debug_mode:
            print("PDA Configuration error: ", message)
        exit(1)

# if there is a input section (Input), dats gon be used instead of
# reading it from the console
section_list = get_section_list(content)
if "Input" in section_list:
    emulator_input = get_section_content(content, "Input")
    print("Input: ", emulator_input)
else:
    print("There was no Input section -> reading from console.")
    emulator_input = input("Input: ")

# running the emulator
if config["type"] == "DFA":
    result = emulator.run_dfa(emulator_input, content, debug_mode)
    print("DFA Result: ", result)
elif config["type"] == "NFA":
    result = emulator.run_nfa(emulator_input, content, debug_mode)
    print("NFA Result: ", result)
    # emulator.bruteforce_nfa(7, emulator_input, 1)
elif config["type"] == "both":
    result_dfa = emulator.run_dfa(emulator_input, content, debug_mode)
    result_nfa = emulator.run_nfa(emulator_input, content, debug_mode)
    print("DFA Result: ", result_dfa)
    print("NFA Result: ", result_nfa)
elif config["type"] == "CFG":
    # for y in range(20):
    result = emulator.run_cfg(emulator_input[0], content, debug_mode)
    print("CFG Result: ", result)
    # results = []
    # results = emulator.run_all_cfg(emulator_input[0], content, debug_mode)
    # for x in results:
    #     print(x)
elif config["type"] == "PDA":
    result = emulator.run_pda(emulator_input, content, debug_mode)
    print("PDA Result: ", result)
else:
    print("Error: Invalid type. Must be: DFA, NFA, CFG, PDA")

exit(0)

# ---------------- JSON ----------------

# import parsejson

# c = parsejson.json_load_file("input.json")
# section_list = parsejson.get_section_list(c)
# section_content = parsejson.get_section_content(c, section_list[0])

# print("section_list:\n", section_list,"\n")
# print("section_content:\n", section_content,"\n")