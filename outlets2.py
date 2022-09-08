import requests
import regex as re
from datetime import datetime
import gspread


def get_pharmacist_id(pharmacyId, outletId):

    headers = {"Content-Type": "application/json; charset=utf-8"}

    dictToSend = {"pharmacyId": pharmacyId, "outletId": outletId}
    res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', headers= headers, json=dictToSend)
    dictFromServer = res.json()
    ss = dictFromServer['response']['pharmacists']
    ds = []
    for i in ss:
        ids = i['id']
        ds.append(ids)

    return ds


def get_slots(id, date, timey, token):

    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    
    ids         = []
    ssts        = []
    starts      = []
    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
    sh = ac.open("chatbot_logger")
    wks = sh.worksheet("Sheet1")
    for j in id:
        dictToSend = {"pharmacistId":j, "date": date}
        res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
        dictFromServer = res.json()
        
        if 'availabilitySlots' in dictFromServer['response']:
            for i in dictFromServer['response']['availabilitySlots']:
                if i['isChecked'] == True:
                    start = i['startTime']
                    sst = str(j) + "--" + str(start)
                    ids.append(j)
                    ssts.append(sst)
                    starts.append(start)



    now = timey
    current_time = datetime.strptime(now, "%I:%M %p")
    current_time = datetime.strftime(current_time, "%H:%M:%S")
    wks.update_acell("I3", str(current_time))
    
    upcoming = []
    for i in starts:
        if i > current_time:
            ss = datetime.strptime(i, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")
            ss = ss.total_seconds()
            if ss > 300:
                upcoming.append(i)
    ss = sorted(upcoming)

    for i in ssts:
        reg = re.sub(r"\d{1,3}\-\-", r"", i)
        if ss[0] == reg:
            idt = re.sub(r"(\d{1,3})\-\-\d{1,2}\:\d{1,2}\:\d{1,2}", r"\1", i)
    

    return ss[0], idt          


def pharmacist_name(id):
    
    headers = {"Content-Type": "application/json; charset=utf-8"}


    res = requests.get('https://jarvin-dev.azurewebsites.net/api/v1/GetPharmacistsDetails/{}'.format(id), headers= headers)
    dictFromServer = res.json()
    ss = dictFromServer['response']['pharmacistDetails']['name']    
    return ss



def get_slots_sup(id, date, timen, token):

    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
    
    ids         = []
    ssts        = []
    starts      = []

    for j in id:
        dictToSend = {"pharmacistId": j, "date": date}
        res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
        dictFromServer = res.json()
        
        if 'availabilitySlots' in dictFromServer['response']:
            for i in dictFromServer['response']['availabilitySlots']:
                if i['isChecked'] == True:
                    start = i['startTime']
                    sst = str(j) + "--" + str(start)
                    ids.append(j)
                    ssts.append(sst)
                    starts.append(start)
    print(starts)
    for i in starts:
        
        if i == timen:
            tim = i
            for j in ssts:
                reg = re.sub(r"\d{1,3}\-\-", r"", j)
                if tim == reg:
                    idt = re.sub(r"(\d{1,3})\-\-\d{1,2}\:\d{1,2}\:\d{1,2}", r"\1", j)
            return tim, idt
        else:
            pass 
        


ids = [1, 8, 13, 23, 25, 32, 34, 35, 36, 39, 40, 48, 52, 55]       
ss = get_slots_sup(ids, "2022-09-09", "21:00:00", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NjI1NzA5NzIsImV4cCI6MTY2MzE3NTc3MiwiaWF0IjoxNjYyNTcwOTcyfQ.KL8M4PZVlv0pVNkE0ROb_zipz7uC110kDU_CECgWJfs")
print(ss)