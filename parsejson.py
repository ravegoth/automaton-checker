import json

def json_load_file(file_name):
    # a json
    return json.loads(open(file_name, "r", encoding="utf-8").read().strip())

def get_section_list(c):
    # keys in the main dict
    return list(c.keys())

def get_section_content(c, section):
    # the content of a section
    return c[section]