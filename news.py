import requests
import json
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def news():
    url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=yourapikey'
    news = requests.get(url)
    
    news_dict = json.load(news)
    articles = news_dict['articles']
    speak('From Times of India')
    speak('Todays Headlines are...')
    for index, article in enumerate(articles):
        speak(article['title'])
        if index == len(articles)-1:
            break
        speak('Next Headline...')
    speak('These were some of the top headlines today.')

def getNewsUrl():
    return 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=yourapikey'

if __name__ == '__main__':
    news()