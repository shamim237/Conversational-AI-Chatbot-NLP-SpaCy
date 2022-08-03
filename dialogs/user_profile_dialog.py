import gspread
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from botbuilder.core import MessageFactory, UserState
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, DateTimePrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.book_appointment import AppointmentDialog
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from dialogs.tobe_loggedin_dialog import ToBeLoggedInDialog
from dialogs.health_record_dialog import HealthRecordDialog
from user_info import check_user



class UserProfileDialog(ComponentDialog):

    def __init__(self, user_state: UserState):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)
        self.user_profile_accessor = user_state.create_property("UserProfile")
        self.user_state = user_state
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,self.scnd_step,self.third_step,self.fourth_step, self.fifth_step,
                ],))
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(DateTimePrompt(DateTimePrompt.__name__))
        self.add_dialog(AppointmentDialog(AppointmentDialog.__name__))
        self.add_dialog(ToBeLoggedInDialog(ToBeLoggedInDialog.__name__))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.initial_dialog_id = "WFDialog"
        

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId

        ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
        sh = ac.open("logs_checker")
        wks = sh.worksheet("Sheet1")
        

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role

        try:
            wks.update_acell("B1", str(userId))
            wks.update_acell("C1", str(token))
            wks.update_acell("D1", str(pharmacyId))
        except:
            pass

        status = check_user(userId, token)

        if userId == 0 or status == "Fail" or status == 400:
            return await step_context.begin_dialog(ToBeLoggedInDialog.__name__)
        else:
            if status == "Success":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Hello! I am Jarvis, your personalized health assistant."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("How are you feeling today?")),)

    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global prompts

        prompts = "nothing"
        step_context.values["goodbad"] = step_context.result
        health = predict_class(step_context.result)

        if health == "good":
            prompts = "Would you like to subscribe to a daily health tip from an expert?"
            await step_context.context.send_activity(
                MessageFactory.text(f"Glad to hear it.\n\nHow can I help you today?"))
            reply = MessageFactory.text("Do you want me to do any of these?")
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Book an Appointment",
                        type=ActionTypes.im_back,
                        value= "Book an Appointment",),
                    CardAction(
                        title = "Pill Reminder",
                        type = ActionTypes.im_back,
                        value = "Pill Reminder",),
                    CardAction(
                        title = "Upload Health Records",
                        type = ActionTypes.im_back,
                        value = "Upload Health Records",),
                        ])
            return await step_context.context.send_activity(reply)         

        if health == "bad":
            prompts = "Have you consulted with a Doctor/Pharmacist?"
            await step_context.context.send_activity(
                MessageFactory.text(f"Sorry to hear that!"))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Have you consulted with any Doctor/Pharmacist?")),)
        if health == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay! I am initializing the book appointment process!"))
            return await step_context.begin_dialog(AppointmentDialog.__name__)

        if health == "health_records":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay! I am initializing the upload health records process!"))
            return await step_context.begin_dialog(HealthRecordDialog.__name__)
        if health == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
            return await step_context.begin_dialog(PillReminderDialog.__name__)
        if health == "adv_pill_reminder":
            ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
            sh = ac.open("logs_checker")
            wks = sh.worksheet("Sheet1")
            wks.update_acell("A2", str(step_context.result))
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
        else:
            prompts = "What would you like to start with?"
            await step_context.context.send_activity(
                MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("What would you like to start with?")),) 



    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global prompts
        global prompts2
        global upload
        global book 

        upload = "39jnxonjnxn"
        book = "cisnvinvb"

        step_context.values["2ndpath"] = step_context.result
        prompts2 = "nothing2"
        msg = predict_class(step_context.result)

        if prompts == "Would you like to subscribe to a daily health tip from an expert?":
            msg = step_context.result
            if msg ==  "Book an Appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the book appointment process!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            if msg == "Upload Health Records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the upload health records process!"))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)
            if msg == "Pill Reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                return await step_context.begin_dialog(PillReminderDialog.__name__)  

        if prompts == "Have you consulted with a Doctor/Pharmacist?":
            if msg == "positive":
                upload = "asking 1st"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"Would you like to save the prescription, or medical reports with me? I'll keep them all at one safe place.")))
            if msg == "negative":
                book = "asking 1st"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"I think you should see a Doctor or pharmacist. Would you like to book an appointment with a pharmacist?")))
            else:
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records. Do you want me to do any of these?")))

        if prompts == "What would you like to start with?":

            if msg == "appointment":
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            if msg == "health_records":
                return await step_context.begin_dialog(HealthRecordDialog.__name__)
            if msg == "reminder":
                return await step_context.begin_dialog(PillReminderDialog.__name__)
            else:
                upload == "asking 1st"
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry, I can't help you with that! As a Jarvis Health assistant, I can help you with the things which are on the Jarvis APP!"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"Would you like to save the prescription, or medical reports with me? I'll keep them all at one safe place.")))                
                
                
    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global prompts
        global prompts2
        global more_work


        more_work = 'msivn nv '
        msg = step_context.result
        msg = predict_class(msg)

        if upload == "asking 1st":
            if msg == "positive":
                return await step_context.begin_dialog(HealthRecordDialog.__name__)
            if msg == "negative":
                more_work = "askin me"
                reply = MessageFactory.text("What would you like to do?")
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "Book an Appointment",
                            type=ActionTypes.im_back,
                            value= "Book an Appointment",),
                        CardAction(
                            title = "Pill Reminder",
                            type = ActionTypes.im_back,
                            value = "Pill Reminder",),
                            ])
                return await step_context.context.send_activity(reply) 
        if book == "asking 1st":
            if msg  ==  "positive":
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            if msg == "negative":
                more_work = "dusking me"
                reply = MessageFactory.text("What would you like to do?")
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "Upload Health Records",
                            type=ActionTypes.im_back,
                            value= "Upload Health Records",),
                        CardAction(
                            title = "Pill Reminder",
                            type = ActionTypes.im_back,
                            value = "Pill Reminder",),
                            ])
                return await step_context.context.send_activity(reply) 


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if more_work == "askin me":
            msg = step_context.result
            if msg == "Book an Appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the book appointment process!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            if msg == "Pill Reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

        if more_work == "dusking me":
            msg = step_context.result
            if msg == "Upload Health Records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the health record upload process!"))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)
            if msg == "Pill Reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

