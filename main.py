import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greet():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your desktop assistant Jenny. How can I help you today?")


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return "None"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "None"


def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email.")


faq_database = {
    "what is your name": "I am your desktop assistant Jenny.",
    "what can you do": "I can perform various tasks like searching the web, opening websites, sending emails, and more."
}


def handle_faq(query):
    for question, answer in faq_database.items():
        if question in query:
            speak(answer)
            return True
    return False


def assistant():
    try:
        greet()
        while True:
            query = listen()

            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in query:
                webbrowser.open("https://youtube.com")

            elif 'open google' in query:
                webbrowser.open("https://google.com")

            elif 'open chat gpt' in query:
                webbrowser.open("https://openai.com")

            elif 'open stackoverflow' in query:
                webbrowser.open("https://stackoverflow.com")

            elif 'open amazon' in query:
                webbrowser.open("https://amazon.com")

            elif 'open facebook' in query:
                webbrowser.open("https://facebook.com")

            elif 'open twitter' in query:
                webbrowser.open("https://twitter.com")

            elif 'open instagram' in query:
                webbrowser.open("https://instagram.com")

            elif 'the time' in query:
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {str_time}")

            elif 'open vs code' in query:
                username = getpass.getuser()
                code_path = f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                if os.path.exists(code_path):
                    os.startfile(code_path)
                else:
                    speak("VS Code is not installed in the specified path.")

            elif 'send email' in query:
                try:
                    speak("What should I say?")
                    content = listen()
                    to = "recipient@example.com"  # Replace with actual recipient email
                    send_email(to, content)
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't send the email.")

            elif 'exit' in query or 'bye' in query or 'close program' in query:
                speak("Goodbye! Have a great day!")
                break

            elif 'hello' in query or 'hi' in query:
                responses = [
                    "Hello! How can I help you?",
                    "Hi there! What can I do for you?",
                    "Hello, what can I assist you with?"
                ]
                speak(random.choice(responses))

            elif any(word in query for word in ['thank', 'thanks', 'thank you']):
                responses = [
                    "You're welcome!",
                    "Glad I could help!",
                    "No problem!",
                    "You're welcome. Is there anything else I can assist with?"
                ]
                speak(random.choice(responses))

            else:
                if not handle_faq(query):
                    responses = [
                        "I'm not sure I understand.",
                        "Could you please repeat that?",
                        "I'm still learning. Can you be more specific?",
                        "Sorry, I didn't get that.",
                        "Let me check that for you."
                    ]
                    speak(random.choice(responses))
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Something went wrong. Please try again.")


if __name__ == "__main__":
    assistant()