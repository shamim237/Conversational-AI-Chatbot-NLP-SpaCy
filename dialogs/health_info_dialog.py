from lib.card import CardAction
from nlp_model.predict import predict_class
from lib.message_factory import MessageFactory
from botbuilder.schema import ActionTypes, SuggestedActions
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, PromptOptions
from dialogs.adv_book_app_dialog import AdvBookAppDialog
from dialogs.adv_appoint_dialog import SupAdvBookAppDialog
from botbuilder.schema import ActionTypes, SuggestedActions
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.bypass_appoint_dialog import ByPassAppointmentDialog
from dialogs.adv_health_record_dialog import AdvHealthRecordDialog
from dialogs.upcoming_appoint_dialog import UpcomingAppointmentDialog


class HealthInfoDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "goodbad"):
        super(HealthInfoDialog, self).__init__(dialog_id or HealthInfoDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(AdvBookAppDialog(AdvBookAppDialog.__name__))
        self.add_dialog(ByPassAppointmentDialog(ByPassAppointmentDialog.__name__))
        self.add_dialog(SupAdvBookAppDialog(SupAdvBookAppDialog.__name__))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(AdvHealthRecordDialog(AdvHealthRecordDialog.__name__))
        self.add_dialog(HealthProfileDialog(HealthProfileDialog.__name__))
        self.add_dialog(UpcomingAppointmentDialog(UpcomingAppointmentDialog.__name__))
        self.add_dialog(WaterfallDialog("WFDialog",
                [
                    self.initial_step,
                    self.scnd_step,
                    self.third_step,
                    self.fourth_step,

                ],))

        self.initial_dialog_id = "WFDialog"


    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global main
        global prompts

        main = step_context.context.activity.text
        prompts = "init"

        msg = predict_class(step_context.context.activity.text)

        if msg == "good":
            prompts = "Would you like to subscribe to a daily health tip from an expert?"
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. I am assuming that your health is well.", extra = main))
            reply = MessageFactory.text("Would you like my help with any of these?", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Book an Appointment",
                        type=ActionTypes.im_back,
                        value= "Book an Appointment",
                        extra = main),
                    CardAction(
                        title = "Pill Reminder",
                        type = ActionTypes.im_back,
                        value = "Pill Reminder",
                        extra = main),
                    CardAction(
                        title = "Upload Health Records",
                        type = ActionTypes.im_back,
                        value = "Upload Health Records",
                        extra = main),
                        ])
            return await step_context.context.send_activity(reply)      

        if msg == "bad":
            prompts = "Have you consulted with a Doctor/Pharmacist?"
            await step_context.context.send_activity(
                MessageFactory.text(f"Sorry to hear that!", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Have you consulted with any Doctor or Pharmacist?", extra = main)),)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload
        global book
        global anythings

        upload = "39jnxonjnxn"
        book = "auyayay"
        anythings = "cisdddb" 

        if prompts == "Would you like to subscribe to a daily health tip from an expert?":
            
            msgs = step_context.result
            
            if msgs == "Book an Appointment" or msgs == "Reservar una cita":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)
            
            if msgs == "Upload Health Records" or msgs == "Cargar registros de salud":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!", extra = main))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)
            
            if msgs == "Pill Reminder" or msgs == "Recordatorio de pastillas":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)  

        if prompts == "Have you consulted with a Doctor/Pharmacist?":
            
            msg = predict_class(step_context.result)
            
            if msg == "positive":
                upload = "asking 1st"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"Would you like to save the prescription, or medical reports with me? I'll keep them all at one safe place.", extra = main)))
            
            if msg == "negative":
                book = "asking 1st"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"I think you should see a Doctor or pharmacist. Would you like to book an appointment with a pharmacist?", extra = main)))
            
            if msg == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)

            if msg == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if msg == "health_profile":
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if msg == "adv_pill_reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            if msg == "adv_health_record":
                return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

            if msg == "adv_appointment":
                return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

            if msg == "upcoming_app":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. Please let me check...", extra = main))
                return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)

            if msg == "bypass_appoint":
                return await step_context.begin_dialog(ByPassAppointmentDialog.__name__)

            else:
                anythings = "ki bole"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records. What would you like me to do?", extra = main)))


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global more_work

        more_work = "buttons"


        if upload == "asking 1st":
            msg = step_context.result
            msg = predict_class(msg)

            if msg == "positive":
                return await step_context.begin_dialog(HealthRecordDialog.__name__)

            if msg == "negative":
                more_work = "askin me"
                reply = MessageFactory.text("What would you like to do?", extra = main)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "Book an Appointment",
                            type=ActionTypes.im_back,
                            value= "Book an Appointment",
                            extra = main),
                        CardAction(
                            title = "Pill Reminder",
                            type = ActionTypes.im_back,
                            value = "Pill Reminder",
                            extra = main),
                            ])
                return await step_context.context.send_activity(reply)

            if msg == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)

            if msg == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if msg == "health_profile":
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if msg == "adv_pill_reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            if msg == "adv_health_record":
                return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

            if msg == "adv_appointment":
                return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

            if msg == "upcoming_app":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. Please let me check...", extra = main))
                return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)

            if msg == "bypass_appoint":
                return await step_context.begin_dialog(ByPassAppointmentDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! I am not able to understand.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care!", extra = main))
                return await step_context.end_dialog()

        if book == "asking 1st":
            msgt = predict_class(step_context.result)

            if msgt  ==  "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)

            if msgt == "negative":
                more_work = "dusking me"
                reply = MessageFactory.text("What would you like to do?", extra = main)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title   = "Upload Health Records",
                            type    = ActionTypes.im_back,
                            value   = "Upload Health Records",
                            extra = main),
                        CardAction(
                            title   = "Pill Reminder",
                            type    = ActionTypes.im_back,
                            value   = "Pill Reminder",
                            extra = main),
                            ])
                return await step_context.context.send_activity(reply) 

            if msgt == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)

            if msgt == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if msgt == "health_profile":
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if msgt == "adv_pill_reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            if msgt == "adv_health_record":
                return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

            if msgt == "adv_appointment":
                return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

            if msgt == "upcoming_app":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. Please let me check...", extra = main))
                return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)

            if msgt == "bypass_appoint":
                return await step_context.begin_dialog(ByPassAppointmentDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! I am not able to understand.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care!", extra = main))
                return await step_context.end_dialog()                

        if anythings == "ki bole":
            msgs = predict_class(step_context.result)
            if msgs == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)

            if msgs == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if msg == "health_profile":
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if msgs == "adv_pill_reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)  

            if msg == "adv_health_record":
                return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

            if msg == "adv_appointment":
                return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

            if msg == "upcoming_app":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. Please let me check...", extra = main))
                return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)     
            
            if msg == "bypass_appoint":
                return await step_context.begin_dialog(ByPassAppointmentDialog.__name__) 

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! I am not able to understand.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for connecting with Jarvis Care!", extra = main))
                return await step_context.end_dialog()        


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if more_work == "askin me":
            msg = step_context.result
            if msg == "Book an Appointment" or msg == "Reservar una cita":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
                return await step_context.begin_dialog(AdvBookAppDialog.__name__)
            if msg == "Pill Reminder" or msg == "Recordatorio de pastillas":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

        if more_work == "dusking me":
            msg = step_context.result
            if msg == "Upload Health Records" or msg == "Cargar registros de salud":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am initializing the health record upload process!", extra = main))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)
            if msg == "Pill Reminder" or msg == "Recordatorio de pastillas":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)