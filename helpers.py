import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
g = geocoder.ip('me')
data = json.load(open('Jarvis\data.json'))

def speak(audio) -> None:
        engine.say(audio)
        engine.runAndWait()

def screenshot():
    img = pyautogui.screenshot()
    img.save('/screenshot/screenshot.png')

def cpu():
    usage = str(psutil.cpu_percent())
    speak(f'{usage} CPU is being used.')
    
    battery = psutil.sensors_battery()
    speak(f'Battery is at {battery}.')

def joke():
    for i in range(3):
        speak(pyjokes.get_jokes()[i])

def weather():
    api = f'https://fcc-weather-api.glitch.me/api/current?lat={str(g.latlng[0])}&lon={str(g.latlng[1])}'
    
    data = requests.get(api)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        weather_desc = data_json['weather'][0]
        speak(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
        speak('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')
        speak('weather type ' + weather_desc['main'])
        speak('Temperature: ' + str(main['temp']) + 'degree celcius')
        speak('Humidity is ' + str(main['humidity']))
    
