import requests

def save_reminder_spec_days(patientId, pharmacyId, token, pillName, med_type, pill_time, dates, dosage, color_code, shape_type, place):
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
                    "shapeType": shape_type,
                    "colorCode": color_code,
                    "dosage": dosage,
                    "doseTimes": "1",
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "inTakeTimings": pill_time,
                    "dropFor": place,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status