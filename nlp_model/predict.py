import requests
from googletrans import Translator
translator = Translator()

def predict_class(msg):
    raw  = translator.detect(msg)
    if raw.lang != "en":
        convert = translator.translate(msg, dest= "en")
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/predict/{}'.format(convert.text))
    else:
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/predict/{}'.format(msg))

    return res.text

def response(msg):
    raw  = translator.detect(msg)
    if raw.lang != "en":
        convert = translator.translate(msg, dest= "en")
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/response/{}'.format(convert.text))
    else:
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/response/{}'.format(msg))
    return res.text