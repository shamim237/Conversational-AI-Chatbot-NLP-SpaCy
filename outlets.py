from datetime import datetime
import requests
import re
import json
import random

def check_outlet(email, pharmacyId, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', headers= headers, json=dictToSend)
    dictFromServer = res.json()
    outlet = dictFromServer['response']['patientData']['outletId']
    return outlet


def outlet_name(outlet_id, token):
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetOutletDetails/{}'.format(outlet_id), headers= headers,)
    dictFromServer = res.json()
    outlet_name = dictFromServer['response']['outletDetails']['outletName']
    return outlet_name

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
    all = str(ss).replace("[", "").replace("]", "").replace("'",'"')
    all = re.sub(r"\"(\d{1,6})\"", r"\1", all)
    all = re.sub(r"(\d{1,6})\}(\,)", r"\1\2", all)
    all = re.sub(r"(\d{1,6}\,\s)\{", r"\1", all)
    all = re.sub(r"\,\s\d\:\s\d{1,9}", r"", all)
    all = json.loads(all)


    if str(pharmas) in all:
        ss = all[pharmas]
        return ss
    else:
        ss = "The name you entered is not in the list of pharmacist. Please check the spelling and try again."
        return ss

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

        starts = []
        ends = []
    
        for i in dictFromServer['response']['availabilitySlots']:
            if i['isChecked'] == True:
                start = i['startTime']
                end = i['endTime']
                starts.append(start)
                ends.append(end)

        timesk = []

        for i in range(len(starts)):
            timesk.append(starts[i] + " - " + ends[i])

        timess = []
        for i in starts:
            if i > time:
                ss = datetime.strptime(i, "%H:%M:%S") - datetime.strptime(time, "%H:%M:%S")
                timess.append(ss.total_seconds())
            
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
                ss = i.split(" - ")
                ss = datetime.strptime(ss[0], "%H:%M:%S").strftime("%I:%M %p") + " - " + datetime.strptime(ss[1], "%H:%M:%S").strftime("%I:%M %p")
                return ss

    else:
        return "No slots available" 





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
        timeslots = sorted(timeslots)
        timeslots = "\n".join(timeslots)
        timeslots = re.findall(r"\d{2}\:\d{2}\:\d{2}", timeslots)
        timest = []
        for i in timeslots:
            timeslots = datetime.strptime(i, "%H:%M:%S").strftime("%I:%M %p")
            timest.append(timeslots)

        timest = timest[0] + " - " + timest[1] + "\n" + timest[2] + " - " + timest[3] + "\n" + timest[4] + " - " + timest[5] + "\n" + timest[6] + " - " + timest[7]
        timest = timest.split("\n")

        return timest

    else:
        
        return "No slots available" 

# ss = get_timeslots2(23, "2022-08-10", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NjAwMTYwMDMsImV4cCI6MTY2MDYyMDgwMywiaWF0IjoxNjYwMDE2MDAzfQ.iAWMXS8a3xa7o9qRSIz59LxbW_uPdtdRsEmMN3OPxEk")
# print(ss)


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

# ss = get_avail_slot("48", "1", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjIzOCIsIm5hbWUiOiJTaGFtaW0gTWFoYnViIiwibmJmIjoxNjYxMTQwNDk3LCJleHAiOjE2NjE3NDUyOTcsImlhdCI6MTY2MTE0MDQ5N30.iKgWCC-AP7tisQJ3T1d7q23sBgJIIrWEERNd9qiFegg")
# print(len(ss))      
# if len(ss) == 0:
#     print("No slots available")

def timeConversion(s):
   if s[-2:] == "AM" :
      if s[:2] == '12':
          a = str('00' + s[2:8])
          a = a.replace(" AM", "")
          a = str(a) + ":00"
          a = a.replace(" ", "")

      else:
          a = s[:-2]
          a = a.replace(" AM", "")
          a = str(a) + ":00"
          a = a.replace(" ", "")
   else:
      if s[:2] == '12':
          a = s[:-2]
          a = a.replace(" PM", "")
          a = str(a) + ":00"
          a = a.replace(" ", "")
      else:
          a = str(int(s[:2]) + 12) + s[2:8]
          a = a.replace(" PM", "")
          a = str(a) + ":00"
          a = a.replace(" ", "")
   return a


# ss = get_timeslots(23, "2022-08-10", "13:00:00", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NjAwMTYwMDMsImV4cCI6MTY2MDYyMDgwMywiaWF0IjoxNjYwMDE2MDAzfQ.iAWMXS8a3xa7o9qRSIz59LxbW_uPdtdRsEmMN3OPxEk")
# print(ss)
# time = ss.split(" - ")
# print(time)
# time1 = timeConversion(time[0])
# time2 = timeConversion(time[1])

# print(time1)
# print(time2)