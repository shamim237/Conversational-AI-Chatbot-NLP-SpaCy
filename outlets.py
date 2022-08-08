from datetime import datetime
import requests
import re
import json


def check_outlet(email, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', headers= headers, json=dictToSend)
    dictFromServer = res.json()
    outlet = dictFromServer['response']['patientData']['outletId']
    return outlet

# cc = check_outlet("sha237mim@gmail.com", "1", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NTk5NjYxMTgsImV4cCI6MTY2MDU3MDkxOCwiaWF0IjoxNjU5OTY2MTE4fQ.BWkDTTlNxhSvhBofMe1YCRfqzf6K88wMmJoC-YcTulE")
# print("Outlet: ", cc)

def outlet_name(outlet_id, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetOutletDetails/{}'.format(outlet_id), headers= headers,)
    dictFromServer = res.json()
    outlet_name = dictFromServer['response']['outletDetails']['outletName']
    return outlet_name

# cc = outlet_name("7", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NTk5NjYxMTgsImV4cCI6MTY2MDU3MDkxOCwiaWF0IjoxNjU5OTY2MTE4fQ.BWkDTTlNxhSvhBofMe1YCRfqzf6K88wMmJoC-YcTulE")
# print("Outlet_name: ", cc)

def get_pharma_id(outlet_id, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists',  headers= headers, json=dictToSend)
    dictFromServer = res.json()
    pharmacist = dictFromServer['response']["pharmacists"]
    pharma = []
    for i in pharmacist:
        pharma.append(i['id'])
    ids = str(pharma).replace("[", "").replace("]", "").replace("'", "")
    return ids



def match(pharmas, outlet_id, pharmacyId):

    dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', json=dictToSend)
    dictFromServer = res.json()
    pharmacist = dictFromServer['response']['pharmacists']
    pharma = []
    ids = []
    for i in pharmacist:
        pharma.append(i['name'])
        ids.append(i['id'])
    pharma = str(pharma).replace("[", "").replace("]", "").replace("'", "")
    ids = str(ids).replace("[", "").replace("]", "").replace("'", "")

    pharma = pharma.lower()
    pharma = pharma.split(", ")
    ids = ids.split(", ")
    ss = []
    for i in range(len(pharma)):
        list = {pharma[i]:ids[i]}
        ss.append(list)
    #print(ss)
    all = str(ss).replace("[", "").replace("]", "").replace("'",'"')
    all = re.sub(r"\"(\d{1,6})\"", r"\1", all)
    all = re.sub(r"(\d{1,6})\}(\,)", r"\1\2", all)
    all = re.sub(r"(\d{1,6}\,\s)\{", r"\1", all)
    #print(type(all))
    all = re.sub(r"\,\s\d\:\s\d{1,9}", r"", all)
    #all = re.sub(r"('\w+\s\w+)\s('\:)", r"\1\2", all)
    all = all.replace("dr mohaimin ", "dr mohaimin")
    all = json.loads(all)

    # print(all)
    if str(pharmas) in all:
        ss = all[pharmas]
        #print(ss)
        return ss
    else:
        ss = "The name you entered is not in the list of pharmacist. Please check the spelling and try again."
        return ss

# ss = match('josh buttler roy', 7, 1)
# print(ss)


def autos(outlet_id, pharmacyId, token):
    # headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + "token".format(token)}
    dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', json=dictToSend)
    dictFromServer = res.json()
    pharmacist = dictFromServer['response']["pharmacists"][0]['name']
    pharmacist = pharmacist.lower()
    return pharmacist





def get_timeslots(id, date, time, token):

    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

    dictToSend = {"pharmacistId": id, "date": date}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
    dictFromServer = res.json()

    if 'availabilitySlots' in dictFromServer['response']:
    
        timeslots = dictFromServer['response']['availabilitySlots']
        timeslots = str(timeslots).replace("[", "").replace("]", "").replace("'", "").replace(", {", "\n").replace("}", "").replace("{", "")
        timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False\n", r"", timeslots)
        timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False", r"", timeslots)
        timeslots = timeslots.replace(", isChecked: True", "")
        timeslots = timeslots.replace("startTime: ", "").replace(", endTime: ", " - ")
        timesk = timeslots.split("\n")
        stime = re.sub("(\d{2}\:\d{2}\:\d{2})\s\-\s\d{2}\:\d{2}\:\d{2}", r"\1", timeslots)
        stime = stime.split("\n")
        timess = []
        for i in stime:
            #print(i)
            format = '%H:%M:%S'
            if i > time:
                times = datetime.strptime(i, format) - datetime.strptime(time, format)
                timess.append(times)
            else:
                times = datetime.strptime(time, format) - datetime.strptime(i, format)
                timess.append(times)
        
        timess = str(timess).replace("[", "").replace("]", "").replace("datetime.timedelta(seconds=", "").replace(")", "").replace("(", "").replace(", ", ",")

        timess = timess.split(",")
        timess = [int(i) for i in timess]

        count = 0
        for i in timess:
            count += 1 
            ss = min(timess)
            if ss > 10800:
                return "NOPE"
            if ss == i:
                break
        cou = 0
        for i in timesk:
            cou += 1
            if cou == count:
                return i

    else:
        return "No slots available" 

# ss = get_timeslots(106, "2022-08-10", "3 PM", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NTk5NjYxMTgsImV4cCI6MTY2MDU3MDkxOCwiaWF0IjoxNjU5OTY2MTE4fQ.BWkDTTlNxhSvhBofMe1YCRfqzf6K88wMmJoC-YcTulE")
# print(ss)
import random
from datetime import datetime

def get_timeslots2(id, date, token):

    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"pharmacistId": id, "date": date}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
    dictFromServer = res.json()

    if 'availabilitySlots' in dictFromServer['response']:
    
        timeslots = dictFromServer['response']['availabilitySlots']

        timeslots = str(timeslots).replace("[", "").replace("]", "").replace("'", "").replace(", {", "\n").replace("}", "").replace("{", "")
        timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False\n", r"", timeslots)
        timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False", r"", timeslots)
        timeslots = timeslots.replace(", isChecked: True", "")
        timeslots = timeslots.replace("startTime: ", "").replace(", endTime: ", " - ")
        timeslots = timeslots.split("\n")
        timeslots = random.sample(timeslots, 4)
        

        return timeslots

    else:
        
        return "No slots available" 

# sd = get_timeslots2("23", "2022-08-09", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NTk5NjYxMTgsImV4cCI6MTY2MDU3MDkxOCwiaWF0IjoxNjU5OTY2MTE4fQ.BWkDTTlNxhSvhBofMe1YCRfqzf6K88wMmJoC-YcTulE")
# print(sd)

def get_avail_slot(outletid, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outletid}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', headers=headers, json=dictToSend)
    dictFromServer = res.json()
    pharmacist = dictFromServer['response']["pharmacists"]
    pharma = []
    for i in pharmacist:
        if i['availability'] == []:
            pass
        else:
            pharma.append(i['name'])  
    return pharma        
# sd = get_avail_slot(7, 1, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NTk5NjYxMTgsImV4cCI6MTY2MDU3MDkxOCwiaWF0IjoxNjU5OTY2MTE4fQ.BWkDTTlNxhSvhBofMe1YCRfqzf6K88wMmJoC-YcTulE")
# print(sd)