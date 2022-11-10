import requests
from datetime import datetime
import recognizers_suite as Recognizers
from recognizers_suite import Culture
culture = Culture.English

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


def appoint_id(userId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"patientId": userId, "pageIndex": 1, "pageSize": 20, "appointmentType": "Future"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetAllPatientAppointment', headers= headers, json=dictToSend)
    dictFromServer = res.json()
    stat = dictFromServer['status']
    if stat == "Success":
        ids = dictFromServer['response']['appointment'][0]['id']
        return ids

# ss = appoint_id("106", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NjMzMjUxNDMsImV4cCI6MTY2MzkyOTk0MywiaWF0IjoxNjYzMzI1MTQzfQ.flP57DJYaYMcEPZbspLzl5dKO8UFvWhQrLrgHjgnFt")
# print(ss)


def upcoming_appointment(id, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {
                    "pageIndex": 1,
                    "pageSize": 20,
                    "patientId": id,
                    "appointmentType": "future"
                }
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetAllPatientAppointment', headers= headers, json=dictToSend)
    dictFromServer = res.json()
    return dictFromServer



def date_cal(date):

    today = datetime.now()
    today = datetime.strftime(today, "%Y-%m-%d")   
    today = datetime.strptime(today, "%Y-%m-%d").date()

    raw = Recognizers.recognize_datetime(date, culture) 
    times = []     
    for i in raw:
        raw = i.resolution
        dd = raw['values']
        for j in dd:
            tim = j['value']  
            times.append(tim) 
    for i in times:
        datey = datetime.strptime(i, "%Y-%m-%d").date()
        if datey >= today:
            return i
        else:
            pass
