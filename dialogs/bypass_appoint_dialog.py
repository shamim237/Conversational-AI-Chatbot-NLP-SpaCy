from lib.message_factory import MessageFactory
from lib.card import CardAction
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
from botbuilder.schema import ActionTypes, SuggestedActions
from dialogs.non_upapp_dialog import UploadNonInDialogApp
from dialogs.adv_book_app_dialog import AdvBookAppDialog
from dialogs.profile_update_dialog import HealthProfileDialog




class ByPassAppointmentDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "bypass-appoint"):
        super(ByPassAppointmentDialog, self).__init__(dialog_id or ByPassAppointmentDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__)) 
        self.add_dialog(UploadNonInDialogApp(UploadNonInDialogApp.__name__)) 
        self.add_dialog(AdvBookAppDialog(AdvBookAppDialog.__name__))
        self.add_dialog(HealthProfileDialog(HealthProfileDialog.__name__))
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
        global main
        global pharmacyId

        main = step_context.context.activity.text

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role  


        await step_context.context.send_activity(
            MessageFactory.text("Our team of expert pharmacists can help you with that.", extra = step_context.context.activity.text)) 
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Do you want me to schedule an appointment with one of our pharmacists?", extra = step_context.context.activity.text)),)                   


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global choose

        choose = "sisvkaskl"


        msg = predict_class(step_context.result)

        if msg == "positive":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Wait a second...", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog(AdvBookAppDialog.__name__)

        else:
            choose = "choose options"
            reply = MessageFactory.text("How can I help you?\nI can- ", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Book an Appointment",
                        type=ActionTypes.im_back,
                        value= "Book an Appointment",
                        extra = main),
                    CardAction(
                        title = "Set a Pill Reminder",
                        type = ActionTypes.im_back,
                        value = "Set a Pill Reminder",
                        extra = main),
                    CardAction(
                        title = "Save Health Records",
                        type = ActionTypes.im_back,
                        value = "Save Health Records",
                        extra = main),
                    CardAction(
                        title = "Update your health profile",
                        type = ActionTypes.im_back,
                        value = "Update your health profile",
                        extra = main),
                        ])
            return await step_context.context.send_activity(reply)    


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if choose == "choose options":
            
            msg = step_context.result

            if msg == "Book an Appointment" or msg == "Reservar una cita":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Wait a second..."))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you."))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)
            
            if msg == "Save Health Records" or msg == "Guardar registros de salud":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!"))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)
            
            if msg == "Set a Pill Reminder" or msg == "Establecer un recordatorio de píldora":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!"))
                return await step_context.begin_dialog(PillReminderDialog.__name__) 

            if msg == "Update your health profile" or msg == "Actualiza tu perfil de salud": 
                return await step_context.begin_dialog(HealthProfileDialog.__name__)