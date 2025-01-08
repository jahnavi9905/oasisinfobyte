import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}\n")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, the service is down.")
            return None

def get_date():
    today = datetime.date.today()
    return today.strftime("%B %d, %Y")

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    command = listen()
    if command:
        if "hello" in command:
            speak("Hi there! How are you?")
        elif "date" in command:
            date = get_date()
            speak(f"Today's date is {date}")
        elif "time" in command:
            time = get_time()
            speak(f"The current time is {time}")
        elif "search" in command:
            speak("What would you like to search for?")
            query = listen()
            if query:
                speak(f"Searching for {query}")
                search_web(query)
        else:
            speak(f"You said: {command}")
