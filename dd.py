# 
# ss =  {'attachmentUrl': 'https://jarvin-dev.azurewebsites.net/appimages/thumbs/0001488.pdf', 'local_timestamp': '11:31 am'}

# # for i in ss.keys():
# #     if 
# if "attachmentUrl" and "attachmentId" in ss:
#     print("ache")

# from google_trans_new import google_translator  

# detector = google_translator() 
# # ss = "hey bro"
# raw = detector.detect('')

# print(raw)

# ss = 36.5
# print(type(ss))


# # dd = {'attachmentId': '1303', 'attachmentUrl': 'https://jarvin-dev.azurewebsites.net/appimages/thumbs/0001303.jpeg'}

# # id = list(dd.values())[1]

# # print(id)

# # ss = 123
# print("It's the patient name. You can find it on the\033 diagnostic reports.\033 for")
# # dd = str(ss)
# # print(dd)
# patient_name = ["my"]
# my = ["my", "My", "MY", "I", "me", "myself"]
# if patient_name[0] in my:
#     print("ache")
# else:

# duration = 'for 7 days'
# duration = duration.lower()
# duration = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
# print(duration)
#     print
# ("nai")
# print("Tap '\U0001F4CE' to upload")
# from datetime import datetime
# timey = "07:12 pm"
# now = timey
# current_time = datetime.strptime(now, "%I:%M %p")
# current_time = datetime.strftime(current_time, "%H:%M:%S")
# print(current_time)
# ss = ["Fss", "dddd"]
# import geocoder
# g = geocoder.ip('me')
# print(g.country)
# print(ss[0].lower())
# # # import logging
# from datetime import datetime
# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# culture = Culture.English

# def date_cal(date):

#     today = datetime.now()
#     today = datetime.strftime(today, "%Y-%m-%d")   
#     today = datetime.strptime(today, "%Y-%m-%d").date()

#     raw = Recognizers.recognize_datetime(date, culture) 
#     times = []     
#     for i in raw:
#         raw = i.resolution
#         dd = raw['values']
#         for j in dd:
#             tim = j['value']  
#             times.append(tim) 
#     for i in times:
#         datey = datetime.strptime(i, "%Y-%m-%d").date()
#         if datey >= today:
#             return i
#         else:
#             pass

# ss =  date_cal("23 september")
# print(ss)

# # from datetime import datetime, timedelta
# filtered_days = ['2022-09-15']

# dat = filtered_days[0]
# dat = datetime.strptime(dat, "%Y-%m-%d")
# dat = datetime.strftime(dat, "%Y-%m-%d")
# dat = dat.split("-")
# ss= ["0", "4"]
# print(len(ss))
# print(dat)
# # logging.basicConfig(filename='output.txt', level=logging.DEBUG, format='')
# quants = ['4 ml']

# ss = "".join(quants)

# print(ss)
# # def we_prints(data):
# #     logging.info(data)
# # #     print(data)

# # we_prints("some data we are logging")
# from datetime import datetime

# today = datetime.now()
# today = datetime.strftime(today, "%Y-%m-%d")

# datet = "2022-09-06"

# datet = datetime.strptime(datet, "%Y-%m-%d").date()
# today = datetime.strptime(today, "%Y-%m-%d").date()
# if datet> today:
#     print("future date")
# else:
#     print("past date")

# # from datetime import datetime
# # format = "%H:%M:%S"
# # ss = ['22:30:00','22:45:00', '23:00:00']
# # print(type(ss))
# # for i in ss:
# #     if i > '22:45:00':
# #         times = datetime.strptime(i, format) - datetime.strptime("22:45:00", format)
# #         print(times)
# #     else:
# #         times = datetime.strptime("22:45:00", format) - datetime.strptime(i, format)
# #         print(times)

# # a=''
# # def timeConversion(s):
# #    if s[-2:] == "AM" :
# #       if s[:2] == '12':
# #           a = str('00' + s[2:8])
# #           a = a.replace(" AM", "")
# #           a = str(a) + ":00"
# #       else:
# #           a = s[:-2]
# #           a = a.replace(" AM", "")
# #           a = str(a) + ":00"
# #    else:
# #       if s[:2] == '12':
# #           a = s[:-2]
# #           a = a.replace(" PM", "")
# #           a = str(a) + ":00"
# #       else:
# #           a = str(int(s[:2]) + 12) + s[2:8]
# #           a = a.replace(" PM", "")
# #           a = str(a) + ":00"
# #    return a

# from word2number import w2n

# dosage = "ten ml"
# dosage = str(dosage)
# dosage = dosage.lower()
# dosage = dosage.replace("ml", "").replace("mg", "")
# print(int(dosage))
# if dosage.isdigit():
#     print("integer")
# else:
#     print("string")
# try:
#     dosage_ml = w2n.word_to_num("ten ml")
# except:
#     dosage_ml = 1

