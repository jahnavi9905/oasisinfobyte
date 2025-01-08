import speech_recognition as sr
import pyttsx3
import smtplib
import schedule
import time
import requests
import wikipedia

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

def send_email(recipient, subject, body):
    # Simplified example, update with your email server details
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    message = f'Subject: {subject}\n\n{body}'
    server.sendmail('your_email@gmail.com', recipient, message)
    server.quit()

def set_reminder(time, task):
    schedule.every().day.at(time).do(speak, task)

def get_weather(api_key, city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    weather_data = response.json()
    return weather_data['weather'][0]['description']

def answer_question(query):
    summary = wikipedia.summary(query, sentences=2)
    return summary

if __name__ == "__main__":
    speak("Hello! How can I assist you today?")
    command = listen()
    
    if command:
        if "email" in command:
            speak("To whom should I send the email?")
            recipient = listen()
            speak("What is the subject?")
            subject = listen()
            speak("What should be the body of the email?")
            body = listen()
            send_email(recipient, subject, body)
            speak("Email sent.")
        
        elif "reminder" in command:
            speak("What time should I set the reminder for? (24-hour format HH:MM)")
            time = listen()
            speak("What is the task?")
            task = listen()
            set_reminder(time, task)
            speak(f"Reminder set for {time}.")
        
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            api_key = "your_openweathermap_api_key"
            weather_description = get_weather(api_key, city)
            speak(f"The current weather in {city} is {weather_description}.")
        
        elif "question" in command:
            speak("What would you like to know?")
            query = listen()
            answer = answer_question(query)
            speak(answer)
        
        else:
            speak(f"You said: {command}")

    # Run pending scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)
