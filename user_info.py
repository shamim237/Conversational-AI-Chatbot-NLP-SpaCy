import requests

def check_user(userId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    params = {"patientId": userId}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetPatientById', params=params, headers= headers)
    dictFromServer = res.json()
    stat = dictFromServer['status']
    return stat

# aa = check_user("106", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NTk1MjI2NDksImV4cCI6MTY2MDEyNzQ0OSwiaWF0IjoxNjU5NTIyNjQ5fQ.6Fio8EoUsNyGZwdXB1XmXCoFPPyPf0SyaF9RGZeU7zs")
# print(aa)

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