from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from botbuilder.dialogs.choices import Choice
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from pill_reminder import get_patient_id
from outlets import check_outlet, outlet_name, get_avail_slot, get_timeslots, match, get_timeslots2, timeConversion
from user_info import check_email
from appointment import save_appoint
from botbuilder.dialogs.choices import Choice
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
import gspread

class AppointmentDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(AppointmentDialog, self).__init__(dialog_id or AppointmentDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))                
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.date_step,
                    self.pharmacist_step,
                    self.time_step,
                    self.slot_step,
                    self.save1_step,
                    self.save2_step,
                    self.extra_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role  

        return await step_context.prompt("date_prompt", PromptOptions(
            prompt=MessageFactory.text("On which date you would like to book an appointment? Hint: YYYY-MM-DD."),
                retry_prompt= MessageFactory.text(
                "Please enter a valid day or date. P.S. It can't be past date."),))


    async def pharmacist_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global outletid
        global outletName
        global pharmacists
        global date
        global email

        global permi
        global msgs
        permi = "sivdddnisvi"

        msgs = predict_class(step_context.result)

        if msgs == "reminder" or msgs == "health_records" or msgs == "adv_pill_reminder":
            permi = "permission nite hbe"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like to end the book appointment workflow?")),) 


################################################################################# real appointment #########################################################################################################################################

        date = step_context.result

        email = check_email(userId, token)
        outletid = check_outlet(email, pharmacyId, token)
        outletName = outlet_name(outletid, token)
        pharmacists = get_avail_slot(outletid, pharmacyId, token)
        
        if len(pharmacists) == 0:
            await step_context.context.send_activity(
                MessageFactory.text(f"Sorry! No slots are available for the selected outlet. Please try again after changing an outlet."))
            return await step_context.end_dialog()
        
        if len(pharmacists) == 1:
            listofchoice = [Choice(pharmacists[0])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation"),choices=listofchoice))

        if len(pharmacists) == 2:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation"),choices=listofchoice))

        if len(pharmacists) == 3:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation"),choices=listofchoice))

        if len(pharmacists) == 4:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation"),choices=listofchoice))

        if len(pharmacists) == 5:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3]), Choice(pharmacists[4])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation"),choices=listofchoice))

        if len(pharmacists) == 6:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3]), Choice(pharmacists[4]), Choice(pharmacists[5])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation"),choices=listofchoice))

    async def time_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        if permi == "permission nite hbe":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                if msgs == "health_records":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the upload health records process!"))
                    return await step_context.begin_dialog(HealthRecordDialog.__name__)

                if msgs == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)
                
                if msgs == "adv_pill_reminder":
                    ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
                    sh = ac.open("logs_checker")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.result))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__) 


        global permi1
        global msgs1
        permi1 = "sivdddnisvi"

        msgs1 = predict_class(step_context.result)

        if msgs1 == "adv_pill_reminder" or msgs1 == "reminder" or msgs1 == "health_records":
            permi1 = "permission nite hbe"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like to end the pill reminder workflow?")),) 

###################################################################### real appointment ##############################################################################################################################################        

        global pharmacist

        pharmacist = step_context.result.value
        return await step_context.prompt(
            "time_prompt",
            PromptOptions(
                prompt=MessageFactory.text("At what time of a day would you like to consult?")),)


    async def slot_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if permi1 == "permission nite hbe":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                if msgs1 == "health_records":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the upload health records process!"))
                    return await step_context.begin_dialog(HealthRecordDialog.__name__)

                if msgs1 == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if msgs1 == "adv_pill_reminder":
                    ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
                    sh = ac.open("logs_checker")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.result))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__) 


        global permi2
        global msgs2
        permi2 = "sivdddnisvi"

        msgs2 = predict_class(step_context.result)

        if msgs2 == "adv_pill_reminder" or msgs2 == "reminder" or msgs2 == "health_records":
            permi2 = "permission nite hbe"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like to end the pill reminder workflow?")),) 


