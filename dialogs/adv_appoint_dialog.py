from unittest import case
import gspread
from outlets import outlet_name
from user_info import check_name
from user_info import outlet_ids
from recognizers_suite import Culture
import recognizers_suite as Recognizers
from datetime import datetime, timedelta
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from lib.message_factory import MessageFactory
from lib.card import CardAction
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from nlp_model.appoint_predict import predict_appoint
from dialogs.book_appointment import AppointmentDialog
from appointment import save_appoint, date_cal, appoint_id
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from botbuilder.schema import ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from outlets2 import get_pharmacist_id, get_slots, get_slots_sup, pharmacist_name
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from dialogs.appoint_case.case_2 import caseTwoDialog
from dialogs.appoint_case.case_3 import caseThreeDialog



class SupAdvBookAppDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(SupAdvBookAppDialog, self).__init__(dialog_id or SupAdvBookAppDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__)) 
        self.add_dialog(AppointmentDialog(AppointmentDialog.__name__)) 
        self.add_dialog(caseTwoDialog(caseTwoDialog.__name__))
        self.add_dialog(caseThreeDialog(caseThreeDialog.__name__))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(HealthProfileDialog(HealthProfileDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.first_step,
                    self.scnd_step,
                    self.third_step,
                    self.fourth_step,
                    self.fifth_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global wks
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        timey = step_context.context.activity.additional_properties
        timey = timey.get('local_timestamp')

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        main = step_context.context.activity.text
        wks.update_acell("A6", str(main))     

        pred = predict_appoint(main)

        try:
            wks.update_acell("L3", str(pred))
        except:
            pass

        global date
        global time
        global timet
        global times
        global datek
        global use_time1
        global endTime1
        global doc_name1
        
        global pharmacistsIds
        global pharmacistId1

        times = "aklala"
        timet = "akakka"
        datek = "sjsjsjjs"
        endTime1 = "asjsjjs"
        use_time1 = "jsjsuiww"
        doc_name1 = "asysusu"
        pharmacistsIds = "kksksks"
        pharmacistId1 = "jsjsjs"

        classes         = []
        date            = []
        time            = []


        for x in pred.keys():
            
            if x == "DATE":
                dates = pred[x]
                date.append(dates)
                classes.append(x)
            
            if x == "TIME":
                times = pred[x]
                time.append(times)
                classes.append(x)  



        outletId        = outlet_ids(userId, token)
        outletName      = outlet_name(outletId, token)
        pharmacistsIds  = get_pharmacist_id(pharmacyId, outletId) 



        global case1a 
        case1a = "eieieie"

        if "DATE" in classes and "TIME" in classes:

            datek = date_cal(date[0])
            datekk = datetime.strptime(datek, "%Y-%m-%d").date()
            culture = Culture.English
            extract = Recognizers.recognize_datetime(time[0], culture) 
            timet = []     
            for i in extract:
                    extract = i.resolution
                    lit = extract['values']
                    for j in lit:
                            tim = j['value']  
                            timet.append(tim)

            today = datetime.now()
            today = datetime.strftime(today, "%Y-%m-%d")   
            today = datetime.strptime(today, "%Y-%m-%d").date()  



            if datek is None:
                case1a = "abar date nibo"
                await step_context.context.send_activity(
                    MessageFactory.text("I can only book appointments for times in the future.", extra = step_context.context.activity.text))                
                return await step_context.prompt("date_prompt", PromptOptions(
                    prompt=MessageFactory.text("Please enter an upcoming date or day.", extra = step_context.context.activity.text),
                        retry_prompt= MessageFactory.text(
                        "Please enter a valid day or date. P.S. It can't be past date.", extra = step_context.context.activity.text),))

            if datekk == today:
                case1a = "time a problem"
                now = timey
                current_time = datetime.strptime(now, "%I:%M %p")
                current_time = datetime.strftime(current_time, "%H:%M:%S")
                
                wks.update_acell("O1", str(current_time))
                wks.update_acell("O2", str(timet[0]))
                
                if current_time > timet[0]:
                    await step_context.context.send_activity(
                        MessageFactory.text("I can only book appointments for times in the future.", extra = step_context.context.activity.text))
                    return await step_context.prompt(
                        "time_prompt",
                        PromptOptions(
                            prompt=MessageFactory.text("When do you want to book the appointment?", extra = step_context.context.activity.text)),) 
                else:
                    pass                    

            else:
                
                slots = get_slots_sup(pharmacistsIds, datek, timet[0], token)

                if slots is None:
                    case1a = "different time"
                    await step_context.context.send_activity(
                        MessageFactory.text("Sorry! All our pharmacists are occupied at the selected time.", extra = step_context.context.activity.text))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to book the appointment at a different time?", extra = step_context.context.activity.text)),) 
                else:                       
                    case1a          = "confrim or not"
                    doc_name1       = pharmacist_name(slots[1])
                    pharmacistId1   = slots[1]
                    userName        = check_name(userId, token) 

                    times           = slots[0]
                    ss              = datetime.strptime(times, "%H:%M:%S")
                    dd              = ss + timedelta(minutes= 15)
                    endTime1        = datetime.strftime(dd, "%H:%M:%S")

                    use_time1       = datetime.strptime(times, "%H:%M:%S").strftime("%I:%M %p")

                    if userName != "not found":
                        await step_context.context.send_activity(
                            MessageFactory.text("Hey " + str(userName) + ", on " + str(datek) + " at " + str(use_time1) + ", " + str(doc_name1) + " of " + str(outletName) + " outlet is available.", extra = step_context.context.activity.text))
                    else:
                        await step_context.context.send_activity(
                            MessageFactory.text("On " + str(datek) + " at " + str(use_time1) + ", " + str(doc_name1) + " of " + str(outletName) + " outlet is available.", extra = step_context.context.activity.text))            
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to confirm the appointment?", extra = step_context.context.activity.text)),)


        if "DATE" in classes and "TIME" not in classes:
            return await step_context.begin_dialog(caseTwoDialog.__name__)

        if "DATE" not in classes and "TIME" in classes:
            return await step_context.begin_dialog(caseThreeDialog.__name__)



    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1b
        global times2
        global use_time2
        global endTime2
        global doc_name2
        global pharmacistId2
        global dat
        global appointId1

        timey           = step_context.context.activity.additional_properties
        timey           = timey.get('local_timestamp')
        times2          = "aklala"
        endTime2        = "asjsjjs"
        use_time2       = "jsjsuiww"
        doc_name2       = "asysusu"
        pharmacistId2   = "jsjsjs"
        case1b          = "kiskskks"
        appointId1      = "atatatat"
        dat             = "skskksk"

        if case1a == "abar date nibo":
            dat = step_context.result
            outletId         = outlet_ids(userId, token)
            outletName       = outlet_name(outletId, token)
            pharmacistsIds1  = get_pharmacist_id(pharmacyId, outletId) 
            slots            = get_slots_sup(pharmacistsIds1, dat, timet[0], token)
            doc_name2        = pharmacist_name(slots[1])
            pharmacistId2    = slots[1]
            userName         = check_name(userId, token) 
            times2           = slots[0]
            ss               = datetime.strptime(times2, "%H:%M:%S")
            dd               = ss + timedelta(minutes= 15)
            endTime2         = datetime.strftime(dd, "%H:%M:%S")
            use_time2        = datetime.strptime(times2, "%H:%M:%S").strftime("%I:%M %p")         

            if userName != "not found":
                case1b = "confirm or not2"
                await step_context.context.send_activity(
                    MessageFactory.text("Hey " + str(userName) + ", on " + str(dat) + " at " + str(use_time2) + ", " + str(doc_name2) + " of " + str(outletName) + " outlet is available.", extra = step_context.result))
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("On " + str(dat) + " at " + str(use_time2) + ", " + str(doc_name2) + " of " + str(outletName) + " outlet is available.", extra = step_context.result))            
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to confirm the appointment?", extra = step_context.result)),)


        if case1a == "different time":
            msg = predict_class(step_context.result)
            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!", extra = step_context.result))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog()                               


        if case1a == "confrim or not":
            msg = predict_class(step_context.result)
            if msg == "positive":
                case1b = "question ask"
                save_appoint(datek, times, endTime1, userId, pharmacistId1, doc_name1, pharmacyId, token)
                appointId1 = appoint_id(userId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name1) + " has been booked on " + str(date[0]) + " at " + str(use_time1) + ".", extra = step_context.result)) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = step_context.result))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?", extra = step_context.result)),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!", extra = step_context.result))
                return await step_context.begin_dialog(AppointmentDialog.__name__)

        global pharmacistId3
        global endTime3
        global times3
        global doc_name3
        global use_time3

        pharmacistId3 = "jksksks"
        endTime3      = "ksksksk"
        times3        = "ksaksks"
        doc_name3     = "sususus"  
        use_time3     = "jjsjsjs"


        if case1a == "time a problem": 
            corr_time = step_context.result
            now = timey
            current_time = datetime.strptime(now, "%I:%M %p")
            current_time = datetime.strftime(current_time, "%H:%M:%S")  

            if current_time < corr_time:
                today = datetime.now()
                today = datetime.strftime(today, "%Y-%m-%d") 
                case1b          = "confirm or not3"      
                slots3          = get_slots_sup(pharmacistsIds, today, corr_time, token)
                doc_name3       = pharmacist_name(slots3[1])
                pharmacistId3   = slots3[1]
                userName        = check_name(userId, token) 
                outletId        = outlet_ids(userId, token)
                outletName      = outlet_name(outletId, token)
                times3          = slots3[0]
                ss              = datetime.strptime(times3, "%H:%M:%S")
                dd              = ss + timedelta(minutes= 15)
                endTime3        = datetime.strftime(dd, "%H:%M:%S")
                use_time3       = datetime.strptime(times3, "%H:%M:%S").strftime("%I:%M %p")

                if userName != "not found":
                    await step_context.context.send_activity(
                        MessageFactory.text("Hey " + str(userName) + ", Today at " + str(use_time3) + ", " + str(doc_name3) + " of " + str(outletName) + " outlet is available.", extra = step_context.result))
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Today at " + str(use_time3) + ", " + str(doc_name3) + " of " + str(outletName) + " outlet is available.", extra = step_context.result))            
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to confirm the appointment?", extra = step_context.result)),)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Sorry! The time you have entered is invalid!", extra = step_context.result))   
                await step_context.context.send_activity(
                    MessageFactory.text("Thank you for connecting with Jarvis Care.", extra = step_context.result))                                                     
                return await step_context.end_dialog()  


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1c
        global appointId2
        global appointId3

        appointId3  = "aauuauau"
        appointId2  = "atettets"
        case1c      = "ksksaksk"

        if case1b == "confirm or not2":
            msg = predict_class(step_context.result)
            if msg == "positive":
                case1c = "question ask2"
                save_appoint(dat, times2, endTime2, userId, pharmacistId2, doc_name2, pharmacyId, token)
                appointId2 = appoint_id(userId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name2) + " has been booked on " + str(dat) + " at "  + str(use_time2) + ".", extra = step_context.result)) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = step_context.result))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?", extra = step_context.result)),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!", extra = step_context.result))
                return await step_context.begin_dialog(AppointmentDialog.__name__)         


        if case1b == "question ask":

            msgs = predict_class(step_context.result)

            if msgs == "positive":       
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                reply = MessageFactory.text("go to question page", extra = step_context.result)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= str(appointId1),
                            extra= step_context.result)])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()    
            
            else:
                case1c = "update or not"
                await step_context.context.send_activity(
                    MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition.", extra = step_context.result))    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to update health profile now?", extra = step_context.result)),)

        if case1b == "confirm or not3":
            msg = predict_class(step_context.result)
            if msg == "positive":
                case1c = "question ask3"
                save_appoint(datek, times3, endTime3, userId, pharmacistId3, doc_name3, pharmacyId, token)
                appointId3 = appoint_id(userId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name3) + " has been booked on " + str(datek) + " at "  + str(use_time3) + ".", extra = step_context.result)) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = step_context.result))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?", extra = step_context.result)),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!", extra = step_context.result))
                return await step_context.begin_dialog(AppointmentDialog.__name__)  



    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1d
        case1d = "sjksksk"

        if case1c == "question ask2" or case1c == "question ask3":
            msgs = predict_class(step_context.result)
            if msgs == "positive":
                if case1c == "question ask2":       
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                    reply = MessageFactory.text("go to question page", extra = step_context.result)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= "go to question page",
                                type=ActionTypes.im_back,
                                value= str(appointId2),
                                extra= step_context.result)])
                    await step_context.context.send_activity(reply)
                    return await step_context.end_dialog()   
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                    reply = MessageFactory.text("go to question page", extra = step_context.result)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= "go to question page",
                                type=ActionTypes.im_back,
                                value= str(appointId3),
                                extra= step_context.result)])
                    await step_context.context.send_activity(reply)
                    return await step_context.end_dialog()   

            else:
                case1d = "update or not2"
                await step_context.context.send_activity(
                    MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition.", extra = step_context.result))    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to update health profile now?", extra = step_context.result)),)         
        
        if case1c == "update or not":
            msg = predict_class(step_context.result) 

            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = step_context.result))

                return await step_context.begin_dialog(HealthProfileDialog.__name__) 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog() 

            


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if case1d == "update or not2":
            msg = predict_class(step_context.result) 

            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = step_context.result))

                return await step_context.begin_dialog(HealthProfileDialog.__name__) 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog() 