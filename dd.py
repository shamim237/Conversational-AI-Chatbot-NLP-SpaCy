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
from word2number import w2n

dosage = w2n.word_to_num("two")
print(dosage)