####################################################################### real appointment ##############################################################################################################################################

        global confirmation
        global timeslot
        global slot
        global id

        confirmation  = "aaa1"
        timeslot = "aaa2"

        pharmas = pharmacist.lower()
        id = match(pharmas, outletid, pharmacyId)
        time = step_context.result
        slot = get_timeslots(id, date, time, token)
        
        if slot == "No slots available":
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("No slots are available for " + str(pharmacist) + " on " + str(date) + ". Please try another date or pharmacist!")),)

        if slot == "NOPE":
            timeslot = "again"
            aslots = get_timeslots2(id, date, token)

            reply = MessageFactory.text("Sorry!. Pharmacist is not available at " + str(time) + ". Please choose a different time slot")
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= aslots[0],
                        type=ActionTypes.im_back,
                        value= aslots[0]),
                    CardAction(
                        title= aslots[1],
                        type=ActionTypes.im_back,
                        value= aslots[1]),
                    CardAction(
                        title= aslots[2],
                        type=ActionTypes.im_back,
                        value= aslots[2]),
                    CardAction(
                        title= aslots[3],
                        type=ActionTypes.im_back,
                        value= aslots[3]),])
            return await step_context.context.send_activity(reply)                
        
        else:
            confirmation = "confirm or not"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(slot) + " on " + str(date) + ". Shall I confirm the appointment?")),)


    async def save1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if permi2 == "permission nite hbe":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                if msgs2 == "health_records":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the upload health records process!"))
                    return await step_context.begin_dialog(HealthRecordDialog.__name__)

                if msgs2 == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if msgs2 == "adv_pill_reminder":
                    ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
                    sh = ac.open("logs_checker")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.result))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__) 


        global permi3
        global msgs3
        permi3 = "sivdddnisvi"

        msgs3 = predict_class(step_context.result)

        if msgs3 == "adv_pill_reminder" or msgs3 == "reminder" or msgs3 == "health_records":
            permi3 = "permission nite hbe"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like to end the pill reminder workflow?")),) 



############################################################################# real appointment ##############################################################################################################################################

        global times
        times = "vmsovo"

        if timeslot == "again":
            times = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(times) + " on " + str(date) + ". Shall I confirm the appointment?")),)

        if confirmation == "confirm or not":
            msg = step_context.result
            confirm = predict_class(msg)

            if confirm == "positive":
                time = slot.split(" - ")
                time1 = timeConversion(time[0])
                time2 = timeConversion(time[1])
                patientId = step_context.context.activity.from_property.id
                pharmacistId = id
                save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment has been confirmed."))
                return await step_context.end_dialog()

            if confirm == "negative":
                await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment."))
                return await step_context.end_dialog()


    async def save2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if permi3 == "permission nite hbe":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                if msgs3 == "health_records":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the upload health records process!"))
                    return await step_context.begin_dialog(HealthRecordDialog.__name__)

                if msgs3 == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if msgs3 == "adv_pill_reminder":
                    ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
                    sh = ac.open("logs_checker")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.result))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__) 


        global permi4
        global msgs4
        permi4 = "sivdddnisvi"

        msgs4 = predict_class(step_context.result)

        if msgs4 == "adv_pill_reminder" or msgs4 == "reminder" or msgs4 == "health_records":
            permi4 = "permission nite hbe"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Would you like to end the pill reminder workflow?")),) 


#################################################################### real appointment ##############################################################################################################################################

        yesno = predict_class(step_context.result)

        if yesno == "positive":
            # endTime = times
            timet = times.split(" - ")
            time1 = timeConversion(timet[0])
            time2 = timeConversion(timet[1])
            patientId = get_patient_id(email, pharmacyId)
            pharmacistId = id
            save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
            await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment has been confirmed."))
            return await step_context.end_dialog()

        if yesno == "negative":
            await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment."))
            return await step_context.end_dialog()


    async def extra_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

    
        if permi4 == "permission nite hbe":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                if msgs4 == "health_records":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the upload health records process!"))
                    return await step_context.begin_dialog(HealthRecordDialog.__name__)

                if msgs4 == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if msgs4 == "adv_pill_reminder":
                    ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
                    sh = ac.open("logs_checker")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.result))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay! I am initializing the pill reminder process!"))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__) 