import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import re
import smtplib, ssl, cv2, pytesseract
import numpy as np
from PIL import ImageGrab, ImageTk, Image  
from email.message import EmailMessage

class PurdueHousingBot:
    email_re = r"""(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

    window: tk.Tk
    sender_email: tk.StringVar
    sender_password: tk.StringVar
    receiver_emails: tk.StringVar
    timer: tk.IntVar
    isRunning: tk.BooleanVar
    message: tk.StringVar

    def __init__(self, root):
        self.window = root
        self.window.title("Purdue Housing Bot")
        self.window.geometry("475x250")
        self.window.minsize(475, 250)
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=10) 
        self.window.option_add("*Font", default_font)
        self.window.iconbitmap("purdue_housing_bot.ico")
        self.sender_email = tk.StringVar(self.window)
        self.sender_password = tk.StringVar(self.window)
        self.receiver_emails = tk.StringVar(self.window)
        self.timer = tk.IntVar(self.window, value=20)
        self.isRunning = tk.BooleanVar(self.window, value=False)
        self.message = tk.StringVar(self.window, value="Not Running.")
        
        self.create_widgets()
        self.window.after(0, self.run_program)
    
    def create_widgets(self):
        email_label = ttk.Label(self.window, text="Enter sender email:")
        email_label.grid(row=0, column=0)
        self.email_entry = ttk.Entry(self.window, textvariable=self.sender_email, width=32)
        self.email_entry.grid(row=1, column=0, pady=(0, 10))
        
        password_label = ttk.Label(self.window, text="Enter sender password:")
        password_label.grid(row=2, column=0)
        self.password_entry = ttk.Entry(self.window, textvariable=self.sender_password, show='*', width=32)
        self.password_entry.grid(row=3, column=0, pady=(0, 10))
        image = Image.open("purdue_logo.png")
        image = image.resize((150, 80))
        test = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.window, image=test)
        image_label.image = test    
        image_label.grid(row=0, column=1, rowspan=4)
        
        receiver_email_label = ttk.Label(self.window, text="Enter the emails of the people you want to send to, seperated by commas:")
        receiver_email_label.grid(row=4, column=0, columnspan=2, padx=(10, 0))
        self.receiver_email_entry = ttk.Entry(self.window, textvariable=self.receiver_emails, width=64)
        self.receiver_email_entry.grid(row=5, column=0, columnspan=2, padx=(10, 0), pady=(0, 10))
        

        time_label = ttk.Label(self.window, textvariable=self.timer, font="TkDefaultFont 30")
        time_label.grid(row=6, column=1, rowspan=2)
        

        self.test_btn = ttk.Button(self.window, text="Test", command=self.send_test_email)
        self.test_btn.grid(row=6, column=0)

        self.start_btn = ttk.Button(self.window, text="Start", command=self.start_program)
        self.start_btn.grid(row=7, column=0)
        
        self.stop_btn = ttk.Button(self.window, text="Stop", state="disabled", command=self.stop_program)
        self.stop_btn.grid(row=8, column=0)

        self.message_label = ttk.Label(self.window, textvariable=self.message)
        self.message_label.grid(row=8, column=1)
    
    def validate_email(self) -> bool:
        return bool(re.match(self.email_re, self.sender_email.get()))
    
    def validate_password(self) -> bool:
        return len(self.sender_password.get()) > 0
    
    def process_reciever_emails(self) -> list[str]:
        return list(map(lambda email: email.strip(), self.receiver_emails.get().split(",")))

    def validate_emails(self):
        emails = self.process_reciever_emails()
        return all(map(lambda email: re.match(self.email_re, email), emails))
    
    def validate_inputs(self) -> bool:
        is_sender_email_valid = self.validate_email()
        is_password_valid = self.validate_password()
        is_receiver_emails_valid = self.validate_emails()
        
        if is_sender_email_valid and is_password_valid and is_receiver_emails_valid:
            return True
        else:
            error_message = ("" if is_sender_email_valid else "Sender email is invalid.\n") + \
                            ("" if is_password_valid else "Password is invalid.\n") + \
                            ("" if is_receiver_emails_valid else "Receiver emails are invalid.\n")
            messagebox.showerror(title="Error", message=error_message)
            return False
    
    def start_program(self):
        if self.validate_inputs():
            self.email_entry.config(state='disabled')
            self.password_entry.config(state='disabled')
            self.receiver_email_entry.config(state='disabled')
            self.isRunning.set(True)
            self.stop_btn.config(state="normal")
            self.start_btn.config(state="disabled")
            self.message.set("Running.")
        
    def stop_program(self):
        self.email_entry.config(state='normal')
        self.password_entry.config(state='normal')
        self.receiver_email_entry.config(state='normal')
        self.isRunning.set(False)
        self.stop_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.message.set("Not Running.")
    
    def run_program(self):
        if self.isRunning.get():
            if self.timer.get() == 0:
                self.check_screen()
                self.timer.set(20)
            else:
                self.timer.set(self.timer.get() - 1)
        self.window.after(1000, self.run_program)

    def check_screen(self):
        expectedOutput = "We couldn't find any available rooms."
        result = self.screen_to_string()
        print(result)
        if expectedOutput not in result:
            self.send_email(subject="Purdue Housing Bot: New Housing Available", body="There is new housing available. Login here: https://purdue.starrezhousing.com/StarRezPortalX/")

    def screen_to_string(self) -> str:  
        pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        cap = ImageGrab.grab()
        result = pytesseract.image_to_string(cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY), lang='eng') 
        return result

    def send_test_email(self):
        self.send_email(subject="Purdue Housing Bot: Test Email", body="This is a test email. Please check that all emails recieved the message.")
        self.message.set("Test email sent.")
        self.window.after(5000, lambda: self.message.set("Not Running."))


    def send_email(self, subject: str, body: str):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_email.get()
        msg['To'] = self.process_reciever_emails()
        msg.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            try:
                server.login(self.sender_email.get(), self.sender_password.get())
                server.send_message(msg)
            except:
                messagebox.showerror(title="Error", message="Failed to send email.") 
                self.stop_program()

if __name__ == "__main__":
    root = tk.Tk()  
    app = PurdueHousingBot(root)
    root.mainloop()