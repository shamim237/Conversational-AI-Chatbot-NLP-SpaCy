import requests



def check_reminder(id, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"pageIndex": 1, "pageSize": 100, "pharmacyId": pharmacyId, "patientId": id, "lastUpdatedTimeTicks": 0}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['response']['pillReminder']
    if status == []:
        return 'not set'
    else:
        return 'already set'

def get_patient_id(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['response']['patientData']['id']
    return status


def save_reminder_one_time(patientId, pharmacyId, token, pillName, pillType, dosage, time, day, isRecurring, recurringValue):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": pillType,
                    "shapeType": "0",
                    "colorCode": "#DB4F64",
                    "dosage": dosage,
                    "doseTimes": 1,
                    "isRecurring": isRecurring,
                    "recurringValue": recurringValue,
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_multi_time(patientId, pharmacyId, token, pillName, pillType, dosage, time, day, isRecurring, recurringValue, dosage_time):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": pillType,
                    "shapeType": "0",
                    "colorCode": "#DB4F64",
                    "dosage": dosage,
                    "doseTimes": dosage_time,
                    "isRecurring": isRecurring,
                    "recurringValue": recurringValue,
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_one_time_capsule(patientId, pharmacyId, token, pillName, pillType, dosage, time, day, isRecurring, recurringValue):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": pillType,
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": dosage,
                    "doseTimes": 1,
                    "isRecurring": isRecurring,
                    "recurringValue": recurringValue,
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_multi_time_capsule(patientId, pharmacyId, token, pillName, pillType, dosage, time, day, isRecurring, recurringValue, dosage_time):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": pillType,
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": dosage,
                    "doseTimes": dosage_time,
                    "isRecurring": isRecurring,
                    "recurringValue": recurringValue,
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_one(patientId, pharmacyId, token, pillName, time, day):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "0",
                    "shapeType": "0",
                    "colorCode": "#DB4F64",
                    "dosage": "1",
                    "doseTimes": "1",
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_multi(patientId, pharmacyId, token, pillName, time, day, dosage_time):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "0",
                    "shapeType": "0",
                    "colorCode": "#DB4F64",
                    "dosage": 1,
                    "doseTimes": dosage_time,
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_one_capsule(patientId, pharmacyId, token, pillName, time, day):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "2",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": "1",
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_multi_capsule(patientId, pharmacyId, token, pillName, time, day, dosage_time):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "2",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": 1,
                    "doseTimes": dosage_time,
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_one_syrup(patientId, pharmacyId, token, pillName, time, day, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "4",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": "1",
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "dosageInMl": dose,
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_multi_syrup(patientId, pharmacyId, token, pillName, time, day, dosage_time, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "4",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": dosage_time,
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "dosageInMl": dose,
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status


def save_reminder_spec_days_one_syringe(patientId, pharmacyId, token, pillName, time, day, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "3",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": "1",
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "dosageInMl": dose,
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_multi_syringe(patientId, pharmacyId, token, pillName, time, day, dosage_time, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "3",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": dosage_time,
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "dosageInMl": dose,
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status


def save_reminder_spec_days_one_drops(patientId, pharmacyId, token, pillName, time, day, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "1",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": dose,
                    "doseTimes": "1",
                    "isRecurring": "false",
                    "dropFor": "Eye",
                    "recurringValue": "0",
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_spec_days_multi_drops(patientId, pharmacyId, token, pillName, time, day, dosage_time, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "1",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": dose,
                    "doseTimes": dosage_time,
                    "isRecurring": "false",
                    "recurringValue": "0",
                    "dropFor": "Eye",
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status



def save_reminder_one_time_syrup(patientId, pharmacyId, token, pillName, time, day, isRecurring, recurringValue, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "4",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": "1",
                    "isRecurring": isRecurring,
                    "recurringValue": recurringValue,
                    "dosageInMl": dose,
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_multi_time_syrup(patientId, pharmacyId, token, pillName, time, day, isRecurring, recurringValue, dosage_time, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "4",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": dosage_time,
                    "isRecurring":isRecurring,
                    "recurringValue": recurringValue,
                    "dosageInMl": dose,
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status


def save_reminder_one_time_syringe(patientId, pharmacyId, token, pillName, time, day, isRecurring, recurringValue, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "3",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": "1",
                    "isRecurring": isRecurring,
                    "recurringValue": recurringValue,
                    "dosageInMl": dose,
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_multi_time_syringe(patientId, pharmacyId, token, pillName, time, day, isRecurring, recurringValue, dosage_time, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "3",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": "1",
                    "doseTimes": dosage_time,
                    "isRecurring":isRecurring,
                    "recurringValue": recurringValue,
                    "dosageInMl": dose,
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status



def save_reminder_one_time_drop(patientId, pharmacyId, token, pillName, time, day, isRecurring, recurringValue, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    send = []
    for i in day:
        dictToSend = {
                        "id":0,
                        "pillReminderId":0,
                        "day": i,
                        "time": time,
                    }
        send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "3",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": dose,
                    "doseTimes": "1",
                    "isRecurring": isRecurring,
                    "recurringValue": recurringValue,
                    "dropFor": "Eye",
                    "inTakeTimings": time,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status

def save_reminder_multi_time_drop(patientId, pharmacyId, token, pillName, time, day, isRecurring, recurringValue, dosage_time, dose):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    strs = ' '.join(map(str, time))
    strs = strs.replace(" ", ",")
    send = []
    for j in time:
        for i in day:
            dictToSend = {
                            "id":0,
                            "pillReminderId":0,
                            "day": i,
                            "time": j,
                        }
            send.append(dictToSend)
    sent = send
    dictToSend = {
                    "id": 0,
                    "patientId": patientId,
                    "pharmacyId": pharmacyId,
                    "pillName": pillName,
                    "pillType": "3",
                    "shapeType": "-1",
                    "colorCode": "",
                    "dosage": dose,
                    "doseTimes": dosage_time,
                    "isRecurring":isRecurring,
                    "recurringValue": recurringValue,
                    "dropFor": "Eye",
                    "inTakeTimings": strs,
                    "pillReminderSlots": sent,
                }

    res = requests.post('https://jarvin-dev.azurewebsites.net/api/CreatePillReminder', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer
    return status