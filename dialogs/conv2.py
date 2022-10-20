from lib.message_factory import MessageFactory
from lib.card import CardAction
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from botbuilder.dialogs.choices import Choice
from nlp_model.predict import predict_class, response
from botbuilder.dialogs.choices import Choice
from botbuilder.schema import ActionTypes, SuggestedActions
import gspread



class Conv2Dialog(ComponentDialog):
    def __init__(self, dialog_id: str = "conv2"):
        super(Conv2Dialog, self).__init__(dialog_id or Conv2Dialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.first_step,
                    self.secnd_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId
        global main

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role  
        main = step_context.context.activity.text


        msg = predict_class(main)

        if msg == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text("Let me check the earliest appointment slots for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("early-book")

        if msg == "adv_appointment":
            return await step_context.begin_dialog("adv-book")

        if msg == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("pill-reminder") 

        if msg == "health_profile":
            return await step_context.begin_dialog("health-profile") 

        if msg == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("adv-reminder") 

        if msg == "adv_health_record":
            return await step_context.begin_dialog("adv-record")  

        if msg == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text("Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if msg == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")                                  

        else:
            return await step_context.next()


    async def secnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        msg = predict_class(step_context.result)

        if msg == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text("Let me check the earliest appointment slots for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("early-book")

        if msg == "adv_appointment":
            return await step_context.begin_dialog("adv-book")

        if msg == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("pill-reminder") 

        if msg == "health_profile":
            return await step_context.begin_dialog("health-profile") 

        if msg == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("adv-reminder") 

        if msg == "adv_health_record":
            return await step_context.begin_dialog("adv-record")  

        if msg == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text("Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if msg == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")                                  

        else:
            prompts = "nothing understand"
            resp = response(step_context.result)
            if len(resp) == 1:
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(resp[0], extra = step_context.context.activity.text)),)
            if len(resp) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text(resp[0], extra = main))                        
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(resp[1], extra = step_context.context.activity.text)),)
            if len(resp) == 3:
                await step_context.context.send_activity(
                    MessageFactory.text(resp[0], extra = main)) 
                await step_context.context.send_activity(
                    MessageFactory.text(resp[1], extra = main))                         
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(resp[2], extra = step_context.context.activity.text)),)