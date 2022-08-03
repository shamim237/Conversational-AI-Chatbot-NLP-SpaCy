import requests


def register(email, pharmacyId, name):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "name": name, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientRegistration', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['status']
    print(status)

def new_user_id(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    userId = dictFromServer['response']['patientData']['id']
    return userId

def new_token(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    token = dictFromServer['response']['token']
    return token