# print(dosage_ml)
# # s = '09:05 PM'
# # result = timeConversion(s)
# # print(result)
# # # now = datetime.datetime.now()
# # # hour = now.hour

# # # if hour < 12:
# # #     greeting = "Good morning"
# # # elif hour < 18:
# # #     greeting = "Good afternoon"
# # # else:
# # #     greeting = "Good evening"

# # # print("{}!".format(greeting))
# from recognizers_number import recognize_number, Culture

# result = recognize_number("temperatures is  98.9", Culture.English)

# res = []
# for i in result:
#     raw = i.resolution
#     dd = raw['value']
#     res.append(dd) 

# print(res)

# if 36.1 <= float(res[0]) <= 37.2 or 97 <= float(res[0]) <= 99.9:
#     print("normal")

# if 37.3 <= float(res[0]) <= 38.9 or 100.0 <= float(res[0]) <= 100.4:
#     print("abnormal")

# else:
#     print("nothing")

# # timeslots = datetime.strptime("22:30:00", "%H:%M:%S")
# # print(timeslots.strftime("%I:%M %p"))
# import parsedatetime
# import dateparser
# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# import warnings
# from datetime import datetime
# warnings.filterwarnings(
#     "ignore",
#     message="The localize method is no longer necessary, as this time zone supports the fold attribute",
# )
# culture = Culture.English

# # p = parsedatetime.Calendar()
# # time_struct, parse_status = p.parse("8 am and 9 pm")
# # dates = datetime(*time_struct[:6]).strftime("%H:%M:%S")
# # print(time_struct)

# # datess = dateparser.parse("today from 7 days")
# # #datess = datetime.strftime(datess, '%Y-%m-%d')
# # print(datess)

# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# from datetime import datetime
# extract = Recognizers.recognize_datetime("8 am", culture= Culture.English) 
# times = []  
# tk = []   
# for i in extract:
#     keys = i.resolution
#     values = keys['values']
#     for j in values:
#         timea = j['value']  
#         times.append(timea) 

# for i in times:
#     dp = datetime.strptime(i, "%H:%M:%S")
#     dt = datetime.strftime(dp, "%I:%M %p")
#     tk.append(dt)
# print(tk)

# from recognizers_number import recognize_number, Culture

# result = recognize_number("4 ml", Culture.English)
# nums = []
# for i in result:
#     k = i.resolution
#     num = k['value']
#     nums.append(num)

# print(nums)
# ss = "a"
# if "a" != ss:
#     print("nai")
# else:
#     print("ache")
# # time = time.split(" ")
# pm = ["AM", "PM", "A.M", "P.M", "am", "pm", "a.m", "p.m"]

# if "AM" in time or "PM" in time or "A.M" in time or "P.M" in time or "am" in time or "pm" in time or "a.m" in time or "p.m" in time:
#     print(time)
# else:
#     print("time nai")
# usertext = "4 in the afternoon"

# extract = Recognizers.recognize_datetime(time, culture) 
# times = []     
# for i in extract:
#     keys = i.resolution
#     values = keys['values']
#     print(keys)
#     for j in values:
#         timea = j['value']  
#         times.append(timea) 

# times = ",".join(times)
# print(times)
# times=[]
# # time = "9:30"
# # u_times = ["afternoon"]
# # tt = str(time) + " in the " + str(u_times[0])
# tt = "12.30 a.m"
# time = re.sub(r"(\d{1,10})\.(\d+)", r"\1:\2", tt)
# print(time)
# raw = Recognizers.recognize_datetime(tt, culture)
# for i in raw:
#     raw = i.resolution
#     dd = raw['values']
#     for j in dd:
#         tim = j['value']  
#         times.append(tim) 
# from word2number import w2n
# print(w2n.word_to_num("one"))
# print(times)
# recognizer = DateTimeRecognizer(Culture.English)
# model = recognizer.get_datetime_model()
# mode_result = model.parse(times)

# print(mode_result)
# import requests

# class DirectLineAPI(object):
#     """Shared methods for the parsed result objects."""

#     def __init__(self, direct_line_secret):
#         self._direct_line_secret = direct_line_secret
#         self._base_url = 'https://directline.botframework.com/v3/directline'
#         self._set_headers()
#         self._start_conversation()

#     def _set_headers(self):
#         headers = {'Content-Type': 'application/json'}
#         value = ' '.join(['Bearer', self._direct_line_secret])
#         headers.update({'Authorization': value})
#         self._headers = headers

#     def _start_conversation(self):
#         # For Generating a token use
#         url = '/'.join([self._base_url, 'tokens/generate'])
#         botresponse = requests.post(url, headers=self._headers)
#         jsonresponse = botresponse.json()
#         self._token = jsonresponse['token']

