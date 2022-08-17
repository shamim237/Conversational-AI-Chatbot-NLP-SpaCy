# dd = {'attachmentId': '1303', 'attachmentUrl': 'https://jarvin-dev.azurewebsites.net/appimages/thumbs/0001303.jpeg'}

# id = list(dd.values())[1]

# print(id)










# from datetime import datetime
# format = "%H:%M:%S"
# ss = ['22:30:00','22:45:00', '23:00:00']
# print(type(ss))
# for i in ss:
#     if i > '22:45:00':
#         times = datetime.strptime(i, format) - datetime.strptime("22:45:00", format)
#         print(times)
#     else:
#         times = datetime.strptime("22:45:00", format) - datetime.strptime(i, format)
#         print(times)

# a=''
# def timeConversion(s):
#    if s[-2:] == "AM" :
#       if s[:2] == '12':
#           a = str('00' + s[2:8])
#           a = a.replace(" AM", "")
#           a = str(a) + ":00"
#       else:
#           a = s[:-2]
#           a = a.replace(" AM", "")
#           a = str(a) + ":00"
#    else:
#       if s[:2] == '12':
#           a = s[:-2]
#           a = a.replace(" PM", "")
#           a = str(a) + ":00"
#       else:
#           a = str(int(s[:2]) + 12) + s[2:8]
#           a = a.replace(" PM", "")
#           a = str(a) + ":00"
#    return a


# s = '09:05 PM'
# result = timeConversion(s)
# print(result)
# # now = datetime.datetime.now()
# # hour = now.hour

# # if hour < 12:
# #     greeting = "Good morning"
# # elif hour < 18:
# #     greeting = "Good afternoon"
# # else:
# #     greeting = "Good evening"

# # print("{}!".format(greeting))

# timeslots = datetime.strptime("22:30:00", "%H:%M:%S")
# print(timeslots.strftime("%I:%M %p"))
# import parsedatetime

# p = parsedatetime.Calendar()
# time_struct, parse_status = p.parse("3 pm")
# dates = datetime(*time_struct[:6]).strftime("%H:%M:%S")
# print(dates)

# import datetime


# def time_in_range(start, end, x):
#     """Return true if x is in the range [start, end]"""
#     if start <= end:
#         return start <= x <= end
#     else:
#         return start <= x or x <= end

# # st = datetime.datetime.strptime("22:30:00", "%H:%M:%S")
# # et = datetime.datetime.strptime("23:30:00", "%H:%M:%S")

# # print(st)
# start = datetime.time(22, 30, 0)
# end = datetime.time(11, 0, 0)
# ss= time_in_range(start, end, datetime.time(22,45,00))
# print(ss)

# from datetime import datetime
# import requests
# import re
# import json
# import random

# def check_outlet(email, pharmacyId, token):
#     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
#     dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', headers= headers, json=dictToSend)
#     dictFromServer = res.json()
#     outlet = dictFromServer['response']['patientData']['outletId']
#     return outlet

# def outlet_name(outlet_id, token):
#     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
#     res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetOutletDetails/{}'.format(outlet_id), headers= headers,)
#     dictFromServer = res.json()
#     outlet_name = dictFromServer['response']['outletDetails']['outletName']
#     return outlet_name


# def get_pharma_id(outlet_id, pharmacyId, token):
#     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
#     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists',  headers= headers, json=dictToSend)
#     dictFromServer = res.json()
#     pharmacist = dictFromServer['response']["pharmacists"]
#     pharma = []
#     for i in pharmacist:
#         pharma.append(i['id'])
#     ids = str(pharma).replace("[", "").replace("]", "").replace("'", "")
#     return ids



# def match(pharmas, outlet_id, pharmacyId):

#     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', json=dictToSend)
#     dictFromServer = res.json()
#     pharmacist = dictFromServer['response']['pharmacists']
#     pharma = []
#     ids = []
#     for i in pharmacist:
#         pharma.append(i['name'])
#         ids.append(i['id'])
#     pharma = str(pharma).replace("[", "").replace("]", "").replace("'", "")
#     ids = str(ids).replace("[", "").replace("]", "").replace("'", "")

#     pharma = pharma.lower()
#     pharma = pharma.split(", ")
#     ids = ids.split(", ")
#     ss = []
#     for i in range(len(pharma)):
#         list = {pharma[i]:ids[i]}
#         ss.append(list)
#     #print(ss)
#     all = str(ss).replace("[", "").replace("]", "").replace("'",'"')
#     all = re.sub(r"\"(\d{1,6})\"", r"\1", all)
#     all = re.sub(r"(\d{1,6})\}(\,)", r"\1\2", all)
#     all = re.sub(r"(\d{1,6}\,\s)\{", r"\1", all)
#     #print(type(all))
#     all = re.sub(r"\,\s\d\:\s\d{1,9}", r"", all)
#     #all = re.sub(r"('\w+\s\w+)\s('\:)", r"\1\2", all)
#     all = all.replace("dr mohaimin ", "dr mohaimin")
#     all = json.loads(all)

