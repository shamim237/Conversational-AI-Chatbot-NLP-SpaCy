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

# ss = upcoming_appointment("106", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NjA3MTA0NTMsImV4cCI6MTY2MTMxNTI1MywiaWF0IjoxNjYwNzEwNDUzfQ.lC9KMEwbclWpXPqUtOwdU-m3_C7rsmhFTY147lbxmN8")
# if ss['response']['appointment'] == []:
#     print("You have no upcoming appointments.")
# else:
#     apps = []
#     pharmacist = []
#     dates = []
#     starttimes = []
#     endtimes = []

#     appoint = ss['response']['appointment']
#     count = 0
#     for i in appoint:
#         count += 1
#         pharmacistName = i["pharmacistName"]
#         date = i["dateUtc"]
#         date = date[:10]
#         startTime = i["startTime"]
#         endTime = i["endTime"]
#         apps.append(count)
#         pharmacist.append(pharmacistName)
#         dates.append(date)
#         starttimes.append(startTime)
#         endtimes.append(endTime)

#     sss = []
#     for i in range(len(apps)):
#         dd = "Appointment " + str(apps[i]) + ": \n" + "Pharmacist: " + pharmacist[i] + "\n" + "Date: " + dates[i] + "\n" + "Time: " + starttimes[i] + " - " + endtimes[i]
#         sss.append(dd)

#     print("\n".join(sss))
#     # print(len(apps))


