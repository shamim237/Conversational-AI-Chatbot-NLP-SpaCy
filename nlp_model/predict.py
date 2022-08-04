import requests


def predict_class(msg):
    res = requests.get('https://chatbot-zibew.herokuapp.com/send_msg/{}'.format(msg))
    return res.text


ss = predict_class("remind me to take crocin 250mg daily at 9pm for two months")
print(ss)
