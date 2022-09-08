import gspread
import warnings
import dateparser
import parsedatetime
from outlets import outlet_name
from user_info import check_name
from user_info import outlet_ids
from appointment import save_appoint
from recognizers_suite import Culture
import recognizers_suite as Recognizers
from datetime import datetime, timedelta
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from botbuilder.core import MessageFactory
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from nlp_model.appoint_predict import predict_appoint
from dialogs.book_appointment import AppointmentDialog
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from outlets2 import get_pharmacist_id, get_slots, get_slots_sup, pharmacist_name
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions

warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)
culture = Culture.English


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
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        timey = step_context.context.activity.additional_properties
        timey = timey.get('local_timestamp')

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        main = wks.acell("L20").value
        wks.update_acell("L4", main)

        pred = predict_appoint(main)

        try:
            wks.update_acell("L2", main)
            wks.update_acell("L3", str(pred))
        except:
            pass

        global date
        global time
        global timet
        global times
        global datet
        global use_time1
        global endTime1
        global doc_name1
        
        global pharmacistsIds
        global pharmacistId1

        times = "aklala"
        timet = "akakka"
        datet = "sjsjsjjs"
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

            if "/" or "-" in date[0]:
                datet = dateparser.parse(date[0])
                datet = datetime.strftime(datet, '%Y-%m-%d')

            else:
                p = parsedatetime.Calendar()
                time_struct, parse_status = p.parse(date[0])
                datet = datetime(*time_struct[:6]).strftime("%Y-%m-%d")  


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
            
            datey = datet         
            datey = datetime.strptime(datey, "%Y-%m-%d").date()
 

            if datey < today:
                case1a = "abar date nibo"
                await step_context.context.send_activity(
                    MessageFactory.text("The date you have mentioned is a past date!"))                
                return await step_context.prompt("date_prompt", PromptOptions(
                    prompt=MessageFactory.text("Please enter an upcoming date or day."),
                        retry_prompt= MessageFactory.text(
                        "Please enter a valid day or date. P.S. It can't be past date."),))

            if datey == today:
                case1a = "time a problem"
                now = timey
                current_time = datetime.strptime(now, "%I:%M %p")
                current_time = datetime.strftime(current_time, "%H:%M:%S")
                
                wks.update_acell("O1", str(current_time))
                wks.update_acell("O2", str(timet[0]))
                
                if current_time > timet[0]:
                    await step_context.context.send_activity(
                        MessageFactory.text("The time you have mentioned is in the past!"))
                    return await step_context.prompt(
                        "time_prompt",
                        PromptOptions(
                            prompt=MessageFactory.text("Please enter an upcoming time.")),) 
                else:
                    pass                    

            else:
                
                slots = get_slots_sup(pharmacistsIds, datet, timet[0], token)

                if slots is None:
                    case1a = "different time"
                    await step_context.context.send_activity(
                        MessageFactory.text("Sorry! All our pharmacists are occupied at the selected time."))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to book the appointment at a different time?")),) 
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
                            MessageFactory.text("Hey " + str(userName) + ", on " + str(datet) + " at " + str(use_time1) + ", " + str(doc_name1) + " of " + str(outletName) + " outlet is available."))
                    else:
                        await step_context.context.send_activity(
                            MessageFactory.text("On " + str(datet) + " at " + str(use_time1) + ", " + str(doc_name1) + " of " + str(outletName) + " outlet is available."))            
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to confirm the appointment?")),)

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################

        global datex
        global cas2a

        cas2a   = "ahasss"
        datex  = "ahahah"


        if "DATE" in classes and "TIME" not in classes:
            
            if "/" or "-" in date[0]:
                datet = dateparser.parse(date[0])
                datex = datetime.strftime(datet, '%Y-%m-%d')

            else:
                p = parsedatetime.Calendar()
                time_struct, parse_status = p.parse(date[0])
                datex = datetime(*time_struct[:6]).strftime("%Y-%m-%d")
            
            cas2a = "time kokhon"
            return await step_context.prompt(
                "time_prompt",
                PromptOptions(
                    prompt=MessageFactory.text("At what time would you like to consult?")),)


