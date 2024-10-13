import os, sys
from colorama import Fore, init
import time 
from tqdm import tqdm
#Windows
init()

file_list = []
file_e = []

def searching_files(base_directory):
    with tqdm(
        total=500000,  
        unit="file",
        desc=Fore.BLUE + "[*] Searching files"+ Fore.RESET,
        bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET)) as pbar:
    
        for root, _, files in os.walk(base_directory):
            for file in files:
                if file == 'ransomware.py' or file == 'allfiles1.py':
                    full_route = os.path.join(root, file)
                    file_e.append(full_route)
                else: 
                    full_route = os.path.join(root, file)
                    read_file(full_route)

                pbar.update(1)
                #time.sleep(0.2)
    pbar.close()
    sys.stdout.flush()
    print(f"{Fore.GREEN}[!] Total files found: {len(file_list)}")
    #print(f"{Fore.YELLOW}{file_list}")





def read_file(route):
    try:
        with open(route, 'r'):
            file_list.append(route)
    except Exception:
        pass