#     # print(all)
#     if str(pharmas) in all:
#         ss = all[pharmas]
#         #print(ss)
#         return ss
#     else:
#         ss = "The name you entered is not in the list of pharmacist. Please check the spelling and try again."
#         return ss


# def autos(outlet_id, pharmacyId, token):
#     # headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + "token".format(token)}
#     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', json=dictToSend)
#     dictFromServer = res.json()
#     pharmacist = dictFromServer['response']["pharmacists"][0]['name']
#     pharmacist = pharmacist.lower()
#     return pharmacist


# def get_timeslots(id, date, time, token):

#     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

#     dictToSend = {"pharmacistId": id, "date": date}
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
#     dictFromServer = res.json()

#     if 'availabilitySlots' in dictFromServer['response']:
    
#         timeslots = dictFromServer['response']['availabilitySlots']
#         timeslots = str(timeslots).replace("[", "").replace("]", "").replace("'", "").replace(", {", "\n").replace("}", "").replace("{", "")
#         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False\n", r"", timeslots)
#         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False", r"", timeslots)
#         timeslots = timeslots.replace(", isChecked: True", "")
#         timeslots = timeslots.replace("startTime: ", "").replace(", endTime: ", " - ")
#         timesk = timeslots.split("\n")
#         stime = re.sub("(\d{2}\:\d{2}\:\d{2})\s\-\s\d{2}\:\d{2}\:\d{2}", r"\1", timeslots)
#         stime = stime.split("\n")
#         timess = []
#         for i in stime:
#             #print(i)
#             format = '%H:%M:%S'
#             if i > time:
#                 times = datetime.strptime(i, format) - datetime.strptime(time, format)
#                 timess.append(times)
#             else:
#                 times = datetime.strptime(time, format) - datetime.strptime(i, format)
#                 timess.append(times)
        
#         timess = str(timess).replace("[", "").replace("]", "").replace("datetime.timedelta(seconds=", "").replace(")", "").replace("(", "").replace(", ", ",")

#         timess = timess.split(",")
#         timess = [int(i) for i in timess]

#         count = 0
#         for i in timess:
#             count += 1 
#             ss = min(timess)
#             if ss > 10800:
#                 return "NOPE"
#             if ss == i:
#                 break
#         cou = 0
#         for i in timesk:
#             cou += 1
#             if cou == count:
#                 return i

#     else:
#         return "No slots available" 
        

# def get_timeslots2(id, date, token):

#     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
#     dictToSend = {"pharmacistId": id, "date": date}
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
#     dictFromServer = res.json()

#     if 'availabilitySlots' in dictFromServer['response']:
    
#         timeslots = dictFromServer['response']['availabilitySlots']

#         timeslots = str(timeslots).replace("[", "").replace("]", "").replace("'", "").replace(", {", "\n").replace("}", "").replace("{", "")
#         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False\n", r"", timeslots)
#         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False", r"", timeslots)
#         timeslots = timeslots.replace(", isChecked: True", "")
#         timeslots = timeslots.replace("startTime: ", "").replace(", endTime: ", " - ")
#         timeslots = timeslots.split("\n")
#         timeslots = random.sample(timeslots, 4)
#         timeslots = sorted(timeslots)
#         timeslots = "\n".join(timeslots)
#         timeslots = re.findall(r"\d{2}\:\d{2}\:\d{2}", timeslots)
#         timest = []
#         for i in timeslots:
#             #print(i)
#             timeslots = datetime.strptime(i, "%H:%M:%S").strftime("%I:%M %p")
#             timest.append(timeslots)

#         timest = timest[0] + " - " + timest[1] + "\n" + timest[2] + " - " + timest[3] + "\n" + timest[4] + " - " + timest[5] + "\n" + timest[6] + " - " + timest[7]
#         timest = timest.split("\n")

#         return timest

#     else:
        
#         return "No slots available" 


# def get_avail_slot(outletid, pharmacyId, token):
#     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
#     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outletid}
#     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', headers=headers, json=dictToSend)
#     dictFromServer = res.json()
#     pharmacist = dictFromServer['response']["pharmacists"]
#     pharma = []
#     for i in pharmacist:
#         if i['availability'] == []:
#             pass
#         else:
#             pharma.append(i['name'])  
#     return pharma        


