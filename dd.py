# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# from datetime import datetime

# def date_validate(date):

#     try:

#         today = datetime.now()
#         today = datetime.strftime(today, "%Y-%m-%d")   
#         today = datetime.strptime(today, "%Y-%m-%d").date()

#         raw = Recognizers.recognize_datetime(date, culture = Culture.English) 
#         dates = []     
#         for i in raw:
#             raw = i.resolution
#             dd = raw['values']
#             # print(dd)
#             for j in dd:
#                 tim = j['value']  
#                 dates.append(tim) 
#         f_date = []
#         for i in dates:
#             datey = datetime.strptime(i, "%Y-%m-%d").date()
#             if datey >= today:
#                 datey = datetime.strftime(datey, "%Y-%m-%d")
#                 f_date.append(datey)
#             else:
#                 return None
#     except:
#         return None

#     return f_date

# ss = date_validate("not tell you")
# print(ss)

# print(datess)

# datek = ",".join(datess)

# print(datek)

# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# from datetime import datetime



# ss = time_validate("at 11pm")
# print(ss)