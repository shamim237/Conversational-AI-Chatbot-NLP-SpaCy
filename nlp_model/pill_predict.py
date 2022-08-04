import requests
# import gspread


def reminder_class(msg):
    res = requests.get('https://spacy-zibew.herokuapp.com/predict/{}'.format(msg))
    return res.json()


# ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
# sh = ac.open("logs_checker")
# wks = sh.worksheet("Sheet1")
# main = wks.acell("A2").value
# print(main)

# ss = reminder_class(main)
# print(ss)