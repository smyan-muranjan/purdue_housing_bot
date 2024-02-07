import smtplib, ssl, cv2, time, pytesseract
import numpy as np
from PIL import ImageGrab

def imToString():  
    pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Change to location of tesseract.exe
    cap = ImageGrab.grab(bbox =(1150, 700, 2250, 850))  # Modify for area of screen to capture.
    result = pytesseract.image_to_string(cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY), lang ='eng') 
    return result

def sendEmail():
    emailSender = '' # Enter email address to send address from.
    emailPassword = '' # Enter password of email address to send address from.
    emailRecievers = [] # List of recievers of email.
    body = "There is new housing available." 
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(emailSender, emailPassword)
        for reciever in emailRecievers:
            server.sendmail(emailSender, reciever, body)

def main():
    expectedOutput = "We couldn't find any available rooms."
    starttime = time.monotonic()
    while True:
        result = imToString()
        print(result)
        if expectedOutput not in result:
            sendEmail()
        time.sleep(60.0 - ((time.monotonic() - starttime) % 60.0))
        

if __name__ == "__main__":
    main()
