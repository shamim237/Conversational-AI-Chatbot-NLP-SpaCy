from lib.message_factory import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
import gspread



class PillReminderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "bypass-reminder"):
        super(PillReminderDialog, self).__init__(dialog_id or PillReminderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
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
        global main
        global pharmacyId

        main = step_context.context.activity.text
        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        wks.update_acell("E4", str(step_context.context.activity.text))
        wks.update_acell("E5", str(step_context.context.activity))

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please provide medicine name, dosage, time and duration for setting up the pill reminder.\n\nEx: remind me to take Aspirin 100mg tablets daily at 10 am for 3 weeks.", extra =  step_context.context.activity.text)),)  


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global excepts
        excepts = "msmnsmn"

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

            response = predict_class(step_context.result)

            if response == "adv_pill_reminder":
                return await step_context.begin_dialog("adv-reminder")

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

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

            wks.update_acell("E10", str(step_context.result))
            response = predict_class(step_context.result)
            wks.update_acell("E11", str(response))
            
            if response == "adv_pill_reminder":
                return await step_context.begin_dialog("adv-reminder")
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Let me set a pill reminder for you.", extra =  step_context.context.activity.text)) 
                return await step_context.begin_dialog("pill-reminder")
