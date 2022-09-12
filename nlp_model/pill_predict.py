import requests

def reminder_class(msg):
    res = requests.get('https://spacy-zibew.herokuapp.com/predict/{}'.format(msg))
    return res.json()

# ss = reminder_class("set a pill reminder for bendix tablet daily at 9 pm")
# print(ss)