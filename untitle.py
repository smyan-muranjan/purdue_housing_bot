import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import reduce
import re

email_re = r"""(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

validate_email = lambda: True if re.match(email_re, senderEmail.get()) else False

validate_password = lambda: len(senderPassword.get()) > 0

strip_email = lambda email: email.strip()

def validate_emails():
    emails = list(map(strip_email, receiverEmails.get().split(",")))
    return all(map(lambda email: re.match(email_re, email), emails))

def validate_inputs():
    is_sender_email_valid = validate_email()
    is_password_valid = validate_password()
    is_receiver_emails_valid = validate_emails()
    if is_sender_email_valid and is_password_valid and is_receiver_emails_valid:
        pass
    else:
        error_message = ("" if is_sender_email_valid else "Sender email is invalid.\n") + \
                        ("" if is_password_valid else "Password is invalid.\n") + \
                        ("" if is_receiver_emails_valid else "Receiver emails are invalid.\n")
        messagebox.showerror(title="Error", message=error_message)
    

def runProgram(timer: tk.IntVar, isRunning: tk.BooleanVar):
    if isRunning.get():
        if timer.get() == 0:
            timer.set(60)
        else:
            timer.set(timer.get() - 1)
    window.after(1000, lambda: runProgram(timer, isRunning))

window = tk.Tk()
window.title("Purdue Housing Bot")
senderEmail = tk.StringVar(window)
senderPassword = tk.StringVar(window)
receiverEmails = tk.StringVar(window)
timer = tk.IntVar(window, value=60)
isRunning = tk.BooleanVar(window, value=False)
ttk.Label(window, text="Enter your email:").pack()
ttk.Entry(window, textvariable=senderEmail).pack()
ttk.Label(window, text="Enter your password:").pack()
ttk.Entry(window, textvariable=senderPassword, show='*').pack()
ttk.Label(window, text="Enter the emails of the people you want to send to:").pack()
ttk.Entry(window, textvariable=receiverEmails).pack()
ttk.Button(window, text="Save", command=validate_inputs).pack()
ttk.Label(window, textvariable=timer).pack()
ttk.Button(window, text="Start", command=lambda: isRunning.set(True)).pack()
ttk.Button(window, text="Stop", command=lambda: isRunning.set(False)).pack()
window.after(0, lambda: runProgram(timer, isRunning))
window.mainloop()