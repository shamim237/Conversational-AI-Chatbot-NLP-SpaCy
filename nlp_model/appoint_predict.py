import requests

def predict_appoint(msg):
    res = requests.get('https://appoint-spacy.herokuapp.com/predict/{}'.format(msg))
    return res.json()

# ss = predict_appoint("Book an appointment with Josh Butler of Mirpur Pharmacy at 9:30 AM on 31st September 2022")
# print(ss)