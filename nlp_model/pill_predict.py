import requests

def reminder_class(msg):
    res = requests.get('https://spacy-zibew.herokuapp.com/predict/{}'.format(msg))
    return res.json()

