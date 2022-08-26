import requests

def check_user(userId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    params = {"patientId": userId}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetPatientById', params=params, headers= headers)
    dictFromServer = res.json()
    stat = dictFromServer['status']
    return stat

def check_email(userId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    params = {"patientId": userId}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetPatientById', params=params, headers= headers)
    dictFromServer = res.json()
    stat = dictFromServer['status']
    if stat == "Success":
        email = dictFromServer['response']['patientData']['email']
        return email
    else:
        return "No email"

def check_name(userId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    params = {"patientId": userId}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetPatientById', params=params, headers= headers)
    dictFromServer = res.json()
    stat = dictFromServer['status']
    if stat == "Success":
        name = dictFromServer['response']['patientData']['name']
        return name
    else:
        return "not found"

# ss = check_name("97", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NjE0ODQ5MTQsImV4cCI6MTY2MjA4OTcxNCwiaWF0IjoxNjYxNDg0OTE0fQ.dvhrGX9TwAs8W3ovHQviJXZ0KMg_LyXlC7jQzz03nfE")
# print(ss)