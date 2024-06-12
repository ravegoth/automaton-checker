import re

# VARIABLES

input_file = "input.txt"

# FUNCTII

def load_file(input_file = input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return False

def skip_comment_lines(text):
    # sterge orice incepe cu # dupa linii
    lines = text.split("\n")
    text = "\n".join([line for line in lines if not line.startswith("#")])
    text = re.sub(r"#.*", "", text)
    # sterge liniile care au doar spatiu/tab/newline
    lines = text.split("\n")
    text = "\n".join([line for line in lines if not line.strip() == ""])
    return text

def lab_parse(file_name = "input.txt"):
    # reading the file
    input_text = load_file(file_name)
    
    # preprocessing
    input_text = skip_comment_lines(input_text)

    # sigma
    letters = []
    m = re.search(r"Sigma:\n(.*?)\nEnd", input_text, re.DOTALL)
    letters = m.group(1).split("\n")
    # trim
    letters = [line.strip() for line in letters]

    # states
    states = []
    m = re.search(r"States:\n(.*?)\nEnd", input_text, re.DOTALL)
    states = m.group(1).split("\n")
    # trim
    states = [line.strip() for line in states]

    # transitions
    transitions = []
    m = re.search(r"Transitions:\n(.*?)\nEnd", input_text, re.DOTALL)
    transitions = m.group(1).split("\n")
    transitions = [line.split(",") for line in transitions]
    transitions = [(t[0].strip(), t[1].strip(), t[2].strip()) for t in transitions]

    # initial
    initial_state = ""
    m = re.search(r"Initial:\n(.*?)\nEnd", input_text, re.DOTALL)
    initial_state = m.group(1).strip()

    # final
    final_states = []
    m = re.search(r"Final:\n(.*?)\nEnd", input_text, re.DOTALL)
    final_states = m.group(1).split("\n")
    final_states = [line.strip() for line in final_states]
    
    return {
        "letters": letters,
        "states": states,
        "transitions": transitions,
        "initial_state": initial_state,
        "final_states": final_states
    }

# EXTRAGEREA PRINCIPALA

# raspuns = lab_parse()
# letters = raspuns["letters"]
# states = raspuns["states"]
# transitions = raspuns["transitions"]
# initial_state = raspuns["initial_state"]
# final_states = raspuns["final_states"]

# AFISARE DATE (pt debug)

# def debug_text():
#     print("Litere: ", letters)
#     print("Stari: ", states)
#     print("Tranzitii:")
#     for t in transitions:
#         print("In starea {}, {} duce in {}".format(t[0], t[1], t[2]))
#     print("Starea initiala: ", initial_state)
#     print("Stari finale: ", final_states)

# METODE DE ACCESARE A DATELOR

def get_section_content(content, section_name):
    # caz in care nume are :, il stergem ca sa se evite confuzii
    section_name = section_name.replace(":", "")

    input_text = skip_comment_lines(content)
    
    # extragere de la Nume: pana la primul end dupa el
    m = re.search(r"{}:\n(.*?)\nEnd".format(section_name), input_text, re.DOTALL)
    
    # daca nu exista sectiunea, return False
    if m is None:
        return False
    
    # daca nu exista continut, return ""
    if m.group(1).strip() == "":
        return ""
    
    # trim fiecare linie
    m = m.group(1).split("\n")
    m = [line.strip() for line in m]
    
    try:
        return m
    except AttributeError:
        return False # nu exista sectiunea

def get_section_list(content):
    input_text = skip_comment_lines(content)
    
    # extragere de la Nume: pana la primul end dupa el
    m = re.findall(r"(\w+):", input_text)
    
    return m