# def is_between(time, time_range):
#     if time_range[1] < time_range[0]:
#         return time >= time_range[0] or time <= time_range[1]
#     return time_range[0] <= time <= time_range[1]

# print(is_between(":00", ("09:00", "16:00")))  # True
# print(is_between("17:00", ("09:00", "16:00")))  # False
# print(is_between("01:15", ("21:30", "04:30")))  # True


        # for i in dictFromServer['response']['availabilitySlots']:
        #     if i['isChecked'] == True:
        #         start = i['startTime']

        #         ss.append(start)
        #         end = i['endTime']
        # return ss

# import parsedatetime
# import datetime
# import gspread
# from datetime import date, timedelta
# import json
# import recognizers_suite as Recognizers
# from recognizers_suite import Culture, ModelResult
# from word2number import w2n
# culture = Culture.English

# # ss = Recognizers.recognize_datetime("2022-07-24, 2022-12-25, 2022-12-05", culture) 
# # timess = []     
# # for i in ss:
# #     ss = i.resolution
# #     dd = ss['values']
# #     for j in dd:
# #         tim = j['value']  
# #         timess.append(tim) 
# # print(timess)


# ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
# sh = ac.open("logs_checker")
# wks = sh.worksheet("Sheet1")
# wks.update_acell("A1", "ss")
# wks.update_acell("B1", "dd")
# import pandas as pd


# sheet_id = "1n2ol4JaDokXMctufEIxrmRLNZbhriKKSihwKYlO7h6s"

# df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# print(df['sentence'][0])


# final_days = []
# recur_dates = ["2022-07-25", "2022-07-27"]
# dates_initials = ["2022-07-25", "2022-07-26", "2022-07-27", "2022-07-28", "2022-07-29", "2022-07-30", "2022-07-31", "2022-08-01", "2022-08-02", "2022-08-03", "2022-08-04", "2022-08-05", "2022-08-06", "2022-08-07", "2022-08-08", "2022-08-09", "2022-08-10", "2022-08-11", "2022-08-12", "2022-08-13", "2022-08-14", "2022-08-15", "2022-08-16", "2022-08-17", "2022-08-18", "2022-08-19", "2022-08-20", "2022-08-21"]
# dates_finals = ["2022-07-27", "2022-07-28", "2022-07-29", "2022-07-30", "2022-07-31", "2022-08-01", "2022-08-02", "2022-08-03", "2022-08-04", "2022-08-05", "2022-08-06", "2022-08-07", "2022-08-08", "2022-08-09", "2022-08-10", "2022-08-11", "2022-08-12", "2022-08-13", "2022-08-14", "2022-08-15", "2022-08-16", "2022-08-17", "2022-08-18", "2022-08-19", "2022-08-20", "2022-08-21"]
# for i in recur_dates:
#     recur_dates1 = i
#     print(recur_dates1)
#     recur_dates1 = recur_dates1.split("-")
#     date_list = []
#     for x in range(0, 28):
#         dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
#         date_list.append(dates.strftime("%Y-%m-%d"))
#     for i in date_list:
#         if i in dates_initials or i in dates_finals:
#             final_days.append(i)
#         else:
#             pass


# print(final_days)

# list  = ["10:00:00", "16:00:00"]

# str = ' '.join(map(str, list))
# str = str.replace(" ", ",")
# print(str)


# # print(
# #     'Returns:\n',
# #     json.dumps(
# #         ss,
# #         default=lambda o: o.__dict__,
# #         indent='\t',
# #         ensure_ascii=False)
# # )
# # try:
# #     print(w2n.word_to_num('1'))
# # except:
# #     print('Not a number')

# times = []     
# for i in ss:
#     ss = i.resolution
#     dd = ss['values']
#     for j in dd:
#         tim = j['value']  
#         times.append(tim) 

# print(times)
# times = "one times"
# dosage_time = times.replace("times", "").replace("time", "").replace("for", "").replace("only", "")
# dosage_time = w2n.word_to_num("one times")
# print(dosage_time)

# import datetime 
# #base = datetime.datetime.today()
# date_list = []
# for x in range(0, 14):
#     dates = date(2022,7,26) + datetime.timedelta(days=7*x)
#     date_list.append(dates.strftime("%Y-%m-%d"))

# print(date_list)

# lists = ["2", "4", "6"]
# print(lists[-1])
# #         if var == "med_name":
#             med_name= step_context.result
#             med_type = predict_class(med_name)

