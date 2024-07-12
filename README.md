# purdue_housing_bot
This program sends an email whenever new housing is available on the Purdue Housing Portal. Run purdue_housing_bot.py in the src folder after installing prerequisites. Read the instructions fully.

## Prerequisites:
### Install Tesseract OCR
This is the software that converts an image to text.  
- ### Install for Mac
    - To install tesseract, first install [homebrew](https://brew.sh/) if you don't already have it. Then run the following command in your terminal: ```brew install tesseract```
    - The tesseract directory can be found using `brew info tesseract`,
e.g. `/usr/local/Cellar/tesseract/3.05.02/share/tessdata/`.

- ### Install for Windows

   - Installer for Windows for Tesseract is available from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Both 32-bit and 64-bit installers are available. The directory where the Tesseract is located is probably `C:\Program Files\Tesseract-OCR`.

### Install Python
Download Python [here](https://www.python.org/downloads/). Make sure to download the correct version for your operating system.

### Install required packages using Pip
Run the following commands in your terminal
```
pip install tk
pip install opencv-python
pip install pytesseract
pip install numpy
pip install pillow
```
### Install webpage refresher
Visit the Chrome web store and download an automatic page refresher [here](https://chromewebstore.google.com/search/refresh). Set the refresh rate to 20 seconds and activate it on the housing portal.

### Setup email server
- Create a new Google account to send the emails from.
- Follow the instructions [here](https://mailmeteor.com/blog/gmail-smtp-settings) for the rest of the setup instructions.

## Instructions
- Enter the email and app password **(note: this is different than the account password, refer to "Setup email server")** of the email account you set up.
- Enter the emails you would like to send the email to. Separate emails with commas.
- Enter the location of the tesseract.exe file. Refer to prerequisites for more information on where this might be.
- Hit test to take a test screenshot and send a test email.
- Hit run and start your auto refresh on your browser.
- **Make sure your screen is on the housing portal**