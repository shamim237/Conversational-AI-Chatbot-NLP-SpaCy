import gspread
from outlets import outlet_name
from user_info import check_name
from user_info import outlet_ids
from appointment import save_appoint, appoint_id
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
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from outlets2 import get_pharmacist_id, get_slots_sup, pharmacist_name
from botbuilder.schema import ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
culture = Culture.English


##########################################################################################################################################################################################################
############################################################## case-3: book an appointment at 8 pm ######################################################################################################


class caseThreeDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseThreeDialog, self).__init__(dialog_id or caseThreeDialog.__name__)

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

        global wks
        global time
        global main
        global time3x
        global token
        global timey
        global userId
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
        pred = predict_appoint(main)
        wks.update_acell("A17", str(pred))

        classes         = []
        time            = []

        for x in pred.keys():
            if x == "TIME":
                times = pred[x]
                time.append(times)
                classes.append(x)  

  
        extracts = Recognizers.recognize_datetime(time[0], culture) 
        time3x = []     
        for i in extracts:
                extracts = i.resolution
                lits = extracts['values']
                for j in lits:
                        tims = j['value']  
                        time3x.append(tims)
            
            
        return await step_context.prompt("date_prompt", PromptOptions(
            prompt=MessageFactory.text("On which date you would like to book an appointment?", extra = step_context.context.activity.text),
                retry_prompt= MessageFactory.text(
                "Please enter a valid day or date. P.S. It can't be past date.", extra = step_context.context.activity.text),))


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

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


        date3x           = step_context.result
        wks.update_acell("O1", str(date3x))
        outletId         = outlet_ids(userId, token)
        wks.update_acell("O2", str(outletId))
        outletName3x       = outlet_name(outletId, token)
        pharmacistsIds   = get_pharmacist_id(pharmacyId, outletId)  
        wks.update_acell("O3", str(pharmacistsIds))           
        slots3x          = get_slots_sup(pharmacistsIds, date3x, time3x[0], token)


        if slots3x is None:
            case3b = "different time3x"
            await step_context.context.send_activity(
                MessageFactory.text("Sorry! All our pharmacists are occupied at the selected time.", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to book the appointment at a different time?", extra = main)),) 
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
                    MessageFactory.text("Hey " + str(userName) + ", on " + str(date3x) + " at " + str(use_time3x) + ", " + str(doc_name3x) + " of " + str(outletName3x) + " outlet is available.", extra = main))
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("On " + str(date3x) + " at " + str(use_time3x) + ", " + str(doc_name3x) + " of " + str(outletName3x) + " outlet is available.", extra = main))            
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to confirm the appointment?", extra = main)),)



    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case3c
        global appointId
        appointId   = "aayayyaaa" 
        case3c      = "ruausauzz"

        if case3b == "confirm or not3x":
            msgsxy = predict_class(step_context.result)
            if msgsxy == "positive":
                case3c = "question ask3xx"
                save_appoint(date3x, times3xx, endTime3x, userId, pharmacistId3x, doc_name3x, pharmacyId, token)
                appointId = appoint_id(userId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name3x) + " has been booked on " + str(date3x) + " at "  + str(use_time3x) + ".", extra = main)) 
                await step_context.context.send_activity(
                    MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?", extra = main)),)     

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!", extra = main))
                return await step_context.begin_dialog(AppointmentDialog.__name__)  

        if case3b == "different time3x":
            msgx = predict_class(step_context.result)
            if msgx == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!", extra = main))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()    


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1d
        case1d = "sjksksk"

        if case3c == "question ask3xx":
            msgs = predict_class(step_context.result)
            if msgs == "positive":       
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page.", extra = main))
                reply = MessageFactory.text("go to question page", extra = main)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= str(appointId), 
                            extra = main)])
                await step_context.context.send_activity(reply)
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()    
            else:
                case1d = "update or not2"
                await step_context.context.send_activity(
                    MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition.", extra = main))    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to update health profile now?", extra = main)),) 


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:        

        if case1d == "update or not2":
            msg = predict_class(step_context.result) 

            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = main))

                return await step_context.begin_dialog(HealthProfileDialog.__name__) 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog() 