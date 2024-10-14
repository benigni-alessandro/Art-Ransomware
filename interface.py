import tkinter as tk
from tkinter import *
import threading
from tkinter import ttk
from threading import Timer
from tkinter import messagebox as MessageBox
from tkinter import simpledialog
from PIL import Image, ImageTk
import re

root = tk.Tk()
root.title("Joc dels barrets")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
#root.geometry("%dx%d" % (width, height))
root.attributes('-fullscreen',True)


def start_timer(countdown):
    if countdown >= 0:
            hours, remainder = divmod(countdown, 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_label.config(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
            root.after(1000, start_timer, countdown - 1)
    else:
        timer_label.config(text="TIME IS UP!")




# frames

frame0 = tk.Frame(root, width=width, height=height/2, bg="black", borderwidth=20)
frame0.pack_propagate(False)

frame1 = ttk.Frame(root, width= width, height=height/2)
frame1.pack_propagate(False)

#titulo
titulo = ttk.Label(frame0, text="ArtLock Ransomware", font=("sans-serif", 50, "normal"))
titulo.place(relx=0.5, y=25, anchor="center")
titulo.config(foreground='white', background='black')
frame0.pack()
#image
image1 = Image.open("image.jpg")
imageR = ImageTk.PhotoImage(image1)
label1 = tk.Label(frame0, image = imageR, width=400, height=250)
label1.image = imageR


label1.place(relx=0.5, rely=0.5, anchor="center")
# subtitle
subtitle = ttk.Label(frame0, text="Your system has been encrypted", font=("sans-serif", 16, "normal"))
subtitle.place(relx=0.5, rely=0.96, anchor="center")
subtitle.config(foreground='white', background='black')


#frame 1
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

# Label para el mensaje de advertencia
adv = tk.Label(frame1, text=ransom_message, font=("Arial", 12), justify="center", anchor="center")
adv.place(relx=0.5, rely=0.37, anchor="center", width=width, height=height)
adv.config(foreground='white', background='black')




bitcoin_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
# Label para la dirección de Bitcoin
address_label = tk.Label(frame1, text=f"Pay to Bitcoin Address: {bitcoin_address}", font=("Arial", 14), bg='black', fg='red', justify='center')
address_label.place(relx=0.5, rely=0.8, anchor="center")

# Label para el temporizador
timer_label = tk.Label(frame1, font=("Arial", 16), bg='black', fg='yellow')
timer_label.place(relx=0.5, rely=0.9, anchor="center")
start_timer(48 * 3600)
frame0.pack()
frame1.pack()


root.mainloop()
