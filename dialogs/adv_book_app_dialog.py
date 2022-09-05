from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from outlets import check_outlet, outlet_name, get_avail_slot, get_timeslots, match, get_timeslots2, timeConversion
from user_info import check_email, outlet_ids
from outlets2 import get_pharmacist_id, get_slots, pharmacist_name
from appointment import save_appoint
from user_info import check_name
from datetime import datetime, timedelta
from dialogs.non_upapp_dialog import UploadNonInDialogApp
import gspread



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
        self.add_dialog(UploadNonInDialogApp(UploadNonInDialogApp.__name__)) 
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.first_step,
                    self.scnd_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId
        global doc_name
        global times
        global use_time
        global endTime
        global dates
        global pharmacistId

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        timet = step_context.context.activity.local_timestamp
        act = step_context.context.activity

        wks.update_acell("J12", str(timet))
        wks.update_acell("J13", str(act))

        outletId        = outlet_ids(userId, token)
        wks.update_acell("J1", str(outletId))
        outletName      = outlet_name(outletId, token)
        wks.update_acell("J2", str(outletName))   
        pharmacistsIds  = get_pharmacist_id(pharmacyId, outletId) 
        wks.update_acell("J3", str(pharmacistsIds))
        dates           = datetime.today().strftime('%Y-%m-%d')
        wks.update_acell("J4", str(dates))
        slots_id        = get_slots(pharmacistsIds, dates, timet,  token) 
        wks.update_acell("J5", str(slots_id))
        doc_name        = pharmacist_name(slots_id[1])
        pharmacistId    = slots_id[1]
        wks.update_acell("J6", str(doc_name))
        userName        = check_name(userId, token) 
        wks.update_acell("J7", str(userName))

        times           = slots_id[0]
        ss = datetime.strptime(times, "%H:%M:%S")
        dd = ss + timedelta(minutes= 15)
        endTime = datetime.strftime(dd, "%H:%M:%S")

        wks.update_acell("J8", str(times))
        use_time        = datetime.strptime(times, "%H:%M:%S").strftime("%I:%M %p")

        if userName != "not found":
            await step_context.context.send_activity(
                MessageFactory.text("Hey " + str(userName) + ", Today at " + str(use_time) + ", " + str(doc_name) + " of " + str(outletName) + " outlet is available."))
        else:
            await step_context.context.send_activity(
                MessageFactory.text("Today at " + str(use_time) + ", " + str(doc_name) + " of " + str(outletName) + " outlet is available."))            
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Would you like to confirm the appointment?")),)

    
    
    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        msg = predict_class(step_context.result)

        if msg == "positive":
            save_appoint(dates, times, endTime, userId, pharmacistId, doc_name, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text("Thank You! Your appointment with " + str(doc_name) + " has been booked today at " + str(use_time) + ".")) 
            await step_context.context.send_activity(
                MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?")),)     

        else:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("When would you like to book the appointment?")),)                       