#         # Start conversation and get us a conversationId to use
#         url = '/'.join([self._base_url, 'conversations'])
#         botresponse = requests.post(url, headers=self._headers)

#         # Extract the conversationID for sending messages to bot
#         jsonresponse = botresponse.json()
#         self._conversationid = jsonresponse['conversationId']

#     def send_message(self, text):
#         """Send raw text to bot framework using directline api"""
#         url = '/'.join([self._base_url, 'conversations', self._conversationid, 'activities'])
#         jsonpayload = {
#             'conversationId': self._conversationid,
#             'type': 'message',
#             'from': {'id': 'user1'},
#             'text': text
#         }
#         botresponse = requests.post(url, headers=self._headers, json=jsonpayload)
#         if botresponse.status_code == 200:
#             return "message sent"
#         return "error contacting bot"

#     def get_message(self):
#         """Get a response message back from the botframework using directline api"""
#         url = '/'.join([self._base_url, 'conversations', self._conversationid, 'activities'])
#         botresponse = requests.get(url, headers=self._headers,
#                                    json={'conversationId': self._conversationid})
#         if botresponse.status_code == 200:
#             jsonresponse = botresponse.json()
#             return jsonresponse['activities'][1]['text']
#         return "error contacting bot for response"



# bot = DirectLineAPI('KD5AAPQeTrI.c_5h0YHGQn-RZWPfr8k9WxSNMGi7JyNPrjCfZR789-I')
# bot.send_message("Hi")
# botresponse = bot.get_message()
# print(botresponse)










# ss = Recognizers.recognize_datetime("8am and 9pm", culture) 
# timess = []     
# for i in ss:
#         ss = i.resolution
#         dd = ss['values']
#         for j in dd:
#                 tim = j['value']  
#                 timess.append(tim) 

# print(timess)
# # import datetime


# # def time_in_range(start, end, x):
# #     """Return true if x is in the range [start, end]"""
# #     if start <= end:
# #         return start <= x <= end
# #     else:
# #         return start <= x or x <= end

# # # st = datetime.datetime.strptime("22:30:00", "%H:%M:%S")
# # # et = datetime.datetime.strptime("23:30:00", "%H:%M:%S")

# # # print(st)
# # start = datetime.time(22, 30, 0)
# # end = datetime.time(11, 0, 0)
# # ss= time_in_range(start, end, datetime.time(22,45,00))
# # print(ss)

# # from datetime import datetime
# # import requests
# # import re
# # import json
# # import random

# # def check_outlet(email, pharmacyId, token):
# #     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
# #     dictToSend = {"email": email, "pharmacyId": pharmacyId, "loginType": "Google"}
# #     res = requests.post('https://jarvin-dev.azurewebsites.net/api/PatientLogin', headers= headers, json=dictToSend)
# #     dictFromServer = res.json()
# #     outlet = dictFromServer['response']['patientData']['outletId']
# #     return outlet

# # def outlet_name(outlet_id, token):
# #     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
# #     res = requests.get('https://jarvin-dev.azurewebsites.net/api/GetOutletDetails/{}'.format(outlet_id), headers= headers,)
# #     dictFromServer = res.json()
# #     outlet_name = dictFromServer['response']['outletDetails']['outletName']
# #     return outlet_name


# # def get_pharma_id(outlet_id, pharmacyId, token):
# #     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
# #     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
# #     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists',  headers= headers, json=dictToSend)
# #     dictFromServer = res.json()
# #     pharmacist = dictFromServer['response']["pharmacists"]
# #     pharma = []
# #     for i in pharmacist:
# #         pharma.append(i['id'])
# #     ids = str(pharma).replace("[", "").replace("]", "").replace("'", "")
# #     return ids



# # def match(pharmas, outlet_id, pharmacyId):

# #     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
# #     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', json=dictToSend)
# #     dictFromServer = res.json()
# #     pharmacist = dictFromServer['response']['pharmacists']
# #     pharma = []
# #     ids = []
# #     for i in pharmacist:
# #         pharma.append(i['name'])
# #         ids.append(i['id'])
# #     pharma = str(pharma).replace("[", "").replace("]", "").replace("'", "")
# #     ids = str(ids).replace("[", "").replace("]", "").replace("'", "")

# #     pharma = pharma.lower()
# #     pharma = pharma.split(", ")
# #     ids = ids.split(", ")
# #     ss = []
# #     for i in range(len(pharma)):
# #         list = {pharma[i]:ids[i]}
# #         ss.append(list)
# #     #print(ss)
# #     all = str(ss).replace("[", "").replace("]", "").replace("'",'"')
# #     all = re.sub(r"\"(\d{1,6})\"", r"\1", all)
# #     all = re.sub(r"(\d{1,6})\}(\,)", r"\1\2", all)
# #     all = re.sub(r"(\d{1,6}\,\s)\{", r"\1", all)
# #     #print(type(all))
# #     all = re.sub(r"\,\s\d\:\s\d{1,9}", r"", all)
# #     #all = re.sub(r"('\w+\s\w+)\s('\:)", r"\1\2", all)
# #     all = all.replace("dr mohaimin ", "dr mohaimin")
# #     all = json.loads(all)

