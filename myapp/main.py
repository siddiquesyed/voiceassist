import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import speech_recognition as sr
import pyttsx3 
import wikipedia
import webbrowser
import pyautogui
import os
import datetime
import calendar

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio) # type: ignore
            print("You said: " + text)    
        except:
            print("Sorry could not recognize what you said")
            text = listen()     
    return text

# Define a function to recognize date and time 
def today_date():
    now = datetime.datetime.now()
    date_now = datetime.datetime.today()
    week_now = calendar.day_name[date_now.weekday()]  # Accessing day_name attribute
    month_now = now.month
    day_now = now.day
    return f"Today is {week_now}, {month_now}/{day_now}."

# Define a function to handle commands
def handle_command(command):
    # Perform different actions based on the command
    if "hello" in command:
        print("Hi, nice to meet you!")
        speak("hi nice to meet you")
    elif "who are you" in command or "define yourself" in command:
        print("Hello, I am a virtual assistant. I am here to make your life easier. You can command me to perform various tasks.")
        speak("Hello, I am a virtual assistant. I am here to make your life easier. You can command me to perform various tasks.")
    elif "what is your name" in command :
        print("My name is virtual assistant")
        speak("My name is virtual assistant")
    elif "who am I" in command:
        print("You must probably be a human")
        speak("You must probably be a human")
    elif "how are you" in command:  
        print("I am fine, thank you\nHow are you?")
        speak("I am fine, thank you. How are you?")
    elif "date" in command or "day" in command or "month" in command:
        get_today = today_date()
        print(get_today)
        speak(get_today) 
    elif "who is" in command:
        person = command.split("who is")[-1]
        wiki = wikipedia.summary(person, sentences=2)
        print(wiki)
        speak(wiki)
    elif "open" in command:
        command = command.replace("open", " ")

        speak("opening" + command)

        pyautogui.press("super")

        pyautogui.typewrite(command)

        pyautogui.press("enter")

    elif "search" in command:
        query = command.split("search")[-1]
        speak("searching" + query)
        webbrowser.open("https://www.google.com/search?q=" + query)
    elif "play" in command:
        song = command.split("play")[-1]
        os.system("mpg321 " + song)
    elif "time" in command:
        now = datetime.datetime.now()
        hour = now.hour
        meridien = "AM"
        if hour >= 12:
            meridien = "PM"
            hour -= 12
        if hour == 0:
            hour = 12
        minute = str(now.minute)
        speak_text = "It is " + str(hour) + ":" + minute + " " +  meridien + "."
        print(speak_text)
        speak(speak_text)
    elif "exit" or "bye" or "stop" or "close" in command:
        print("Bye!Have a nice day, see you again")
        speak("bye have a nice day see you again")
        exit()
    
    else:
        speak("")

# Define a Kivy App class
class VoiceAssistantApp(App):
    def build(self):
        self.icon="voice-assistant.png"
        layout = BoxLayout(orientation='vertical')
        self.output_label = Label(text="Listening...")
        self.listen_button = Button(text="Listen")
        self.listen_button.bind(on_press=self.on_listen_button_press) # type: ignore
        layout.add_widget(self.output_label)
        layout.add_widget(self.listen_button)
        return layout
    
    def on_listen_button_press(self, instance):
        command = listen()
        self.output_label.text = "You said: " + command
        handle_command(command)

# Run the Kivy application
if __name__ == '__main__':
    VoiceAssistantApp().run()
   
