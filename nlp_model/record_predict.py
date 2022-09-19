import requests
from googletrans import Translator
translator = Translator()


def predict_record(msg):
    raw  = translator.detect(msg)
    if raw.lang != "en":
        convert = translator.translate(msg, dest= "en")
        res = requests.get('https://health-record-jarvis.herokuapp.com/predict/{}'.format(convert.text))
    else:
        res = requests.get('https://health-record-jarvis.herokuapp.com/predict/{}'.format(msg))
    return res.json()


# ss = predict_record("hey jarvis, upload prescription")
# print(ss)