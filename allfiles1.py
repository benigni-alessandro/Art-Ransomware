import os, sys
from colorama import Fore, init
import time
from tqdm import tqdm

# Windows
init()

file_list = []
file_e = []
carpetas_excluidas = ['AppData', 'Program Files', 'ProgramData', 'Windows']
extensiones_excluidas = ['.sys', '.dll', '.exe', '.bat', '.cmd', '.key']

def searching_files(base_directory):
    for root, dirs, files in os.walk(base_directory):
        dirs[:] = [d for d in dirs if d not in carpetas_excluidas]
        for file in files:
            if not any(file.lower().endswith(ext) for ext in extensiones_excluidas):
                full_route = os.path.join(root, file)
                read_file(full_route)



def read_file(route):
    try:
        with open(route, 'r'):
            file_list.append(route)
    except Exception:
        pass


