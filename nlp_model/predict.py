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
# ss = predict_class("book an appointment on today")
# print(ss)


def response(msg):
    raw  = translator.detect(msg)
    if raw.lang != "en":
        convert = translator.translate(msg, dest= "en")
        res = requests.get('https://contextual-jarvis.herokuapp.com/predict/{}'.format(convert.text))
    else:
        res = requests.get('https://contextual-jarvis.herokuapp.com/predict/{}'.format(msg))
    return res.text