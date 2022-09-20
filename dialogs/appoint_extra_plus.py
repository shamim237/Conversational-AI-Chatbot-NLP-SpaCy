from lib.message_factory import MessageFactory
from lib.card import CardAction
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
from appointment import appoint_id, save_appoint
from botbuilder.dialogs.choices import Choice
from botbuilder.schema import ActionTypes, SuggestedActions
from dialogs.non_upapp_dialog import UploadNonInDialogApp



class AppointExtraPlusDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(AppointExtraPlusDialog, self).__init__(dialog_id or AppointExtraPlusDialog.__name__)

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
                    self.save3_step,

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
            prompt=MessageFactory.text("On which date you would like to book an appointment?", extra = step_context.context.activity.text),
                retry_prompt= MessageFactory.text(
                "Please enter a valid day or date. P.S. It can't be past date.", extra = step_context.context.activity.text),))


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
    
        if len(pharmacists) == 0:
            await step_context.context.send_activity(
                MessageFactory.text(f"Sorry! No slots are available for the selected outlet. Please try again after changing an outlet.", extra = step_context.result))
            await step_context.context.send_activity(
                MessageFactory.text(f"In the meantime...", extra = step_context.result))
            return await step_context.begin_dialog(UploadNonInDialogApp.__name__) 
        
        if len(pharmacists) == 1:
            listofchoice = [Choice(pharmacists[0])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = step_context.result),choices=listofchoice))

        if len(pharmacists) == 2:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = step_context.result),choices=listofchoice))

        if len(pharmacists) == 3:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = step_context.result),choices=listofchoice))

        if len(pharmacists) == 4:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = step_context.result),choices=listofchoice))

        if len(pharmacists) == 5:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3]), Choice(pharmacists[4])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = step_context.result),choices=listofchoice))

        if len(pharmacists) == 6:
            listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3]), Choice(pharmacists[4]), Choice(pharmacists[5])]
            return await step_context.prompt((ChoicePrompt.__name__),
            PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = step_context.result),choices=listofchoice))


    async def time_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global pharmacist

        pharmacist = step_context.result.value
        return await step_context.prompt(
            "time_prompt",
            PromptOptions(
                prompt=MessageFactory.text("At what time would you like to consult?", extra = step_context.result)),)


    async def slot_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global confirmation
        global timeslot
        global slot
        global ids
        global take_time

        take_time       = "sksmism"
        confirmation    = "aaa1aha"
        timeslot        = "aaa2ajj"

        timey = step_context.context.activity.additional_properties
        time_now = timey.get('local_timestamp')


        pharmas = pharmacist.lower()
        ids = match(pharmas, outletid, pharmacyId)
        time = step_context.result
        slot = get_timeslots(ids, date, time, time_now, token)
        
        if slot == "No slots available":
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("No slots are available for " + str(pharmacist) + " on " + str(date) + ". Please try another date or pharmacist!", extra = step_context.result)),)

        if slot == "NOPE":
            timeslot = "again"
            aslots = get_timeslots2(ids, date, token)

            reply = MessageFactory.text("Sorry!. Pharmacist is not available at " + str(time) + ". Please choose a different time slot", extra = step_context.result)
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

        if slot is None:
            take_time = "valid future time"
            await step_context.context.send_activity(
                MessageFactory.text(f"You can't book an appointment on the past time!", extra = step_context.result)) 
            
            return await step_context.prompt(
                "time_prompt",
                PromptOptions(
                    prompt=MessageFactory.text("Please enter an upcoming time at when you want consult to a pharmacist.", extra = step_context.result)),)                          
        
        else:
            confirmation = "confirm or not"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(slot) + " on " + str(date) + ". Shall I confirm the appointment?", extra = step_context.result)),)


    async def save1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global times
        global question
        global appointId1
        global scnd_time
    

        question    = "ssiojgv"
        times       = "vmsovo"
        appointId1  = "auauauu"
        scnd_time   = "sinnsivn"

        if timeslot == "again":
            times = step_context.result
            scnd_time = "ask to save 2nd time"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(times) + " on " + str(date) + ". Shall I confirm the appointment?", extra = step_context.result)),)

        if confirmation == "confirm or not":
            msg = step_context.result
            confirm = predict_class(msg)

            if confirm == "positive":
                question = "ask question"
                time = slot.split(" - ")
                time1 = timeConversion(time[0])
                time2 = timeConversion(time[1])
                patientId = step_context.context.activity.from_property.id
                pharmacistId = ids
                save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                appointId1 = appoint_id(patientId, token)
                await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on" + str(date) + ".", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = step_context.result))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to answer it now?", extra = step_context.result)),)

            if confirm == "negative":
                await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = step_context.result))
                return await step_context.end_dialog()

        global timeslot2
        global slott
        global idt
        global confirmation2
        
        idt             = "akakakaa"
        slott           = "skskksss"
        timeslot2       = "kskvmkss"
        confirmation2   = "kjasnfsj"

        if take_time == "valid future time":

            timey = step_context.context.activity.additional_properties
            time_now = timey.get('local_timestamp')
            time_scnd = step_context.result
            pharmas = pharmacist.lower()
            idt = match(pharmas, outletid, pharmacyId)
            slott = get_timeslots(idt, date, time_scnd, time_now, token)

            if slott == "No slots available":
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("No slots are available for " + str(pharmacist) + " on " + str(date) + ". Please try another date or pharmacist!", extra = step_context.result)),)

            if slott == "NOPE":
                timeslot2 = "again2"
                aslots = get_timeslots2(idt, date, token)
                reply = MessageFactory.text("Sorry!. Pharmacist is not available at " + str(time) + ". Please choose a different time slot", extra = step_context.result)
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

            if slott is None:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! You have failed to provide a valid time.", extra = step_context.result)) 
                return await step_context.end_dialog()
            
            else:
                confirmation2 = "confirm or not2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(slott) + " on " + str(date) + ". Shall I confirm the appointment?", extra = step_context.result)),)


    async def save2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global question2
        global appointId2

        appointId2  = "aoaoaoao"
        question2   = "ksnvinsn"

        if question == "ask question":
            yesno = predict_class(step_context.result)

            if yesno == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                reply = MessageFactory.text("go to question page", extra = step_context.result)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= str(appointId1),
                            extra= step_context.result)])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()   

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog()  

        if scnd_time == "ask to save 2nd time":
            yesno = predict_class(step_context.result)

            if yesno == "positive":
                timet = times.split(" - ")
                time1 = timeConversion(timet[0])
                time2 = timeConversion(timet[1])
                patientId = get_patient_id(email, pharmacyId)
                pharmacistId = id
                question2 = "questionnare ask2"
                save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                appointId2 = appoint_id(patientId, token)
                await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on" + str(date) + ".", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = step_context.result))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to answer it now?", extra = step_context.result)),)

            else:
                await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = step_context.result))
                return await step_context.end_dialog()

        global times2
        global appointId3
        global scnd_time2 
        global question21

        times2     = "ahshshs"
        appointId3 = "aaiaiai"
        scnd_time2 = "sjkskns"
        question21 = "skkskss"


        if timeslot2 == "again2":
            times2 = step_context.result
            scnd_time2 = "ask to save 2nd time2"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(times2) + " on " + str(date) + ". Shall I confirm the appointment?", extra = step_context.result)),)

        if confirmation2 == "confirm or not2":

            msg = step_context.result
            confirm = predict_class(msg)

            if confirm == "positive":
                question21 = "ask question2"
                time = slott.split(" - ")
                time1 = timeConversion(time[0])
                time2 = timeConversion(time[1])
                patientId = step_context.context.activity.from_property.id
                pharmacistId = idt
                save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                appointId3 = appoint_id(patientId, token)
                await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on" + str(date) + ".", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = step_context.result))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to answer it now?", extra = step_context.result)),)

            if confirm == "negative":
                await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = step_context.result))
                return await step_context.end_dialog()



    async def save3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if question2 == "questionnare ask2":
            
            msg = predict_class(step_context.result)

            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                reply = MessageFactory.text("go to question page", extra = step_context.result)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= str(appointId2),
                            extra = step_context.result)])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()   

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog()  

        global question22
        global appointId4
        global question24

        question22 = "sskahah"
        appointId4 = "aiaidid"
        question24 = "ghshshh"

        if scnd_time2 == "ask to save 2nd time2":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                timet = times2.split(" - ")
                time1 = timeConversion(timet[0])
                time2 = timeConversion(timet[1])
                patientId = get_patient_id(email, pharmacyId)
                pharmacistId = id
                question22 = "questionnare ask22"
                save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                appointId4 = appoint_id(patientId, token)
                await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on" + str(date) + ".", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = step_context.result))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would  you like to answer it now?", extra = step_context.result)),)

            else:
                await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = step_context.result))
                await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = step_context.result))
                return await step_context.end_dialog()

        if question21 == "ask question2":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                reply = MessageFactory.text("go to question page", extra = step_context.result)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= str(appointId3),
                            extra = step_context.result)])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()   

            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog() 

    async def save4_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if question22 == "questionnare ask22":
            msg = predict_class(step_context.result)
            if msg == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Thank You! I am opening the questionnare page.", extra = step_context.result))
                reply = MessageFactory.text("go to question page", extra = step_context.result)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= "go to question page",
                            type=ActionTypes.im_back,
                            value= str(appointId4),
                            extra = step_context.result)])
                await step_context.context.send_activity(reply)
                return await step_context.end_dialog()   
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = step_context.result))
                return await step_context.end_dialog() 
