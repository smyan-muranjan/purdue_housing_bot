import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import smtplib, ssl, cv2, time, pytesseract
import numpy as np
from PIL import ImageGrab
from email.message import EmailMessage

class PurdueHousingBot:
    email_re = r"""(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

    def __init__(self, root):
        self.window = root
        self.window.title("Purdue Housing Bot")
        
        self.sender_email = tk.StringVar(self.window)
        self.sender_password = tk.StringVar(self.window)
        self.receiver_emails = tk.StringVar(self.window)
        self.timer = tk.IntVar(self.window, value=20)
        self.isRunning = tk.BooleanVar(self.window, value=False)
        self.message = tk.StringVar(self.window)
        
        self.create_widgets()
        self.window.after(0, self.run_program)
    
    def create_widgets(self):
        email_label = ttk.Label(self.window, text="Enter your email:")
        email_label.pack()
        self.email_entry = ttk.Entry(self.window, textvariable=self.sender_email)
        self.email_entry.pack()
        
        password_label = ttk.Label(self.window, text="Enter your password:")
        password_label.pack()
        self.password_entry = ttk.Entry(self.window, textvariable=self.sender_password, show='*')
        self.password_entry.pack()
        
        receiver_email_label = ttk.Label(self.window, text="Enter the emails of the people you want to send to:")
        receiver_email_label.pack()
        self.receiver_email_entry = ttk.Entry(self.window, textvariable=self.receiver_emails)
        self.receiver_email_entry.pack()
        
        time_label = ttk.Label(self.window, textvariable=self.timer)
        time_label.pack()
        
        self.test_btn = ttk.Button(self.window, text="Test", command=self.send_test_email)
        self.test_btn.pack()

        self.start_btn = ttk.Button(self.window, text="Start", command=self.start_program)
        self.start_btn.pack()
        
        self.stop_btn = ttk.Button(self.window, text="Stop", state="disabled", command=self.stop_program)
        self.stop_btn.pack()

        self.message_label = ttk.Label(self.window, textvariable=self.message)
        self.message_label.pack()
    
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
        
    def stop_program(self):
        self.email_entry.config(state='normal')
        self.password_entry.config(state='normal')
        self.receiver_email_entry.config(state='normal')
        self.isRunning.set(False)
        self.stop_btn.config(state="disabled")
        self.start_btn.config(state="normal")
    
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
