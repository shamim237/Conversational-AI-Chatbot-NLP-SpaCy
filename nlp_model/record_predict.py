import requests

def predict_record(msg):
    res = requests.get('https://health-record-jarvis.herokuapp.com/predict/{}'.format(msg))
    return res.json()

# ss = predict_record("keep blood test report")
# print(ss)