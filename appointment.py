import requests


def get_patientId(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    id = dictFromServer['response']['patientData']['id']
    return id


def save_appoint(date, startTime, endTime, patientId, pharmacistId, pharmacist, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"dateUtc": date, "startTime": startTime, "endTime": endTime, "patientId": patientId, "pharmacistId": pharmacistId, "pharmacistName": pharmacist, "pharmacyId": pharmacyId}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/UpsertAppointment', headers= headers, json=dictToSend)
    dictFromServer = res.json()
    # print(dictFromServer)