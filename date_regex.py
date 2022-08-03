import parsedatetime
import datetime
from datetime import date, timedelta

def cal_date(present, date_str):

    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(date_str)
    dates = datetime.datetime(*time_struct[:6]).strftime("%Y-%m-%d")
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
    dates = datetime.datetime(*time_struct[:6]).strftime("%Y-%m-%d")
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
