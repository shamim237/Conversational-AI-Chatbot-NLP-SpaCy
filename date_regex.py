import parsedatetime
from datetime import datetime
from datetime import date, timedelta
import recognizers_suite as Recognizers
from recognizers_suite import Culture
culture = Culture.English

def date_validate(date):

    try:

        today = datetime.now()
        today = datetime.strftime(today, "%Y-%m-%d")   
        today = datetime.strptime(today, "%Y-%m-%d").date()

        raw = Recognizers.recognize_datetime(date, culture = Culture.English) 
        dates = []     
        for i in raw:
            raw = i.resolution
            dd = raw['values']
            # print(dd)
            for j in dd:
                tim = j['value']  
                dates.append(tim) 
        f_date = []
        for i in dates:
            datey = datetime.strptime(i, "%Y-%m-%d").date()
            if datey >= today:
                datey = datetime.strftime(datey, "%Y-%m-%d")
                f_date.append(datey)
            else:
                return None
    except:
        return None

    return f_date


def time_validate(time):

    extract = Recognizers.recognize_datetime(time, culture = Culture.English) 
    times = []     
    for i in extract:
        keys = i.resolution
        values = keys['values']
        print(values)
        for j in values:
            timea = j['value']  
            times.append(timea)  

    return times
    

def cal_date(present, date_str):

    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(date_str)
    dates = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
    dates = dates.split("-")

    present_date = present
    dat = present_date.split("-")

    dates1 = date(int(dat[0]), int(dat[1]), int(dat[2]))

    dd = date(int(dates[0]), int(dates[1]), int(dates[2])) - date(int(dat[0]), int(dat[1]), int(dat[2]))
    datee = []

    for i in range(dd.days):
        day = dates1 + timedelta(days=i)
        datee.append(day)


    listToStr = ' '.join(map(str, datee))

    listt = listToStr.replace(" ", "\n")

    list1 = listt.split("\n")

    return list1




def cal_date_adv(date_str):

    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(date_str)
    dates = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
    dates = dates.split("-")

    dat= date.today()
    dat = date.strftime(dat, "%Y-%m-%d")
    dat = dat.split("-")

    dates1 = date(int(dat[0]), int(dat[1]), int(dat[2]))

    dd = date(int(dates[0]), int(dates[1]), int(dates[2])) - date(int(dat[0]), int(dat[1]), int(dat[2]))
    datee = []

    for i in range(dd.days):
        day = dates1 + timedelta(days=i)
        datee.append(day)


    listToStr = ' '.join(map(str, datee))

    listt = listToStr.replace(" ", "\n")

    list1 = listt.split("\n")

    return list1

def cal_date_stend(start, date_str):


    raw = Recognizers.recognize_datetime(start, culture) 
    times = []     
    for i in raw:
        raw = i.resolution
        dd = raw['values']
        for j in dd:
            tim = j['value']  
            times.append(tim) 


    filtered_days = []

    for i in times:
        check = datetime.strptime(i, "%Y-%m-%d")
        present = datetime.now()
        if check.date() < present.date():
            pass
        else:
            filtered_days.append(i)


    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(date_str)
    dates = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
    dates = dates.split("-")

    dat = filtered_days[0]
    dat = datetime.strptime(dat, "%Y-%m-%d")
    dat = datetime.strftime(dat, "%Y-%m-%d")
    dat = dat.split("-")

    dates1 = date(int(dat[0]), int(dat[1]), int(dat[2]))

    dd = date(int(dates[0]), int(dates[1]), int(dates[2])) - date(int(dat[0]), int(dat[1]), int(dat[2]))
    datee = []

    for i in range(dd.days):
        day = dates1 + timedelta(days=i)
        datee.append(day)


    listToStr = ' '.join(map(str, datee))

    listt = listToStr.replace(" ", "\n")

    list1 = listt.split("\n")

    return list1

# ss = cal_date_stend("tomorrow","7 days")
# print(ss) 

def cal_date_by_day(days, timeline):

    raw = Recognizers.recognize_datetime(days, culture) 
    times = []     
    for i in raw:
        raw = i.resolution
        dd = raw['values']
        for j in dd:
            tim = j['value']  
            times.append(tim) 

    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(timeline)
    dates = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
    dates = datetime.strptime(dates, "%Y-%m-%d")    

    present_date = datetime.now()
    length = dates.date() - present_date.date()
    act_length = length.days


    filtered_days = []

    for i in times:
        check = datetime.strptime(i, "%Y-%m-%d")
        present = datetime.now()
        if check.date() < present.date():
            pass
        else:
            filtered_days.append(i)

    filtered_days = sorted(filtered_days)


    init_date = datetime.strptime(filtered_days[0], "%Y-%m-%d")
    lengths = dates.date() - init_date.date()
    prob_length = lengths.days 

    lens = act_length - prob_length   
    

    if lens == 0:

        p = parsedatetime.Calendar()
        time_struct, parse_status = p.parse(timeline)
        dates = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
        dates = dates.split("-")

        present_date = filtered_days[0]
        dat = present_date.split("-")
        dates1 = date(int(dat[0]), int(dat[1]), int(dat[2]))
        dd = date(int(dates[0]), int(dates[1]), int(dates[2])) - date(int(dat[0]), int(dat[1]), int(dat[2]))
        datee = []
        for i in range(dd.days):
            day = dates1 + timedelta(days=i)
            datee.append(day)

        listToStr = ' '.join(map(str, datee))
        listt = listToStr.replace(" ", "\n")
        list1 = listt.split("\n")

        final_days = []
        for i in filtered_days:
            recur_dates1 = i
            recur_dates1 = recur_dates1.split("-")
            date_list = []
            for x in range(0, act_length):
                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                date_list.append(dates.strftime("%Y-%m-%d"))
            for i in date_list:
                if i in list1:
                    final_days.append(i)
                else:
                    pass 

        return final_days
    
    else:

        tims = act_length + lens
        p = parsedatetime.Calendar()
        time_struct, parse_status = p.parse(str(tims) + " days")
        dates = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
        dates = dates.split("-")

        present_date = filtered_days[0]
        dat = present_date.split("-")

        dates1 = date(int(dat[0]), int(dat[1]), int(dat[2]))
        dd = date(int(dates[0]), int(dates[1]), int(dates[2])) - date(int(dat[0]), int(dat[1]), int(dat[2]))

        datee = []
        for i in range(dd.days):
            day = dates1 + timedelta(days=i)
            datee.append(day)

        listToStr = ' '.join(map(str, datee))
        listt = listToStr.replace(" ", "\n")
        list1 = listt.split("\n")

        final_days = []
        for i in filtered_days:
            recur_dates1 = i
            recur_dates1 = recur_dates1.split("-")
            date_list = []
            for x in range(0, tims):
                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                date_list.append(dates.strftime("%Y-%m-%d"))
            for i in date_list:
                if i in list1:
                    final_days.append(i)
                else:
                    pass 

        return final_days


def cal_day(days):

    raw = Recognizers.recognize_datetime(days, culture) 
    times = []     
    for i in raw:
        raw = i.resolution
        dd = raw['values']
        for j in dd:
            tim = j['value']  
            times.append(tim) 


    filtered_days = []

    for i in times:
        check = datetime.strptime(i, "%Y-%m-%d")
        present = datetime.now()
        if check.date() < present.date():
            pass
        else:
            filtered_days.append(i)

    filtered_days = sorted(filtered_days)

    return filtered_days



# ss = cal_day("saturday, monday, tuesday")
# print(ss)

    

