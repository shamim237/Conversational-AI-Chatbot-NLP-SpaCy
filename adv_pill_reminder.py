import requests

def save_reminder_spec_days(patientId, pharmacyId, token, pillName, med_type, pill_time, dates, dosage):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in dates:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": pill_time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": med_type,
                    "shapeType": "0",
                    "colorCode": "#DB4F64",
                    "dosage": dosage,
                    "doseTimes": "1",
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "inTakeTimings": pill_time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status