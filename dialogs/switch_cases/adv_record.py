from nlp_model.predict import predict_class
from lib.message_factory import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from dialogs.upcoming_appoint_dialog import UpcomingAppointmentDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.adv_book_app_dialog import AdvBookAppDialog
from dialogs.adv_appoint_dialog import SupAdvBookAppDialog

class SwitchCase4(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(SwitchCase4, self).__init__(dialog_id or SwitchCase4.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(HealthProfileDialog(HealthProfileDialog.__name__))
        self.add_dialog(AdvBookAppDialog(AdvBookAppDialog.__name__))
        self.add_dialog(SupAdvBookAppDialog(SupAdvBookAppDialog.__name__))
        self.add_dialog(UpcomingAppointmentDialog(UpcomingAppointmentDialog.__name__))        
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        pred = predict_class(step_context.context.activity.text)

        if pred == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(PillReminderDialog.__name__)

        if pred == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(AdvPillReminderDialog.__name__) 

        if pred == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Wait a second...", extra = step_context.context.activity.text))
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(AdvBookAppDialog.__name__)

        if pred == "adv_appointment":
            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

        if pred == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Let me check...", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)

        if pred == "health_profile":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(HealthProfileDialog.__name__)  