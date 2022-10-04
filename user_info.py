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

def outlet_ids(userId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    params = {"patientId": userId}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetPatientById', params=params, headers= headers)
    dictFromServer = res.json()
    stat = dictFromServer['status']
    if stat == "Success":
        st = dictFromServer['response']['patientData']['outletId']
        return st



# def check(userId, temp, sys, dia, token):
#     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
#     params = {"patientId": userId}
#     res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetPatientById', params=params, headers= headers)
#     dictFromServer = res.json()
#     stat = dictFromServer
    
#     dictToSend2 = {
#                     "pharmacyId": 1,
#                     "outletId": 7,
#                     "name": name,
#                     "email": email,
#                     "countryCode": countrycode,
#                     "phoneNumber": number,
#                     "age": age,
#                     "sex": sex,
#                     "isPhoneVerified": verify,
#                     "pictureId": pic,
#                     "pictureUrl": picurl,
#                     "temparature": temp,
#                     "fastingBloodSugar": fsugar,
#                     "bloodSugar": bloods,
#                     "bloodPressureSys": sys,
#                     "bloodPressureDia": dia,
#                     "pulse": pulse,
#                     "allergies": allergy,
#                     "address": add,
#                     "totalAppointments": appoint,
#                     "rating": rating,
#                     "totalCalls": calls,
#                     "dob": dob,
#                     "temparatureUnit": unit,
#                     "language": lang
#                     }
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/v1/UpdatePatientProfile', json=dictToSend2)

#     return stat

# ss = check("97", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk3IiwibmFtZSI6IkppYm9uIiwibmJmIjoxNjY0ODY1MzI3LCJleHAiOjE2NjU0NzAxMjcsImlhdCI6MTY2NDg2NTMyN30.jDRQ1MFkPwAdSilsAnp1itJqtPfwR0wFbwue5BONbV0")
# print(ss)


