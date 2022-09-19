import requests

def predict_appoint(msg):
    res = requests.get('https://appoint-spacy.herokuapp.com/predict/{}'.format(msg))
    return res.json()

ss = predict_appoint("Book an appointment on 23 sept")
print(ss)