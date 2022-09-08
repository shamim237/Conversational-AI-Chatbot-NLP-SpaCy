import requests

def predict_appoint(msg):
    res = requests.get('https://appoint-spacy.herokuapp.com/predict/{}'.format(msg))
    return res.json()

# ss = predict_appoint("book an appointment at 10 pm today")
# print(ss)