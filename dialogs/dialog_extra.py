from lib.message_factory import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from prompt.email_prompt import EmailPrompt
from dialogs.book_appointment import AppointmentDialog
from dialogs.adv_book_app_dialog import AdvBookAppDialog
from dialogs.adv_appoint_dialog import SupAdvBookAppDialog
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.bypass_appoint_dialog import ByPassAppointmentDialog
from dialogs.adv_health_record_dialog import AdvHealthRecordDialog
from dialogs.upcoming_appoint_dialog import UpcomingAppointmentDialog


class DialogExtra(ComponentDialog):
    def __init__(self, dialog_id: str = "passing"):
        super(DialogExtra, self).__init__(dialog_id or DialogExtra.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(AppointmentDialog(AppointmentDialog.__name__))
        self.add_dialog(AdvBookAppDialog(AdvBookAppDialog.__name__))
        self.add_dialog(ByPassAppointmentDialog(ByPassAppointmentDialog.__name__))
        self.add_dialog(SupAdvBookAppDialog(SupAdvBookAppDialog.__name__))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(AdvHealthRecordDialog(AdvHealthRecordDialog.__name__))
        self.add_dialog(HealthProfileDialog(HealthProfileDialog.__name__))
        self.add_dialog(UpcomingAppointmentDialog(UpcomingAppointmentDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,
                    self.scnd_step,
                    self.third_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Would you like me to do anything else for you?", extra =  step_context.context.activity.text),))   

    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global prompts
        prompts = "ajkajaj"

        msg = predict_class(step_context.result)     

        if msg == "negative":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay! Thank You.", extra = step_context.context.activity.text))
            return await step_context.end_dialog()    
        if msg == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Please wait for a second...", extra = step_context.context.activity.text))
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(AdvBookAppDialog.__name__)   

        if msg == "adv_appointment":
            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

        if msg == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. I'm setting up a pill reminder!", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(PillReminderDialog.__name__) 

        if msg == "health_profile":
            return await step_context.begin_dialog(HealthProfileDialog.__name__)  

        if msg == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(AdvPillReminderDialog.__name__) 

        if msg == "adv_health_record":
            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)  

        if msg == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)

        if msg == "bypass_appoint":
            return await step_context.begin_dialog(ByPassAppointmentDialog.__name__)  

        else:
            prompts = "What would you like to start with?"
            await step_context.context.send_activity(
                MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = step_context.context.activity.text))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("What would you like to start with?", extra = step_context.context.activity.text)),) 

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        msg = predict_class(step_context.result)

        if prompts == "What would you like to start with?":

            if msg == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Please wait for a second...", extra = step_context.context.activity.text))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra =step_context.context.activity.text))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)

            if msg == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = step_context.context.activity.text))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if msg == "health_profile":
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if msg == "adv_pill_reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = step_context.context.activity.text))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            if msg == "adv_health_record":
                return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

            if msg == "adv_appointment":
                return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

            if msg == "upcoming_app":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. Please let me check...", extra = step_context.context.activity.text))
                return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)

            if msg == "bypass_appoint":
                return await step_context.begin_dialog(ByPassAppointmentDialog.__name__) 