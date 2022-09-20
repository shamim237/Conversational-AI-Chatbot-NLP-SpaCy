from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
import gspread
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.simple_reminder_dialog import SimplePillReminderDialog


class PillReminderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(PillReminderDialog, self).__init__(dialog_id or PillReminderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(SimplePillReminderDialog(SimplePillReminderDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.init_step,
                    self.scnd_step,
                    self.third_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def init_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please provide medicine name, dosage, time and duration for setting up the pill reminder.\n\nExample: remind me to take Aspirin 100mg tablets daily at 10 am for 3 weeks.", extra =  step_context.context.activity.text)),)  


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global excepts
        excepts = "msmnsmn"

        response = predict_class(step_context.result)

        if response == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You!", extra =  step_context.context.activity.text))
            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

        else:
            excepts = "didn't do it"
            await step_context.context.send_activity(
                MessageFactory.text(f"To set a pill reminder, please follow the example:", extra =  step_context.context.activity.text)) 
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("'set a pill reminder for Bendix Syrup daily at 9 pm'", extra =  step_context.context.activity.text)),)  


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        wks.update_acell("E10", str(step_context.result))
        response = predict_class(step_context.result)
        wks.update_acell("E11", str(response))
        
        if response == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text("Thank You!", extra =  step_context.context.activity.text))
            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
        else:
            await step_context.context.send_activity(
                MessageFactory.text("Alright! I am initializing other process for setting up a pill reminder!", extra =  step_context.context.activity.text)) 
            return await step_context.begin_dialog(SimplePillReminderDialog.__name__)
