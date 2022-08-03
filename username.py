import requests


def check_name_gmail(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    name = dictFromServer['response']['patientData']['name']
    if name is None:
        return "Not Found"
    else:
        return name

def check_name_email(email, pharmacyId, password):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "password": password, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    name = dictFromServer['response']['patientData']['name']
    return name

def check_passwrd_email(email, pharmacyId, password):
    dictToSend = {"email": email, "password": password, "pharmacyId": pharmacyId, "loginType": "Email"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['status']
    return status
