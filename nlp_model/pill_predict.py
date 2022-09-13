import requests

def reminder_class(msg):
    res = requests.get('https://spacy-zibew.herokuapp.com/predict/{}'.format(msg))
    return res.json()

# ss = reminder_class("Remind me to take 5ml glucoplus twice a day")
# print(ss)