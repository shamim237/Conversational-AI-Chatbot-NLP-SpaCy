import requests

def validatecode(email, code, pharmacyId):
    dictToSend = {"email": email, "forgotPasswordCode": code, "pharmacyId": pharmacyId}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/ValidateForgotPasswordCode', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['response']['isValid']
    if status == True:
        stat = "correct code"
        return stat
    else:
        stat = "incorrect code"
        return stat