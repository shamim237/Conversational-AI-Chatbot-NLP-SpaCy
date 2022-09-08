import requests

def predict_class(msg):
    res = requests.get('https://chatbot-zibew.herokuapp.com/send_msg/{}'.format(msg))
    return res.text

# ss = predict_class("book an appointment on today")
# print(ss)