#             if med_type == "tablet":
#                 if dosage_time == 1 and option == "Recurring":
                    
#                     patientid = userId
#                     pharmacyid = 1
#                     tokens = token
#                     pillName = med_name
#                     pillType = "0"
#                     dosage = "1"
#                     isRecurring = "true"
#                     pill_time = times

#                     dates_initial = cal_date(recur_dates[0], long_date)
#                     dates_final = cal_date(recur_dates[-1], long_date)

#                     dates_initials = []
#                     dates_finals = []

#                     if long_date == "1 Month":
#                         count = 0
#                         for i in range(len(dates_initial)):
#                             count += 1
#                             dates_initials.append(dates_initial[i])
#                             if count == 28:
#                                 break

#                     if long_date == "2 Months":
#                         count = 0
#                         for i in range(len(dates_initial)):
#                             count += 1
#                             dates_initials.append(dates_initial[i])
#                             if count == 56:
#                                 break

#                     if long_date == "3 Months":
#                         count = 0
#                         for i in range(len(dates_initial)):
#                             count += 1
#                             dates_initials.append(dates_initial[i])
#                             if count == 84:
#                                 break
# ##########################################################
#                     if long_date == "1 Month":
#                         count = 0
#                         for i in range(len(dates_final)):
#                             count += 1
#                             dates_finals.append(dates_final[i])
#                             if count == 28:
#                                 break

#                     if long_date == "2 Months":
#                         count = 0
#                         for i in range(len(dates_final)):
#                             count += 1
#                             dates_finals.append(dates_final[i])
#                             if count == 56:
#                                 break

#                     if long_date == "3 Months":
#                         count = 0
#                         for i in range(len(dates_final)):
#                             count += 1
#                             dates_finals.append(dates_final[i])
#                             if count == 84:
#                                 break


#                     final_days = []

#                     if long_date == "Two Weeks":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 14):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass

#                     if long_date == "Three Weeks":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 21):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass                        

#                     if long_date == "1 Month":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 28):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass
#                     if long_date == "2 Months":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 56):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass   

#                     if long_date == "3 Months":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 84):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass 

#                     if long_date == "Two Weeks":
#                         recurringValue = "2"
#                         test_dict(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     if long_date == "Three Weeks":
#                         recurringValue = "3"
#                         set_reminder_tablet_three_weeks(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     if long_date == "1 Month":
#                         recurringValue = "4"
#                         test_dict(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     if long_date == "2 Months":
#                         recurringValue = "8"
#                         set_reminder_tablet_two_months(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     if long_date == "3 Months":
#                         recurringValue = "12"
#                         set_reminder_tablet_three_months(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)

#                     await step_context.context.send_activity(
#                         MessageFactory.text(f"Your pill reminder has been set."))
#                     return await step_context.prompt(
#                         TextPrompt.__name__,
#                         PromptOptions(prompt=MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + ".")),)

# ##########################################################################################################################################################################################################

#                 if dosage_time >= 2 and option == "Recurring":
                    
#                     patientid = userId
#                     pharmacyid = 1
#                     tokens = token
#                     pillName = med_name
#                     pillType = "0"
#                     dosage = dosage_time
#                     isRecurring = "true"
#                     pill_time = times

#                     dates_initial = cal_date(recur_dates[0], long_date)
#                     dates_final = cal_date(recur_dates[-1], long_date)

#                     dates_initials = []
#                     dates_finals = []

#                     if long_date == "1 Month":
#                         count = 0
#                         for i in range(len(dates_initial)):
#                             count += 1
#                             dates_initials.append(dates_initial[i])
#                             if count == 28:
#                                 break

#                     if long_date == "2 Months":
#                         count = 0
#                         for i in range(len(dates_initial)):
#                             count += 1
#                             dates_initials.append(dates_initial[i])
#                             if count == 56:
#                                 break

#                     if long_date == "3 Months":
#                         count = 0
#                         for i in range(len(dates_initial)):
#                             count += 1
#                             dates_initials.append(dates_initial[i])
#                             if count == 84:
#                                 break
# ##########################################################
#                     if long_date == "1 Month":
#                         count = 0
#                         for i in range(len(dates_final)):
#                             count += 1
#                             dates_finals.append(dates_final[i])
#                             if count == 28:
#                                 break

#                     if long_date == "2 Months":
#                         count = 0
#                         for i in range(len(dates_final)):
#                             count += 1
#                             dates_finals.append(dates_final[i])
#                             if count == 56:
#                                 break

#                     if long_date == "3 Months":
#                         count = 0
#                         for i in range(len(dates_final)):
#                             count += 1
#                             dates_finals.append(dates_final[i])
#                             if count == 84:
#                                 break


