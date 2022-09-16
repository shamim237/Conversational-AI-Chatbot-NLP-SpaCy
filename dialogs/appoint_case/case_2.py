import gspread
from outlets import outlet_name
from user_info import check_name
from user_info import outlet_ids
from appointment import appoint_id, save_appoint, date_cal
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
culture = Culture.English

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################


class caseTwoDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseTwoDialog, self).__init__(dialog_id or caseTwoDialog.__name__)

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
        global date
        global datex
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
        date            = []

        for x in pred.keys():
            if x == "DATE":
                dates = pred[x]
                date.append(dates)
                classes.append(x)
                    
        datex = date_cal(date[0])
        
        return await step_context.prompt(
            "time_prompt",
            PromptOptions(
                prompt=MessageFactory.text("At what time would you like to consult?")),)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################
        global case2b
        global timesxx
        global endTimex
        global use_timex
        global doc_namex
        global outletNamex
        global pharmacistIdx


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


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################

        global case2c 
        global appointId
        appointId   = "aayayyaaa"
        case2c      = "ruauausss"

        if case2b == "confirm or notx":            
            msgsx = predict_class(step_context.result)
            if msgsx == "positive":
                case2c = "question ask3x"
                save_appoint(datex, timesxx, endTimex, userId, pharmacistIdx, doc_namex, pharmacyId, token)
                appointId = appoint_id(userId, token)
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


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1d
        case1d = "sjksksk"

        if case2c == "question ask3x":
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
                            value= str(appointId),)])
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