from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from prompt.email_prompt import EmailPrompt
from dialogs.book_appointment import AppointmentDialog
from dialogs.health_record_dialog import HealthRecordDialog


class BookNonInDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(BookNonInDialog, self).__init__(dialog_id or BookNonInDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(AppointmentDialog(AppointmentDialog.__name__))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,
                    self.final_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("I think you should see a Doctor or pharmacist. Would you like to book an appointment with a pharmacist?"),))

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        msg = step_context.context.activity.text
        msg = predict_class(msg)

        if msg == "positive":
            await step_context.context.send_activity(
                MessageFactory.text("I am initializing the book appointment process."))
            return await step_context.begin_dialog(AppointmentDialog.__name__)
        else:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text(f"What would you like to do?")))             
    
        