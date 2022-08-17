from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, PromptOptions
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from dialogs.book_appointment import AppointmentDialog
from appointment import upcoming_appointment
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.health_record_dialog import HealthRecordDialog
import gspread

class UpcomingAppointmentDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(UpcomingAppointmentDialog, self).__init__(dialog_id or UpcomingAppointmentDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))           
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(AppointmentDialog(AppointmentDialog.__name__))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(HealthProfileDialog(HealthProfileDialog.__name__))        
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.init_step,
                    self.init2_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def init_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId
        global prompts 

        ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
        sh = ac.open("logs_checker")
        wks = sh.worksheet("Sheet1")

        


        prompts = "appapapap"

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        wks.update_acell("A1", str(userId))
        wks.update_acell("B1", str(token))

        appoint = upcoming_appointment(userId, token) 

        wks.update_acell("C1", str(appoint))

        if appoint['response']['appointment'] == []:
            prompts = "no upcoming appointment"
            await step_context.context.send_activity(
                MessageFactory.text(f"Sorry! You have no upcoming appointments."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like me to book an appointment for you?")),) 
        else:
            prompts = "have upcoming appointment"
            apps = []
            pharmacist = []
            dates = []
            starttimes = []
            endtimes = []

            appoints = appoint['response']['appointment']
            wks.update_acell("C2", str(appoints))
            count = 0
            for i in appoints:
                count += 1
                pharmacistName = i["pharmacistName"]
                date = i["dateUtc"]
                startTime = i["startTime"]
                endTime = i["endTime"]
                apps.append(count)
                pharmacist.append(pharmacistName)
                dates.append(date)
                starttimes.append(startTime)
                endtimes.append(endTime)

            sss = []
            for i in range(len(apps)):
                dd = "Appointment " + str(apps[i]) + ": \n" + "Pharmacist: " + pharmacist[i] + "\n" + "Date: " + dates[i] + "\n" + "Time: " + starttimes[i] + " - " + endtimes[i] + "\n"
                sss.append(dd)

            wks.update_acell("C3", "\n".join(sss))
            wks.update_acell("C4", str(len(apps)))

            send = "\n".join(sss) + "\n"

            wks.update_acell("C5", str(len(apps)))
            wks.update_acell("C6", str(send))

            # await step_context.context.send_activity(
            #     MessageFactory.text(f"You have " + len(apps) + " upcoming appointments."))
            # await step_context.context.send_activity(
            #     MessageFactory.text(send))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("You have " + str(len(apps)) + " upcoming appointments." + "\n" + str(send))),) 

    async def init2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if prompts == "no upcoming appointment":
            response = predict_class(step_context.result)

            if response == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            if response == "negative":
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?")),) 
            if response == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)

            if response == "health_records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!"))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)

            if response == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!"))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if response == "health_profile":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!"))
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if response == "adv_pill_reminder":
                ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
                sh = ac.open("logs_checker")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("A2", str(step_context.result))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!"))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?")),)   

        if prompts == "have upcoming appointment":
            response = predict_class(step_context.result)

            if response == "positive":
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Okay. Please tell me what would you like to do?")),)

            if response == "negative":
                await step_context.context.send_activity(
                    MessageFactory.text("Okay. But I can help you connect with a pharmacist, set a pill reminder, and upload health records."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Do you want anything of these?")),) 

            if response == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!"))
                return await step_context.begin_dialog(AppointmentDialog.__name__)

            if response == "health_records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!"))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)

            if response == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!"))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if response == "health_profile":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!"))
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if response == "adv_pill_reminder":
                ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
                sh = ac.open("logs_checker")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("A2", str(step_context.result))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!"))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?")),)   