# #     # print(all)
# #     if str(pharmas) in all:
# #         ss = all[pharmas]
# #         #print(ss)
# #         return ss
# #     else:
# #         ss = "The name you entered is not in the list of pharmacist. Please check the spelling and try again."
# #         return ss


# # def autos(outlet_id, pharmacyId, token):
# #     # headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + "token".format(token)}
# #     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outlet_id}
# #     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', json=dictToSend)
# #     dictFromServer = res.json()
# #     pharmacist = dictFromServer['response']["pharmacists"][0]['name']
# #     pharmacist = pharmacist.lower()
# #     return pharmacist


# # def get_timeslots(id, date, time, token):

# #     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}

# #     dictToSend = {"pharmacistId": id, "date": date}
# #     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
# #     dictFromServer = res.json()

# #     if 'availabilitySlots' in dictFromServer['response']:
    
# #         timeslots = dictFromServer['response']['availabilitySlots']
# #         timeslots = str(timeslots).replace("[", "").replace("]", "").replace("'", "").replace(", {", "\n").replace("}", "").replace("{", "")
# #         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False\n", r"", timeslots)
# #         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False", r"", timeslots)
# #         timeslots = timeslots.replace(", isChecked: True", "")
# #         timeslots = timeslots.replace("startTime: ", "").replace(", endTime: ", " - ")
# #         timesk = timeslots.split("\n")
# #         stime = re.sub("(\d{2}\:\d{2}\:\d{2})\s\-\s\d{2}\:\d{2}\:\d{2}", r"\1", timeslots)
# #         stime = stime.split("\n")
# #         timess = []
# #         for i in stime:
# #             #print(i)
# #             format = '%H:%M:%S'
# #             if i > time:
# #                 times = datetime.strptime(i, format) - datetime.strptime(time, format)
# #                 timess.append(times)
# #             else:
# #                 times = datetime.strptime(time, format) - datetime.strptime(i, format)
# #                 timess.append(times)
        
# #         timess = str(timess).replace("[", "").replace("]", "").replace("datetime.timedelta(seconds=", "").replace(")", "").replace("(", "").replace(", ", ",")

# #         timess = timess.split(",")
# #         timess = [int(i) for i in timess]

# #         count = 0
# #         for i in timess:
# #             count += 1 
# #             ss = min(timess)
# #             if ss > 10800:
# #                 return "NOPE"
# #             if ss == i:
# #                 break
# #         cou = 0
# #         for i in timesk:
# #             cou += 1
# #             if cou == count:
# #                 return i

# #     else:
# #         return "No slots available" 
        

# # def get_timeslots2(id, date, token):

# #     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
# #     dictToSend = {"pharmacistId": id, "date": date}
# #     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacistAvailabilityByDate', headers= headers, json=dictToSend)
# #     dictFromServer = res.json()

# #     if 'availabilitySlots' in dictFromServer['response']:
    
# #         timeslots = dictFromServer['response']['availabilitySlots']

# #         timeslots = str(timeslots).replace("[", "").replace("]", "").replace("'", "").replace(", {", "\n").replace("}", "").replace("{", "")
# #         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False\n", r"", timeslots)
# #         timeslots = re.sub(r"startTime:\s\d{2}\:\d{2}\:\d{2}\,\sendTime\:\s\d{2}\:\d{2}\:\d{2}\,\sisChecked: False", r"", timeslots)
# #         timeslots = timeslots.replace(", isChecked: True", "")
# #         timeslots = timeslots.replace("startTime: ", "").replace(", endTime: ", " - ")
# #         timeslots = timeslots.split("\n")
# #         timeslots = random.sample(timeslots, 4)
# #         timeslots = sorted(timeslots)
# #         timeslots = "\n".join(timeslots)
# #         timeslots = re.findall(r"\d{2}\:\d{2}\:\d{2}", timeslots)
# #         timest = []
# #         for i in timeslots:
# #             #print(i)
# #             timeslots = datetime.strptime(i, "%H:%M:%S").strftime("%I:%M %p")
# #             timest.append(timeslots)

# #         timest = timest[0] + " - " + timest[1] + "\n" + timest[2] + " - " + timest[3] + "\n" + timest[4] + " - " + timest[5] + "\n" + timest[6] + " - " + timest[7]
# #         timest = timest.split("\n")

# #         return timest

# #     else:
        
# #         return "No slots available" 


