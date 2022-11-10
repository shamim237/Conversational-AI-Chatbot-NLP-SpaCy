from lib.message_factory import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from prompt.email_prompt import EmailPrompt

class NonAnyDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(NonAnyDialog, self).__init__(dialog_id or NonAnyDialog.__name__)

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
                    self.initial_step,
                    self.scnd_step,
                    self.final_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("I can help you connect with a pharmacist, set a pill reminder, and upload health records. Do you want me to do any of these?", extra = step_context.context.activity.text),))

    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global want
        want = "isisnii"
        
        msg = step_context.context.activity.text
        msg = predict_class(msg)

        if msg == "positive":
            want = "options"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Okay, Tell me which one you want me to do?", extra = step_context.context.activity.text),))
        
        if msg == "appointment":
            return await step_context.begin_dialog("book-appoint")
        
        if msg == "adv_health_record":
            return await step_context.begin_dialog("adv-record") 
        else:
            want = "nothing"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text(f"What would you like to do?", extra = step_context.context.activity.text),))             
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        msg = step_context.result
        msg = predict_class(msg)

        if want == "options" or want == "nothing":
            
            if msg == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text("I am initializing the book appointment process.", extra = step_context.context.activity.text))
                return await step_context.begin_dialog("book-appoint")
            
            if msg == "adv_health_record":
                return await step_context.begin_dialog("adv-record") 
            else:
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"Sorry! I don't understand. What would you like to do?", extra = step_context.context.activity.text),))             
                                