import os
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
import time

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice', 'ru')
for voice in voices:
    if voice.name == 'Anna':
        tts.setProperty('voice', voice.id)

hello = ["привет", "здравствуй", "ку", "приветик"]

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите... ")
        audio = r.listen(source)
    try:
        our_speech = r.recognize_google(audio, language="ru")
        print("Вы сказали: " + our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"


def do_command(message):
    message = message.lower()
    #for hello
    if "привет" in message:
        say("привет")
    elif "скажи погоду" in message:
        weather()
    elif "который час" in message:
        hours = time.strftime('%H', time.localtime())
        min = time.strftime('%M', time.localtime())
        say("Сейчас " + str(hours) + " часов " + str(min) + " минут")

def say(message):
    tts.say(message)
    tts.runAndWait()

def weather():
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Tyumen&appid=5476bc176cad78117f140a4a55570fc4&mode=html")
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find('div', title="Current Temperature")
    temp = quotes.text
    temp = temp.replace('C', '')
    temp = temp.replace('°', '')
    temp = str(round(float(temp)))
    print("Погода в Тюмени " + str(temp) + " градусов")
    say("Погода в Тюмени " + str(temp) + " градусов")

if __name__ == '__main__':
    while True:
        command = listen()
        do_command(command)