# # def get_avail_slot(outletid, pharmacyId, token):
# #     headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + str(token)}
# #     dictToSend = {"pageIndex": 40, "pageSize": 2, "pharmacyId": pharmacyId, "outletId": outletid}
# #     res = requests.post('https://jarvin-dev.azurewebsites.net/api/GetPharmacists', headers=headers, json=dictToSend)
# #     dictFromServer = res.json()
# #     pharmacist = dictFromServer['response']["pharmacists"]
# #     pharma = []
# #     for i in pharmacist:
# #         if i['availability'] == []:
# #             pass
# #         else:
# #             pharma.append(i['name'])  
# #     return pharma        


# # def is_between(time, time_range):
# #     if time_range[1] < time_range[0]:
# #         return time >= time_range[0] or time <= time_range[1]
# #     return time_range[0] <= time <= time_range[1]

# # print(is_between(":00", ("09:00", "16:00")))  # True
# # print(is_between("17:00", ("09:00", "16:00")))  # False
# # print(is_between("01:15", ("21:30", "04:30")))  # True


#         # for i in dictFromServer['response']['availabilitySlots']:
#         #     if i['isChecked'] == True:
#         #         start = i['startTime']

#         #         ss.append(start)
#         #         end = i['endTime']
#         # return ss

# from inspect import Traceback
# import logging
# from traceback import TracebackException
# # from traceback import TracebackException


# # try:
# #     1/0
# # except ZeroDivisionError as err:
# #     logger.error(err)


# import parsedatetime
# import datetime
# import gspread
# from datetime import date, timedelta


#         dat= date.today()
#         print(dat)
#         dat = date.strftime(dat, "%Y-%m-%d")
#         dat = dat.split("-")
#         print(dat)

#         # dates = datetime.datetime(timess[0].strftime("%Y-%m-%d"))
#         dates = timess[0].split("-")
#         past = datetime.datetime.strptime(timess[1], "%Y-%m-%d")
#         print(dates)
#         present = datetime.datetime.now()
#         if past.date() < present.date():
#                 print("past date")
#         else:
#                 print("future date")

# except IndexError as err:
#         logger.error(err)
# except NameError as err:
#         logger.error(err)
# except ImportError as err:
#         logger.error(err)
# except KeyError as err:
#         logger.error(err)
# except AssertionError as err:
#         logger.error(err)        
# except AttributeError as err:
#         logger.error(err)   
# except NotImplementedError as err:
#         logger.error(err)   
# except OSError as err:
#         logger.error(err)   
# except ReferenceError as err:
#         logger.error(err)  
# except RuntimeError as err:
#         logger.error(err)  
# except SystemError as err:
#         logger.error(err)  
# except SyntaxError as err:
#         logger.error(err)
# except TypeError as err:
#         logger.error(err)  
# except ValueError as err:
#         logger.error(err)  













# # p = parsedatetime.Calendar()
# # time_struct, parse_status = p.parse("34 days")
# # dates = datetime.datetime(*time_struct[:6]).strftime("%Y-%m-%d")
# # # dates = dates.split("-") 
# # print(dates)

# # dates = datetime.datetime.strptime(dates, "%Y-%m-%d")
# # present_date = datetime.datetime.now()

# # length = dates.date() - present_date.date()

# # print(length.days)
# # ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
# # sh = ac.open("logs_checker")
# # wks = sh.worksheet("Sheet1")
# # wks.update_acell("A1", "ss")
# # wks.update_acell("B1", "dd")
# # import pandas as pd


# # sheet_id = "1n2ol4JaDokXMctufEIxrmRLNZbhriKKSihwKYlO7h6s"

# # df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# # print(df['sentence'][0])


# # final_days = []
# # recur_dates = ["2022-07-25", "2022-07-27"]
# # dates_initials = ["2022-07-25", "2022-07-26", "2022-07-27", "2022-07-28", "2022-07-29", "2022-07-30", "2022-07-31", "2022-08-01", "2022-08-02", "2022-08-03", "2022-08-04", "2022-08-05", "2022-08-06", "2022-08-07", "2022-08-08", "2022-08-09", "2022-08-10", "2022-08-11", "2022-08-12", "2022-08-13", "2022-08-14", "2022-08-15", "2022-08-16", "2022-08-17", "2022-08-18", "2022-08-19", "2022-08-20", "2022-08-21"]
# # dates_finals = ["2022-07-27", "2022-07-28", "2022-07-29", "2022-07-30", "2022-07-31", "2022-08-01", "2022-08-02", "2022-08-03", "2022-08-04", "2022-08-05", "2022-08-06", "2022-08-07", "2022-08-08", "2022-08-09", "2022-08-10", "2022-08-11", "2022-08-12", "2022-08-13", "2022-08-14", "2022-08-15", "2022-08-16", "2022-08-17", "2022-08-18", "2022-08-19", "2022-08-20", "2022-08-21"]
# # for i in recur_dates:
# #     recur_dates1 = i
# #     print(recur_dates1)
# #     recur_dates1 = recur_dates1.split("-")
# #     date_list = []
# #     for x in range(0, 28):
# #         dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
# #         date_list.append(dates.strftime("%Y-%m-%d"))
# #     for i in date_list:
# #         if i in dates_initials or i in dates_finals:
# #             final_days.append(i)
# #         else:
# #             pass


