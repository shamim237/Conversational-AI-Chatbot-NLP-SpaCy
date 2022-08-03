import requests

def check_health_record(id, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"pageIndex": 1, "pageSize": 40, "pharmacyId": pharmacyId, "patientId": id, "lastUpdatedTimeTicks": 0}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetAllHealthRecords', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['response']['healthRecords']
    if status == []:
        return 'no record'
    else:
        return 'recorded'

    
def save_health_record_1(patientId, title, description, healthRecordType, healthRecordDoctor, healthRecordPatient, pictureId, pictureUrl, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"id": 0,"patientId": patientId, "pharmacyId": pharmacyId, "title": title, "description": description, "healthRecordType": healthRecordType,
     "healthRecordDoctor": healthRecordDoctor, "healthRecordPatient": healthRecordPatient, "healthRecordImages": [
        {"pictureId": pictureId, "pictureUrl": pictureUrl}
        ] }
    requests.post('https://jarvin-dev.azurewebsites.net/api/AddHealthRecord', headers=headers, json=dictToSend)

def save_health_record_2(patientId, title, description, healthRecordType, healthRecordDoctor, healthRecordPatient, pictureId, pictureUrl, pictureId2, pictureUrl2, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"id": 0,"patientId": patientId, "pharmacyId": pharmacyId, "title": title, "description": description, "healthRecordType": healthRecordType,
     "healthRecordDoctor": healthRecordDoctor, "healthRecordPatient": healthRecordPatient, "healthRecordImages": [
        {"pictureId": pictureId, "pictureUrl": pictureUrl}, {"pictureId": pictureId2, "pictureUrl": pictureUrl2}
        ] }
    requests.post('https://jarvin-dev.azurewebsites.net/api/AddHealthRecord', headers=headers, json=dictToSend)


def save_health_record_3(patientId, title, description, healthRecordType, healthRecordDoctor, healthRecordPatient, pictureId, pictureUrl, pictureId2, pictureUrl2, pictureId3, pictureUrl3, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"id": 0,"patientId": patientId, "pharmacyId": pharmacyId, "title": title, "description": description, "healthRecordType": healthRecordType,
     "healthRecordDoctor": healthRecordDoctor, "healthRecordPatient": healthRecordPatient, "healthRecordImages": [
        {"pictureId": pictureId, "pictureUrl": pictureUrl}, {"pictureId": pictureId2, "pictureUrl": pictureUrl2}, {"pictureId": pictureId3, "pictureUrl": pictureUrl3}
        ] }
    requests.post('https://jarvin-dev.azurewebsites.net/api/AddHealthRecord', headers=headers, json=dictToSend)

def save_health_record_4(patientId, title, description, healthRecordType, healthRecordDoctor, healthRecordPatient, pictureId, pictureUrl, pictureId2, pictureUrl2, pictureId3, pictureUrl3, pictureId4, pictureUrl4, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"id": 0,"patientId": patientId, "pharmacyId": pharmacyId, "title": title, "description": description, "healthRecordType": healthRecordType,
     "healthRecordDoctor": healthRecordDoctor, "healthRecordPatient": healthRecordPatient, "healthRecordImages": [
        {"pictureId": pictureId, "pictureUrl": pictureUrl}, {"pictureId": pictureId2, "pictureUrl": pictureUrl2}, {"pictureId": pictureId3, "pictureUrl": pictureUrl3}, {"pictureId": pictureId4, "pictureUrl": pictureUrl4}
        ] }
    requests.post('https://jarvin-dev.azurewebsites.net/api/AddHealthRecord', headers=headers, json=dictToSend)


def save_health_record_5(patientId, title, description, healthRecordType, healthRecordDoctor, healthRecordPatient, pictureId, pictureUrl, pictureId2, pictureUrl2, pictureId3, pictureUrl3, pictureId4, pictureUrl4, pictureId5, pictureUrl5, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"id": 0,"patientId": patientId, "pharmacyId": pharmacyId, "title": title, "description": description, "healthRecordType": healthRecordType,
     "healthRecordDoctor": healthRecordDoctor, "healthRecordPatient": healthRecordPatient, "healthRecordImages": [
        {"pictureId": pictureId, "pictureUrl": pictureUrl}, {"pictureId": pictureId2, "pictureUrl": pictureUrl2}, {"pictureId": pictureId3, "pictureUrl": pictureUrl3}, {"pictureId": pictureId4, "pictureUrl": pictureUrl4}, {"pictureId": pictureId5, "pictureUrl": pictureUrl5}
        ] }
    requests.post('https://jarvin-dev.azurewebsites.net/api/AddHealthRecord', headers=headers, json=dictToSend)