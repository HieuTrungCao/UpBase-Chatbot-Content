import os
import random

path_structure = "resource/structure.txt"
path_introduction_style = "resource/introduction_style.txt"

with open(path_structure, "r") as structure_obj:
        structures = structure_obj.read()
        structure_obj.close

structures = structures.split("\n")

with open(path_introduction_style, "r") as instruction_style_obj:
        instruction_styles = instruction_style_obj.read()
        instruction_style_obj.close

instruction_styles = instruction_styles.split("\n")

def get_structure():
    index = random.randint(0, len(structures) - 1)

    return structures[index]

def get_style():
    index = random.randint(0, len(instruction_styles) - 1)
    
    return instruction_styles[index]