# # print(final_days)

# # list  = ["10:00:00", "16:00:00"]

# # str = ' '.join(map(str, list))
# # str = str.replace(" ", ",")
# # print(str)


# # # print(
# # #     'Returns:\n',
# # #     json.dumps(
# # #         ss,
# # #         default=lambda o: o.__dict__,
# # #         indent='\t',
# # #         ensure_ascii=False)
# # # )
# # # try:
# # #     print(w2n.word_to_num('1'))
# # # except:
# # #     print('Not a number')

# # times = []     
# # for i in ss:
# #     ss = i.resolution
# #     dd = ss['values']
# #     for j in dd:
# #         tim = j['value']  
# #         times.append(tim) 

# # print(times)
# # times = "one times"
# # dosage_time = times.replace("times", "").replace("time", "").replace("for", "").replace("only", "")
# # dosage_time = w2n.word_to_num("one times")
# # print(dosage_time)

# # import datetime 
# # #base = datetime.datetime.today()
# # date_list = []
# # for x in range(0, 14):
# #     dates = date(2022,7,26) + datetime.timedelta(days=7*x)
# #     date_list.append(dates.strftime("%Y-%m-%d"))

# # print(date_list)

# # lists = ["2", "4", "6"]
# # print(lists[-1])
# # #         if var == "med_name":
# #             med_name= step_context.result
# #             med_type = predict_class(med_name)

# #             if med_type == "tablet":
# #                 if dosage_time == 1 and option == "Recurring":
                    
# #                     patientid = userId
# #                     pharmacyid = 1
# #                     tokens = token
# #                     pillName = med_name
# #                     pillType = "0"
# #                     dosage = "1"
# #                     isRecurring = "true"
# #                     pill_time = times

# #                     dates_initial = cal_date(recur_dates[0], long_date)
# #                     dates_final = cal_date(recur_dates[-1], long_date)

# #                     dates_initials = []
# #                     dates_finals = []

# #                     if long_date == "1 Month":
# #                         count = 0
# #                         for i in range(len(dates_initial)):
# #                             count += 1
# #                             dates_initials.append(dates_initial[i])
# #                             if count == 28:
# #                                 break

# #                     if long_date == "2 Months":
# #                         count = 0
# #                         for i in range(len(dates_initial)):
# #                             count += 1
# #                             dates_initials.append(dates_initial[i])
# #                             if count == 56:
# #                                 break

# #                     if long_date == "3 Months":
# #                         count = 0
# #                         for i in range(len(dates_initial)):
# #                             count += 1
# #                             dates_initials.append(dates_initial[i])
# #                             if count == 84:
# #                                 break
# # ##########################################################
# #                     if long_date == "1 Month":
# #                         count = 0
# #                         for i in range(len(dates_final)):
# #                             count += 1
# #                             dates_finals.append(dates_final[i])
# #                             if count == 28:
# #                                 break

# #                     if long_date == "2 Months":
# #                         count = 0
# #                         for i in range(len(dates_final)):
# #                             count += 1
# #                             dates_finals.append(dates_final[i])
# #                             if count == 56:
# #                                 break

# #                     if long_date == "3 Months":
# #                         count = 0
# #                         for i in range(len(dates_final)):
# #                             count += 1
# #                             dates_finals.append(dates_final[i])
# #                             if count == 84:
# #                                 break


# #                     final_days = []

# #                     if long_date == "Two Weeks":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 14):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass

# #                     if long_date == "Three Weeks":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 21):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass                        

# #                     if long_date == "1 Month":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 28):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass
# #                     if long_date == "2 Months":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 56):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass   

# #                     if long_date == "3 Months":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 84):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass 

# #                     if long_date == "Two Weeks":
# #                         recurringValue = "2"
# #                         test_dict(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     if long_date == "Three Weeks":
# #                         recurringValue = "3"
# #                         set_reminder_tablet_three_weeks(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     if long_date == "1 Month":
# #                         recurringValue = "4"
# #                         test_dict(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     if long_date == "2 Months":
# #                         recurringValue = "8"
# #                         set_reminder_tablet_two_months(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     if long_date == "3 Months":
# #                         recurringValue = "12"
# #                         set_reminder_tablet_three_months(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)

# #                     await step_context.context.send_activity(
# #                         MessageFactory.text(f"Your pill reminder has been set."))
# #                     return await step_context.prompt(
# #                         TextPrompt.__name__,
# #                         PromptOptions(prompt=MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + ".")),)

# # ##########################################################################################################################################################################################################

