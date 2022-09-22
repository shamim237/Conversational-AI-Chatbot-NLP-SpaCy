import requests
from googletrans import Translator
translator = Translator()

def predict_appoint(msg):
    raw  = translator.detect(msg)
    if raw.lang != "en":
        convert = translator.translate(msg, dest= "en")
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/predict_book/{}'.format(convert.text))
    else:
        res = requests.get('https://jarvis-chatbot-model.herokuapp.com/predict_book/{}'.format(msg))
    return res.json()

# ss = predict_appoint("Book an appointment on 23 sept")
# print(ss)