#                     final_days = []

#                     if long_date == "Two Weeks":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 14):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass

#                     if long_date == "Three Weeks":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 21):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass                        

#                     if long_date == "1 Month":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 28):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass
#                     if long_date == "2 Months":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 56):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass   

#                     if long_date == "3 Months":
#                         for i in recur_dates:
#                             recur_dates1 = recur_dates[i]
#                             recur_dates1 = recur_dates1.split("-")
#                             date_list = []
#                             for x in range(0, 84):
#                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
#                                 date_list.append(dates.strftime("%Y-%m-%d"))
#                             for i in date_list:
#                                 if i in dates_initials or i in dates_finals:
#                                     final_days.append(i)
#                                 else:
#                                     pass 

#                     # if long_date == "Two Weeks":
#                     #     recurringValue = "2"
#                     #     set_reminder_tablet_two_weeks_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     # if long_date == "Three Weeks":
#                     #     recurringValue = "3"
#                     #     set_reminder_tablet_three_weeks_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     # if long_date == "1 Month":
#                     #     recurringValue = "4"
#                     #     set_reminder_tablet_one_months_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     # if long_date == "2 Months":
#                     #     recurringValue = "8"
#                     #     set_reminder_tablet_two_months_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
#                     # if long_date == "3 Months":
#                     #     recurringValue = "12"
#                     #     set_reminder_tablet_three_months_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)

#                     await step_context.context.send_activity(
#                         MessageFactory.text(f"Your pill reminder has been set."))
#                     return await step_context.prompt(
#                         TextPrompt.__name__,
#                         PromptOptions(prompt=MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + ".")),)



#             if med_type == "capsule":
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Your pill reminder has been set."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(prompt=MessageFactory.text("I will remind you to take one [medicine name] at [8 pm] [daily / weekly / every Thursday]")),)
            
#             if med_type == "syrup":
#                 dose = "syrup dose koto"
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(prompt=MessageFactory.text("What's the recommended dosage in ml?")),)
                
#             if med_type == "syringe":
#                 dose = "syringe dose koto"
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(prompt=MessageFactory.text("What's the recommended dosage in ml?")),)
            
#             if med_type == "drop":
#                 dose = "drop dose koto"
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(prompt=MessageFactory.text("How many drops are recommended by the doctor?")),)

#             else: 
#                 type = "type of medicine"
#                 reply = MessageFactory.text("What type of medicine is it?")
#                 reply.suggested_actions = SuggestedActions(
#                     actions=[
#                         CardAction(
#                             title= "Tablet",
#                             type=ActionTypes.im_back,
#                             value= "Tablet"),
#                         CardAction(
#                             title= "Drop",
#                             type=ActionTypes.im_back,
#                             value= "Drop",
#                             ),
#                         CardAction(
#                             title= "Capsule",
#                             type=ActionTypes.im_back,
#                             value= "Capsule"),
#                         CardAction(
#                             title= "Syringe",
#                             type=ActionTypes.im_back,
#                             value= "Syringe"),
#                         CardAction(
#                             title= "Syrup",
#                             type=ActionTypes.im_back,
#                             value= "Syrup"),])
#                 return await step_context.context.send_activity(reply)

# import parsedatetime
# import datetime
# from datetime import date, timedelta

# def cal_date(date_str):

#     p = parsedatetime.Calendar()
#     time_struct, parse_status = p.parse(date_str)
#     dates = datetime.datetime(*time_struct[:6]).strftime("%Y-%m-%d")
#     dates = dates.split("-")

#     dat= date.today()
#     dat = date.strftime(dat, "%Y-%m-%d")
#     dat = dat.split("-")

#     dates1 = date(int(dat[0]), int(dat[1]), int(dat[2]))

#     dd = date(int(dates[0]), int(dates[1]), int(dates[2])) - date(int(dat[0]), int(dat[1]), int(dat[2]))
#     datee = []

#     for i in range(dd.days):
#         day = dates1 + timedelta(days=i)
#         datee.append(day)


#     listToStr = ' '.join(map(str, datee))

#     listt = listToStr.replace(" ", "\n")

#     list1 = listt.split("\n")

#     return list1


# ss = cal_date("eleven days")
# print(ss)

# import pandas as pd
# sheet_id = "1n2ol4JaDokXMctufEIxrmRLNZbhriKKSihwKYlO7h6s"
# df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
# main = df['sentence'][0]

# print(main)
# from word2number import w2n

# dosage = w2n.word_to_num("two")
# print(dosage)

