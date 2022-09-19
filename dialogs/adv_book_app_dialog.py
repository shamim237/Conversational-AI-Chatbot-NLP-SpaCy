import gspread
from outlets import outlet_name
from user_info import check_name
from user_info import outlet_ids
from appointment import appoint_id, save_appoint
from datetime import datetime, timedelta
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from botbuilder.core import MessageFactory
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from dialogs.book_appointment import AppointmentDialog
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from outlets2 import get_pharmacist_id, get_slots, pharmacist_name
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions



class AdvBookAppDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(AdvBookAppDialog, self).__init__(dialog_id or AdvBookAppDialog.__name__)

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

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global opt
        global userId
        global token
        global pharmacyId
        global doc_name
        global times
        global use_time
        global endTime
        global dates
        global pharmacistId

        opt = "aiaiaiaia"
        use_time = "auiaai"
        doc_name = 'uauauau'
        endTime = "kakakak"
        times = "kaskak"
        pharmacistId = "asjjajaj"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        timey = step_context.context.activity.additional_properties
        timey = timey.get('local_timestamp')

        outletId        = outlet_ids(userId, token)
        wks.update_acell("D1", str(outletId))
        outletName      = outlet_name(outletId, token)
        wks.update_acell("D2", str(outletName))
        pharmacistsIds  = get_pharmacist_id(pharmacyId, outletId)
        wks.update_acell("D3", str(pharmacistsIds)) 
        dates           = datetime.today().strftime('%Y-%m-%d')
        wks.update_acell("D4", str(dates)) 
        slots_id        = get_slots(pharmacistsIds, dates, timey, token) 
        wks.update_acell("D5", str(slots_id)) 
        
        if slots_id is None:
            opt =  "asking another"
            await step_context.context.send_activity(
                MessageFactory.text(f"Sorry! No slots are available at this moment", extra = step_context.result))
            
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to book the appointment at a different time?", extra = step_context.context.activity.text)),)

        if slots_id != None:
            opt = "saving appointment"
            doc_name        = pharmacist_name(slots_id[1])
            pharmacistId    = slots_id[1]
            userName        = check_name(userId, token) 

            times           = slots_id[0]
            ss = datetime.strptime(times, "%H:%M:%S")
            dd = ss + timedelta(minutes= 15)
            endTime = datetime.strftime(dd, "%H:%M:%S")
            use_time        = datetime.strptime(times, "%H:%M:%S").strftime("%I:%M %p")

            if userName != "not found":
                await step_context.context.send_activity(
                    MessageFactory.text("Hey " + str(userName) + ", Today at " + str(use_time) + ", " + str(doc_name) + " of " + str(outletName) + " outlet is available.", extra = step_context.context.activity.text))
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Today at " + str(use_time) + ", " + str(doc_name) + " of " + str(outletName) + " outlet is available.", extra = step_context.context.activity.text))            
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to confirm the appointment?", extra = step_context.context.activity.text)),)
    
    
    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global step1
        global appointId
        appointId   = "aayayyaaa"
        step1       = "nvsjknvsk"

        if opt == "saving appointment":

            msg = predict_class(step_context.result)

            if msg == "positive":
                step1 = "question ask"
                save_appoint(dates, times, endTime, userId, pharmacistId, doc_name, pharmacyId, token)
                appointId = appoint_id(userId, token)
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! Your appointment with " + str(doc_name) + " has been booked today at " + str(use_time) + ".", extra = step_context.result)) 
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

        if opt == "asking another":
            msg = predict_class(step_context.result)  
            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Alright!", extra = step_context.result))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog()                 



    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global update
        update = "jksjsjs"

        if step1 == "question ask":
            msgs = predict_class(step_context.result)

            if msgs == "positive":       
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                reply = MessageFactory.text("go to question page")
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= str(appointId),
                            )])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()    
            
            else:
                update = "update or not"
                await step_context.context.send_activity(
                    MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition.", extra = step_context.result))    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to update health profile now?", extra = step_context.result)),)


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if update == "update or not":
            msg = predict_class(step_context.result) 

            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = step_context.result))

                return await step_context.begin_dialog(HealthProfileDialog.__name__) 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog()             


