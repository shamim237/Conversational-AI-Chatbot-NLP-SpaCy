import requests
from googletrans import Translator
translator = Translator()

def reminder_class(msg):

    raw  = translator.detect(msg)
    if raw.lang != "en":
        convert = translator.translate(msg, dest= "en")
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/predict_pill/{}'.format(convert.text))
    else:
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/predict_pill/{}'.format(msg))

    return res.json()
# ss = reminder_class("remind me to take 4 glucoplus twice a day")
# print(ss)