##########################################################################################################################################################################################################
############################################################## case-3: book an appointment at 8 pm ######################################################################################################

        global case3a
        global time3x

        case3a = "qwuiwi"
        time3x = "uauaki"

        if "DATE" not in classes and "TIME" in classes:

            case3a = "date kokhon"
            
            extracts = Recognizers.recognize_datetime(time[0], culture) 
            time3x = []     
            for i in extracts:
                    extracts = i.resolution
                    lits = extracts['values']
                    for j in lits:
                            tims = j['value']  
                            time3x.append(tims)
            
            
            return await step_context.prompt("date_prompt", PromptOptions(
                prompt=MessageFactory.text("On which date you would like to book an appointment?"),
                    retry_prompt= MessageFactory.text(
                    "Please enter a valid day or date. P.S. It can't be past date."),))


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1b
        global times2
        global use_time2
        global endTime2
        global doc_name2
        global pharmacistId2
        global dat
        timey = step_context.context.activity.additional_properties
        timey = timey.get('local_timestamp')
        times2 = "aklala"
        endTime2 = "asjsjjs"
        use_time2 = "jsjsuiww"
        doc_name2 = "asysusu"
        pharmacistId2 = "jsjsjs"
        case1b = "kiskskks"
        dat = "skskksk"

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
                    MessageFactory.text("Hey " + str(userName) + ", on " + str(dat) + " at " + str(use_time2) + ", " + str(doc_name2) + " of " + str(outletName) + " outlet is available."))
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("On " + str(dat) + " at " + str(use_time2) + ", " + str(doc_name2) + " of " + str(outletName) + " outlet is available."))            
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to confirm the appointment?")),)


        if case1a == "different time":
            msg = predict_class(step_context.result)
            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care."))
                return await step_context.end_dialog()                               


        if case1a == "confrim or not":
            msg = predict_class(step_context.result)
            if msg == "positive":
                case1b = "question ask"
                save_appoint(datet, times, endTime1, userId, pharmacistId1, doc_name1, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name1) + " has been booked on " + str(date[0]) + " at " + str(use_time1) + ".")) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?")),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
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
                        MessageFactory.text("Hey " + str(userName) + ", Today at " + str(use_time3) + ", " + str(doc_name3) + " of " + str(outletName) + " outlet is available."))
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Today at " + str(use_time3) + ", " + str(doc_name3) + " of " + str(outletName) + " outlet is available."))            
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to confirm the appointment?")),)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Sorry! The time you have entered is invalid!"))   
                await step_context.context.send_activity(
                    MessageFactory.text("Thank you for connecting with Jarvis Care."))                                                     
                return await step_context.end_dialog()  

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################
        
        global case2b
        global timesxx
        global doc_namex
        global outletNamex
        global pharmacistIdx
        global endTimex
        global use_timex

        case2b = "aahahyy"
        timesxx = "hahahah"
        doc_namex = "auiauua"
        outletNamex = "uuauai"
        pharmacistIdx = "uususus"
        endTimex = "wwiwia"
        use_timex = "usususu"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        if cas2a == "time kokhon":
            
            timex           = step_context.result
            
            outletId        = outlet_ids(userId, token)
            
            pharmacistsIds  = get_pharmacist_id(pharmacyId, outletId)
                         
            slotsx          = get_slots_sup(pharmacistsIds, datex, timex, token)

            if slotsx is None:
                case2b = "different time2x"
                await step_context.context.send_activity(
                    MessageFactory.text("Sorry! All our pharmacists are occupied at the selected time."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to book the appointment at a different time?")),)
            else:             
                doc_namex       = pharmacist_name(slotsx[1])
                
                pharmacistIdx   = slotsx[1]
                userName        = check_name(userId, token) 
                outletNamex     = outlet_name(outletId, token)
                timesxx         = slotsx[0]
                ss              = datetime.strptime(timesxx, "%H:%M:%S")
                dd              = ss + timedelta(minutes= 15)
                endTimex        = datetime.strftime(dd, "%H:%M:%S")
                use_timex       = datetime.strptime(timesxx, "%H:%M:%S").strftime("%I:%M %p")


                if userName != "not found":
                    case2b = "confirm or notx"
                    await step_context.context.send_activity(
                        MessageFactory.text("Hey " + str(userName) + ", on " + str(datex) + " at " + str(use_timex) + ", " + str(doc_namex) + " of " + str(outletNamex) + " outlet is available."))
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("On " + str(datex) + " at " + str(use_timex) + ", " + str(doc_namex) + " of " + str(outletNamex) + " outlet is available."))            
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to confirm the appointment?")),)

##########################################################################################################################################################################################################
############################################################## case-3: book an appointment at 8 pm ######################################################################################################

        global case3b
        global date3x
        global times3xx
        global doc_name3x
        global outletName3x
        global pharmacistId3x
        global endTime3x
        global use_time3x

        case3b          = "aahahyy"
        date3x          = "oaoaoao"
        times3xx        = "hahahah"
        doc_name3x      = "auiauua"
        outletName3x    = "uuauais"
        pharmacistId3x  = "uususus"
        endTime3x       = "wwiwias"
        use_time3x      = "usususu"                

        if case3a == "date kokhon":

            date3x           = step_context.result
            wks.update_acell("O1", str(date3x))
            outletId         = outlet_ids(userId, token)
            wks.update_acell("O2", str(outletId))
            outletName       = outlet_name(outletId, token)
            pharmacistsIds   = get_pharmacist_id(pharmacyId, outletId)  
            wks.update_acell("O3", str(pharmacistsIds))           
            slots3x          = get_slots_sup(pharmacistsIds, date3x, time3x[0], token)


            if slots3x is None:
                case3b = "different time3x"
                await step_context.context.send_activity(
                    MessageFactory.text("Sorry! All our pharmacists are occupied at the selected time."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to book the appointment at a different time?")),) 
            else:

                wks.update_acell("O4", str(slots3x)) 
                doc_name3x       = pharmacist_name(slots3x[1])
                wks.update_acell("O5", str(doc_name3x)) 
                pharmacistId3x   = slots3x[1]
                userName         = check_name(userId, token) 
                times3xx         = slots3x[0]
                wks.update_acell("O5", str(times3xx)) 
                ss               = datetime.strptime(times3xx, "%H:%M:%S")
                dd               = ss + timedelta(minutes= 15)
                endTime3x        = datetime.strftime(dd, "%H:%M:%S")
                use_time3x       = datetime.strptime(times3xx, "%H:%M:%S").strftime("%I:%M %p")

                wks.update_acell("O6", str(time3x[0]))

                if userName != "not found":
                    case3b = "confirm or not3x"
                    await step_context.context.send_activity(
                        MessageFactory.text("Hey " + str(userName) + ", on " + str(date3x) + " at " + str(use_time3x) + ", " + str(doc_name3x) + " of " + str(outletName3x) + " outlet is available."))
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("On " + str(date3x) + " at " + str(use_time3x) + ", " + str(doc_name3x) + " of " + str(outletName3x) + " outlet is available."))            
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to confirm the appointment?")),)


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1c
        case1c = "ksksaksk"

        if case1b == "confirm or not2":
            msg = predict_class(step_context.result)
            if msg == "positive":
                case1c = "question ask2"
                save_appoint(dat, times2, endTime2, userId, pharmacistId2, doc_name2, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name2) + " has been booked on " + str(dat) + " at "  + str(use_time2) + ".")) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?")),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)         


        if case1b == "question ask":

            msgs = predict_class(step_context.result)

            if msgs == "positive":       
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page."))
                reply = MessageFactory.text("go to question page")
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= "go to question page",)])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()    
            
            else:
                case1c = "update or not"
                await step_context.context.send_activity(
                    MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition."))    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to update health profile now?")),)

        if case1b == "confirm or not3":
            msg = predict_class(step_context.result)
            if msg == "positive":
                case1c = "question ask3"
                save_appoint(datet, times3, endTime3, userId, pharmacistId3, doc_name3, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name3) + " has been booked on " + str(datet) + " at "  + str(use_time3) + ".")) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?")),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)  

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################

        global case2c 
        case2c = "ruauau"

        if case2b == "confirm or notx":            
            msgsx = predict_class(step_context.result)
            if msgsx == "positive":
                case2c = "question ask3x"
                save_appoint(datex, timesxx, endTimex, userId, pharmacistIdx, doc_namex, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_namex) + " has been booked on " + str(datex) + " at "  + str(use_timex) + ".")) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?")),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)  

        if case2b == "different time2x":
            msg2x = predict_class(step_context.result)
            if msg2x == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care."))
                return await step_context.end_dialog()  

