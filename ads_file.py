#!/usr/bin/env python3
import argparse
import os
import sys
from termcolor import colored
import signal
import subprocess
import win32file
import win32con
import winreg

# Ctrl + C Handler
def def_handler(sig, frame):
    print(colored(f"\n[!] Saliendo...\n"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Función para crear un ADS
def ads_creation(filename, streamname):
    try:
        # Crear un flujo de datos alternativo en un archivo
        with open(f"{filename}:{streamname}", "wb") as ads_file:
            ads_file.write(b"Datos dentro del flujo de datos alternativo.")
        print(colored(f"[+] ADS creado: {filename}:{streamname}", "green"))
    except Exception as e:
        print(colored(f"[-] Error creando ADS: {e}", "red"))

# Función para crear un ADS en Windows
def create_ads_windows(file_path, stream_name, data):
    try:
        # Crear o abrir el archivo ADS
        handle = win32file.CreateFile(
            f"{file_path}:{stream_name}",
            win32con.GENERIC_WRITE,
            0,
            None,
            win32con.OPEN_ALWAYS,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )
        # Escribir los datos en el ADS
        win32file.WriteFile(handle, data)
        win32file.CloseHandle(handle)
        print(colored("[+] ADS creado con éxito.", "green"))
    except Exception as e:
        print(colored(f"[-] Error al crear el ADS: {e}", "red"))

# Función principal
if __name__ == '__main__':
    print(colored("[!] Inicio del ransomware...", "green"))

    # Configuración de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help=colored("[*] Especifica el archivo para trabajar con ADS", "green"))
    parser.add_argument("-o", "--output", help=colored("[*] Mostrar flujos de datos", "green"), action="store_true")
    parser.add_argument("-a", "--add", help=colored("[*] Añadir stream al archivo", "green"), type=str)
    parser.add_argument("-e", "--extract", help=colored("[*] Extraer todos los flujos de datos", "green"), action="store_true")
    parser.add_argument("-d", "--delete", help=colored("[*] Eliminar todos los flujos de datos", "red"), action="store_true")
    args = parser.parse_args()

    sistema = sys.platform.lower()

    # Identificación del sistema operativo
    if 'win' in sistema:
        sistema = "windows"
    elif 'linux' in sistema:
        sistema = "linux"
    else:
        print(colored("[!] Sistema operativo no soportado.", "red"))
        sys.exit(1)

    # Proceso para sistemas Linux (Placeholder, ya que ADS no es aplicable en Linux)
    if sistema == "linux":
        print(colored("[!] ADS no soportado en Linux. Solo disponible en Windows.", "red"))

    # Proceso para sistemas Windows
    elif sistema == "windows":
        if args.file:
            decoy = args.file
            print(colored(f"[+] Archivo especificado: {decoy}", "green"))

            if args.add:
                exefile = args.add
                print(colored(f"[+] ADS a añadir: {exefile}", "red"))

                # Llamar a la función para crear el ADS
                ads_creation(decoy, exefile)

                # Intentar ejecutar el archivo ADS (si es ejecutable)
                try:
                    exepath = f"{decoy}:{exefile}"
                    subprocess.run([exepath], check=True)
                    print(colored("[+] ADS ejecutado correctamente", "green"))
                except subprocess.CalledProcessError as e:
                    print(colored(f"[-] Error ejecutando el ADS: {e}", "red"))

        else:
            print(colored("[!] Debes especificar un archivo.", "red"))
            sys.exit(1)
