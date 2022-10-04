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


def update_profile(userId, temp, sys, dia, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    params = {"patientId": userId}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetPatientById', params=params, headers= headers)
    dictFromServer = res.json()
    stat = dictFromServer['status']

    if temp > "45":
        unit = "true"
    else:
        unit = "false"
    # print(unit)

    if stat == "Success":
        outletid = dictFromServer['response']['patientData']['outletId'] 
        pharmacyid = dictFromServer['response']['patientData']['pharmacyId'] 
        name = dictFromServer['response']['patientData']['name'] 
        email = dictFromServer['response']['patientData']['email'] 
        countrycode = dictFromServer['response']['patientData']['countryCode'] 
        number = dictFromServer['response']['patientData']['phoneNumber'] 
        age = dictFromServer['response']['patientData']['age'] 
        sex = dictFromServer['response']['patientData']['sex'] 
        verify = dictFromServer['response']['patientData']['isPhoneVerified'] 
        pic = dictFromServer['response']['patientData']['pictureId'] 
        picurl = dictFromServer['response']['patientData']['pictureUrl'] 
        fsugar = dictFromServer['response']['patientData']['fastingBloodSugar'] 
        bloods = dictFromServer['response']['patientData']['bloodSugar'] 
        pulse = dictFromServer['response']['patientData']['pulse'] 
        allergy = dictFromServer['response']['patientData']['allergies'] 
        add = dictFromServer['response']['patientData']['address'] 
        appoint = dictFromServer['response']['patientData']['totalAppointments'] 
        rating = dictFromServer['response']['patientData']['rating'] 
        calls = dictFromServer['response']['patientData']['totalCalls'] 
        dob = dictFromServer['response']['patientData']['dob'] 
        # unit = dictFromServer['response']['patientData']['temparatureUnit'] 
        lang = dictFromServer['response']['patientData']['language']    
        # print(unit)
        headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
        dictToSend2 = {
                        "id": userId,
                        "pharmacyId": pharmacyid,
                        "outletId": outletid,
                        "name": str(name),
                        "email": str(email),
                        "countryCode": str(countrycode),
                        "phoneNumber": str(number),
                        "age": age,
                        "sex": str(sex),
                        "isPhoneVerified": verify,
                        "pictureId": pic,
                        "pictureUrl": str(picurl),
                        "temparature": str(temp),
                        "fastingBloodSugar": str(fsugar),
                        "bloodSugar": str(bloods),
                        "bloodPressureSys": str(sys),
                        "bloodPressureDia": str(dia),
                        "pulse": str(pulse),
                        "allergies": str(allergy),
                        "address": str(add),
                        "totalAppointments": appoint,
                        "rating": rating,
                        "totalCalls": calls,
                        "dob": dob,
                        "temparatureUnit": unit,
                        "language": str(lang)
                        }
        res2 = requests.post('https://jarvin-dev.azurewebsites.net/api/v1/UpdatePatientProfile', headers= headers, json=dictToSend2)
        dictFromServer2 = res2.json()
        stat2 = dictFromServer2

        return stat2

# ss = update_profile("97", "39.9", "170", "80", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk3IiwibmFtZSI6IkppYm9uIiwibmJmIjoxNjY0ODc0NzY4LCJleHAiOjE2NjU0Nzk1NjgsImlhdCI6MTY2NDg3NDc2OH0.ZU_NQPtVCGHKtE6cFFaMZtsxyvRg2IGpQR3UixhPS7U")
# print(ss)