# #                 if dosage_time >= 2 and option == "Recurring":
                    
# #                     patientid = userId
# #                     pharmacyid = 1
# #                     tokens = token
# #                     pillName = med_name
# #                     pillType = "0"
# #                     dosage = dosage_time
# #                     isRecurring = "true"
# #                     pill_time = times

# #                     dates_initial = cal_date(recur_dates[0], long_date)
# #                     dates_final = cal_date(recur_dates[-1], long_date)

# #                     dates_initials = []
# #                     dates_finals = []

# #                     if long_date == "1 Month":
# #                         count = 0
# #                         for i in range(len(dates_initial)):
# #                             count += 1
# #                             dates_initials.append(dates_initial[i])
# #                             if count == 28:
# #                                 break

# #                     if long_date == "2 Months":
# #                         count = 0
# #                         for i in range(len(dates_initial)):
# #                             count += 1
# #                             dates_initials.append(dates_initial[i])
# #                             if count == 56:
# #                                 break

# #                     if long_date == "3 Months":
# #                         count = 0
# #                         for i in range(len(dates_initial)):
# #                             count += 1
# #                             dates_initials.append(dates_initial[i])
# #                             if count == 84:
# #                                 break
# # ##########################################################
# #                     if long_date == "1 Month":
# #                         count = 0
# #                         for i in range(len(dates_final)):
# #                             count += 1
# #                             dates_finals.append(dates_final[i])
# #                             if count == 28:
# #                                 break

# #                     if long_date == "2 Months":
# #                         count = 0
# #                         for i in range(len(dates_final)):
# #                             count += 1
# #                             dates_finals.append(dates_final[i])
# #                             if count == 56:
# #                                 break

# #                     if long_date == "3 Months":
# #                         count = 0
# #                         for i in range(len(dates_final)):
# #                             count += 1
# #                             dates_finals.append(dates_final[i])
# #                             if count == 84:
# #                                 break
# import re
# bp = "190.92/80"
# bp = str(bp).lower()
# bp = bp.replace("its ", "").replace("it's ", "").replace("it is ", "")

# sys = re.sub(r"(\d+)\/\d+", r"\1", bp)
# dia = re.sub(r"\d+\/(\d+)", r"\1", bp)

# if  100 <= float(sys) <= 129:
#     print("normal")
# else:
#     print("abnormal")

# print(sys, dia)
# #                     final_days = []
# from recognizers_number import recognize_number, Culture
# temp  = "its 100.7"
# result = recognize_number(str(temp), Culture.English)
# res = []
# for i in result:
#     raw = i.resolution
#     dd = raw['value']
#     res.append(dd) 
# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# culture = Culture.English

# raw = Recognizers.recognize_datetime("Fri, Wed, Thu", culture) 
# times = []     
# for i in raw:
#     raw = i.resolution
#     dd = raw['values']
#     print(dd)
#     for j in dd:
#         tim = j['value']  
#         times.append(tim) 

# print(times)
# temps = res[0]

# if 36.1 <= float(temps) <= 40.6 or 97.8 <= float(temps) <= 106.3:
#     print("normal")
# else:
#     print("wrong")
# {'status': 'Success', 'response': {'patientData': {'id': 97, 'pharmacyId': 1, 'outletId': 7, 'name': 'Jibon', 'email': 'shamimmahbub230@gmail.com', 'countryCode': None, 'phoneNumber': None, 'age': None, 'sex': None, 'isPhoneVerified': False, 'pictureId': 0, 'pictureUrl': 'https://jarvin-dev.azurewebsites.net/appimages/default-image.png', 'temparature': None, 'fastingBloodSugar': None, 'bloodSugar': None, 'bloodPressureSys': None, 'bloodPressureDia': None, 'pulse': None, 'allergies': None, 'address': None, 'createdOnUtc': '2022-04-23T16:44:47.5279837', 'totalAppointments': 0, 'rating': 0.0, 'totalCalls': 0, 'dob': None, 'temparatureUnit': False, 'language': 'en'}, 'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk3IiwibmFtZSI6IkppYm9uIiwibmJmIjoxNjY0ODY2NzgxLCJleHAiOjE2NjU0NzE1ODEsImlhdCI6MTY2NDg2Njc4MX0.RacB-QUXeqy3vgqk8Dn71CXOLPxCvzmpWWUPYNTNAh8'}}

# #                     if long_date == "Two Weeks":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 14):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass

# #                     if long_date == "Three Weeks":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 21):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass                        

# #                     if long_date == "1 Month":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 28):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass
# #                     if long_date == "2 Months":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 56):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass   

