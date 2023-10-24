from difflib import get_close_matches
import pyttsx3
import json
import speech_recognition as sr

data = json.load(open('Jarvis\data.json'))
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 1
        r.energy_threshold = 400
        r.adjust_for_ambient_noise(source, duration=1.5)
        speech = r.listen(source)
    try:
        print('recognising')
        text = r.recognize_google(speech, language='en-in')
        print(text)
    except Exception as e:
        print('Could not recognise')
        return 'None'
    return text

def translate(word):
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak(f'Did you mean {x}? Yes or No?')
        response = takeCommand().lower()
        if 'yes' in response:
            speak(data[x])
        elif 'no' in response:
            speak('Cannot understand word. Please speak again.')
        else:
            speak('I didnot understand. Please try again.')
    else:
        speak('Word doesnot exist. Please check again.')

if __name__ == '__main__':
    translate()
    