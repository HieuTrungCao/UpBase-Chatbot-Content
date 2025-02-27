import os
import random
import csv
import io

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

def csv_to_string(csv_file_path=None, csv_string=None, delimiter=',', quotechar='"', escapechar=None, quoting=csv.QUOTE_MINIMAL):
    """
    Converts a CSV file or string to a string representation of the CSV data.

    Args:
        csv_file_path (str, optional): The path to the CSV file. Defaults to None.
        csv_string (str, optional): A string containing CSV data. Defaults to None.
        delimiter (str, optional): The delimiter used in the CSV. Defaults to ','.
        quotechar (str, optional): The quote character used in the CSV. Defaults to '"'.
        escapechar (str, optional): The escape character used in the CSV. Defaults to None.
        quoting (int, optional): The quoting behavior. Defaults to csv.QUOTE_MINIMAL.

    Returns:
        str: A string representation of the CSV data, or None if an error occurs.
    """
    if csv_file_path:
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar, escapechar=escapechar, quoting=quoting)
                rows = list(reader)
        except FileNotFoundError:
            print(f"Error: File not found at {csv_file_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    elif csv_string:
        try:
            csvfile = io.StringIO(csv_string)
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar, escapechar=escapechar, quoting=quoting)
            rows = list(reader)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    else:
        print("Error: Either csv_file_path or csv_string must be provided.")
        return None

    output_string = ""
    for row in rows:
        output_string += ",".join(row) + "\n"

    return output_string