# #                     if long_date == "3 Months":
# #                         for i in recur_dates:
# #                             recur_dates1 = recur_dates[i]
# #                             recur_dates1 = recur_dates1.split("-")
# #                             date_list = []
# #                             for x in range(0, 84):
# #                                 dates = date(recur_dates1[0],recur_dates1[1],recur_dates1[2]) + timedelta(days=7*x)
# #                                 date_list.append(dates.strftime("%Y-%m-%d"))
# #                             for i in date_list:
# #                                 if i in dates_initials or i in dates_finals:
# #                                     final_days.append(i)
# #                                 else:
# #                                     pass 

# #                     # if long_date == "Two Weeks":
# #                     #     recurringValue = "2"
# #                     #     set_reminder_tablet_two_weeks_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     # if long_date == "Three Weeks":
# #                     #     recurringValue = "3"
# #                     #     set_reminder_tablet_three_weeks_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     # if long_date == "1 Month":
# #                     #     recurringValue = "4"
# #                     #     set_reminder_tablet_one_months_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     # if long_date == "2 Months":
# #                     #     recurringValue = "8"
# #                     #     set_reminder_tablet_two_months_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
# #                     # if long_date == "3 Months":
# #                     #     recurringValue = "12"
# #                     #     set_reminder_tablet_three_months_multi(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)

# #                     await step_context.context.send_activity(
# #                         MessageFactory.text(f"Your pill reminder has been set."))
# #                     return await step_context.prompt(
# #                         TextPrompt.__name__,
# #                         PromptOptions(prompt=MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + ".")),)



# #             if med_type == "capsule":
# #                 await step_context.context.send_activity(
# #                     MessageFactory.text(f"Your pill reminder has been set."))
# #                 return await step_context.prompt(
# #                     TextPrompt.__name__,
# #                     PromptOptions(prompt=MessageFactory.text("I will remind you to take one [medicine name] at [8 pm] [daily / weekly / every Thursday]")),)
            
# #             if med_type == "syrup":
# #                 dose = "syrup dose koto"
# #                 return await step_context.prompt(
# #                     TextPrompt.__name__,
# #                     PromptOptions(prompt=MessageFactory.text("What's the recommended dosage in ml?")),)
                
# #             if med_type == "syringe":
# #                 dose = "syringe dose koto"
# #                 return await step_context.prompt(
# #                     TextPrompt.__name__,
# #                     PromptOptions(prompt=MessageFactory.text("What's the recommended dosage in ml?")),)
            
# #             if med_type == "drop":
# #                 dose = "drop dose koto"
# #                 return await step_context.prompt(
# #                     TextPrompt.__name__,
# #                     PromptOptions(prompt=MessageFactory.text("How many drops are recommended by the doctor?")),)

# #             else: 
# #                 type = "type of medicine"
# #                 reply = MessageFactory.text("What type of medicine is it?")
# #                 reply.suggested_actions = SuggestedActions(
# #                     actions=[
# #                         CardAction(
# #                             title= "Tablet",
# #                             type=ActionTypes.im_back,
# #                             value= "Tablet"),
# #                         CardAction(
# #                             title= "Drop",
# #                             type=ActionTypes.im_back,
# #                             value= "Drop",
# #                             ),
# #                         CardAction(
# #                             title= "Capsule",
# #                             type=ActionTypes.im_back,
# #                             value= "Capsule"),
# #                         CardAction(
# #                             title= "Syringe",
# #                             type=ActionTypes.im_back,
# #                             value= "Syringe"),
# #                         CardAction(
# #                             title= "Syrup",
# #                             type=ActionTypes.im_back,
# #                             value= "Syrup"),])
# #                 return await step_context.context.send_activity(reply)

# # import parsedatetime
# # import datetime
# # from datetime import date, timedelta

# # def cal_date(date_str):

# #     p = parsedatetime.Calendar()
# #     time_struct, parse_status = p.parse(date_str)
# #     dates = datetime.datetime(*time_struct[:6]).strftime("%Y-%m-%d")
# #     dates = dates.split("-")

# #     dat= date.today()
# #     dat = date.strftime(dat, "%Y-%m-%d")
# #     dat = dat.split("-")

# #     dates1 = date(int(dat[0]), int(dat[1]), int(dat[2]))

# #     dd = date(int(dates[0]), int(dates[1]), int(dates[2])) - date(int(dat[0]), int(dat[1]), int(dat[2]))
# #     datee = []

# #     for i in range(dd.days):
# #         day = dates1 + timedelta(days=i)
# #         datee.append(day)


# #     listToStr = ' '.join(map(str, datee))

# #     listt = listToStr.replace(" ", "\n")

# #     list1 = listt.split("\n")

# #     return list1


# # ss = cal_date("eleven days")
# # print(ss)

# # import pandas as pd
# # sheet_id = "1n2ol4JaDokXMctufEIxrmRLNZbhriKKSihwKYlO7h6s"
# # df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
# # main = df['sentence'][0]

# # print(main)
# # from word2number import w2n

# # dosage = w2n.word_to_num("two")
# # print(dosage)

