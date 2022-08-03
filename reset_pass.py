import requests


def sendcode(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/ForgotPasswordSendEmail', json=dictToSend)
    dictFromServer = res.json()

def resetpass(email, code, password, pharmacyId):
    dictToSend = {"email": email, "forgotPasswordCode": code, "newPassword": password, "pharmacyId": pharmacyId}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/UpdatePatientPassword', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['response']['message']
    if status == "Updadted Successfully":
        stat = "done"
        return stat
    else:
        stat = "not done"
        return stat

