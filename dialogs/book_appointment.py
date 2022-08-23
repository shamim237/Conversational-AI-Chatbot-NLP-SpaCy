from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog, DialogTurnStatus
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
from dialogs.non_upapp_dialog import UploadNonInDialogApp

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
        self.add_dialog(UploadNonInDialogApp(UploadNonInDialogApp.__name__)) 
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
            prompt=MessageFactory.text("On which date you would like to book an appointment?"),
                retry_prompt= MessageFactory.text(
                "Please enter a valid day or date. P.S. It can't be past date."),))


    async def pharmacist_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global outletid
        global outletName
        global pharmacists
        global date
        global email
        global endnot
        endnot = "snvsnvs"

        date = step_context.result

        email = check_email(userId, token)
        outletid = check_outlet(email, pharmacyId, token)
        outletName = outlet_name(outletid, token)
        pharmacists = get_avail_slot(outletid, pharmacyId, token)

        msg = predict_class(step_context.result)

        if msg == "reminder":
            endnot = "yesno"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions("Would you like to end the appointment workflow?"))
        else:
        
            if len(pharmacists) == 0:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! No slots are available for the selected outlet. Please try again after changing an outlet."))
                await step_context.context.send_activity(
                    MessageFactory.text(f"In the meantime..."))
                return await step_context.begin_dialog(UploadNonInDialogApp.__name__) 
            
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

        global pharmacist

        if endnot == "yesno":
            msg = predict_class(step_context.result)
            if msg == "positive":
                await step_context.context.send_activity(MessageFactory.text("Okay. I am initializing the process of setting a pill reminder."))
                return await step_context.begin_dialog(PillReminderDialog.__name__)
            else:
                await step_context.context.send_activity(MessageFactory.text("Alright. Please share me the missing information for booking the ongoing appointment"))
                return DialogTurnResult(DialogTurnStatus.Waiting)

        else:

            pharmacist = step_context.result.value
            return await step_context.prompt(
                "time_prompt",
                PromptOptions(
                    prompt=MessageFactory.text("At what time would you like to consult?")),)


    async def slot_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

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
                return await step_context.cancel_all_dialogs()

            if confirm == "negative":
                await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment."))
                return await step_context.cancel_all_dialogs()


    async def save2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        yesno = predict_class(step_context.result)

        if yesno == "positive":
            timet = times.split(" - ")
            time1 = timeConversion(timet[0])
            time2 = timeConversion(timet[1])
            patientId = get_patient_id(email, pharmacyId)
            pharmacistId = id
            save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
            await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment has been confirmed."))
            return await step_context.cancel_all_dialogs()

        if yesno == "negative":
            await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment."))
            return await step_context.cancel_all_dialogs()

