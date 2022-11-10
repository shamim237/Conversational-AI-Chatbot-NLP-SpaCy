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

# ss = get_pharmacist_id("1", "48")
# print(ss)


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
    # wks.update_acell("I3", str(current_time))
    upcoming = []
    for i in starts:
        if i > current_time:
            ss = datetime.strptime(i, "%H:%M:%S") - datetime.strptime(current_time, "%H:%M:%S")
            ss = ss.total_seconds()
            if ss > 300:
                upcoming.append(i)
    ss = sorted(upcoming)
    # print(upcoming)

    if len(upcoming) > 0:
        for i in ssts:
            reg = re.sub(r"\d{1,3}\-\-", r"", i)
            if ss[0] == reg:
                idt = re.sub(r"(\d{1,3})\-\-\d{1,2}\:\d{1,2}\:\d{1,2}", r"\1", i)
        return ss[0], idt 
    else:
        return "None"
    

          
# ids = [8, 13, 23, 25, 32, 34, 35, 36, 39, 40, 48, 52, 55]
# ss = get_slots(ids, "2022-09-20", "10:53 am", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNiIsIm5hbWUiOiJTaGFtaW0iLCJuYmYiOjE2NjM2NDk1NTcsImV4cCI6MTY2NDI1NDM1NywiaWF0IjoxNjYzNjQ5NTU3fQ.MeQYK_XNlLhZrpUqOfPrUVhWafHDTrfsK8TuDBy2zFg")
# print(ss)   


def pharmacist_name(id):
    
    headers = {"Content-Type": "application/json; charset=utf-8"}


    res = requests.get('https://jarvin-dev.azurewebsites.net/api/v1/GetPharmacistsDetails/{}'.format(id), headers= headers)
    dictFromServer = res.json()
    ss = dictFromServer['response']['pharmacistDetails']['name']    
    return ss



def get_slots_sup(id, date, timen, time_now, token):

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

    today = datetime.now()
    today = datetime.strftime(today, "%Y-%m-%d")
    today = datetime.strptime(today, "%Y-%m-%d").date()
    
    datet = date
    datet = datetime.strptime(datet, "%Y-%m-%d").date()
    

    timex = time_now
    current_time = datetime.strptime(timex, "%I:%M %p")
    current_time = datetime.strftime(current_time, "%H:%M:%S")

    for i in starts:
        if datet > today:
            if i == timen:
                tim = i
                for j in ssts:
                    reg = re.sub(r"\d{1,3}\-\-", r"", j)
                    if tim == reg:
                        idt = re.sub(r"(\d{1,3})\-\-\d{1,2}\:\d{1,2}\:\d{1,2}", r"\1", j)
                return tim, idt
        if datet < today:
            pass
        if datet == today:
            if timen > current_time and i == timen:
                tim = i
                for j in ssts:
                    reg = re.sub(r"\d{1,3}\-\-", r"", j)
                    if tim == reg:
                        idt = re.sub(r"(\d{1,3})\-\-\d{1,2}\:\d{1,2}\:\d{1,2}", r"\1", j)
                return tim, idt
            else:
                return "time is past"
        else:
            pass 
        