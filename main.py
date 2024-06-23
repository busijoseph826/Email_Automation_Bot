import smtplib
import speech_recognition as sr
import pyttsx3
import datetime
import os
from email.message import EmailMessage


# Load environment variables from .env file if using dotenv
# load_dotenv()

# Initialize the recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak a given text
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and return the text
def get_info():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=5)
            print('Listening...')
            talk('Listening...')
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()
    except sr.UnknownValueError:
        talk("Sorry, I did not get that. Could you please repeat?")
        return get_info()
    except sr.RequestError:
        talk("Sorry, my speech service is down. Please try again later.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to send an email
def send_email(receiver, subject, message):
    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        
        email_address = os.getenv('EMAIL_ADDRESS', 'your-email@example.com')
        email_password = os.getenv('EMAIL_PASSWORD', 'your-password')
        
        server.login(email_address, email_password)
        
        email = EmailMessage()
        email['From'] = email_address
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(message)
        
        server.send_message(email)
        server.close()
        
        talk('Your email is sent.')
        print('Your email is sent.')
    except Exception as e:
        talk(f"Failed to send email. Error: {e}")
        print(f"Failed to send email. Error: {e}")

# Function to wish the user based on the time of day
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good Morning Sir!, this is your email automation bot"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon Sir!, this is your email automation bot"
    else:
        greeting = "Good Evening Sir!, this is your email automation bot"
    
    print(greeting)
    talk(greeting)

# Main function to gather email information and send the email
def get_email_info():
    email_list = {
        'ramya': '20BQ1A4253@vvit.net',
        'deepak': '20BQ1A4205@vvit.net',
        'harsha': '20BQ1A4245@vvit.net',
        'sundeep': '20BQ1A4232@vvit.net'
    }

    print('To whom you want to send email?')
    talk('To whom you want to send email?')
    name = get_info()
    
    while name not in email_list:
        print('Please say the recipient name correctly.')
        talk('Please say the recipient name correctly.')
        name = get_info()
    
    receiver = email_list[name]
    
    print('What is the subject of your email?')
    talk('What is the subject of your email?')
    subject = get_info()

    print("Tell me the text in your email.")
    talk("Tell me the text in your email.")
    message = get_info()

    if receiver and subject and message:
        send_email(receiver, subject, message)
    
    print("Do you want to send more emails?")
    talk("Do you want to send more emails?")
    send_more = get_info()

    if 'yes' in send_more:
        get_email_info()
    else:
        print('Bye Sir, have a nice day.')
        talk('Bye Sir, have a nice day.')

# Entry point of the script
if __name__ == "__main__":
    wishme()
    get_email_info()
