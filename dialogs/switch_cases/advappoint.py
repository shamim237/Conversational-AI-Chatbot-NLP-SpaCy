from nlp_model.predict import predict_class
from lib.message_factory import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from dialogs.adv_health_record_dialog import AdvHealthRecordDialog
from dialogs.upcoming_appoint_dialog import UpcomingAppointmentDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog


class SwitchCase(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(SwitchCase, self).__init__(dialog_id or SwitchCase.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(AdvHealthRecordDialog(AdvHealthRecordDialog.__name__))
        self.add_dialog(HealthProfileDialog(HealthProfileDialog.__name__))
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

        if pred == "adv_health_record":
            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)  

        if pred == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Let me check...", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(UpcomingAppointmentDialog.__name__)

        if pred == "health_profile":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = step_context.context.activity.text))
            return await step_context.begin_dialog(HealthProfileDialog.__name__)  