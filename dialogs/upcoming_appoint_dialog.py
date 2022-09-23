from lib.message_factory import MessageFactory
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
                    self.init3_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def init_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global main
        global pharmacyId
        global prompts 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        


        prompts = "appapapap"
        main = step_context.context.activity.text
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
                MessageFactory.text(f"Sorry! You have no upcoming appointments.", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like me to book an appointment for you?", extra = main)),) 
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
                date = date[:10]
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

            send = "\n".join(sss) + "\n"

            await step_context.context.send_activity(
                MessageFactory.text("You have " + str(len(apps)) + " upcoming appointments." + "\n\n" + str(send), extra = main))

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Do you want to know anything else from me?", extra = main)),) 

    async def init2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global promp
        promp = "askmdfmk"

        if prompts == "no upcoming appointment":
            response = predict_class(step_context.result)

            if response == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!", extra = main))
                return await step_context.begin_dialog(AppointmentDialog.__name__)
            if response == "negative":
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?", extra = main)),) 
            if response == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!", extra = main))
                return await step_context.begin_dialog(AppointmentDialog.__name__)

            if response == "health_records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!", extra = main))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)

            if response == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if response == "health_profile":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = main))
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if response == "adv_pill_reminder":
                ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                sh = ac.open("chatbot_logger")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("A2", str(step_context.result))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?", extra = main)),)   

        if prompts == "have upcoming appointment":
            response = predict_class(step_context.result)

            if response == "positive":
                promp = "what to do"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Okay. Please tell me what would you like to do?", extra = main)),)

            if response == "negative":
                promp = "what not to do"
                await step_context.context.send_activity(
                    MessageFactory.text("Okay. But I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Do you want anything of these?", extra = main)),) 

            if response == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!", extra = main))
                return await step_context.begin_dialog(AppointmentDialog.__name__)

            if response == "health_records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!", extra = main))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)

            if response == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if response == "health_profile":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = main))
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if response == "adv_pill_reminder":
                ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                sh = ac.open("chatbot_logger")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("A2", str(step_context.result))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?", extra = main)),)   


    async def init3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if promp == "what to do":
            response = predict_class(step_context.result)

            if response == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!", extra = main))
                return await step_context.begin_dialog(AppointmentDialog.__name__)

            if response == "health_records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!", extra = main))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)

            if response == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if response == "health_profile":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = main))
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if response == "adv_pill_reminder":
                ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                sh = ac.open("chatbot_logger")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("A2", str(step_context.result))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?", extra = main)),)  

        if promp == "what not to do":
            response = predict_class(step_context.result)

            if response == "appointment":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of booking an appointment!", extra = main))
                return await step_context.begin_dialog(AppointmentDialog.__name__)

            if response == "health_records":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of uploading health records!", extra = main))
                return await step_context.begin_dialog(HealthRecordDialog.__name__)

            if response == "reminder":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)

            if response == "health_profile":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a health profile!", extra = main))
                return await step_context.begin_dialog(HealthProfileDialog.__name__)

            if response == "adv_pill_reminder":
                ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                sh = ac.open("chatbot_logger")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("A2", str(step_context.result))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay. I am initializing the process of setting up a pill reminder!", extra = main))
                return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What would you like to start with?", extra = main)),)  

