import pyttsx3
import wikipedia
import speech_recognition as sr
import webbrowser
import datetime
import os
import sys
import smtplib
from news import news, getNewsUrl
from diction import translate, speak, takeCommand
from youtube import youtube
from sys import platform
from helpers import *
import getpass
import cv2

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

class Kush:
    def __init__(self) -> None:
        if platform == 'linux' or platform == 'linux2':
            self.chrome_path = '/usr/bin/google-chrome'
        elif platform == 'win32' or platform == 'win64':
            self.chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        else:
            print('unsupported Operating System')
            exit(1)
        webbrowser.register(
            'chrome', None, webbrowser.BackgroundBrowser(self.chrome_path)
        )
    
    def wish(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak('Good Morning!')
        if hour >=12 and hour < 18:
            speak('Good Afternoon!')
        else:
            speak('Good Evening!')
        
        weather()
        speak('I am KUSH, How may I help you?')
    
    def sendMail(self, to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('email', 'password')
        server.sendmail('email', to, content)
        server.close()
        
    def execute_query(self, query):
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace('wikipedia', ' ')
            result = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            speak(result)
        
        elif 'youtube downloader' in query:
            exec(open('youtube_downloader.py').read())
        
        elif 'voice' in query:
            if 'female' in query:
                engine.setProperty('voice', voices[1].id)
            else:
                engine.setProperty('voice', voices[0].id)
            speak("Hello Sir, I have switched my voice. How is it?")
        
        if 'Kush are you there' in query:
            speak("Yes Sir, I am at your service!")
        
        elif 'open youtube' in query:
            webbrowser.get('chrome').open_new_tab('https://youtube.com')
            
        elif 'joke' in query:
            joke()
        
        elif 'screenshot' in query:
            speak('Taking Screenshot!')
            screenshot()
        
        elif 'open google' in query:
            webbrowser.get('chrome').open_new_tab('https://google.com')
        
        elif 'search youtube' in query:
            speak('What do you want searched!')
            youtube(takeCommand())
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f'Sir, the time is {strTime}')
        
        elif 'search' in query:
            speak('What do you want to search?')
            search = takeCommand()
            url = 'https://google.com/search?q='+search
            webbrowser.get('chrome').open_new_tab(url)
            speak('Here is what I found on google for'+search)
        
        elif 'your name' in query:
            speak('My name is Kush')
            
        elif 'shutdown' in query:
            if platform == "win32" or platform == 'win64':
                os.system('shutdown /p /f')
            elif platform == "linux" or platform == "linux2" or "darwin":
                os.system('poweroff')
            
        elif 'remember that' in query:
            speak("What should i remember sir?")
            rememberMessage = takeCommand()
            speak("you said me to remember"+rememberMessage)
            remember = open('data.txt', 'w')
            remember.write(rememberMessage)
            remember.close()   
        
        elif 'do you remember anything' in query:
            remember = open('data.txt', 'r')
            speak("you said me to remember that" + remember.read())
            
        elif 'sleep' in query:
            sys.exit()
        
        elif 'news' in query:
            news()
            speak('Do you want to read the article?...')
            test = takeCommand()
            if 'yes' in test:
                speak('Opening Browser...')
                webbrowser.open(getNewsUrl())
                speak('Here is the news article for you.')
            else:
                speak('Thats it.')
        
        elif 'voice' in query:
            if 'female' in query:
                engine.setProperty('voice', voices[0].id)
            else:
                engine.setProperty('voice', voices[1].id)
            speak("I have changed my voice.")
        
        elif 'email to' in query:
            try:
                speak('What should I email?')
                content = takeCommand()
                to = 'email'
                self.sendEmail(to, content)
                speak('Email has been sent!')

            except Exception as e:
                speak('There was an issue. I was not able to send the email')
        
def wakeUp():
    bot = Kush()
    bot.wish()
    while True:
        query = takeCommand().lower()
        bot.execute_query()
    
if __name__ == '__main__':
    verifier = cv2.face.LBPHFaceRecognizer_create()
    verifier.read('Jarvis/Face-Recognition/model/trainer.yml')
    cascade_path = 'Jarvis/Face-Recognition/haarcascade_frontalface_default.xml'
    face = cv2.CascadeClassifier(cascade_path)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 2
    names = ['', 'Kushagra']
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    cam.set(3, 640)
    cam.set(4, 480)
    
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    while True:
        ret, frame = cam.read()
        converted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face.detectMultiScale(
            converted_img, 
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH))
        )
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 100), 2)
            
            id, accuracy = verifier.predict(converted_img[y:y+h, x:x+h])
            
            if accuracy < 100:
                speak('Face Verification done.')
                cam.release()
                cv2.destroyAllWindows()
                wakeUp()
            else:
                speak('Face Verification Unsuccessful.')
                break