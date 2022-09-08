import gspread
from outlets import outlet_name
from user_info import check_name
from user_info import outlet_ids
from appointment import save_appoint
from datetime import datetime, timedelta
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from botbuilder.core import MessageFactory
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from outlets2 import get_pharmacist_id, get_slots, pharmacist_name
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from dialogs.appoint_extra_plus import AppointExtraPlusDialog



class AppointExtraDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(AppointExtraDialog, self).__init__(dialog_id or AppointExtraDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__)) 
        self.add_dialog(AppointExtraPlusDialog(AppointExtraPlusDialog.__name__))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.first_step,
                    self.scnd_step,
                    self.third_step,

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
        timey = step_context.context.activity.additional_properties

        wks.update_acell("P10", str(timey))
        timey = timey.get('local_timestamp')
        wks.update_acell("P11", str(timey))

        outletId        = outlet_ids(userId, token)
        wks.update_acell("P1", str(outletId))
        outletName      = outlet_name(outletId, token)
        wks.update_acell("P2", str(outletName))   
        pharmacistsIds  = get_pharmacist_id(pharmacyId, outletId) 
        wks.update_acell("P3", str(pharmacistsIds))
        dates           = datetime.today().strftime('%Y-%m-%d')
        wks.update_acell("P4", str(dates))
        slots_id        = get_slots(pharmacistsIds, dates, timey, token) 
        wks.update_acell("P5", str(slots_id))
        doc_name        = pharmacist_name(slots_id[1])
        pharmacistId    = slots_id[1]
        wks.update_acell("P6", str(doc_name))
        userName        = check_name(userId, token) 
        wks.update_acell("P7", str(userName))

        times           = slots_id[0]
        ss = datetime.strptime(times, "%H:%M:%S")
        dd = ss + timedelta(minutes= 15)
        endTime = datetime.strftime(dd, "%H:%M:%S")

        wks.update_acell("P8", str(times))
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

        global step1
        step1 = "nvsjknvsk"

        msg = predict_class(step_context.result)

        if msg == "positive":
            step1 = "question ask"
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
            await step_context.context.send_activity(
                MessageFactory.text("Alright!"))
            return await step_context.begin_dialog(AppointExtraPlusDialog.__name__)                    


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        if step1 == "question ask":
            msg = predict_class(step_context.result)

            if msg == "positive":       
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
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. Thanks for connecting with Jarvis Care."))
                return await step_context.end_dialog()


           

