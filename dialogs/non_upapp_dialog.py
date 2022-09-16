from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from prompt.email_prompt import EmailPrompt
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog


class UploadNonInDialogApp(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(UploadNonInDialogApp, self).__init__(dialog_id or UploadNonInDialogApp.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))        
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,
                    self.final_step,
                    self.final1_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role        

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Would you like to save the prescription, or medical reports with me? I'll keep them all at one safe place."),))

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global prop
        prop = "lsvkns vn"

        msg = step_context.context.activity.text
        msg = predict_class(msg)

        if msg == "positive":
            await step_context.context.send_activity(
                MessageFactory.text("I am initializing the health record uploading process."))
            return await step_context.begin_dialog(HealthRecordDialog.__name__)
        else:
            prop = "ki korba"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text(f"What would you like to do?")))             
    
    async def final1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:  

        if prop == "ki korba":
            msg = predict_class(step_context.result)

            if msg == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!"))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if msg == "adv_pill_reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!"))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

    