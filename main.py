import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil 
import subprocess
# from elevenlabs import generate, play
# from elevenlabs import set_api_key
# from api_key import api_key_data

# set_api_key(api_key_data)

# def engine_talk(query):
#     audio = generate(
#         text=query, 
#         voice='Grace',
#         model="eleven_monolingual_v1"
#     )
#     play(audio)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon, it's {day} and the time is {t}")
    else:
        speak(f"Good evening, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is ")
    week={
    "monday": "Boss, from 9:00 to 9:50 you have Software class, from 09:50 to 10:40 you have Resources class, from 12:40 to 1:40 you have a break, and today you have further classes from 2:00 onwards.",
    "tuesday": "Boss, from 9:00 to 11:50 you have Java class, from 12:40 to 01:40 you have a break, from 1:40 to 2:30 you have Full Stack Development class.",
    "wednesday": "Boss, today you have a full day of classes. From 9:00 to 09:50 you have Computer Graphics class, from 11:00 to 11:50 you have Resources class, from 12:00 to 1:40 you have a break, and today you have Mentoring from 2:00 onwards.",
    "thursday": "Boss, today you have a full day of classes. From 9:00 to 09:50 you have Resources class, from 09:50 to 12:40 you have Full Stack Development Lab, from 12:40 to 1:40 you have a break, and today you have Aptitude from 2:40 onwards.",
    "friday": "Boss, today you have a full day of classes. From 9:50 to 10:40 you have Mini Project class, from 11:00 to 11:50 you have Computer Graphics class, from 11:50 to 12:40 you have Software class, from 12:40 to 1:40 you have a break, and today you have Computer Graphics Lab from 1:40 onwards.",
    "saturday": "Boss, today you have a more relaxed day. From 9:00 to 10:40 you have Computer Graphics and Full Stack Development class, from 11:00 to 12:40 you have Software and Mini Project class, and then rest of the day is off for you.",
    "sunday": "Boss, today is a holiday, but keep an eye on upcoming deadlines and use this time to catch up on any reading or project work. Be sure to watch the latest episode of One Piece."
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "word" in command:
        speak("opening Microsoft Word")
        os.startfile('C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE')

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im Calculator.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "word" in command:
        speak("closing Microsoft Word")
        os.system('taskkill /f /im WINWORD.EXE')

def browsing(query):
    if 'google' in query:
        speak("Boss, what should i search on google..")
        search_query = command().lower()
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(f"https://www.google.com/search?q={search_query}")
        # webbrowser.open(f"{s}")
    # elif 'edge' in query:
    #     speak("opening your microsoft edge")
    #     os.startfile()

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our work")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging...")

if __name__ == "__main__":
    wishMe()
    # engine_talk("Allow me to introduce myself I am Jarvis, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")
    while True:
        query = command().lower()
        # query  = input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decrease")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open word" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close word" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
            sys.exit()
