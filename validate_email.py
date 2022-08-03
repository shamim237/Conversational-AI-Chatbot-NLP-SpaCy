import requests


def validateuser(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/ValidateEmail', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['status']
    return status

def email_or_gmail(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['status']
    return status

def user_id(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    userId = dictFromServer['response']['patientData']['id']
    return userId

def gmail_token(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    token = dictFromServer['response']['token']
    return token   

def user_id_email(email, pharmacyId, password):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "password": password, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    userId = dictFromServer['response']['patientData']['id']
    return userId

def email_token(email, pharmacyId, password):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "password": password, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    token = dictFromServer['response']['token']
    return token   
