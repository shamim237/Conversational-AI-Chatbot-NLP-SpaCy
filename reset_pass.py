import requests


def sendcode(email, pharmacyId):
    dictToSend = {"email": email, "pharmacyId": pharmacyId}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/ForgotPasswordSendEmail', json=dictToSend)
    dictFromServer = res.json()


# def validatecode(email, code):
#     dictToSend = {"email": email, "forgotPasswordCode": code, "pharmacyId": 1}
#     res = requests.post('https://jarviscare.azurewebsites.net/api/ValidateForgotPasswordCode', json=dictToSend)
#     dictFromServer = res.json()
#     status = dictFromServer['response']['isValid']
#     if status == True:
#         stat = "correct code"
#         return stat
#     else:
#         stat = "incorrect code"
#         return stat


def resetpass(email, code, password, pharmacyId):
    dictToSend = {"email": email, "forgotPasswordCode": code, "newPassword": password, "pharmacyId": pharmacyId}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/UpdatePatientPassword', json=dictToSend)
    dictFromServer = res.json()
    status = dictFromServer['response']['message']
    if status == "Updadted Successfully":
        stat = "done"
        return stat
    else:
        stat = "not done"
        return stat

ss = resetpass("zarinmushrat87@gmail.com", "692852", "zarin1234", "1")
print(ss)

# le = input("Enter email: ")
# le = le.lower()
# sendcode(le)
# code = input("Enter code: ")
# code = code.lower()
# stat = validatecode(le, code)
# if stat == "correct code":
#     password = input("Enter new password: ")
#     password = password.lower()
#     #stat = resetpass(le, code, password)
#     print("done")
# else:
#     print(stat)
#     print("Please try again")

# # dictToSend = {"email": "smjibon237@gmail.com", "pharmacyId": 1}
# # res = requests.post('https://jarviscare.azurewebsites.net/api/ForgotPasswordSendEmail', json=dictToSend)
# # dictFromServer = res.json()


# # def validatecode(email, code):
# #     dictToSend = {"email": email, "forgotPasswordCode": code, "pharmacyId": 1}
# #     res = requests.post('https://jarviscare.azurewebsites.net/api/ValidateForgotPasswordCode', json=dictToSend)
# #     dictFromServer = res.json()
# #     status = dictFromServer['response']['isValid']
# #     return status
# # ##print(status)

# # stats = validatecode("smjibon237@gmail.com", "797748")

# # if stats is True:
# #     print("valid")
# # if stats == "False":
# #     print("invalid")

# # def resetpass(email, code, password):
# #     dictToSend = {"email": email, "forgotPasswordCode": code, "newPassword": password, "pharmacyId": 1}
# #     res = requests.post('https://jarviscare.azurewebsites.net/api/UpdatePatientPassword', json=dictToSend)
# #     dictFromServer = res.json()
# #     status = dictFromServer['response']['message']
# #     return status