##########################################################################################################################################################################################################
############################################################## case-3: book an appointment at 8 pm ######################################################################################################

        global case3c 
        case3c = "ruausau"

        if case3b == "confirm or not3x":
            msgsxy = predict_class(step_context.result)
            if msgsxy == "positive":
                case3c = "question ask3xx"
                save_appoint(date3x, times3xx, endTime3x, userId, pharmacistId3x, doc_name3x, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name3x) + " has been booked on " + str(date3x) + " at "  + str(use_time3x) + ".")) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?")),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)  

        if case3b == "different time3x":
            msgx = predict_class(step_context.result)
            if msgx == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care."))
                return await step_context.end_dialog()    


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1d
        case1d = "sjksksk"

        if case1c == "question ask2" or case1c == "question ask3" or case2c == "question ask3x" or case3c == "question ask3xx":
            msgs = predict_class(step_context.result)
            if msgs == "positive":       
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page."))
                reply = MessageFactory.text("go to question page")
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= "go to question page",)])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()    
            else:
                case1d = "update or not2"
                await step_context.context.send_activity(
                    MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition."))    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to update health profile now?")),)         
        
        if case1c == "update or not":
            msg = predict_class(step_context.result) 

            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!"))

                return await step_context.begin_dialog(HealthProfileDialog.__name__) 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care."))
                return await step_context.end_dialog() 

            


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if case1d == "update or not2":
            msg = predict_class(step_context.result) 

            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!"))

                return await step_context.begin_dialog(HealthProfileDialog.__name__) 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care."))
                return await step_context.end_dialog() 