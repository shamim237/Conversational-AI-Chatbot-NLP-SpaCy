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


def get_slots(id, date, token):

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


    # now = time
    # current_time = re.sub(r"\d{1,4}\-\d{1,2}\-\d{1,2}\W+(\d{1,2}\:\d{1,2}\:\d{1,2})\+\d{1,2}\:\d{1,2}", r"\1", now) #localTimestamp:"2022-09-05T12:06:39+06:00"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    wks.update_acell("I3", str(current_time))
    
    upcoming = []
    for i in starts:
        if i > current_time:
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
